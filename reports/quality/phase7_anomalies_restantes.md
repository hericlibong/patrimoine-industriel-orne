# Phase 7 — Anomalies et réserves restantes

Date : 22 juillet 2026

Cette liste distingue les erreurs corrigées des incertitudes qui doivent rester
visibles. Aucune anomalie restante n'empêche l'utilisation interne du socle
pilote ; plusieurs empêchent cependant de présenter certaines informations
comme vérifiées ou exhaustives.

## Anomalies et réserves ouvertes

| ID | Périmètre | Constat | Traitement actuel | Suite attendue |
|---|---|---|---|---|
| ANO-001 | Varenne `IA00060965` | 31 objets Palissy ne renvoient pas directement à la notice du site | liens candidats de confiance faible | contrôler l'origine exacte dans le complexe de forge |
| ANO-002 | 3 notices POP | `HIST` vaut `$26` dans l'objet structuré | texte rendu de la page utilisé et provenance conservée | intégrer un repli contrôlé lors de l'extraction complète |
| ANO-003 | 26 sites | aucune source récente suffisante pour la situation actuelle | valeurs `inconnu` publiées comme telles | recherche documentaire ou observation de terrain |
| ANO-004 | 30 sites pilotes | aucun rapprochement CASIAS dédié | aucune association inventée | extraction nominative et revue des candidats en phase 8 |
| ANO-005 | 9 sites | localisation signalée pour emprise absente, taille atypique, adresse ambiguë ou point hors contour | point et contour conservés sans déplacement | contrôle historique, orthophoto ou terrain selon le cas |
| ANO-006 | 30 points et 29 contours | aucune géométrie n'atteint un niveau vérifié | `point_approximatif` et `zone_documentaire` | relever la précision seulement avec une preuve adaptée |
| ANO-007 | 17 phases | période issue de `SCLE` faute de bornes d'activité structurées | méthode `siecles_source_site` visible | préciser la chronologie depuis les dossiers et archives |
| ANO-008 | Images éditoriales | aucun registre d'autorisations photographiques n'existe encore | aucune photographie tierce dans le socle V1 | créer le registre avant tout enrichissement photographique public |

## Neuf localisations à vérifier

| Référence | Motif principal | Décision conservatoire |
|---|---|---|
| `IA00061003` | emprise documentaire très petite | conserver la zone comme approximative |
| `IA00060901` | emprise documentaire très grande | conserver la zone comme approximative |
| `IA00060915` | emprise absente | afficher uniquement le point approximatif |
| `IA00061073` | adresse non unique | conserver le point POP sans géocodage |
| `IA00060969` | résultat BAN non concordant | rejeter le point BAN et conserver le point POP |
| `IA00061117` | emprise documentaire très grande | conserver la zone comme approximative |
| `IA00060909` | adresse non unique | conserver le point POP sans géocodage |
| `IA00061166` | adresse non unique | conserver le point POP sans géocodage |
| `IA00061060` | point situé hors du contour documentaire | conserver les deux géométries séparées à vérifier |

## Anomalies corrigées

| ID | Correction |
|---|---|
| COR-001 | `PA00110771`, qui renvoie à `IA00060964`, n'est plus attribuée à tort à `IA00060965` |
| COR-002 | la commune de `IA00061166` est corrigée d'une sélection erronée vers Écouché-les-Vallées |
| COR-003 | les périodes historiques manquantes dans les exports sont ajoutées aux 30 sites et 47 phases |
| COR-004 | le code provisoire `industrie_actuelle` est remplacé par le code contrôlé `activite_industrielle` |
| COR-005 | les quatre sources contemporaines sont enregistrées sous leur producteur réel et non sous une étiquette générique |

## Décision

Les anomalies ouvertes sont non bloquantes pour la validation méthodologique du
pilote. Elles deviennent bloquantes uniquement pour les affirmations qu'elles
concernent : précision spatiale vérifiée, situation actuelle, rattachement des
objets, causalité historique ou réutilisation d'une image.
