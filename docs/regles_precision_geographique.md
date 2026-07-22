# Règles de précision géographique

Version 1.0 — validée le 22 juillet 2026 à la clôture de la phase 6

## Principe

La précision décrit **ce que la géométrie permet réellement de localiser**. Elle
ne dépend ni de la beauté de la carte, ni du nombre de décimales, ni de la seule
présence d'une coordonnée dans une source.

La forme, la méthode, la précision et la fiabilité sont enregistrées séparément.

## Niveaux validés

| Code | Ce que la géométrie localise | Condition minimale |
|---|---|---|
| `emprise_site_verifiee` | limites de l'ensemble industriel | limites contrôlées avec une source adaptée et une revue humaine |
| `parcelle_verifiee` | parcelle rattachée au site | correspondance cadastrale contrôlée, et non simple intersection d'un point |
| `batiment_verifie` | bâtiment industriel identifié | bâtiment reconnu sur une source cartographique, une orthophotographie ou le terrain |
| `point_site_verifie` | point appartenant au site | rattachement au site contrôlé, sans contour suffisamment fiable |
| `point_adresse` | adresse géocodée | adresse unique concordante, sans validation du bâtiment industriel |
| `point_approximatif` | position générale du site | point source cohérent, mais cible physique non vérifiée |
| `zone_documentaire` | zone indiquée par une source | contour non encore aligné et vérifié sur le terrain actuel |

Les quatre premiers niveaux exigent une validation humaine appuyée par une
source permettant réellement d'identifier la cible.

## Règles d'attribution

1. Une coordonnée POP valide reste `point_approximatif` tant que le bâtiment ou
   le site n'a pas été reconnu sur une source adaptée.
2. Un contour POP reste `zone_documentaire` tant que ses limites n'ont pas été
   contrôlées.
3. Une parcelle rencontrée automatiquement par un point est une candidate, pas
   une `parcelle_verifiee`.
4. Un résultat BAN concordant reste `point_adresse` et ne prouve pas le bâtiment
   industriel.
5. En présence de plusieurs géométries, elles sont conservées séparément avec
   leur méthode et leur précision propres.
6. La géométrie affichée par défaut utilise le niveau le plus prudent compatible
   avec la source.
7. Le centre d'une commune n'est jamais utilisé comme emplacement de site.
8. `commune_seule` et `non_localise` n'autorisent aucune géométrie de site.
9. Une géométrie n'est jamais déplacée pour la rendre visuellement cohérente.
10. Toute promotion vers un niveau vérifié conserve la source, la méthode, la
    date et la personne ou le protocole de contrôle.

## Application au pilote

- les 30 points POP restent `point_approximatif` ;
- les 29 contours POP restent `zone_documentaire` ;
- les 30 parcelles actuelles restent candidates ;
- les trois résultats BAN acceptés restent des points d'adresse secondaires ;
- aucune géométrie du pilote n'atteint encore un niveau vérifié.

Cette prudence n'empêche pas la cartographie de travail. Elle empêche seulement
la carte de laisser croire qu'un bâtiment ou une emprise a été identifié avec
une précision supérieure à la preuve disponible.
