"""Construit et valide le projet QGIS de contrôle de la phase 6.

Ce script doit être exécuté avec ``python-qgis-ltr.bat`` sous Windows.
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    Qgis,
    QgsApplication,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFillSymbol,
    QgsMapRendererParallelJob,
    QgsMapSettings,
    QgsMarkerSymbol,
    QgsProject,
    QgsRasterLayer,
    QgsReferencedRectangle,
    QgsSingleSymbolRenderer,
    QgsVectorLayer,
)


ROOT = Path(__file__).resolve().parents[1]
PROJECT_PATH = ROOT / "qgis" / "controle_phase6.qgs"
SNAPSHOT_PATH = ROOT / "reports" / "quality" / "phase6_qgis_snapshot.png"
VALIDATION_PATH = ROOT / "reports" / "quality" / "phase6_qgis_validation.json"


VECTOR_LAYERS = [
    {
        "file": "sites_sensibles.geojson",
        "name": "Sites sensibles",
        "kind": "marker",
        "style": {
            "name": "circle",
            "color": "214,39,40,255",
            "outline_color": "255,255,255,255",
            "outline_width": "0.7",
            "size": "4.5",
        },
        "visible": True,
    },
    {
        "file": "sites_pilote.geojson",
        "name": "Sites pilotes",
        "kind": "marker",
        "style": {
            "name": "circle",
            "color": "31,119,180,220",
            "outline_color": "255,255,255,255",
            "outline_width": "0.5",
            "size": "3.2",
        },
        "visible": True,
    },
    {
        "file": "adresses_ban.geojson",
        "name": "Adresses BAN",
        "kind": "marker",
        "style": {
            "name": "triangle",
            "color": "44,160,44,255",
            "outline_color": "20,80,20,255",
            "size": "4",
        },
        "visible": True,
    },
    {
        "file": "emprises_documentaires.geojson",
        "name": "Emprises documentaires POP",
        "kind": "fill",
        "style": {
            "color": "255,127,14,45",
            "outline_color": "255,127,14,255",
            "outline_width": "0.8",
        },
        "visible": True,
    },
    {
        "file": "parcelles_candidates.geojson",
        "name": "Parcelles actuelles candidates",
        "kind": "fill",
        "style": {
            "color": "127,127,127,20",
            "outline_color": "90,90,90,180",
            "outline_style": "dash",
            "outline_width": "0.5",
        },
        "visible": False,
    },
]


def make_vector_layer(spec: dict[str, object]) -> QgsVectorLayer:
    path = ROOT / "qgis" / "data" / str(spec["file"])
    layer = QgsVectorLayer(str(path), str(spec["name"]), "ogr")
    if not layer.isValid():
        raise RuntimeError(f"Couche invalide : {path}")
    layer.setReadOnly(True)
    if spec["kind"] == "marker":
        symbol = QgsMarkerSymbol.createSimple(spec["style"])
    else:
        symbol = QgsFillSymbol.createSimple(spec["style"])
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    return layer


def combined_extent(layers: list[QgsVectorLayer], project: QgsProject):
    target_crs = project.crs()
    extent = None
    for layer in layers:
        transform = QgsCoordinateTransform(layer.crs(), target_crs, project.transformContext())
        layer_extent = transform.transformBoundingBox(layer.extent())
        if extent is None:
            extent = layer_extent
        else:
            extent.combineExtentWith(layer_extent)
    if extent is None:
        raise RuntimeError("Aucune emprise calculable")
    extent.scale(1.08)
    return extent


def render_snapshot(
    layers: list[QgsVectorLayer], project: QgsProject, output: Path
) -> None:
    settings = QgsMapSettings()
    settings.setLayers(list(reversed(layers)))
    settings.setDestinationCrs(project.crs())
    settings.setTransformContext(project.transformContext())
    settings.setExtent(combined_extent(layers, project))
    settings.setOutputSize(QSize(1200, 800))
    settings.setBackgroundColor(QColor("white"))
    settings.setOutputDpi(96)
    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    output.parent.mkdir(parents=True, exist_ok=True)
    if not job.renderedImage().save(str(output), "PNG"):
        raise RuntimeError(f"Impossible d'écrire l'aperçu : {output}")


def build_project() -> dict[str, object]:
    profile = tempfile.TemporaryDirectory(prefix="qgis-phase6-")
    app = QgsApplication([], False, profile.name)
    app.initQgis()
    try:
        project = QgsProject.instance()
        project.clear()
        project.setFileName(str(PROJECT_PATH))
        project.setTitle("Phase 6 — contrôle cartographique du corpus pilote")
        project.setCrs(QgsCoordinateReferenceSystem("EPSG:2154"))
        project.setPresetHomePath(str(PROJECT_PATH.parent))
        project.setFilePathStorage(Qgis.FilePathType.Relative)

        layers = []
        root = project.layerTreeRoot()
        for spec in VECTOR_LAYERS:
            layer = make_vector_layer(spec)
            project.addMapLayer(layer, False)
            node = root.addLayer(layer)
            node.setItemVisibilityChecked(bool(spec["visible"]))
            layers.append(layer)

        osm_source = (
            "type=xyz&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            "&zmax=19&zmin=0"
        )
        osm = QgsRasterLayer(osm_source, "Fond OpenStreetMap", "wms")
        if not osm.isValid():
            raise RuntimeError("Le fond OpenStreetMap n'est pas reconnu par QGIS")
        project.addMapLayer(osm, False)
        root.addLayer(osm)

        extent = combined_extent(layers, project)
        referenced_extent = QgsReferencedRectangle(extent, project.crs())
        project.viewSettings().setDefaultViewExtent(referenced_extent)
        project.viewSettings().setPresetFullExtent(referenced_extent)
        PROJECT_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not project.write(str(PROJECT_PATH)):
            raise RuntimeError(f"Impossible d'écrire le projet : {PROJECT_PATH}")

        project.clear()
        if not project.read(str(PROJECT_PATH)):
            raise RuntimeError("QGIS ne peut pas relire le projet généré")

        validation_layers = []
        layer_results = []
        for spec in VECTOR_LAYERS:
            matches = project.mapLayersByName(str(spec["name"]))
            if len(matches) != 1 or not matches[0].isValid():
                raise RuntimeError(f"Couche non résolue après relecture : {spec['name']}")
            layer = matches[0]
            validation_layers.append(layer)
            layer_results.append(
                {
                    "nom": layer.name(),
                    "source": project.writePath(layer.source()),
                    "objets": layer.featureCount(),
                    "valide": layer.isValid(),
                }
            )

        render_snapshot(validation_layers, project, SNAPSHOT_PATH)
        result = {
            "date_validation": "2026-07-22",
            "qgis_version": Qgis.QGIS_VERSION,
            "projet": str(PROJECT_PATH.relative_to(ROOT)).replace("\\", "/"),
            "projet_relu": True,
            "crs_projet": project.crs().authid(),
            "couches": layer_results,
            "fond_osm_valide": bool(project.mapLayersByName("Fond OpenStreetMap")[0].isValid()),
            "apercu": str(SNAPSHOT_PATH.relative_to(ROOT)).replace("\\", "/"),
        }
        VALIDATION_PATH.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return result
    finally:
        app.exitQgis()
        profile.cleanup()
        for side_effect in (Path(f"{PROJECT_PATH}~"), ROOT / "symbology-style.db"):
            side_effect.unlink(missing_ok=True)


if __name__ == "__main__":
    print(json.dumps(build_project(), ensure_ascii=False, sort_keys=True))
