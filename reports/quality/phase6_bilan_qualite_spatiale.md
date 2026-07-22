# Phase 6 — Bilan de qualité spatiale

Validation finale du 22 juillet 2026.

## Conclusion

La phase 6 est validée. Les données permettent de cartographier les 30 sites du
pilote pour le contrôle et l'analyse, sans leur attribuer une précision
artificielle.

Cette validation autorise le passage à la construction du socle V1. Elle ne
signifie pas que les bâtiments ou les emprises historiques sont tous localisés
avec précision.

## Résultats consolidés

| Indicateur | Résultat |
|---|---:|
| Sites pilotes | 30 |
| Points POP valides | 30 |
| Points cohérents entre Lambert-93 et WGS84 | 30 |
| Emprises documentaires disponibles | 29 |
| Parcelles actuelles candidates | 30 |
| Références cadastrales directement concordantes | 6 |
| Géocodages BAN concordants | 3 |
| Localisations à vérifier | 9 |
| Points grossièrement aberrants | 0 |
| Géométries qualifiées de vérifiées | 0 |
| Coordonnées inventées | 0 |

## Précision retenue

Les 30 points de référence restent des `point_approximatif`. Les 29 contours
restent des `zone_documentaire`. Les parcelles et les points BAN sont conservés
comme éléments secondaires de contrôle.

Les règles complètes sont publiées dans
`docs/regles_precision_geographique.md`. Elles valident notamment la séparation
entre géométrie, méthode de localisation, précision et fiabilité.

## Contrôle cartographique

Le projet a été généré puis relu avec QGIS 3.44.12. Les cinq couches sont
résolues, le CRS de projet est `EPSG:2154` et le fond OpenStreetMap est reconnu.

Neuf localisations ont demandé une décision explicite : une emprise absente,
une très petite, deux très grandes, un point légèrement extérieur au contour,
trois adresses non uniques et un résultat BAN non concordant. Aucun de ces cas
n'a été corrigé silencieusement.

## Contexte territorial

Les distances aux cours d'eau, forêts, indices miniers et voies ferrées ont été
calculées dans le système de travail prévu. Elles sont utilisables comme indices
spatiaux, mais ne prouvent aucune causalité historique.

## Limites qui restent ouvertes

- aucun point, bâtiment, contour ou parcelle n'est encore vérifié au sens fort ;
- quatre contours POP ne sont disponibles qu'en WGS84 dans la donnée dérivée ;
- les références cadastrales anciennes concordent rarement directement avec le
  parcellaire actuel ;
- les fonds et couches actuels ne remplacent ni les plans historiques, ni les
  orthophotographies, ni les vérifications de terrain ;
- les résultats du pilote ne sont pas extrapolables aux 319 dossiers.

Ces limites sont documentées et n'empêchent pas la validation méthodologique de
la phase.

## Décision de phase

**Phase 6 terminée — passage autorisé à la phase 7, “Produire le socle V1”.**
