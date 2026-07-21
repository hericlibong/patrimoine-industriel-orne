# Test des secteurs et installations — phase 4, bloc 1

Date : 21 juillet 2026

Statut : **bloc validé sur l'échantillon de phase 2**

## Périmètre du test

Le test porte sur les 10 notices POP / Mérimée du manifeste validé de phase 2.
Il utilise les champs structurés `DENO` et `ENER`, puis relit `HIST` pour repérer
les activités successives absentes de la dénomination principale.

Ce test mesure la cohérence du vocabulaire, pas sa couverture du futur corpus
complet.

## Résultats quantitatifs

- 10 notices examinées ;
- 13 dénominations d'activité ou d'installation ;
- 13 dénominations classées, soit 100 % sur cet échantillon ;
- 10 activités détaillées différentes ;
- 7 secteurs effectivement rencontrés ;
- 3 notices multi-activités dans `DENO` ;
- 1 notice explicitement multi-secteurs dans `DENO`.

| Secteur | Occurrences d'activités |
|---|---:|
| Agroalimentaire | 4 |
| Métallurgie et travail des métaux | 3 |
| Textile, habillement et cuir | 2 |
| Extraction | 1 |
| Bois, papier et imprimerie | 1 |
| Verre, céramique et matériaux de construction | 1 |
| Production d'énergie | 1 |

Les occurrences comptent des activités, pas des sites. Leur somme ne doit donc
pas être présentée comme un nombre de lieux.

## Cas structurants

- `IA00060965` associe une affinerie et un moulin à blé : un même site possède
  deux activités relevant du métal et de l'agroalimentaire.
- `IA00061082` associe moulin à farine et moulin à huile : deux activités, mais
  un seul secteur agroalimentaire.
- `IA00061113` associe laminoir et usine de quincaillerie : deux activités du
  même secteur métallurgique.
- `IA00061038` est dénommée filature, mais son historique indique une conversion
  ultérieure en minoterie : les champs `DENO` et `TICO` ne suffisent pas toujours
  à reconstruire les phases successives.

## Énergies

Le champ `ENER` contient 11 mentions d'énergie normalisées : hydraulique 7,
thermique 2 et électricité 2. Il contient aussi des rôles — « produite sur
place » ou « achetée » — qui doivent être stockés séparément.

La mention « roue hydraulique verticale » décrit un équipement technique, pas
une énergie. Elle est donc exclue du vocabulaire énergétique. Deux notices ont
un champ `ENER` vide alors que l'historique peut contenir une information utile,
comme la consommation de bois de la briqueterie.

## Décisions

- L'unité classée est l'activité, jamais le site entier.
- Chaque activité reçoit un seul secteur.
- `activite_mixte` est supprimé du vocabulaire des secteurs.
- Un site multi-secteurs conserve plusieurs lignes `activites`.
- Le secteur d'un site est calculé depuis ses activités et n'est pas stocké
  directement dans `sites`.
- Activité, type d'installation, bâtiment, énergie et rôle de l'énergie sont
  des dimensions distinctes.
- Une correspondance exacte peut être automatisée ; un libellé inconnu ou une
  chronologie ambiguë part en validation humaine.

Les mesures détaillées sont conservées dans
`reports/quality/phase4_secteurs_sample.json`.

## Vérifications techniques

- registre YAML chargé et contrôlé sans incohérence ;
- rapport JSON régénéré à l'identique depuis le manifeste de phase 2 ;
- termes inconnus interdits à la classification automatique silencieuse ;
- 45 tests automatisés réussis sur l'ensemble du projet ;
- compilation Python réussie.
