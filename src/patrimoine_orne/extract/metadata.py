"""Création et contrôle des métadonnées associées aux fichiers bruts."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from .naming import as_utc, normalise_token

SCHEMA_VERSION = "1.0"
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_FIELDS = frozenset(
    {
        "schema_version",
        "source_id",
        "resource_id",
        "scope",
        "retrieved_at",
        "source_page_url",
        "request_url",
        "final_url",
        "http_status",
        "content_type",
        "format",
        "license",
        "file_name",
        "file_size_bytes",
        "sha256",
        "extractor",
        "extractor_version",
        "git_commit",
        "query",
        "notes",
    }
)


def sha256_file(path: Path | str, *, chunk_size: int = 1024 * 1024) -> str:
    """Calcule l'empreinte SHA-256 d'un fichier sans le charger entièrement."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def metadata_sidecar_path(data_file: Path | str) -> Path:
    """Retourne le chemin du fichier JSON voisin d'un fichier brut."""
    path = Path(data_file)
    return path.with_name(f"{path.name}.metadata.json")


def create_retrieval_metadata(
    *,
    data_file: Path | str,
    source_id: str,
    resource_id: str,
    scope: str,
    retrieved_at: datetime,
    source_page_url: str,
    request_url: str,
    final_url: str,
    http_status: int,
    content_type: str,
    format: str,
    license: str,
    extractor: str,
    extractor_version: str,
    git_commit: str | None = None,
    query: Mapping[str, Any] | str | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """Produit les métadonnées minimales d'un fichier brut déjà écrit."""
    path = Path(data_file)
    if not path.is_file():
        raise FileNotFoundError(path)
    if not isinstance(http_status, int) or not 100 <= http_status <= 599:
        raise ValueError("http_status doit être un code HTTP valide")

    metadata = {
        "schema_version": SCHEMA_VERSION,
        "source_id": normalise_token(source_id, field="source_id"),
        "resource_id": normalise_token(resource_id, field="resource_id"),
        "scope": normalise_token(scope, field="scope"),
        "retrieved_at": as_utc(retrieved_at).isoformat().replace("+00:00", "Z"),
        "source_page_url": source_page_url,
        "request_url": request_url,
        "final_url": final_url,
        "http_status": http_status,
        "content_type": content_type,
        "format": format.lower().lstrip("."),
        "license": license,
        "file_name": path.name,
        "file_size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "extractor": extractor,
        "extractor_version": extractor_version,
        "git_commit": git_commit,
        "query": query if query is not None else {},
        "notes": notes if notes is not None else [],
    }
    validate_metadata(metadata)
    return metadata


def validate_metadata(metadata: Mapping[str, Any]) -> None:
    """Valide la structure minimale des métadonnées sans accéder au fichier brut."""
    missing = REQUIRED_FIELDS.difference(metadata)
    if missing:
        raise ValueError(f"champs de métadonnées manquants : {', '.join(sorted(missing))}")
    if metadata["schema_version"] != SCHEMA_VERSION:
        raise ValueError("version de schéma non prise en charge")
    if not isinstance(metadata["file_size_bytes"], int) or metadata["file_size_bytes"] < 0:
        raise ValueError("file_size_bytes invalide")
    if not isinstance(metadata["sha256"], str) or not _SHA256_RE.fullmatch(metadata["sha256"]):
        raise ValueError("sha256 invalide")
    if not isinstance(metadata["http_status"], int) or not 100 <= metadata["http_status"] <= 599:
        raise ValueError("http_status invalide")
    if not isinstance(metadata["notes"], list):
        raise ValueError("notes doit être une liste")


def verify_data_file(data_file: Path | str, metadata: Mapping[str, Any]) -> None:
    """Vérifie que le nom, la taille et le hash correspondent au fichier brut."""
    validate_metadata(metadata)
    path = Path(data_file)
    if path.name != metadata["file_name"]:
        raise ValueError("le nom du fichier brut ne correspond pas aux métadonnées")
    if path.stat().st_size != metadata["file_size_bytes"]:
        raise ValueError("la taille du fichier brut ne correspond pas aux métadonnées")
    if sha256_file(path) != metadata["sha256"]:
        raise ValueError("le hash du fichier brut ne correspond pas aux métadonnées")


def write_metadata_sidecar(
    data_file: Path | str,
    metadata: Mapping[str, Any],
    *,
    overwrite: bool = False,
) -> Path:
    """Écrit le JSON voisin après vérification du fichier brut."""
    verify_data_file(data_file, metadata)
    sidecar = metadata_sidecar_path(data_file)
    if sidecar.exists() and not overwrite:
        raise FileExistsError(sidecar)
    sidecar.write_text(
        json.dumps(dict(metadata), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return sidecar
