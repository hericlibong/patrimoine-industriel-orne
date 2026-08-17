# Phase 10 — Carte exploratoire et filtres

**Version :** 1.0 — architecture fonctionnelle validée
**Statut :** validée comme point de départ évolutif
**Date :** 27 juillet 2026

## Rôle de la carte

La carte exploratoire est l'espace principal d'interrogation du corpus. Elle
doit permettre de passer d'une vue départementale aux informations d'un site
sans transformer la publication en catalogue ou en logiciel SIG.

Elle répond à six questions :

1. où se trouvent les 318 sites documentés ?
2. quelles activités et quels secteurs sont documentés dans un territoire ?
3. quelles phases d'activité disposent d'un repère chronologique exploitable ?
4. quels lieux ont connu plusieurs activités ?
5. que sait-on réellement de leur situation actuelle ?
6. avec quelle précision chaque localisation est-elle connue ?

Elle ne prétend pas démontrer qu'un site existe à cause d'une rivière, d'une
forêt, d'une voie ferrée ou d'une ressource proche. Ces éléments forment un
contexte géographique ; une relation historique n'est affirmée que dans le
récit ou une page `Les lieux` lorsqu'elle est sourcée.

## Données qui déterminent l'interface

| Dimension | Couverture réelle | Conséquence |
| --- | ---: | --- |
| Sites localisés | 318 | tous peuvent être affichés dès la vue initiale |
| Phases d'activité | 403 | le filtrage porte sur les phases, pas sur un secteur principal du site |
| Secteurs utilisés | 9 | ils forment le premier niveau du filtre d'activité |
| Sites multi-activités | 73 | la fiche et les résultats doivent accepter plusieurs activités |
| Phases avec période structurée | 42 phases concernant 29 sites | le filtre temporel doit annoncer sa couverture limitée |
| Situation récente documentée | 4 sites | l'inconnu constitue un résultat, pas une donnée à masquer |
| Point approximatif | 290 sites | symbole prudent et libellé constant |
| Zone documentaire | 28 sites | symbole distinct ; aucun faux contour de site |

Le GeoJSON actuel représente les 318 localisations par des points. Pour les 28
`zone_documentaire`, le point est un repère de consultation et non le contour
de la zone. L'interface ne dessinera donc pas une emprise fictive.

## Vue initiale

À l'ouverture de `/explorer` :

- la carte est cadrée sur l'ensemble de l'Orne ;
- les 318 sites sont visibles ;
- aucun filtre n'est actif ;
- la recherche est vide ;
- le nombre `318 sites affichés` est visible ;
- la liste est disponible mais repliée ;
- aucun panneau de site n'est ouvert ;
- les cours d'eau, les forêts et le rail actuel sont visibles avec une
  hiérarchie discrète ;
- les limites communales et les principaux bourgs servent au repérage ;
- la légende distingue immédiatement point approximatif et zone documentaire.

Les sites utilisent une couleur commune. La couleur ne représente pas un
secteur permanent, car 34 sites appartiennent à plusieurs secteurs. Lorsqu'un
secteur est filtré, les sites correspondants sont mis en évidence sans recevoir
une nouvelle identité permanente.

Les 318 points sont suffisamment peu nombreux pour éviter un regroupement en
agrégats chiffrés à l'échelle départementale. Les agrégats masqueraient la
distribution que la carte doit précisément montrer.

## Niveaux de lecture

### 1. Département

- distribution complète des sites ;
- principaux bourgs, rivières, massifs forestiers et axes ferroviaires ;
- aucun nom de site affiché en permanence ;
- sélection possible sans zoom obligatoire.

### 2. Secteur géographique

- davantage de communes et de cours d'eau deviennent lisibles ;
- le survol ou le focus affiche nom, commune et nombre d'activités ;
- la liste se limite automatiquement à l'emprise visible seulement si le
  lecteur active `Limiter à la zone visible`.

La carte ne modifie pas silencieusement les résultats pendant un déplacement.
Par défaut, les filtres décrivent tout le corpus, indépendamment de l'emprise
visible.

### 3. Environnement local

- contexte du bourg, de l'eau, des forêts, du rail et des voies principales ;
- symbole de localisation toujours accompagné de son niveau de précision ;
- aucune surimpression automatique sur un bâtiment ou une parcelle.

Une sélection automatique ne zoome jamais jusqu'à laisser croire qu'un
bâtiment a été vérifié. Le lecteur peut zoomer manuellement, mais le libellé
`Point approximatif` ou `Zone documentaire` reste visible dans le panneau.

## Sélection et aperçu d'un site

### Aperçu court

Au survol avec une souris, ou au focus équivalent depuis la liste :

- nom du site ;
- commune ;
- activités principales sous forme textuelle ;
- repère de précision.

Aucune information essentielle ne dépend du survol.

### Panneau de sélection

Un clic ou l'activation d'un résultat ouvre un panneau unique, sans quitter la
carte :

1. image retenue après revue humaine, si elle existe ;
2. nom et commune ;
3. phrase journalistique courte ;
4. activités successives et dates disponibles ;
5. situation actuelle, en séparant conservation, usages et accessibilité ;
6. précision géographique ;
7. source principale et accès aux autres sources ;
8. lien `Ouvrir ce lieu` lorsqu'une page éditoriale existe.

Sur ordinateur, le panneau apparaît à droite. Sur mobile, il prend la forme
d'un volet inférieur. Il peut être fermé avec un bouton explicite et avec
`Échap` au clavier.

La sélection est enregistrée dans l'URL :

```text
/explorer?site={site_id}
```

L'ouverture d'une page `Les lieux` puis le retour à la carte restaurent le site,
les filtres et le cadrage précédents.

## Carte et liste synchronisées

La carte et la liste sont deux représentations du même résultat.

- `Afficher la liste` ouvre un panneau unique qui remplace temporairement le
  détail du site ; il ne crée pas une troisième colonne.
- Une sélection dans la liste centre la carte et remplace la liste par le
  détail, avec un bouton `Retour aux résultats`.
- La fermeture du détail rend la carte entière sans perdre les filtres.
- La liste indique nom, commune, activités documentées, précision et présence
  éventuelle d'une situation récente.
- Sans recherche textuelle, le tri est alphabétique par commune puis par nom.
- Avec une recherche, les correspondances exactes précèdent les
  correspondances partielles.

La liste constitue aussi l'alternative accessible à la navigation entre les
318 marqueurs.

## Recherche

La recherche porte sur :

- nom du site ;
- commune ;
- lieu-dit ;
- adresse source ;
- activité détaillée ;
- référence IA, pour un usage de vérification.

La recherche ignore les différences de casse et d'accent mais n'effectue pas
de correction approximative agressive. Les suggestions sont regroupées sous
trois intitulés : `Lieux`, `Communes` et `Activités`.

Choisir une commune recadre la carte et ajoute un critère visible. Choisir un
site ouvre directement son panneau. Choisir une activité ajoute le filtre
correspondant.

## Filtres publics du MVP

La barre conserve quatre entrées :

### 1. Activité

Premier niveau : les neuf secteurs réellement présents dans le corpus.

Second niveau facultatif : les activités détaillées du secteur sélectionné,
par exemple `Mouture de céréales`, `Filature textile` ou `Fabrication de
papier`.

Il n'existe pas de secteur principal permanent. Un site multi-secteurs apparaît
dans chacun des secteurs documentés par ses phases.

### 2. Période d'activité

Le filtre utilise uniquement `activites.periodes_codes`, c'est-à-dire les
périodes calculées depuis les bornes documentées d'une phase. Il ne transforme
pas les siècles de construction ou de transformation du site en durée
d'activité.

Le menu indique :

> 42 phases concernant 29 sites sont suffisamment datées pour ce filtre.

Les sept périodes historiques restent disponibles. Les sites sans phase datée
sont exclus lorsqu'une période est sélectionnée, mais restent visibles lorsque
le filtre est vide.

### 3. Situation actuelle

Le premier choix distingue :

- `Documentée par une source récente` — 4 sites ;
- `Non documentée récemment` — 314 sites.

Le menu peut ensuite préciser séparément :

- conservation matérielle ;
- usage actuel ;
- accessibilité.

Ces trois dimensions ne sont jamais fusionnées en un statut unique. Les
effectifs sont calculés par site ; plusieurs usages d'un même site ne
produisent pas de double comptage.

### 4. Précision

Deux choix correspondent au corpus actuel :

- `Point approximatif` — 290 sites ;
- `Zone documentaire` — 28 sites.

Les symboles du filtre sont identiques à ceux de la carte et de la légende.

### Ce qui n'est pas un filtre initial

- commune : traitée par la recherche ;
- eau, forêt et rail : couches de contexte ;
- distances aux éléments territoriaux : réservées aux séquences qui expliquent
  leurs limites ;
- protection patrimoniale : information de fiche, sans élargir la barre
  initiale ;
- CASIAS : recoupement documentaire, pas statut public du site.

## Règles de combinaison

- plusieurs valeurs dans un même filtre sont combinées par `OU` ;
- des filtres différents sont combinés par `ET` ;
- la recherche textuelle est combinée par `ET` avec les filtres ;
- le résultat est toujours dédupliqué par `site_id` ;
- chaque critère actif devient une étiquette supprimable ;
- `Tout effacer` reste visible dès qu'un critère est actif ;
- le nombre de sites est recalculé après chaque modification ;
- les paramètres sont conservés dans l'URL partageable.

### Règle critique activité × période

Une activité et une période doivent correspondre à la même ligne de phase :

```text
un site correspond
si au moins une phase du site possède
une activité sélectionnée ET une période sélectionnée
```

Il est interdit de sélectionner un site parce qu'une première phase correspond
à l'activité et qu'une autre phase, sans rapport, correspond à la période.

Avec plusieurs activités ou périodes, les choix sont d'abord combinés par `OU`
dans leur groupe, puis évalués ensemble sur une même phase.

## Résultat vide

La carte ne retire pas silencieusement un filtre. Elle affiche :

```text
Aucun site ne correspond à ces critères.
[Retirer le dernier critère] [Tout effacer]
```

La liste indique les critères responsables. La carte conserve le fond
géographique mais aucun marqueur de résultat. Elle ne réaffiche jamais les 318
sites en arrière-plan d'une manière pouvant être confondue avec le résultat.

## Couches géographiques

Les commandes de couches sont séparées des filtres :

- cours d'eau ;
- forêts actuelles ;
- rail actuel ;
- limites communales.

Le libellé `actuel` est visible pour les couches contemporaines. Leur activation
ne modifie ni le nombre de résultats ni les filtres. Une note rappelle :

> Les couches de contexte ne prouvent pas une relation historique.

Les couches historiques ne seront ajoutées que lorsqu'une source, une date et
une fonction éditoriale sont identifiées.

## Clavier et accessibilité

- la recherche, les filtres, la liste, le panneau et les commandes de couches
  sont utilisables au clavier ;
- `Entrée` ouvre un résultat ou applique un choix ;
- `Échap` ferme le menu ou le panneau actif ;
- le focus revient au contrôle qui a déclenché l'ouverture ;
- l'ouverture d'un panneau annonce son titre et le nouveau nombre de résultats ;
- la couleur n'est jamais le seul signal de sélection ou de précision ;
- aucun parcours n'oblige à tabuler à travers 318 marqueurs ;
- `Afficher la liste accessible` précède la carte dans l'ordre de navigation ;
- les informations de la carte sont disponibles dans la liste et le panneau ;
- zoom et déplacements animés respectent la préférence de réduction des
  mouvements.

## Mobile et tactile

- recherche visible en permanence ;
- bouton `Filtres` indiquant le nombre de critères actifs ;
- filtres ouverts dans un panneau plein écran avec boutons `Voir les résultats`
  et `Effacer` ;
- carte affichée avant la liste, sans bloquer le défilement de la page ;
- liste ou détail dans un volet inférieur ;
- cibles tactiles d'au moins 44 × 44 pixels ;
- aucun geste de glissement indispensable : fermer, développer et revenir
  possèdent toujours un bouton ;
- légende et couches accessibles dans un panneau compact.

## État conservé et partage

L'URL peut conserver :

```text
/explorer
  ?q=filature
  &activite=filature_textile
  &periode=industrialisation_rail_vapeur
  &situation=non_documentee
  &precision=point_approximatif
  &site={site_id}
```

Le zoom et le centre peuvent être conservés dans l'historique local de
navigation sans rendre l'URL principale illisible. Les identifiants des
critères utilisent les codes stables du registre, tandis que les libellés
publics viennent de `config/classifications.yml`.

## Périmètre technique minimal

Le MVP peut fonctionner avec :

- un index cartographique léger contenant les 318 sites ;
- un index des 403 phases pour le filtrage ;
- les libellés publics des classifications ;
- les couches géographiques simplifiées nécessaires à l'affichage ;
- des fichiers de détail chargés seulement à l'ouverture d'un site.

Aucun serveur, moteur de recherche distant, base embarquée dans le navigateur
ou gestionnaire d'état généraliste n'est nécessaire.

## Portée de la validation

L'architecture suivante est validée comme référence :

1. afficher les 318 points sans agrégats sur la vue départementale ;
2. conserver les couches de contexte visibles mais distinctes des filtres ;
3. limiter le filtre temporel aux 42 phases réellement datées ;
4. conserver `Situation actuelle` comme filtre malgré une couverture récente de
   quatre sites, afin de rendre la lacune explorable ;
5. utiliser un panneau unique alternant liste et détail ;
6. utiliser la liste comme alternative accessible plutôt que rendre les 318
   marqueurs successivement tabulables ;
7. conserver seulement quatre filtres initiaux.

Cette validation ne fige pas les réglages fins. Le prototype pourra faire
évoluer les seuils de zoom, la densité du fond, l'ordre ou le libellé des
contrôles, les dimensions du panneau et les comportements tactiles lorsqu'un
test d'usage, d'accessibilité ou de performance le justifie. Ces ajustements ne
remettent pas en cause l'architecture générale de l'exploration.
