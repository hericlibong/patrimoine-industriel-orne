# Phase 8 — Validation du corpus complet V1

Date : 24 juillet 2026  
Décision : **corpus complet V1 validé**

## Périmètre validé

- 319 dossiers sources ont été traités ;
- 1 dossier de synthèse sans emprise est conservé comme source mais exclu du
  décompte ;
- le corpus principal comprend **318 sites canoniques** ;
- 314 sites portent au moins une activité productive ;
- 4 sites sont des composants non productifs ;
- 403 activités sont structurées ;
- 73 sites ont plusieurs activités et 34 relèvent de plusieurs secteurs.

Les identifiants des 318 sites sont uniques et stables. Les exports JSON,
DuckDB, CSV, Parquet et GeoJSON contiennent les mêmes sites.

## Répartition par secteur

Un site peut appartenir à plusieurs secteurs ; les nombres ne doivent donc pas
être additionnés pour retrouver 318.

| Secteur | Sites | Part du corpus |
|---|---:|---:|
| Agroalimentaire | 113 | 35,5 % |
| Métallurgie et travail des métaux | 79 | 24,8 % |
| Textile, habillement et cuir | 76 | 23,9 % |
| Bois, papier et imprimerie | 32 | 10,1 % |
| Verre, céramique et matériaux de construction | 27 | 8,5 % |
| Construction mécanique et électrique | 10 | 3,1 % |
| Extraction | 9 | 2,8 % |
| Production d'énergie | 6 | 1,9 % |
| Chimie, caoutchouc et plastiques | 3 | 0,9 % |

## Chronologie

Les 318 sites possèdent au moins une période documentaire calculée depuis les
siècles de construction ou de transformation indiqués par la source.

- 242 sites sont associés à la période 1850-1913 ;
- 108 à 1914-1945 ;
- 107 à 1789-1849 ;
- 92 à 1946-1975 ;
- 56 à une période antérieure à 1789 ;
- 7 à 1976-2000.

Ces catégories peuvent se cumuler sur un même site. Elles ne décrivent pas
automatiquement toute sa durée de production.

La chronologie directe des activités est beaucoup moins complète : seulement
42 activités, réparties sur 29 sites, possèdent une période calculée depuis des
dates d'activité structurées. Pour les autres, la publication doit utiliser la
période documentaire du site avec un libellé adapté.

## Situation actuelle

Cette dimension reste très incomplète :

- conservation inconnue pour 315 sites ;
- accessibilité inconnue pour 316 sites ;
- seulement 4 situations actuelles disposent d'une source récente retenue.

Le corpus est donc adapté à un récit historique et territorial. Il ne permet
pas encore de produire un guide départemental de visite ni une statistique
fiable sur ce qu'il reste aujourd'hui.

## Localisation et contexte territorial

- les 318 sites possèdent un point source ;
- 290 points restent approximatifs ;
- 28 sont associés à une zone documentaire ;
- aucune coordonnée n'a été inventée.

Indicateurs recalculés :

- eau : 213 sites à moins de 100 m et 297 à moins de 500 m ;
- forêt : 12 sites dans une formation, 163 dans une formation ou à moins de
  100 m, 293 dans une formation ou à moins de 500 m ;
- minerais : 13 sites à moins de 1 km et 215 à moins de 10 km d'un indice BRGM ;
- rail : 72 sites à moins de 500 m ; 149 sans tronçon répertorié à moins de
  5 km.

Ces proximités sont des indices spatiaux et non des preuves de causalité.

## Enrichissements

- 16 protections MH confirmées sur 16 sites ;
- 31 objets Palissy conservés comme liens documentaires à vérifier ;
- 131 recoupements CASIAS concernant 123 sites ;
- 8 rapprochements CASIAS restent ambigus et ne sont pas affirmés ;
- 170 candidats CASIAS d'élargissement restent hors corpus.

## Limites non bloquantes

Les limites restantes sont conservées dans
`reports/quality/phase8_anomalies_restantes.csv`. Elles ne bloquent pas une
première publication si l'interface :

- affiche le niveau de précision géographique ;
- distingue période documentaire et période d'activité ;
- laisse l'état actuel à `inconnu` en l'absence de source récente ;
- ne transforme pas CASIAS en inventaire patrimonial ;
- ne présente pas les objets Palissy comme encore présents sans vérification.

## Livrables

- `data/processed/corpus_complet_v1.json` ;
- `data/processed/patrimoine_orne_corpus_complet_v1.duckdb` ;
- `data/exports/sites_corpus_complet_v1.csv` ;
- `data/exports/activites_corpus_complet_v1.csv` ;
- `data/exports/sites_corpus_complet_v1.parquet` ;
- `data/exports/activites_corpus_complet_v1.parquet` ;
- `data/exports/sites_corpus_complet_v1.geojson`.

Les empreintes et contrôles techniques sont enregistrés dans
`reports/quality/phase8_validation_corpus_complet.json`.

