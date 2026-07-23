# Phase 8 — Corpus commun de 80 dossiers

Date : 23 juillet 2026

## Résultat

Les 30 dossiers pilotes et les 50 dossiers du premier lot sont réunis dans un
format commun.

| Contrôle | Résultat |
|---|---:|
| dossiers pilotes | 30 |
| dossiers du lot 1 | 50 |
| dossiers communs | 80 |
| références `IA` uniques | 80 |
| activités structurées | 109 |
| dossiers avec un `site_id` | 30 |
| dossiers encore sans `site_id` | 50 |
| URLs de dossier dupliquées | 0 |
| rapprochements potentiels détectés | 0 |

Tous les dossiers possèdent une source et au moins une activité classée.

## Format commun

Chaque dossier comporte désormais les mêmes familles de champs :

- référence et origine du dossier ;
- statut de traitement et éventuel `site_id` ;
- titre, commune, adresse, lieu-dit et URL sources ;
- dénominations, activités, secteurs et installations ;
- périodes d'activité et périodes issues de `SCLE`, conservées séparément ;
- situation actuelle ;
- localisation et précision ;
- protections, objets techniques et sources lorsqu'ils sont disponibles ;
- décision de rapprochement.

Les champs absents ne sont pas inventés. Les 30 pilotes conservent leur
enrichissement, leur géographie et leur identifiant. Les 50 nouveaux dossiers
sont structurés et classés mais restent à enrichir ; leur `site_id` est donc
vide par décision méthodologique.

## Contrôle des doublons

Les contrôles portent sur les références `IA`, les URLs de dossier, l'adresse
ou le lieu-dit normalisés dans une même commune et les points sources distants
de 50 mètres ou moins.

Aucun candidat au rapprochement n'a été trouvé parmi ces 80 dossiers. Cela ne
prouve pas l'absence définitive de relations : de nouveaux indices peuvent
apparaître lors du traitement des 239 dossiers restants.

## Livrables

- corpus JSON complet local : `data/interim/phase8_corpus_80.json` ;
- vue CSV : `reports/quality/phase8_corpus_80.csv` ;
- résumé contrôlé : `reports/quality/phase8_corpus_80_resume.json` ;
- file de rapprochement : `reports/quality/phase8_corpus_80_rapprochements.csv`.

## Portée

Les 80 dossiers correspondent provisoirement à 80 sites de travail. Ce n'est
pas un total départemental. Le nombre canonique restera inconnu jusqu'au
traitement et à la revue des 319 dossiers.
