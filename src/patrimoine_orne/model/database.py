"""Initialisation et chargement de la base DuckDB du projet."""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb


DEFAULT_SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def connect_database(
    database: str | Path = ":memory:", *, install_spatial: bool = False
) -> duckdb.DuckDBPyConnection:
    """Ouvre DuckDB et charge l'extension spatiale requise par le schema."""
    connection = duckdb.connect(str(database))
    try:
        connection.load_extension("spatial")
    except duckdb.Error as error:
        if not install_spatial:
            connection.close()
            raise RuntimeError(
                "L'extension DuckDB 'spatial' est requise. "
                "Relancer avec install_spatial=True ou --install-spatial."
            ) from error
        connection.install_extension("spatial")
        connection.load_extension("spatial")
    return connection


def execute_sql_file(
    connection: duckdb.DuckDBPyConnection, path: str | Path
) -> None:
    """Execute un fichier SQL UTF-8 dans la connexion fournie."""
    connection.execute(Path(path).read_text(encoding="utf-8"))


def initialize_database(
    connection: duckdb.DuckDBPyConnection,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
) -> None:
    """Cree le schema relationnel et ses vues de lecture."""
    execute_sql_file(connection, schema_path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Initialiser la base DuckDB du projet")
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("data/processed/patrimoine_orne.duckdb"),
        help="Fichier DuckDB a creer ou mettre a jour",
    )
    parser.add_argument("--seed", type=Path, help="Jeu SQL optionnel a charger")
    parser.add_argument(
        "--install-spatial",
        action="store_true",
        help="Installer l'extension spatiale si elle n'est pas deja disponible",
    )
    return parser


def main() -> int:
    from .validation import assert_database_valid

    arguments = build_parser().parse_args()
    arguments.database.parent.mkdir(parents=True, exist_ok=True)
    connection = connect_database(
        arguments.database, install_spatial=arguments.install_spatial
    )
    try:
        initialize_database(connection)
        if arguments.seed:
            execute_sql_file(connection, arguments.seed)
        assert_database_valid(connection)
    finally:
        connection.close()
    print(f"Base valide : {arguments.database}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
