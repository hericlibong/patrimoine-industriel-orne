from patrimoine_orne.export.qualifier_medias_v1 import (
    DEFAULT_MEDIA_CSV,
    authorization_registry,
    load_media_rows,
    qualify_rows,
)


def test_media_rights_are_qualified_without_automatic_publication() -> None:
    qualified = qualify_rows(load_media_rows(DEFAULT_MEDIA_CSV))

    assert len(qualified) == 1900
    assert {row["statut_autorisation_code"] for row in qualified} == {"a_demander"}
    assert "publication_autorisee" not in {
        row["usage_media_code"] for row in qualified
    }
    assert sum(row["statut_droits_code"] == "protege" for row in qualified) == 1783
    assert sum(row["statut_droits_code"] == "inconnus" for row in qualified) == 117


def test_authorization_registry_has_one_row_per_distinct_media() -> None:
    registry = authorization_registry(qualify_rows(load_media_rows(DEFAULT_MEDIA_CSV)))

    assert len(registry) == 1888
    assert {row["publication_publique_code"] for row in registry} == {"non_autorisee"}
    assert all(row["credit_a_conserver"] for row in registry)
