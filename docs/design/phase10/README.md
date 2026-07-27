# Maquettes de direction artistique — phase 10

## Direction de référence validée

Cette troisième série est validée comme bon point de départ pour le prototypage.
Elle constitue la référence visuelle de la suite de la phase 10, sans figer les
réglages fonctionnels de la carte ni le comportement du scrollytelling :

- `07_accueil_patrimoine_industriel_oublie.svg`, `.png` et `.jpg` ;
- `08_exploration_carte_vivante.svg`, `.png` et `.jpg` ;
- `09_les_lieux_abadie_temps_statut.svg`, `.png` et `.jpg`.

L'accueil reprend l'expression `Patrimoine industriel oublié`. L'exploration
utilise `map_orne_context_reel.svg`, une carte de maquette générée à partir des
318 localisations et des couches locales de limites communales, cours d'eau,
forêts et rail actuel. Le cas Abadie donne à `Les lieux` une fonction concrète :
lire l'espace sur une photographie, suivre l'évolution documentée, puis
distinguer les dimensions de la situation actuelle et les données inconnues.

Le fichier `reference_oze_1987.jpg` est utilisé dans le panneau d'exploration.
Le fichier `reference_bohin_1982.jpg` reste une référence de travail non
sélectionnée dans ces trois écrans. Ces médias et les deux autres photographies
de référence ne valent ni sélection définitive ni autorisation de publication.

## Bloc 4 — états fonctionnels

La planche `10_exploration_etats_fonctionnels.svg`, `.png` et `.jpg`
matérialise l'architecture fonctionnelle validée de la carte :

- ouverture sur les 318 sites sans agrégats ni panneau ;
- filtre ouvert avec couverture temporelle explicitée ;
- panneau de détail sous forme de volet inférieur sur mobile.

Cette planche complète la maquette artistique `08` et sert de point de départ
évolutif. Les réglages fins seront éprouvés dans le prototype.

## Bloc 5 — niveaux de contenu

La planche `11_fiches_lieux_methode.svg`, `.png` et `.jpg` matérialise
l'architecture validée du bloc 5 :

- panneau factuel disponible pour les 318 sites ;
- page `Les lieux` réservée aux cas sélectionnés et organisée autour d'une
  question journalistique ;
- page méthode éditoriale avec sommaire ancré.

Cette planche sert de point de départ évolutif. Les longueurs, la densité et
l'ordre des modules facultatifs seront éprouvés dans le prototype.

## Seconde proposition revue mais non validée

Direction `Paysage révélé` :

- `04_accueil_paysage_revele.svg` et `.png` ;
- `05_exploration_paysage_revele.svg` et `.png` ;
- `06_portrait_abadie_paysage_revele.svg` et `.png`.

Cette série conserve une valeur de travail pour la composition de l'accueil et
le panneau contextuel de l'exploration. Son titre `L'autre Orne`, sa carte
schématique et son traitement insuffisamment expliqué de `Les lieux` sont
abandonnés.

La carte commune `map_orne_corpus_reel.svg` est dérivée du contour administratif
et des 318 coordonnées du corpus V1. Elle documente la distribution utilisée
dans la maquette, mais ne doit pas servir de modèle à la future carte
interactive : elle ne contient pas le contexte géographique nécessaire.

Les fichiers `reference_paysage_orne.jpg` et
`reference_abadie_vue_aerienne.jpg` servent uniquement à la conception
interne. Leur présence dans ce dossier ne vaut ni sélection éditoriale
définitive ni autorisation de publication.

## Proposition rejetée

Les maquettes `01_`, `02_` et `03_` correspondent à la direction
`Atlas industriel vivant`, rejetée après revue le 27 juillet 2026. Elles sont
conservées pour documenter le processus et ne doivent pas être utilisées comme
base du développement.

Le document correspondant est archivé dans
`archives/phase10_direction_artistique_v0.1_atlas_industriel.md`.
