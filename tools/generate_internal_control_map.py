"""Produit la première carte statique partageable du corpus pilote.

Ce script doit être exécuté avec ``python-qgis-ltr.bat`` sous Windows.
"""

from __future__ import annotations

import gc
import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path

from qgis.PyQt.QtCore import QPointF, QRectF, QSize, Qt
from qgis.PyQt.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen, QPolygonF
from qgis.core import (
    QgsApplication,
    QgsCategorizedSymbolRenderer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFillSymbol,
    QgsGeometry,
    QgsMapRendererParallelJob,
    QgsMapSettings,
    QgsMarkerSymbol,
    QgsPointXY,
    QgsProject,
    QgsRendererCategory,
    QgsSingleSymbolRenderer,
    QgsVectorLayer,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SITES = ROOT / "qgis" / "data" / "sites_pilote.geojson"
RAW_COMMUNES = (
    ROOT
    / "data"
    / "raw"
    / "api_geo"
    / "2026"
    / "2026-07-22"
    / "communes_orne_contours.geojson"
)
BOUNDARY = ROOT / "qgis" / "data" / "orne_contour_simplifie.geojson"
OUTPUT = ROOT / "reports" / "maps" / "carte_pilote_interne.png"
VALIDATION = ROOT / "reports" / "maps" / "carte_pilote_interne_validation.json"

WIDTH = 1800
HEIGHT = 1200
MAP_LEFT = 70
MAP_TOP = 205
MAP_WIDTH = 1190
MAP_HEIGHT = 855

SECTORS = {
    "extraction": ("Extraction", "#6c4fa3"),
    "metallurgie_travail_metaux": ("Métallurgie et métaux", "#a94732"),
    "textile_habillement_cuir": ("Textile, habillement, cuir", "#bd4f82"),
    "bois_papier_imprimerie": ("Bois, papier, imprimerie", "#657b3a"),
    "verre_ceramique_materiaux_construction": ("Matériaux de construction", "#cc791d"),
    "agroalimentaire": ("Agroalimentaire", "#c39b2d"),
    "energie": ("Énergie", "#167c80"),
    "multi": ("Plusieurs secteurs", "#525b66"),
}

CITY_LABELS = {
    "Flers": (-0.569, 48.748),
    "Argentan": (-0.018, 48.744),
    "Alençon": (-0.092, 48.432),
    "L'Aigle": (0.628, 48.764),
    "Mortagne-au-Perche": (0.547, 48.521),
    "Domfront": (-0.648, 48.592),
}


def _simplified_boundary() -> None:
    if BOUNDARY.exists():
        return
    if not RAW_COMMUNES.exists():
        raise FileNotFoundError(
            "Le contour source manque. Télécharger les communes de l'Orne depuis "
            "geo.api.gouv.fr avec geometry=contour."
        )
    communes = QgsVectorLayer(str(RAW_COMMUNES), "Communes de l'Orne", "ogr")
    if not communes.isValid():
        raise RuntimeError(f"Couche communale invalide : {RAW_COMMUNES}")
    geometry = QgsGeometry.unaryUnion(
        [QgsGeometry(feature.geometry()) for feature in communes.getFeatures()]
    ).simplify(0.001)
    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nom": "Orne",
                    "code": "61",
                    "source": "API Découpage administratif",
                },
                "geometry": json.loads(geometry.asJson(precision=6)),
            }
        ],
    }
    BOUNDARY.write_text(
        json.dumps(feature_collection, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def _prepare_sites(directory: Path) -> tuple[Path, Path, Counter[str]]:
    payload = json.loads(SOURCE_SITES.read_text(encoding="utf-8"))
    features = []
    alerts = []
    counts: Counter[str] = Counter()
    for source_feature in payload["features"]:
        feature = json.loads(json.dumps(source_feature))
        properties = feature["properties"]
        sectors = [item.strip() for item in properties["secteurs"].split(",")]
        category = "multi" if len(sectors) > 1 else sectors[0]
        properties["categorie_carte"] = category
        properties["alerte_carte"] = properties["statut"] == "sensible_controle"
        counts[category] += 1
        features.append(feature)
        if properties["alerte_carte"]:
            alerts.append(feature)

    sites_path = directory / "sites.geojson"
    alerts_path = directory / "alerts.geojson"
    sites_path.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False),
        encoding="utf-8",
    )
    alerts_path.write_text(
        json.dumps({"type": "FeatureCollection", "features": alerts}, ensure_ascii=False),
        encoding="utf-8",
    )
    return sites_path, alerts_path, counts


def _make_layers(sites_path: Path, alerts_path: Path):
    boundary = QgsVectorLayer(str(BOUNDARY), "Contour de l'Orne", "ogr")
    sites = QgsVectorLayer(str(sites_path), "Sites pilotes", "ogr")
    alerts = QgsVectorLayer(str(alerts_path), "Localisations à vérifier", "ogr")
    if not all(layer.isValid() for layer in (boundary, sites, alerts)):
        raise RuntimeError("Une couche de la carte interne est invalide")

    boundary.setRenderer(
        QgsSingleSymbolRenderer(
            QgsFillSymbol.createSimple(
                {
                    "color": "246,242,233,255",
                    "outline_color": "113,108,99,255",
                    "outline_width": "0.7",
                }
            )
        )
    )
    categories = []
    for code, (label, color) in SECTORS.items():
        categories.append(
            QgsRendererCategory(
                code,
                QgsMarkerSymbol.createSimple(
                    {
                        "name": "circle",
                        "color": color,
                        "outline_color": "255,255,255,255",
                        "outline_width": "0.55",
                        "size": "4.5",
                    }
                ),
                label,
            )
        )
    sites.setRenderer(QgsCategorizedSymbolRenderer("categorie_carte", categories))
    alerts.setRenderer(
        QgsSingleSymbolRenderer(
            QgsMarkerSymbol.createSimple(
                {
                    "name": "circle",
                    "color": "255,255,255,0",
                    "outline_color": "185,28,28,255",
                    "outline_width": "0.9",
                    "size": "7.0",
                }
            )
        )
    )
    return boundary, sites, alerts


def _render_map(layers, destination_crs):
    boundary = layers[0]
    transform = QgsCoordinateTransform(
        boundary.crs(), destination_crs, QgsProject.instance().transformContext()
    )
    extent = transform.transformBoundingBox(boundary.extent())
    extent.scale(1.04)
    settings = QgsMapSettings()
    settings.setLayers([layers[2], layers[1], layers[0]])
    settings.setDestinationCrs(destination_crs)
    settings.setExtent(extent)
    settings.setOutputSize(QSize(MAP_WIDTH, MAP_HEIGHT))
    settings.setOutputDpi(144)
    settings.setBackgroundColor(QColor("#eef2ed"))
    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    return job.renderedImage(), extent


def _font(size: int, *, bold: bool = False) -> QFont:
    font = QFont("Arial", size)
    font.setBold(bold)
    return font


def _point_to_pixel(point: QgsPointXY, extent) -> tuple[float, float]:
    x = MAP_LEFT + ((point.x() - extent.xMinimum()) / extent.width()) * MAP_WIDTH
    y = MAP_TOP + MAP_HEIGHT - (
        ((point.y() - extent.yMinimum()) / extent.height()) * MAP_HEIGHT
    )
    return x, y


def _compose(image: QImage, extent, counts: Counter[str]) -> QImage:
    canvas = QImage(WIDTH, HEIGHT, QImage.Format.Format_ARGB32)
    canvas.fill(QColor("#faf8f3"))
    painter = QPainter(canvas)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setPen(QColor("#1d2527"))
    painter.setFont(_font(30, bold=True))
    painter.drawText(70, 64, "Patrimoine industriel de l'Orne — corpus pilote")
    painter.setFont(_font(15))
    painter.setPen(QColor("#465054"))
    painter.drawText(
        QRectF(70, 88, 1650, 75),
        int(Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap),
        "30 sites choisis pour éprouver la méthode. Les couleurs représentent les secteurs ; "
        "le cercle rouge signale une localisation qui demande encore une vérification.",
    )

    painter.setPen(QPen(QColor("#c7c1b6"), 2))
    painter.setBrush(QBrush(QColor("white")))
    painter.drawRoundedRect(QRectF(MAP_LEFT - 8, MAP_TOP - 8, MAP_WIDTH + 16, MAP_HEIGHT + 16), 8, 8)
    painter.drawImage(MAP_LEFT, MAP_TOP, image)

    destination_crs = QgsCoordinateReferenceSystem("EPSG:2154")
    transform = QgsCoordinateTransform(
        QgsCoordinateReferenceSystem("EPSG:4326"), destination_crs, layers_context()
    )
    painter.setFont(_font(11, bold=True))
    for label, (longitude, latitude) in CITY_LABELS.items():
        point = transform.transform(QgsPointXY(longitude, latitude))
        x, y = _point_to_pixel(point, extent)
        painter.setBrush(QColor("#3f484b"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(x - 2.5, y - 2.5, 5, 5))
        painter.setPen(QColor("#3f484b"))
        painter.drawText(QRectF(x + 7, y - 13, 145, 24), int(Qt.AlignmentFlag.AlignLeft), label)

    sidebar_x = 1315
    painter.setPen(QColor("#1d2527"))
    painter.setFont(_font(17, bold=True))
    painter.drawText(sidebar_x, 234, "Secteur principal")
    y = 275
    for code, (label, color) in SECTORS.items():
        painter.setPen(QPen(QColor("white"), 2))
        painter.setBrush(QBrush(QColor(color)))
        painter.drawEllipse(QRectF(sidebar_x, y - 11, 21, 21))
        painter.setPen(QColor("#30393c"))
        painter.setFont(_font(12))
        painter.drawText(sidebar_x + 34, y + 5, f"{label}  ·  {counts.get(code, 0)}")
        y += 43

    y += 15
    painter.setPen(QPen(QColor("#b91c1c"), 3))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawEllipse(QRectF(sidebar_x, y - 13, 26, 26))
    painter.setPen(QColor("#30393c"))
    painter.setFont(_font(12))
    painter.drawText(sidebar_x + 40, y + 5, "Localisation à vérifier  ·  9")

    y += 66
    painter.setFont(_font(16, bold=True))
    painter.setPen(QColor("#1d2527"))
    painter.drawText(sidebar_x, y, "À lire avec prudence")
    painter.setFont(_font(12))
    painter.setPen(QColor("#465054"))
    painter.drawText(
        QRectF(sidebar_x, y + 18, 410, 200),
        int(Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap),
        "Ce pilote n'est pas représentatif des 319 dossiers. Les 30 points sont approximatifs. "
        "La carte permet de contrôler la répartition et les cas à revoir ; elle ne prouve ni "
        "l'emprise historique exacte, ni l'état actuel des bâtiments.",
    )

    north_x = MAP_LEFT + MAP_WIDTH - 58
    north_y = MAP_TOP + 48
    painter.setPen(QColor("#30393c"))
    painter.setFont(_font(14, bold=True))
    painter.drawText(north_x - 5, north_y - 16, "N")
    painter.setBrush(QColor("#30393c"))
    painter.drawPolygon(
        QPolygonF(
            [
                QPointF(north_x, north_y - 8),
                QPointF(north_x - 8, north_y + 15),
                QPointF(north_x + 8, north_y + 15),
            ]
        )
    )

    scale_width = 20000 / extent.width() * MAP_WIDTH
    scale_x = MAP_LEFT + 35
    scale_y = MAP_TOP + MAP_HEIGHT - 40
    painter.setPen(QPen(QColor("#30393c"), 3))
    painter.drawLine(int(scale_x), int(scale_y), int(scale_x + scale_width), int(scale_y))
    painter.drawLine(int(scale_x), int(scale_y - 7), int(scale_x), int(scale_y + 7))
    painter.drawLine(
        int(scale_x + scale_width),
        int(scale_y - 7),
        int(scale_x + scale_width),
        int(scale_y + 7),
    )
    painter.setFont(_font(10))
    painter.drawText(int(scale_x), int(scale_y - 12), "20 km")

    painter.setPen(QColor("#5b6466"))
    painter.setFont(_font(10))
    painter.drawText(
        QRectF(70, 1094, 1660, 62),
        int(Qt.AlignmentFlag.AlignLeft | Qt.TextFlag.TextWordWrap),
        "Sources : POP / Mérimée, Région Normandie — contour : API Découpage administratif. "
        "Données et contrôles au 22 juillet 2026. Carte de contrôle interne — version 1.0.",
    )
    painter.end()
    return canvas


def layers_context():
    """Retourne le contexte de transformation de l'application QGIS."""
    return QgsProject.instance().transformContext()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_map() -> dict[str, object]:
    profile = tempfile.TemporaryDirectory(prefix="qgis-phase7-map-")
    app = QgsApplication([], False, profile.name)
    app.initQgis()
    try:
        _simplified_boundary()
        with tempfile.TemporaryDirectory(
            prefix="phase7-map-data-", ignore_cleanup_errors=True
        ) as directory:
            sites_path, alerts_path, counts = _prepare_sites(Path(directory))
            layers = _make_layers(sites_path, alerts_path)
            image, extent = _render_map(
                layers, QgsCoordinateReferenceSystem("EPSG:2154")
            )
            canvas = _compose(image, extent, counts)
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            if not canvas.save(str(OUTPUT), "PNG"):
                raise RuntimeError(f"Impossible d'écrire {OUTPUT}")
            del layers
            gc.collect()
        result = {
            "schema_version": "1.0",
            "date": "2026-07-22",
            "output": OUTPUT.relative_to(ROOT).as_posix(),
            "width_px": WIDTH,
            "height_px": HEIGHT,
            "site_count": sum(counts.values()),
            "alert_count": 9,
            "category_counts": dict(sorted(counts.items())),
            "boundary_source": "API Découpage administratif — communes de l'Orne",
            "sha256": _sha256(OUTPUT),
            "checks_passed": sum(counts.values()) == 30,
        }
        VALIDATION.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return result
    finally:
        app.exitQgis()
        profile.cleanup()


if __name__ == "__main__":
    print(json.dumps(build_map(), ensure_ascii=False, sort_keys=True))
