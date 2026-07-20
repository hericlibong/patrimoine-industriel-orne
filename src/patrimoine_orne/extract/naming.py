"""Construction des noms et chemins des fichiers bruts."""

from __future__ import annotations

import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

_TOKEN_RE = re.compile(r"[^a-z0-9]+")
_EXTENSION_RE = re.compile(r"^[a-z0-9]+(?:\.[a-z0-9]+)*$")


def normalise_token(value: str, *, field: str) -> str:
    """Normalise un élément de nom de fichier en jeton ASCII sûr."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} doit être une chaîne non vide")

    ascii_value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    token = _TOKEN_RE.sub("_", ascii_value).strip("_")
    if not token:
        raise ValueError(f"{field} ne contient aucun caractère utilisable")
    return token


def normalise_extension(extension: str) -> str:
    """Valide une extension simple ou composée, sans point initial obligatoire."""
    if not isinstance(extension, str):
        raise ValueError("extension doit être une chaîne")
    clean_extension = extension.lower().lstrip(".")
    if not _EXTENSION_RE.fullmatch(clean_extension):
        raise ValueError("extension invalide")
    return clean_extension


def as_utc(value: datetime) -> datetime:
    """Convertit une date consciente de son fuseau en UTC."""
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("retrieved_at doit contenir un fuseau horaire")
    return value.astimezone(timezone.utc)


def build_raw_filename(
    *,
    source_id: str,
    resource_id: str,
    scope: str,
    retrieved_at: datetime,
    extension: str,
) -> str:
    """Construit le nom canonique d'un fichier brut."""
    timestamp = as_utc(retrieved_at).strftime("%Y%m%dT%H%M%SZ")
    parts = (
        normalise_token(source_id, field="source_id"),
        normalise_token(resource_id, field="resource_id"),
        normalise_token(scope, field="scope"),
        timestamp,
    )
    return f"{'__'.join(parts)}.{normalise_extension(extension)}"


def build_raw_path(
    *,
    source_id: str,
    resource_id: str,
    scope: str,
    retrieved_at: datetime,
    extension: str,
    root: Path | str = Path("data/raw"),
) -> Path:
    """Construit le chemin canonique d'un fichier brut depuis la racine du projet."""
    retrieved_utc = as_utc(retrieved_at)
    source_token = normalise_token(source_id, field="source_id")
    filename = build_raw_filename(
        source_id=source_token,
        resource_id=resource_id,
        scope=scope,
        retrieved_at=retrieved_utc,
        extension=extension,
    )
    return (
        Path(root)
        / source_token
        / retrieved_utc.strftime("%Y")
        / retrieved_utc.strftime("%Y-%m-%d")
        / filename
    )
