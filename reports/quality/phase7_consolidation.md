# Phase 7 — Consolidation du socle pilote V1

Date de validation : 22 juillet 2026

## Décision

Le premier bloc de la phase 7 est validé après intégration du correctif
chronologique. Le corpus pilote nettoyé, la base DuckDB et les exports des sites
et des activités sont produits par la chaîne existante.

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
| Phases dans le CSV des activités | 47 |
| Phases dans le Parquet des activités | 47 |
| Sites avec au moins une période filtrable | 30 |
| Activités avec au moins une période filtrable | 47 |
| Activités avec des dates normalisées explicites | 30 |
| Activités utilisant `SCLE` comme repérage | 17 |
| Sites avec une période contemporaine récemment sourcée | 4 |
| Identifiants concordants entre les formats | oui |
| Erreurs de validation | 0 |
| Tests automatisés du projet | 102 réussis |

La base relationnelle contient également :

- 47 phases d'activité ;
- 101 relations normalisées entre activités et périodes ;
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
- `data/exports/activites_pilote_v1.csv` : une ligne par phase d'activité avec
  les dates, périodes et méthodes de calcul ;
- `data/exports/activites_pilote_v1.parquet` : même table dans un format
  analytique.

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
- normalisation prudente des dates de 30 phases d'activité ;
- calcul de périodes filtrables pour les 30 sites et les 47 activités ;
- distinction entre périodes de chronologie industrielle et périodes de
  repérage issues de `SCLE` ;
- passage du statut technique des 30 fiches de `candidat` à
  `cartographiable`, sans décision de publication.

## Rôle de chaque format

DuckDB est la référence : il conserve les relations multiples entre un site,
ses activités, ses objets, ses protections et ses sources.

Les exports `sites_pilote_v1` contiennent une ligne ou une entité par site. Les
valeurs multiples y sont regroupées dans des champs séparés par `|`. Les
exports `activites_pilote_v1` contiennent une ligne par phase d'activité afin
de ne pas mélanger les productions successives d'un même site.

Dans DuckDB, `activites_periodes_v1` contient une ligne par couple
activité-période. Cette table est la plus adaptée aux comptages et aux
datavisualisations chronologiques.

## Correctif chronologique

La première version technique du bloc ne contenait pas de colonnes de période
dans les exports. Le vocabulaire avait été validé en phase 4, mais aucun test
fonctionnel ne vérifiait la possibilité de filtrer le CSV par période. Le bloc
a été rouvert et les validations exigent désormais une période pour chacun des
30 sites et chacune des 47 phases.

Trente phases sont datées depuis une chronologie explicite. Pour les 17 phases
restantes, toutes mono-activité dans le pilote, `SCLE` fournit seulement un
repérage chronologique du site. Cette méthode reste visible dans les données et
ne doit pas être présentée comme une preuve de durée continue de production.
Quatre sites reçoivent également la période contemporaine grâce à leur
situation actuelle documentée par une source récente.

## Limites maintenues

- les 30 sites forment un échantillon méthodologique non représentatif ;
- 26 situations actuelles restent inconnues ;
- les 30 points sont approximatifs et aucune localisation n'est déclarée
  vérifiée ;
- les 31 liens Palissy restent des rapprochements candidats de confiance
  faible ;
- les exports plats simplifient les relations multiples ;
- les périodes issues de `SCLE` datent le bâti ou ses transformations et non
  nécessairement toute la durée de l'activité ;
- le corpus complet sera constitué ultérieurement à partir des 319 dossiers
  sources.

## Reproduction

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.socle_v1
```

Le contrôle détaillé, les empreintes SHA-256 et les tailles des fichiers sont
enregistrés dans `reports/quality/phase7_consolidation.json`.
