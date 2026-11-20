"""Sert le dossier prototype/ en local, sans cache navigateur (phase 10.E).

Le serveur standard de Python ne dit rien du cache : le navigateur peut alors garder une
ancienne copie des scripts d'un prototype et la réutiliser après une modification, même
quand la page elle-même est rechargée. Ce serveur interdit cette mise en cache.

    python tools/serveur_prototypes.py            # http://127.0.0.1:8771/
"""

from __future__ import annotations

import functools
import http.server
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1] / "prototype"


class SansCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Expires", "0")
        super().end_headers()


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
    gestion = functools.partial(SansCache, directory=str(RACINE))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), gestion) as serveur:
        print(f"Prototypes servis sans cache sur http://127.0.0.1:{port}/", flush=True)
        serveur.serve_forever()


if __name__ == "__main__":
    main()
