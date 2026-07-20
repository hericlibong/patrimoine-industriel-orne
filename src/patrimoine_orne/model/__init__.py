"""Modèle relationnel DuckDB du patrimoine industriel de l'Orne."""

from .validation import ValidationIssue, assert_database_valid, validate_database


def connect_database(*args, **kwargs):
    """Charge paresseusement l'initialiseur pour permettre son usage en module."""
    from .database import connect_database as connect

    return connect(*args, **kwargs)


def initialize_database(*args, **kwargs):
    """Charge paresseusement le schema DuckDB."""
    from .database import initialize_database as initialize

    return initialize(*args, **kwargs)

__all__ = [
    "ValidationIssue",
    "assert_database_valid",
    "connect_database",
    "initialize_database",
    "validate_database",
]
