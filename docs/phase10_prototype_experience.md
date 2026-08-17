# Phase 10 — prototype de l'expérience

Statut : **bloc 6 terminé le 27 juillet 2026 — prototype 0.1 validé uniquement
comme point de départ, avec réserves importantes**.

La revue conclut que la version 0.1 contient encore trop d'incohérences,
d'abstractions artificielles et de séquences difficiles à comprendre ou
inopérantes. Ces difficultés concernent les trois niveaux de l'expérience :
récit, exploration et `Les lieux`. La direction artistique devra également
être réexaminée.

La validation porte donc sur l'existence d'un prototype concret permettant de
discuter et de poursuivre le travail. Elle ne vaut pas validation éditoriale,
fonctionnelle ou graphique de sa forme actuelle.

## 1. Objet

Le prototype transforme les décisions des blocs 1 à 5 en une expérience
navigable. Il sert à juger le rythme, la hiérarchie et les passages entre
data storytelling, exploration et récits de lieux. Ce n'est pas encore le MVP
technique du bloc 7.

Il conserve l'intention validée :

- publication documentaire et datajournalistique ;
- patrimoine industriel oublié comme sujet central ;
- données et preuves visuelles avant l'accumulation de texte ;
- lecture guidée et exploration libre complémentaires ;
- carte de l'Orne géographiquement identifiable ;
- absence d'inférence sur la situation actuelle ou la précision des sites.

## 2. Écrans matérialisés

### Accueil

L'accueil associe immédiatement un paysage actuel de l'Orne au titre
`Patrimoine industriel oublié`. Il donne deux entrées de même niveau :
commencer le récit ou explorer la carte. Trois chiffres installent l'échelle du
corpus sans former un tableau de bord.

### Récit guidé

Le récit adopte un data scrollytelling mesuré : le texte défile tandis qu'une
carte réelle de l'Orne reste visible. Elle ne change que lorsqu'une preuve
nouvelle apparaît :

1. corpus complet ;
2. implantation du textile ;
3. proximité des cours d'eau ;
4. 73 sites à plusieurs phases ;
5. quatre situations actuelles documentées ;
6. passage vers l'exploration libre.

Une alternative textuelle résume la progression.

### Exploration

La carte affiche les 318 sites sans agrégation dans cette version. Elle
conserve les cours d'eau, forêts, communes, voies ferrées actuelles et repères
urbains. Les quatre couches de contexte peuvent être masquées.

Les filtres publics sont :

- activité ;
- période d'activité ;
- situation actuelle documentée ou non documentée ;
- précision géographique.

Activité et période doivent être vraies sur une même phase. La recherche porte
sur le nom, la commune, le lieu-dit, l'adresse, la référence et les activités.
Le compteur, l'état sans résultat et la remise à zéro sont explicites.

La liste accessible contient exactement les mêmes résultats que la carte. Un
seul panneau latéral présente le site sélectionné sans perdre les filtres.

### Panneau de site

Le panneau distingue :

- l'identité du lieu ;
- les activités et leurs dates sources ;
- la situation actuelle, ou son absence de documentation récente ;
- la précision géographique ;
- le lien vers la source ;
- un accès au récit long lorsqu'un lieu a été sélectionné éditorialement.

### `Les lieux`

Trois cas matérialisent le gabarit :

- Moulin d'Ozé — Moulinex : activités successives ;
- usine Abadie : lecture conjointe de la rivière, du bourg, des voies et des
  bâtiments ;
- établissements Bohin : continuité industrielle et situation actuelle
  documentée.

Chaque récit combine une image, une question journalistique, une lecture du
paysage, une chronologie, un état actuel séparé et les éléments de provenance.
La photographie est donc une preuve à interroger, pas une vignette de
catalogue.

### Méthode

La page méthode rend visibles le périmètre, la construction du corpus, les
classifications, la chronologie, la précision cartographique, les situations
actuelles, les médias, les sources et les limites.

## 3. Contrôles internes effectués

Contrôles réalisés dans un navigateur sur la version 0.1 :

- chargement de 318 marqueurs et de 403 phases ;
- progression effective des six états du récit ;
- résultat de 73 sites sur l'état multi-activités ;
- résultat de quatre sites pour la situation actuelle documentée ;
- filtrage activité–période sur une même phase ;
- recherche et état sans résultat ;
- activation et désactivation des couches géographiques ;
- cohérence carte–liste–panneau ;
- accès au récit d'un lieu puis retour à l'exploration ;
- fermeture du panneau avec `Échap` et restitution du focus ;
- absence de débordement horizontal au format mobile contrôlé.

Ces contrôles vérifient le fonctionnement. Ils ne remplacent pas la revue
éditoriale et la validation de compréhension par le porteur du projet.

## 4. Arbitrages et reprises nécessaires

Le travail suivant devra notamment répondre à ces questions :

1. L'accueil donne-t-il immédiatement la bonne idée du sujet ?
2. Les six étapes du récit sont-elles assez démonstratives et assez courtes ?
3. Les transformations de la carte sont-elles perceptibles sans explication ?
4. La carte statique du prototype suffit-elle à valider la composition avant
   l'ajout du zoom et du déplacement dans le MVP ?
5. Le panneau synthétique donne-t-il assez d'informations avant le récit long ?
6. Le rôle de l'image dans `Les lieux` est-il désormais concret ?
7. Les états documentés, inconnus et géographiquement imprécis sont-ils
   suffisamment distincts ?

## 5. Limites et suite

Le prototype n'ajoute ni framework ni moteur cartographique. Ce choix évite de
figer trop tôt la pile et limite le code à ce qui est nécessaire pour tester
l'expérience.

Le bloc 7 ne devra pas transformer automatiquement cette version en MVP. Il
commencera par recenser les problèmes concrets, puis par décider ce qui doit
être conservé, repris ou supprimé. Les corrections resteront ciblées afin
d'éviter une refonte abstraite ou une nouvelle accumulation de composants.

Ce travail permettra ensuite de construire un MVP reproductible sans figer les
incohérences du prototype 0.1.
