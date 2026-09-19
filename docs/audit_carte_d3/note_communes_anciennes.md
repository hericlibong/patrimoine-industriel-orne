# Note — les communes qui ont changé de nom depuis les archives

**19 septembre 2026. Note de travail, pour recherche.** Aucune correction n'est
appliquée ; rien n'est décidé ici.

## Le problème, en une phrase

Les lieux portent le nom de commune inscrit dans leur notice d'archive ; les
contours de communes dont dispose le projet décrivent les communes
d'aujourd'hui. Quand une commune a fusionné depuis, les deux ne se rencontrent
plus, et le sol de la carte reste troué.

## Où cela se voit

Le contrôle `sol_complet`, ajouté le 19 septembre, fait échouer la génération
lorsqu'une commune portant un lieu n'a pas de contour. Il a arrêté la sonde sur
Noireau et Argentan. Il fonctionne comme prévu : rien ne passe en silence.

**Trois noms de communes, neuf lieux concernés.** Ces trois noms n'existent plus
dans les communes actuelles de l'Orne — 381 au total dans les données du projet.

## Ce que disent les coordonnées

Plutôt que de rapprocher des noms, les coordonnées de chaque lieu ont été
testées contre les contours actuels, pour savoir dans quelle commune
d'aujourd'hui chaque lieu tombe réellement.

| Nom d'archive | Lieux | Tombe dans la commune actuelle |
| --- | --- | --- |
| Athis-de-l'Orne | 5 | Athis-Val de Rouvre (61007) |
| Athis-de-l'Orne | 1 | **Saint-Pierre-du-Regard (61447)** — voir anomalie |
| Frênes | 2 | Tinchebray-Bocage (61486) |
| Goulet | 1 | Monts-sur-Orne (61194) |

Les trois correspondances principales sont cohérentes avec des communes
nouvelles : Athis-Val de Rouvre, Tinchebray-Bocage et Monts-sur-Orne portent
toutes un nom de regroupement.

## L'anomalie à examiner en premier

Un lieu sur les six rattachés à Athis-de-l'Orne — la filature `IA00061120` —
tombe dans **Saint-Pierre-du-Regard**, qui est une autre commune et non un
regroupement d'Athis. Deux explications possibles, qui demandent des réponses
différentes :

- la localisation du lieu est imprécise et le point tombe de l'autre côté d'une
  limite communale ; il faut alors regarder la précision déclarée de ce lieu ;
- le lieu est réellement sur le territoire de Saint-Pierre-du-Regard, et c'est
  la notice d'archive qui le rattache à Athis-de-l'Orne.

**Dans les deux cas, ce n'est pas au code de trancher.** C'est un point de
données, à instruire comme les autres arbitrages du corpus.

## Ce qu'il faudrait pour lever le blocage

Une table qui relie chaque nom de commune d'archive à la commune actuelle qui
la contient, avec pour chaque ligne : le nom d'archive, le code INSEE actuel,
la date de la fusion et la source qui l'atteste.

**Deux sources officielles à interroger** — aucune n'a été consultée pour cette
note :

- le Code officiel géographique de l'INSEE, qui publie l'historique des communes
  et leurs fusions, avec les dates ;
- l'API Géo, déjà utilisée par le projet, qui connaît les communes déléguées et
  leurs communes de rattachement.

La question à poser est simple : **Athis-de-l'Orne, Frênes et Goulet ont-elles
fusionné, quand, et dans quelle commune ?** Le rapprochement par les coordonnées
ci-dessus donne une réponse probable, mais une coordonnée n'est pas une preuve
administrative.

## Ce que cela bloque, et ce que cela ne bloque pas

**Bloqué :** l'ouverture des ensembles Noireau et Argentan dans la carte, tant
que le sol reste troué.

**Non bloqué :** tout le reste. La Risle et Crulai ne sont pas concernées ;
aucune des deux ne porte un nom de commune disparu. Les chiffres du corpus, les
lieux, les relations et les notices ne sont pas en cause — c'est uniquement
l'appariement avec les contours actuels qui manque.

## Ce qu'il ne faut pas faire

Rapprocher automatiquement les noms par ressemblance. « Goulet » ressemble à
« La Lande-de-Goult », qui est une commune réelle de l'Orne et n'a **aucun**
rapport. Un rapprochement par ressemblance de nom aurait produit une erreur
silencieuse.
