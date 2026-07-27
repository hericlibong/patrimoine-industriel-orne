# Phase 10 — bloc 7 : refondation avant le MVP

Statut : **bloc 7 lancé le 27 juillet 2026**.

## 1. Point de départ

Le prototype 0.1 n'est pas retenu comme base d'interface à enrichir. Il sert
désormais de contre-exemple concret permettant de comprendre ce qui éloigne le
projet d'une publication de datajournalisme.

Le diagnostic du porteur du projet est explicite :

- la direction artistique n'est pas bonne et devient illisible sur grand
  écran ;
- le récit cartographique ne permet pas de comprendre ce qui est démontré ni
  ce qui change pendant le défilement ;
- l'exploration cartographique ne fonctionne pas comme une véritable
  exploration ;
- les points se recouvrent et la réaction des filtres n'est pas intelligible ;
- les panneaux de sites sont grossiers ;
- les pages `Les lieux` ne font pas comprendre leur fonction narrative ;
- la typographie, les volumes et les espacements sont démesurés ;
- l'ensemble ressemble à un site web ou à un catalogue découpé en rubriques,
  pas à une publication datajournalistique originale.

Cette appréciation sévère est retenue comme donnée de travail. Le bloc 7 ne
doit ni la minimiser ni chercher à sauver artificiellement le prototype.

## 2. Constats vérifiés sur le prototype

Un contrôle complémentaire a été effectué dans un navigateur sur une fenêtre
de 1440 × 900 pixels.

### Accueil et structure générale

- Le titre principal atteint environ 104 px et occupe près de 330 px de
  hauteur. Il domine le sujet au lieu d'en organiser l'entrée.
- Le héros dépasse la hauteur de la fenêtre et accumule titre, introduction,
  deux boutons et chiffres avant d'avoir produit une première information.
- La navigation permanente `Le récit / Explorer / Les lieux / Méthode`
  installe immédiatement la logique d'un site à rubriques.
- Les mêmes traitements — très grands titres, cartes arrondies, aplats et
  boutons — sont répétés sans fonction journalistique spécifique.

### Récit

- L'introduction du récit utilise encore un titre de 72 px avant la première
  preuve.
- La carte fixe contient simultanément 318 marqueurs, les cours d'eau, les
  communes, les forêts, le rail et les noms de villes.
- Une étape consiste principalement à atténuer ou accentuer certains points.
  Sur cette densité, le changement est difficile à percevoir et encore plus
  difficile à interpréter.
- L'étape sur l'eau, par exemple, met en évidence 213 points et en atténue 105 :
  le résultat reste visuellement proche de la carte précédente.
- Le texte énonce des chiffres mais la visualisation ne construit pas une
  démonstration. Il n'existe ni comparaison claire, ni échelle, ni annotation,
  ni progression spatiale suffisamment explicite.
- Deux grands blocs de texte peuvent apparaître partiellement en même temps,
  tandis que la relation précise entre le bloc actif et l'état de la carte
  reste fragile.
- Le récit est donc un défilement de cartes presque semblables, pas encore un
  data storytelling.

### Exploration

- La page commence par un titre de 72 px et une large zone introductive : la
  carte, qui devrait être l'outil principal, arrive tard dans l'écran.
- Les 318 sites sont matérialisés par 318 boutons superposés sur un SVG fixe.
- Il n'existe ni zoom, ni déplacement, ni adaptation du niveau de détail.
- Les concentrations de points se recouvrent, notamment autour des principaux
  pôles et le long de certains axes.
- Après un filtre, le changement principal consiste à masquer des points. La
  carte ne recadre pas les résultats, n'explique pas les absences et ne
  hiérarchise pas les lieux restants.
- L'état des filtres n'est pas inscrit dans l'adresse et ne peut pas être
  partagé.
- Le panneau vide occupe en permanence une grande colonne et reproduit la
  logique d'une application de gestion.
- L'ensemble demande au lecteur de comprendre simultanément la carte, cinq
  contrôles, quatre couches, deux symboles, un compteur, une liste et un
  panneau.

### `Les lieux`

- Le premier écran juxtapose un titre de 72 px, une question générique et une
  très grande photographie, sans produire encore de lecture visuelle.
- Le nom documentaire complet est ajouté sous le titre éditorial mais ne
  clarifie pas la fonction du lieu dans le récit.
- La suite est découpée en quatre grandes cartes numérotées.
- `Lire le paysage` reste un paragraphe accompagné de pastilles `eau`,
  `bâtiments`, `voies`, `bourg` ; aucun élément de l'image n'est réellement
  annoté ou démontré.
- La chronologie aligne les phases dans un composant générique sans rendre
  sensibles les durées, les ruptures, les incertitudes ou les transformations
  matérielles.
- Les modules pourraient être appliqués à presque n'importe quel lieu. Ils ne
  répondent donc pas encore à une question journalistique propre au cas.

### Direction artistique

- La combinaison grand titre sérif, vert sombre, corail, cartes arrondies et
  grandes respirations fonctionne comme une identité de site institutionnel ou
  éditorial générique.
- Les dimensions choisies dans les maquettes ne résistent pas au passage sur
  un écran réel.
- La hiérarchie repose trop sur la taille et le vide, trop peu sur
  l'articulation entre données, documents, annotations et texte.
- Le système visuel prend davantage de place que l'information qu'il devrait
  servir.

## 3. Ce qui n'est pas repris comme base

Les éléments suivants ne doivent pas être prolongés automatiquement :

- la direction artistique actuelle ;
- le héros d'accueil et ses dimensions ;
- la navigation conçue comme quatre rubriques équivalentes ;
- le storyboard actuel en six étapes ;
- la carte SVG fixe et son système de marqueurs ;
- la barre actuelle de filtres ;
- le panneau latéral et ses cartes génériques ;
- le gabarit actuel de `Les lieux` ;
- le système de composants visuels du prototype.

Ils pourront éventuellement fournir un détail isolé après réexamen, mais ne
constituent plus une architecture de référence.

## 4. Ce qui reste acquis

La refondation ne remet pas en cause :

- le corpus de 318 sites et 403 phases ;
- les sources et les identifiants canoniques ;
- les classifications validées ;
- la distinction entre activité, période, précision et situation actuelle ;
- l'interdiction d'inventer une information absente ;
- les textes historiques et descriptions sources conservés sans réécriture ;
- les médias inventoriés et leur provenance ;
- le sujet : rendre visible le patrimoine industriel oublié de l'Orne ;
- l'ambition d'une publication statique, cartographique et
  datajournalistique, sans serveur pour le MVP.

L'idée d'une lecture guidée complétée par une exploration libre reste une
hypothèse produit. Sa matérialisation doit être entièrement réexaminée.

## 5. Nouvelle méthode du bloc 7

### Étape 7.1 — Reformuler la démonstration

Avant tout écran, il faut définir :

- la question journalistique centrale ;
- les deux ou trois conclusions réellement soutenues par les données ;
- les preuves nécessaires à chaque conclusion ;
- ce que la carte apporte que le texte ou un graphique n'apporte pas ;
- la fonction exacte d'un cas individuel dans la démonstration.

Le storyboard précédent n'est pas présumé correct.

### Étape 7.2 — Choisir une forme éditoriale principale

Le projet doit cesser d'hésiter entre site à rubriques, application
cartographique et article long.

Une forme principale devra être choisie, par exemple une publication longue
interactive où :

- la narration constitue la colonne vertébrale ;
- la carte intervient seulement lorsqu'elle démontre quelque chose ;
- l'exploration est un prolongement clairement identifié ;
- les lieux sont insérés comme études de cas, et non comme une rubrique de
  catalogue.

Cette hypothèse devra être confrontée à d'autres formes possibles avant
validation.

### Étape 7.3 — Rechercher une direction visuelle sur du contenu réel

La nouvelle recherche ne partira pas d'un système graphique abstrait. Elle
utilisera :

- une vraie question ;
- un vrai extrait de données ;
- une vraie carte ;
- une vraie photographie ;
- un vrai cas ;
- une fenêtre de 1440 px comme format de contrôle principal.

Les propositions seront jugées dans le navigateur à leur taille réelle, puis
sur ordinateur portable et mobile. Une vignette ou une planche réduite ne
suffira plus à valider une direction.

### Étape 7.4 — Produire une seule tranche verticale

Avant de reconstruire l'ensemble, une tranche limitée devra relier :

1. une entrée éditoriale courte ;
2. une preuve par les données ;
3. une séquence cartographique intelligible ;
4. un lieu traité comme étude de cas ;
5. une ouverture vers l'exploration.

Elle utilisera des contenus réels et une interaction réelle. Si cette tranche
n'est pas comprise sans explication extérieure, elle sera reprise avant toute
extension.

### Étape 7.5 — Construire le MVP seulement après validation

Une fois la tranche validée :

- définir les exports web strictement nécessaires ;
- choisir le moteur cartographique ;
- construire l'interface statique ;
- intégrer progressivement le corpus ;
- ajouter seulement les tests protégeant les règles critiques.

## 6. Principe d'arrêt

Le projet ira jusqu'au terme du bloc 7 puis s'arrêtera pour une nouvelle
évaluation générale.

Le bloc 8 — qualité, accessibilité et performances — ne sera pas lancé tant que
le MVP du bloc 7 ne sera pas jugé suffisamment cohérent, compréhensible et
publiable pour mériter cette phase de contrôle.
