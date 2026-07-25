from pathlib import Path

import yaml


ROOT = Path(__file__).parents[1]
CONFIG_PATH = ROOT / "config" / "editorial.yml"


def load_config() -> dict:
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def field_index(table: dict) -> dict[str, dict]:
    return {field["nom"]: field for field in table["champs"]}


def test_editorial_configuration_is_versioned_and_documented() -> None:
    config = load_config()

    assert config["version"] == "1.3"
    assert config["status"] == "phase9_bloc4_valide"
    assert (ROOT / "docs" / "modele_editorial.md").exists()


def test_source_and_derived_texts_are_strictly_separated() -> None:
    config = load_config()
    levels = config["niveaux_textes"]

    assert levels["historique_source"]["nature"] == "source"
    assert levels["historique_source"]["modifiable"] is False
    assert levels["description_source"]["modifiable"] is False
    assert levels["resume_documentaire"]["nature"] == "derivee"
    assert levels["resume_documentaire"]["sources_obligatoires"] is True
    assert levels["note_journalistique"]["nature"] == "editoriale"
    assert levels["note_journalistique"]["auteur_obligatoire"] is True


def test_recits_sites_preserves_source_fields_and_provenance() -> None:
    config = load_config()
    table = config["recits_sites"]
    fields = field_index(table)

    assert table["cle_primaire"] == "site_id"
    assert table["relation"] == "sites.site_id"
    assert len(fields) == len(table["champs"])
    for name in (
        "historique_source",
        "historique_source_sha256",
        "description_source",
        "description_source_sha256",
        "source_reference",
        "source_url",
        "resume_documentaire",
        "note_journalistique",
    ):
        assert name in fields
    for name in (
        "historique_source",
        "description_source",
        "source_reference",
        "source_url",
    ):
        assert fields[name]["modifiable"] is False


def test_media_publication_requires_a_separate_rights_decision() -> None:
    config = load_config()
    table = config["medias"]
    fields = field_index(table)

    assert table["cle_primaire"] == "media_site_id"
    assert len(fields) == len(table["champs"])
    for name in (
        "selection_media_code",
        "statut_droits_code",
        "statut_autorisation_code",
        "usage_media_code",
        "credit_source",
        "preuve_droits_url",
        "url_fichier_source",
        "metadonnees_source",
    ):
        assert name in fields

    publication = config["prototype_interne"]["publication_media_exige"]
    assert publication["usage_media_code"] == "publication_autorisee"
    assert "retenu_publication" in config["statuts"]["selection_media"]
    assert "publication_autorisee" in config["statuts"]["usage_media"]


def test_editorial_review_is_human_and_not_an_automatic_selection() -> None:
    config = load_config()
    table = config["revue_editoriale_sites"]
    fields = field_index(table)

    assert table["cle_primaire"] == "site_id"
    for name in (
        "richesse_historique_score",
        "richesse_iconographique_score",
        "media_principal_candidat_reference",
        "besoin_recherche_complementaire",
        "statut_revue_code",
    ):
        assert name in fields
    assert "a_examiner" in config["statuts"]["revue_editoriale"]


def test_integrity_rules_prevent_overwriting_source_texts() -> None:
    integrity = load_config()["integrite"]

    assert "historique_source" in integrity["champs_sources_immuables"]
    assert "description_source" in integrity["champs_sources_immuables"]
    assert integrity["controle_sha256"] == ["historique_source", "description_source"]
    assert integrity["reconstruction"]["saisie_manuelle_dans_champs_sources"] == "interdite"
    assert integrity["reconstruction"]["texte_derive_dans_champ_source"] == "interdite"
    assert "la production echoue si un champ source du corpus est perdu" in integrity["regles"]
