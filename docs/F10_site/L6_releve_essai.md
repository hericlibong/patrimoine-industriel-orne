# L6 — Relevé d'essai du mode lieu

**20 septembre 2026.** Éprouvé sur les cinquante lieux des deux ensembles
ouverts, avec un examen détaillé sur six d'entre eux. Mesuré dans un navigateur,
page réellement affichée, images chargées.

---

## Ce qui a été éprouvé, et comment

La feuille de route prévoyait cinq lieux couvrant les cas difficiles. Ces cas
n'existent presque pas dans les deux ensembles ouverts : aucun lieu sans
historique, aucun lieu sans événement daté, un seul sans image, un seul à trois
activités. L'essai a donc deux parties, selon la décision du porteur du
20 septembre : **six lieux réels** qui forment les extrêmes de ce que nous
publions, puis un **contrôle de robustesse** sur les cas absents, simulés en
mémoire dans le navigateur, sans toucher à aucune donnée.

Deux largeurs d'écran : **1440 pixels**, la largeur de jugement du projet, où le
panneau mesure 360 pixels de large ; et **390 pixels**, un téléphone courant, où
il en mesure 335 et passe sous la carte.

---

## Les six lieux, un par un

| Lieu | Cas | Hauteur au repos | Une fois déplié |
| --- | --- | --- | --- |
| Tréfilerie Boisthorel, Rai | La notice la plus longue, 1 348 caractères | 829 | 1 252 |
| Usine de chaussures, L'Aigle | La notice la plus courte, 143 caractères | 811 | — |
| Usine d'ébénisterie, L'Aigle | Le seul lieu sans image | 490 | 591 |
| Moulin à farine et passementerie, Aube | Trois activités | 813 | 873 |
| Moulin à foulon, Vitrai-sous-Laigle | La plus longue de Crulai | 865 | 1 006 |
| Moulin à farine, Chandai | La plus courte de Crulai | 787 | — |

Hauteurs en pixels, à 1440. Un tiret signifie que la notice tient entière et
n'a pas de « Voir plus ».

**Ce que ces chiffres disent.** Le panneau ne varie pas beaucoup d'un lieu à
l'autre — de 787 à 865 pixels dès qu'il y a une image. La longueur de la notice
ne joue presque pas, puisque seule l'amorce est visible : la notice la plus
longue donne un panneau de 829 pixels, la plus courte 811. Ce qui fait la
différence, c'est l'image. Le seul lieu qui n'en a pas tombe à 490 pixels, soit
340 de moins : l'image occupe à elle seule 40 % de la hauteur du panneau.

**Ce qui tient.** Les quatre blocs sont au rendez-vous partout — identité,
historique, chronologie, sorties. Aucun panneau vide, aucun bloc incohérent.
Depuis chaque lieu, le retour à l'ensemble et la liste des autres lieux sont
présents. Le « Voir plus » fait l'aller et le retour, et le second clic ramène
exactement à la hauteur de départ sur les quatre lieux concernés.

**Sur écran étroit.** Aucun débordement horizontal sur les six lieux : rien ne
dépasse, la page ne se décale pas latéralement. Les hauteurs sont proches de
celles du grand écran parce que le panneau n'est que de 25 pixels plus étroit.
La seule différence notable est la notice la plus longue de la Risle, qui passe
de 1 252 à 1 292 pixels une fois dépliée.

---

## Contrôle de robustesse : les cas qui n'existent pas encore

Sur l'abattoir de L'Aigle, en retirant une information à la fois **en mémoire
dans le navigateur**. Aucune donnée n'a été modifiée : un rechargement de la
page rétablit tout, et les fichiers du corpus n'ont pas été ouverts.

| Ce qui manque | Ce que fait le panneau | Hauteur |
| --- | --- | --- |
| Tout l'historique | Le bloc reste, et dit « Aucun texte historique dans la source » | 472 |
| Tous les événements datés | Le bloc chronologie disparaît, sans laisser de trou | 448 |
| Toutes les activités | « Activité non précisée par la source » | 768 |
| Le lien vers la fiche d'inventaire | La ligne disparaît | 741 |
| L'image, dont l'adresse ne répond pas | La figure se retire d'elle-même ; aucun cadre vide, aucune icône cassée | 513 puis 470 |
| **Tout à la fois** | Nom, commune, les deux mentions de manque, le retour et les 43 autres lieux | 336 |

**Le dernier cas est le plus important.** Un lieu dont on ne saurait rien
produit encore un panneau qui se tient : il donne son nom, sa commune, dit
honnêtement ce qu'il ignore, et laisse repartir. Aucun code technique n'apparaît
à l'écran dans aucun des six essais, et aucune mention parasite du genre
« undefined ».

---

## Les cinquante panneaux mesurés

Au-delà des six lieux, les cinquante ont été mesurés à 1440 pixels.

- **Le plus haut au repos : 885 pixels**, la tréfilerie de Sainte-Colombe à
  Échauffour.
- **Le plus bas : 490**, l'usine d'ébénisterie de L'Aigle, la seule sans image.
- **Hauteur médiane : 789.**
- **Aucun des cinquante ne dépasse 900 pixels au repos.** Le critère du panneau
  court de L2 est tenu sur l'ensemble des lieux publiables, et pas seulement sur
  les six examinés.
- Une fois l'historique déplié, trente panneaux sur quarante-cinq dépassent 900,
  jusqu'à 1 252. C'est attendu et voulu : le lecteur a demandé à voir la suite,
  et « Voir moins » le ramène en arrière.

---

## Parcours et accès au clavier

Le circuit complet a été parcouru : département, entrée dans la Risle, ouverture
d'un lieu, passage à un autre lieu par la liste, retour à l'ensemble, retour au
département, puis entrée dans un autre ensemble. **Aucun panneau vide et aucun
cul-de-sac** à aucune étape.

Le filtre métier survit à l'aller-retour : filtré sur la métallurgie, l'ensemble
montre 24 lieux, le sélecteur est masqué pendant qu'on lit un lieu, et le retour
à l'ensemble retrouve les mêmes 24 lieux.

Sur le panneau du lieu le plus chargé, les 29 éléments cliquables sont tous
atteignables au clavier ; aucun n'est retiré de la tabulation.

---

## Ce qui n'a pas pu être fait

**Les captures d'écran.** L'environnement de travail de l'assistant ne peut pas
photographier cette page : l'onglet piloté ne produit aucune image. Le relevé
ci-dessus repose donc sur des mesures et sur la lecture du contenu réellement
affiché, pas sur des vues. L'examen visuel reste à faire par le porteur, dans
son propre navigateur — c'est précisément ce que L7 prévoit en premier point.

Ce manque n'est pas seulement technique : il vaut aussi règle. Une capture du
panneau d'un lieu incorpore la photographie de l'inventaire, et le dépôt exclut
depuis le 17 août 2026 les rendus qui incorporent des images de tiers. Des
captures ne seraient de toute façon pas versionnées.

---

## Défauts relevés

1. **Une erreur de mesure de ma part, corrigée ici.** Les hauteurs de panneau
   annoncées plus tôt dans la journée — 618, 772 pixels — étaient mesurées sur
   la colonne de la carte et non sur le panneau. Les vraies valeurs sont celles
   de ce relevé : médiane 789, maximum 885. La conclusion ne change pas, le
   critère des 900 reste tenu, mais la marge est plus faible qu'annoncée.

2. **Le bloc historique s'affiche même quand il est vide.** Il dit alors
   « Aucun texte historique dans la source ». C'est honnête, mais cela donne un
   titre sans contenu. Aucun lieu publiable n'est dans ce cas aujourd'hui ; la
   question se posera à l'ouverture d'autres ensembles.

3. **La marge sous 900 pixels est étroite.** Le panneau le plus haut est à 885.
   Monter la borne de hauteur de l'image, comme le porteur l'envisage, ferait
   passer une partie des lieux au-dessus du critère. Les deux décisions sont
   liées et se prennent ensemble.

---

## Critères de réception

| Critère | Résultat |
| --- | --- |
| Aucun lieu ne produit un panneau vide | Tenu, y compris quand toute information manque |
| Aucun bloc incohérent | Tenu ; aucun code technique ni mention parasite affichés |
| Aucun cul-de-sac de navigation | Tenu sur le circuit complet |
| Panneau court, sous 900 pixels au repos | Tenu sur les cinquante lieux, maximum 885 |
| Pas de débordement horizontal sur écran étroit | Tenu sur les six lieux, à 390 pixels |

**L6 est éprouvé. L'examen visuel du porteur reste à faire — c'est le premier
point de L7.**
