"""Téléchargement HTTP reproductible vers la zone de données brutes."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping
from urllib.request import Request, urlopen

from .metadata import create_retrieval_metadata, write_metadata_sidecar
from .naming import build_raw_path

Validator = Callable[[Path], dict[str, Any]]


@dataclass(frozen=True)
class RetrievalSpec:
    """Description complète d'une récupération HTTP."""

    source_id: str
    resource_id: str
    scope: str
    source_page_url: str
    request_url: str
    format: str
    license: str
    query: Mapping[str, Any] | str | None = None
    notes: tuple[str, ...] = ()
    headers: Mapping[str, str] = field(default_factory=dict)
    validator: Validator | None = None
    method: str = "GET"
    body: bytes | None = None


@dataclass(frozen=True)
class RetrievalResult:
    """Résultat local et observations d'une récupération réussie."""

    data_file: Path
    metadata_file: Path
    metadata: dict[str, Any]
    observations: dict[str, Any]


def retrieve(
    spec: RetrievalSpec,
    *,
    retrieved_at: datetime | None = None,
    raw_root: Path | str = Path("data/raw"),
    extractor: str,
    extractor_version: str,
    git_commit: str | None,
    timeout: int = 120,
    max_bytes: int | None = 20 * 1024 * 1024,
) -> RetrievalResult:
    """Télécharge, valide et documente une ressource sans écraser le brut."""
    timestamp = retrieved_at or datetime.now(timezone.utc)
    data_file = build_raw_path(
        source_id=spec.source_id,
        resource_id=spec.resource_id,
        scope=spec.scope,
        retrieved_at=timestamp,
        extension=spec.format,
        root=raw_root,
    )
    data_file.parent.mkdir(parents=True, exist_ok=True)
    if data_file.exists():
        raise FileExistsError(data_file)

    temp_file = data_file.with_name(f".{data_file.name}.part")
    if temp_file.exists():
        raise FileExistsError(temp_file)

    headers = {
        "User-Agent": "PatrimoineIndustrielOrne/0.2 (+datajournalisme)",
        "Accept": "*/*",
        **dict(spec.headers),
    }
    request = Request(
        spec.request_url,
        data=spec.body,
        headers=headers,
        method=spec.method,
    )

    try:
        with urlopen(request, timeout=timeout) as response, temp_file.open("xb") as stream:
            total_bytes = 0
            while chunk := response.read(64 * 1024):
                total_bytes += len(chunk)
                if max_bytes is not None and total_bytes > max_bytes:
                    raise ValueError(f"réponse supérieure à la limite de {max_bytes} octets")
                stream.write(chunk)

            status = int(getattr(response, "status", response.getcode()))
            final_url = response.geturl()
            content_type = response.headers.get("Content-Type", "")

        observations = spec.validator(temp_file) if spec.validator else {}
        os.replace(temp_file, data_file)
        metadata = create_retrieval_metadata(
            data_file=data_file,
            source_id=spec.source_id,
            resource_id=spec.resource_id,
            scope=spec.scope,
            retrieved_at=timestamp,
            source_page_url=spec.source_page_url,
            request_url=spec.request_url,
            final_url=final_url,
            http_status=status,
            content_type=content_type,
            format=spec.format,
            license=spec.license,
            extractor=extractor,
            extractor_version=extractor_version,
            git_commit=git_commit,
            query=spec.query,
            notes=list(spec.notes),
        )
        metadata_file = write_metadata_sidecar(data_file, metadata)
    except Exception:
        temp_file.unlink(missing_ok=True)
        sidecar = data_file.with_name(f"{data_file.name}.metadata.json")
        if data_file.exists() and not sidecar.exists():
            data_file.unlink()
        raise

    return RetrievalResult(
        data_file=data_file,
        metadata_file=metadata_file,
        metadata=metadata,
        observations=observations,
    )
