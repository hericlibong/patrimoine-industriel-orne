# Patrimoine industriel de l'Orne

Projet datajournalistique destiné à montrer comment l'industrie a façonné le
territoire de l'Orne et ce qu'il en reste aujourd'hui.

La première étape ne consiste pas à développer l'application publique. Elle
consiste à construire un socle de données vérifiable, documenté et
reproductible.

## État du projet

**Phases 0 à 3 terminées — phase 4 en cours.**

Le suivi détaillé est maintenu localement dans `docs/roadmap.md`, qui n'est pas
versionné.

## Documents de référence

- [Cadrage](docs/cadrage.md)
- [Méthodologie](docs/methodologie.md)
- [Conventions d'extraction](docs/conventions_extraction.md)
- [Dictionnaire des données](docs/dictionnaire_donnees.md)
- [Modèle des entités principales](docs/modele_donnees.md)
- [Règles du modèle](docs/regles_modele.md)
- [Journal des décisions](docs/journal_decisions.md)
- [Sources à auditer](config/sources.yml)
- [Classifications contrôlées](config/classifications.yml)
- [Règles des secteurs et installations](docs/classifications_secteurs.md)
- [Chronologie et situation actuelle](docs/classifications_chronologie_situation.md)
- [Qualité des classifications](docs/classifications_qualite.md)
- [Périmètre opérationnel](config/perimetre.yml)
- [Méthodes d'extraction validées](config/extraction.yml)
- [Règles structurelles du modèle](config/regles_modele.yml)
- [Validation du modèle V1](reports/quality/phase3_validation_modele.md)
- [Test des secteurs sur l'échantillon](reports/quality/phase4_test_secteurs.md)
- [Test de la chronologie et de la situation actuelle](reports/quality/phase4_chronologie_situation.md)
- [Test de qualité et de reproductibilité](reports/quality/phase4_qualite_classifications.md)

## Base DuckDB de test

Le modèle nécessite Python, DuckDB et l'extension DuckDB Spatial. Le jeu
d'essai est synthétique et ne décrit aucun site réel.

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.model.database `
  --database data/processed/phase3_model_test.duckdb `
  --seed tests/fixtures/model_seed.sql `
  --install-spatial
```

La commande crée le schéma, charge l'échantillon et exécute toutes les
validations transversales.

## Organisation des données

- `data/raw/` : fichiers originaux, jamais modifiés ;
- `data/interim/` : résultats intermédiaires reproductibles ;
- `data/manual/` : corrections humaines documentées ;
- `data/processed/` : corpus nettoyé ;
- `data/exports/` : livrables CSV, Parquet et GeoJSON.
- `data/archive/` : archives locales validées, non versionnées.

## Principes

1. Vérifier les sources avant toute extraction massive.
2. Conserver les données brutes intactes.
3. Distinguer les faits sourcés, les données calculées et les interprétations.
4. Documenter les incertitudes et la précision géographique.
5. Ne construire l'application qu'après validation du socle V1.
