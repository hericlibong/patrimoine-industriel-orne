# Phase 6 — Localisation du corpus pilote

Contrôle effectué le 22 juillet 2026 sur les 30 sites du pilote.

## Résultat simple

| Contrôle | Résultat |
|---|---:|
| Points POP présents et valides | 30 / 30 |
| Emprises documentaires POP disponibles | 29 / 30 |
| Adresses POP renseignées | 7 / 30 |
| Adresses avec un numéro unique soumises au géocodeur | 4 |
| Géocodages concordants avec le point POP | 3 / 4 |
| Parcelles actuelles rencontrées par le point POP | 30 / 30 |
| Références cadastrales anciennes encore directement concordantes | 6 / 30 |
| Géométries qualifiées de vérifiées | 0 |
| Coordonnées inventées | 0 |

Les 30 sites peuvent donc être placés sur une carte de travail. Ils restent
tous signalés comme `geometrie_approximative` jusqu'au contrôle cartographique.

## Coordonnées et emprises POP

Les 30 notices contiennent un point en Lambert-93 et son équivalent WGS84. Les
points sont numériques et se trouvent dans l'enveloppe géographique de l'Orne.
Ce contrôle détecte les erreurs grossières, mais ne prouve pas que le point vise
le bon bâtiment.

Vingt-neuf notices proposent aussi un contour. Pour quatre d'entre elles, le
champ Lambert-93 contient le marqueur `$25`, tandis que le contour WGS84 rendu
par POP reste disponible. Ces emprises sont conservées comme
`zone_documentaire`. La notice `IA00060915` ne possède qu'un point exploitable.

## Géocodage des adresses

Sept notices ont une adresse. Quatre seulement comportent un numéro unique et
ont été interrogées dans le géocodeur BAN de la Géoplateforme. Trois résultats
sont concordants, à une distance comprise entre 7,1 et 52,8 mètres du point POP.

Le résultat de `IA00060969`, ancienne adresse « 25 rue de Mamers » à Alençon,
est rejeté : le géocodeur propose « 25 rue du Mans », à environ 1,2 kilomètre du
point POP. Les trois adresses décrivant une rue entière ou plusieurs numéros ne
produisent volontairement aucun point.

## Cadastre actuel

L'intersection exacte de chaque point POP avec l'API Carto renvoie une parcelle
actuelle pour les 30 sites. Ces parcelles sont enregistrées comme candidates.
Elles ne prouvent ni l'emprise historique du site, ni sa propriété, ni la
présence actuelle des bâtiments industriels.

Seules six références actuelles concordent directement avec une référence
cadastrale citée dans la notice. Les autres écarts sont compatibles avec des
divisions, regroupements, changements de section ou fusions de communes. Ils ne
sont pas traités comme des erreurs.

## Décision pour la suite

- le point POP sert de géométrie de référence provisoire pour l'affichage ;
- le contour POP est conservé comme emprise documentaire lorsqu'il existe ;
- les points BAN et les parcelles actuelles restent des éléments de contrôle ;
- aucun centroïde communal n'est créé ;
- le prochain bloc vérifiera visuellement les géométries et repérera les points
  aberrants avant de relever leur niveau de précision.
