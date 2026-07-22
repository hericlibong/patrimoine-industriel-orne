# Phase 7 — Consolidation du socle pilote V1

Date de validation : 22 juillet 2026

## Décision

Le premier bloc de la phase 7 est validé. Le corpus pilote nettoyé, la base
DuckDB et les trois exports sont produits par une seule commande reproductible.

Cette validation porte sur les 30 sites pilotes. Elle ne transforme pas le
pilote en corpus complet et ne valide pas encore le socle V1 dans son ensemble.

## Résultats

| Contrôle | Résultat |
|---|---:|
| Sites dans le corpus consolidé | 30 |
| Sites dans DuckDB | 30 |
| Lignes dans le CSV | 30 |
| Lignes dans le Parquet | 30 |
| Entités dans le GeoJSON | 30 |
| Identifiants concordants entre les formats | oui |
| Erreurs de validation | 0 |
| Tests automatisés du projet | 99 réussis |

La base relationnelle contient également :

- 47 phases d'activité ;
- 30 états actuels et 33 usages actuels ;
- 6 protections ;
- 31 objets techniques et 31 liens objet-site ;
- 59 géométries, soit 30 points et 29 emprises documentaires ;
- 148 mentions de sources ;
- 61 identifiants externes ;
- 18 sources enregistrées.

## Livrables locaux

- `data/processed/corpus_pilote_socle_v1.json` : corpus consolidé complet ;
- `data/processed/patrimoine_orne_socle_v1.duckdb` : base relationnelle de
  référence ;
- `data/exports/sites_pilote_v1.csv` : table plate facilement consultable ;
- `data/exports/sites_pilote_v1.parquet` : même table dans un format analytique ;
- `data/exports/sites_pilote_v1.geojson` : une entité ponctuelle par site pour
  les usages cartographiques et web.

Ces fichiers sont générés et non versionnés. Le code, les règles et le rapport
de contrôle permettent de les reconstruire.

## Nettoyage appliqué

- intégration des résultats géographiques validés en phase 6 au corpus de
  phase 5 ;
- remplacement des chaînes vides par des valeurs nulles ;
- tri déterministe des sites et des objets ;
- maintien des 30 points au niveau `point_approximatif` ;
- maintien des 29 contours au niveau `zone_documentaire` ;
- conservation des sources, niveaux de confiance et anomalies ;
- passage du statut technique des 30 fiches de `candidat` à
  `cartographiable`, sans décision de publication.

## Rôle de chaque format

DuckDB est la référence : il conserve les relations multiples entre un site,
ses activités, ses objets, ses protections et ses sources.

CSV, Parquet et GeoJSON contiennent une ligne ou une entité par site. Les
valeurs multiples y sont regroupées dans des champs séparés par `|`. Ces
exports sont pratiques pour l'analyse et la cartographie, mais ils ne doivent
pas remplacer la base relationnelle pour modifier les données.

## Limites maintenues

- les 30 sites forment un échantillon méthodologique non représentatif ;
- 26 situations actuelles restent inconnues ;
- les 30 points sont approximatifs et aucune localisation n'est déclarée
  vérifiée ;
- les 31 liens Palissy restent des rapprochements candidats de confiance
  faible ;
- les exports plats simplifient les relations multiples ;
- le corpus complet sera constitué ultérieurement à partir des 319 dossiers
  sources.

## Reproduction

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.socle_v1
```

Le contrôle détaillé, les empreintes SHA-256 et les tailles des fichiers sont
enregistrés dans `reports/quality/phase7_consolidation.json`.
