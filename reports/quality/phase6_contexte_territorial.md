# Phase 6 — Contexte territorial du pilote

Test effectué le 22 juillet 2026 sur les 30 sites du corpus pilote.

## Résultats

### Cours d'eau

| Distance au cours d'eau le plus proche | Sites |
|---|---:|
| Moins de 25 m | 7 |
| De 25 à 100 m | 11 |
| De 100 à 500 m | 9 |
| De 500 m à 2,5 km | 3 |

Les 30 sites sont donc situés à moins de 2,5 km d'un tronçon hydrographique de
la BD TOPO, dont 18 à moins de 100 mètres. Ce résultat est un signal spatial,
pas la preuve d'un usage industriel de l'eau.

### Forêts

| Position par rapport à une formation végétale | Sites |
|---|---:|
| Dans une formation répertoriée | 2 |
| À moins de 100 m | 13 |
| De 100 à 500 m | 14 |
| De 500 m à 2,5 km | 1 |

La BD Forêt v2 diffusée par l'IGN rassemble des données produites entre 2006 et
2019. Elle décrit un contexte forestier relativement récent, mais ne permet pas
de connaître la forêt présente au moment de l'implantation industrielle.

### Géologie et indices miniers

La lithologie générale a été déterminée pour les 30 points avec la couche BRGM
au 1:1 000 000 :

| Lithologie simplifiée | Sites |
|---|---:|
| Argiles | 8 |
| Calcaires, marnes et gypse | 8 |
| Schistes et grès | 6 |
| Granites | 6 |
| Craie | 2 |

Vingt-trois sites ont un indice de mine ou de gîte BRGM à moins de 10 km : trois
à moins de 1 km, sept entre 1 et 5 km et treize entre 5 et 10 km. Les trois cas
les plus proches concernent `IA00061008`, `IA00061155` et `IA00061113`, avec des
indices de fer. Une proximité avec un indice ne prouve pas que le site utilisait
ce gisement.

### Réseau ferroviaire

| Distance au tronçon ferroviaire BD TOPO le plus proche | Sites |
|---|---:|
| Moins de 100 m | 2 |
| De 100 à 500 m | 8 |
| De 500 m à 2 km | 4 |
| De 2 à 5 km | 2 |
| Aucun tronçon dans le rayon de 5 km | 14 |

La BD TOPO conserve certains tronçons non exploités, mais ne constitue pas un
inventaire complet du réseau ferroviaire historique. Ce test décrit donc le
réseau de référence actuel et ses traces encore enregistrées.

### Systèmes de coordonnées

Les 30 points Lambert-93 (`EPSG:2154`) ont été transformés en WGS84
(`EPSG:4326`) avec PROJ. Ils coïncident avec les coordonnées WGS84 fournies par
POP, sans écart mesurable à la précision conservée.

Le Lambert-93 reste le système de travail pour les calculs en France. Le WGS84
reste le système d'échange destiné au web.

## Ce que ce bloc permet de conclure

Les données sont suffisantes pour calculer automatiquement le contexte spatial
des sites. L'eau et les formations forestières sont souvent proches dans cet
échantillon ; la proximité ferroviaire et minérale est plus variable.

Ces résultats ne répondent pas encore à la question « pourquoi le site a-t-il
été implanté ici ? ». Cette réponse nécessitera de croiser les distances avec
les activités et les textes historiques, sans déduire une causalité de la seule
carte.
