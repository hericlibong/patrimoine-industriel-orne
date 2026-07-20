# Patrimoine industriel de l'Orne

Projet datajournalistique destiné à montrer comment l'industrie a façonné le
territoire de l'Orne et ce qu'il en reste aujourd'hui.

La première étape ne consiste pas à développer l'application publique. Elle
consiste à construire un socle de données vérifiable, documenté et
reproductible.

## État du projet

**Phases 0 et 1 terminées — phase 2 en cours.**

Le suivi détaillé est maintenu localement dans `docs/roadmap.md`, qui n'est pas
versionné.

## Documents de référence

- [Cadrage](docs/cadrage.md)
- [Méthodologie](docs/methodologie.md)
- [Conventions d'extraction](docs/conventions_extraction.md)
- [Dictionnaire des données](docs/dictionnaire_donnees.md)
- [Journal des décisions](docs/journal_decisions.md)
- [Sources à auditer](config/sources.yml)
- [Classifications provisoires](config/classifications.yml)
- [Périmètre opérationnel](config/perimetre.yml)

## Organisation des données

- `data/raw/` : fichiers originaux, jamais modifiés ;
- `data/interim/` : résultats intermédiaires reproductibles ;
- `data/manual/` : corrections humaines documentées ;
- `data/processed/` : corpus nettoyé ;
- `data/exports/` : livrables CSV, Parquet et GeoJSON.

## Principes

1. Vérifier les sources avant toute extraction massive.
2. Conserver les données brutes intactes.
3. Distinguer les faits sourcés, les données calculées et les interprétations.
4. Documenter les incertitudes et la précision géographique.
5. Ne construire l'application qu'après validation du socle V1.
