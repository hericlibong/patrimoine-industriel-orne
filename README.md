# Patrimoine industriel de l'Orne

Projet datajournalistique destiné à montrer comment l'industrie a façonné le
territoire de l'Orne et ce qu'il en reste aujourd'hui.

La première étape ne consiste pas à développer l'application publique. Elle
consiste à construire un socle de données vérifiable, documenté et
reproductible.

## État du projet

**Phases 0 à 6 terminées — phase 7 en cours.**

Le premier bloc de la phase 7 est validé : le socle pilote est disponible en
DuckDB, CSV, Parquet et GeoJSON. Les exports des 30 sites et des 47 phases
d'activité comportent désormais des périodes historiques filtrables.

Le suivi détaillé est maintenu localement dans `docs/roadmap.md`, qui n'est pas
versionné.

## Documents de référence

- [Cadrage](docs/cadrage.md)
- [Pistes éditoriales et datavisualisation](docs/pistes_editoriales.md)
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
- [Règles de précision géographique](docs/regles_precision_geographique.md)
- [Périmètre opérationnel](config/perimetre.yml)
- [Méthodes d'extraction validées](config/extraction.yml)
- [Règles structurelles du modèle](config/regles_modele.yml)
- [Validation du modèle V1](reports/quality/phase3_validation_modele.md)
- [Test des secteurs sur l'échantillon](reports/quality/phase4_test_secteurs.md)
- [Test de la chronologie et de la situation actuelle](reports/quality/phase4_chronologie_situation.md)
- [Test de qualité et de reproductibilité](reports/quality/phase4_qualite_classifications.md)
- [Validation finale de la phase 4](reports/quality/phase4_validation_finale.md)
- [Validation finale du corpus pilote](reports/quality/phase5_validation_finale.md)
- [Contrôle des localisations du pilote](reports/quality/phase6_localisation.md)
- [Test du contexte territorial](reports/quality/phase6_contexte_territorial.md)
- [Contrôle cartographique du pilote](reports/quality/phase6_controle_cartographique.md)
- [Bilan de qualité spatiale](reports/quality/phase6_bilan_qualite_spatiale.md)
- [Consolidation du socle pilote V1](reports/quality/phase7_consolidation.md)
- [Projet QGIS de contrôle](qgis/controle_phase6.qgs)

## Produire le socle pilote V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.socle_v1
```

Cette commande reconstruit la base DuckDB de référence et les exports CSV,
Parquet et GeoJSON dans `data/processed/` et `data/exports/`. Le fichier
`sites_pilote_v1.csv` présente une ligne par site ; `activites_pilote_v1.csv`
présente une ligne par phase d'activité avec ses dates et périodes. Ces
livrables sont générés localement et ne sont pas versionnés.

## Localisations du pilote

Les contrôles BAN et cadastraux sont reproductibles avec :

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.extract.pilot_geography
python -m patrimoine_orne.geocode.pilot
python -m patrimoine_orne.extract.territorial_context
python -m patrimoine_orne.geocode.territorial_context
python -m patrimoine_orne.geocode.cartographic_control
```

La première commande interroge les services publics IGN et archive les réponses.
La seconde qualifie les résultats sans transformer une géométrie automatique en
localisation vérifiée.
Les deux suivantes extraient puis calculent le contexte territorial. La dernière
reconstruit les cinq couches GeoJSON utilisées par le projet QGIS de contrôle.

Le fichier projet QGIS est ensuite généré et validé avec l'environnement Python
fourni par QGIS :

```powershell
& "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat" `
  tools\generate_qgis_project.py
```

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
