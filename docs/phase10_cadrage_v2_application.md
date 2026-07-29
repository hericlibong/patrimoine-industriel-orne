# Phase 10 — Cadrage V2 : une application datajournalistique interactive

**Version :** 2.0
**Statut :** cadrage de référence, arrêté le 29 juillet 2026
**Remplace :** `docs/phase10_cadrage_editorial_ux.md`, version 0.7 du 27 juillet
2026, qui décrivait une publication en pages et excluait la forme applicative.
Ce document ne le corrige pas : il repart d'une autre définition du produit.

---

## 1. Ce que nous construisons

**Une application web interactive de datajournalisme sur le patrimoine
industriel oublié de l'Orne.**

Au centre, une carte de l'Orne. Autour, des commandes et des indicateurs. Le
lecteur choisit un métier, une époque, un territoire, et la carte comme les
chiffres répondent ensemble.

On ne lit pas des pages. On manipule des données pour comprendre.

L'application doit être créative et originale dans sa forme. Elle ne doit
ressembler ni à un site institutionnel, ni à un portail patrimonial, ni à un
outil de consultation de base de données.

## 2. Ce que ce n'est pas

Le projet a échoué une première fois parce qu'il avait été décliné en site web :
des rubriques, des pages, un défilement, des gabarits applicables à n'importe
quel lieu. Le résultat était un catalogue documentaire.

Ne sont donc pas des formes acceptables :

- une navigation en rubriques du type récit, explorer, les lieux, méthode ;
- une succession de chapitres qu'on fait défiler ;
- une fiche reproduite trois cent dix-huit fois ;
- un inventaire consultable.

## 3. Le sujet

Quand on parle de l'Orne, on pense à la campagne. Pendant des siècles, ce
département a pourtant fabriqué : forges, moulins, filatures, papeteries,
mines, usines d'épingles et d'aiguilles. Trois cent dix-huit de ces lieux sont
documentés. Presque personne ne le sait, et ils sont toujours là.

Ce que l'application doit faire comprendre :

> **Le paysage de l'Orne n'est pas un décor, c'est une trace.**

Les rivières faisaient tourner les machines. Les vallées étaient des chaînes
d'usines. L'application le montre en donnant les moyens de le vérifier
soi-même.

Le sujet est historique et culturel autant que géographique. Ce n'est pas un
relevé de territoire : ce sont des gens, des familles, des métiers, des
productions et des fins d'activité.

## 4. L'unité de publication : le système industriel

L'application ne s'organise ni autour du site individuel, ni autour du
département.

Elle s'organise autour d'une **douzaine d'ensembles industriels cohérents**.
Deux cent quarante-six des trois cent dix-huit sites appartiennent à un tel
ensemble. Ils prennent trois formes selon ce qui a fixé l'industrie là :

- **la vallée**, quand c'est l'eau — Risle, Noireau, Flers, La Ferté-Macé ;
- **le bassin de ressource**, quand c'est le sous-sol — Halouze,
  La Ferrière-aux-Étangs ;
- **le pôle urbain**, quand c'est la ville — Alençon, Argentan.

Les quarante-quatre sites isolés ne sont pas un manque : ce sont les lieux qui
n'appartenaient à aucun système, et c'est un fait éditorial.

Ce choix règle le problème structurel de la tentative précédente. Trois cent
dix-huit objets à présenter produisent un catalogue. Une douzaine de systèmes à
comprendre produisent une démonstration.

## 5. Comment le lecteur circule

**Le récit n'est pas linéaire.** Il n'y a ni chapitre premier, ni ordre imposé.
Le lecteur choisit son entrée, son exploration et ses vues.

Il manipule, et l'histoire vient à lui.

### Conséquence directe sur l'écriture

Dans un récit linéaire, on maîtrise l'ordre : chaque étape s'appuie sur la
précédente. Ici, non. On ne sait pas par où le lecteur arrive ni ce qu'il a
déjà vu.

Deux règles en découlent, et elles sont contraignantes :

1. **Chaque vue se suffit à elle-même.** Quelqu'un qui arrive directement sur
   une vallée doit comprendre ce qu'il regarde sans être passé par ailleurs.
   Aucune formule du type « comme on l'a vu plus haut ».
2. **La démonstration se construit par répétition depuis des angles
   différents**, non par accumulation d'étapes. Le lecteur qui explore les
   moulins, celui qui explore les forges et celui qui explore une vallée
   doivent tous finir par comprendre la même chose, chacun par son chemin.

### Amorces obligatoires

Une carte ouverte sans amorce est un outil, pas une publication. Le lecteur qui
n'a rien à quoi se raccrocher s'en va.

L'application doit donc proposer, dès l'arrivée, deux ou trois entrées
cliquables formulées comme des questions — du type « pourquoi ces usines
sont-elles toutes au bord de l'eau ? ». Elles déclenchent une première
manipulation à la place du lecteur et le laissent continuer seul.

Sans ces amorces, la forme non linéaire ne tient pas.

## 6. Où vit le récit : trois canaux

**1. La carte annote ce qu'elle montre.** Dès qu'une forme apparaît — un
alignement le long d'une rivière, une concentration autour d'une ville —
l'application l'écrit sur la carte, posée sur la forme elle-même. Pas un
paragraphe dans une colonne voisine.

**2. La sélection ouvre une histoire.** On clique sur un système ou un lieu, un
panneau raconte, on ferme, on revient à la carte.

**3. Les liens se dessinent.** Quand deux sites sont reliés par une source — le
haut fourneau qui alimentait la forge, l'usine rachetée par un industriel — un
trait apparaît entre eux, avec la phrase qui le prouve.

C'est là qu'est le journalisme : dans le choix de ce qu'on signale et dans ce
qu'on écrit dessus. Pas dans un article.

## 7. Les trois niveaux d'écriture

| Niveau | Longueur | Rôle | Origine du texte |
| --- | --- | --- | --- |
| Annotation | Une à trois lignes | Nommer ce que le lecteur a sous les yeux, au moment où il l'a sous les yeux | Écrite pour une situation précise |
| Ensemble | Cent cinquante à deux cent cinquante mots | Expliquer ce qu'un système industriel était et pourquoi il était là | Écrite par nous, à partir de la lecture des notices |
| Lieu | Environ cent mots | Raconter un site : noms, dates, productions, effectifs, fin d'activité | Tirée directement de la notice, sans invention |

L'annotation n'existe que dans son contexte. Si le lecteur avait filtré
autrement, une autre s'afficherait. Ces textes sont écrits pour des
**situations** — un métier croisé avec un territoire, une époque croisée avec
une vallée.

Ces combinaisons sont trop nombreuses pour être toutes couvertes. Le travail
n'est donc pas d'écrire beaucoup, mais de **choisir un petit nombre de moments
qui valent d'être écrits** et de laisser le reste s'expliquer par les données
seules.

### Exemple de référence

Une entrée complète a été écrite et validée le 29 juillet 2026 : le lecteur
choisit « travail du métal », la vallée de la Risle apparaît, l'annotation
annonce « 43 usines sur 25 kilomètres, ici on faisait des épingles », le
panneau d'ensemble raconte la chaîne du haut fourneau de 1491 jusqu'aux
épingles, et un clic ouvre la tréfilerie de La Fonte avec ses cent trente-cinq
ouvriers de 1867, dont dix enfants.

Cet exemple fait référence pour le ton, les longueurs et l'articulation entre
les trois niveaux.

## 8. La carte

### Son rôle

La carte n'est pas le sujet. C'est l'instrument de démonstration. Le lecteur
pose une question, la carte apporte la preuve.

Trois fonctions : prouver que la géographie industrielle existe, comparer les
métiers et les territoires, permettre l'exploration libre.

### Sa forme

**La carte n'est pas en plein écran.** Sur les grands écrans, une carte à bord
perdu devient grossière et perd toute tenue.

Elle doit être **encadrée et habillée** : un cadre assumé, une marge, un
habillage qui la tient — titre de la vue, légende, échelle, indicateurs, source.
La carte est un objet posé dans une composition, pas un fond d'écran.

Cette contrainte est structurante pour la direction artistique et doit être
respectée dès la première proposition visuelle.

### Ce qu'elle ne fait jamais

- présenter un point comme une emprise vérifiée ;
- afficher les trois cent dix-huit sites comme trois cent dix-huit objets
  indifférenciés, ce qui produit un semis illisible ;
- transformer une proximité en explication.

## 9. Ce que le corpus fournit, ce qu'il faut produire

**Disponible et exploitable :** trois cent dix-huit sites localisés avec leur
niveau de précision, quatre cent trois activités, trois cent quatorze textes
historiques riches en noms, dates, productions et effectifs, les distances au
cours d'eau, à la forêt, au minerai et au rail.

**À produire, parce que cela n'existe nulle part :**

- **le niveau de l'ensemble.** Les notices décrivent des sites, jamais des
  systèmes. Aucun texte ne dit que la Risle est une vallée du fil métallique.
  Ce niveau s'écrit à partir de la lecture ;
- **les liens entre sites.** Les textes contiennent des relations explicites du
  type « alimentait en fonte », « fournis par l'usine voisine », « rachetée
  par ». Elles ne sont pas extraites et la table qui devrait les accueillir est
  vide. Sans elles, la carte reste un semis de points au lieu d'un réseau ;
- **les dates.** Les textes citent des centaines d'années qui ne sont pas
  structurées. Sur la Risle, trois cent vingt et une années distinctes sont
  citées pour huit activités datées sur soixante-cinq.

**Non disponible :** la situation actuelle. Trois cent quinze sites sur trois
cent dix-huit ont une conservation inconnue. L'application doit le dire
explicitement plutôt que le combler.

## 10. Sources complémentaires

Le corpus peut être enrichi par d'autres sources — archives départementales,
presse, monographies locales, associations. C'est du journalisme normal.

Deux conditions : la source est enregistrée avec sa date, et elle ne remplace
jamais une source primaire disponible. Le registre existe :
`docs/revue_de_presse.md`.

Le coût est en temps de recherche. C'est un travail à planifier, pas à
improviser.

## 11. Règles de preuve maintenues

Elles viennent des phases 0 à 9 et ne se négocient pas.

- Toute affirmation renvoie à une source vérifiable.
- Ce qu'on ne sait pas est écrit comme tel, jamais déduit.
- Une proximité spatiale n'est pas une causalité.
- Une relation entre deux sites n'est affirmée que si une source l'établit.
- Les dates imprécises restent imprécises. « Vers 1840 » ne devient pas 1840.
- Un point n'est pas une emprise.

## 12. Ce qui reste à arbitrer

Ce cadrage ne tranche pas les points suivants, qui relèvent des étapes
suivantes :

- ce que voit exactement le lecteur dans les premières secondes ;
- l'échelle sur laquelle la carte s'ouvre avant toute manipulation ;
- la liste définitive des leviers de filtrage ;
- le nom de la publication ;
- la direction artistique, qui viendra après une première vue construite et
  testée dans un navigateur à taille réelle.
