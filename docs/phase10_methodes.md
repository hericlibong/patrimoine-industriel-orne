# Comment on travaille, phase par phase

Ce document explique en langage ordinaire ce qui est fait à chaque étape de la
phase 10, pourquoi, et ce que ça change dans la publication. Il est complété au
fur et à mesure.

Les détails techniques restent dans les documents de méthode propres à chaque
étape. Ici, on explique.

---

## Phase 10.A.1 — Retrouver les liens entre les usines

**Fait le 29 juillet 2026.**

### Le problème

Jusqu'ici, la base connaissait chaque usine toute seule. Elle savait qu'il y
avait un haut fourneau à Dompierre et une forge à Champsecret, mais pas que le
premier envoyait sa fonte à la seconde.

Or c'est écrit noir sur blanc dans les fiches historiques. Simplement, personne
ne l'avait sorti des textes.

### Ce qu'on a fait

On a relu les textes des 318 fiches en cherchant les phrases où une usine parle
d'une autre usine. Par exemple :

> *« alimentait en gueuses l'affinerie de Varenne à Champsecret »*

Un programme repère ces formulations, puis essaie de deviner de quelle usine il
s'agit, en croisant deux indices : le nom de lieu cité, et le type d'usine
mentionné. Une « affinerie de Varenne » doit renvoyer à un site situé à
Varenne, pas à n'importe quelle affinerie du département.

### Ce qu'on a décidé de compter comme un lien

Cinq cas : une usine qui en approvisionne une autre, une usine qui reçoit d'une
autre, une usine qui dépend d'une autre, une production qui déménage d'un site à
l'autre, et deux sites physiquement reliés par une voie ferrée.

### Ce qu'on a décidé de ne pas compter

Trois cas, et ces exclusions comptent autant que le reste.

**Un moulin devenu usine n'est pas un lien entre deux sites.** C'est le même
lieu qui change de métier. Il est déjà traité comme tel.

**« Dépendant de l'abbaye de Sées » ou « du château de Flers » n'est pas un lien
industriel.** C'est un propriétaire, pas une usine qui en alimente une autre.

**Une gare n'est pas une usine.** « Relié à la gare du Châtellier » décrit une
voie ferrée, pas un autre site du corpus.

### Ce qu'on a trouvé

Le même schéma revient dans sept endroits du département : **un haut fourneau
qui fait de la fonte, et à côté une forge qui la transforme en fer.** Dompierre
et Champsecret, Livaie, Randonnai, Longny, Carrouges, Saint-Patrice, et la
vallée de la Risle.

À Randonnai, la chaîne va même plus loin : un haut fourneau à Irai alimente deux
forges à Randonnai, qui alimentent une fenderie. Trois niveaux.

À côté, deux autres familles : les usines de Rai qui travaillent le métal de
leur grande voisine, et un groupe du XXᵉ siècle, le Ferodo, qui fait circuler
l'amiante entre plusieurs de ses sites.

### Ce qu'on a ramassé au passage

**Ce que ces usines achetaient et vendaient loin.** Coton de Louisiane et de
Géorgie, cacao de Côte d'Ivoire et du Cameroun transformé à Berlin avant
d'arriver dans l'Orne, minerai vendu en Allemagne et en Belgique, bois de Chine,
de Hongrie et du Canada, colorants d'Inde.

**Qui possédait quoi.** Benjamin Bohin revient six fois, le Ferodo cinq fois.
Mais attention : ça, on l'a déduit en voyant le même nom dans plusieurs fiches.
Aucune source ne dit « ces six usines appartiennent au même homme ». C'est donc
mis de côté, en attendant vérification.

### Ce que ça change dans la publication

**Des traits entre les points sur la carte.**

Aujourd'hui, afficher les 318 sites donne une poussière de points. Demain, quand
on regardera la métallurgie, on verra des paires reliées, et on comprendra d'un
coup d'œil que ces usines formaient des chaînes.

En cliquant sur un trait, on lira la phrase du XIXᵉ siècle qui le prouve.

---

## Phase 10.A.1 — Vérification et arbitrage

**Fait le 29 juillet 2026.**

### Ce qu'on a vérifié

Les treize liens trouvés ont été relus un par un, avec leur phrase.

Dix sont nets. Deux étaient incomplets : la phrase citait **deux** forges et le
programme n'en avait retenu qu'une. Un est douteux, et c'est la source
elle-même qui doute — elle écrit « peut-être ».

### Ce qu'on a tranché

Cinq cas où le texte disait « l'usine de Saint-Sulpice » sans préciser laquelle.
Il y a cinq usines dans cette commune. On a décidé en lisant : les trois sites
concernés avaient tous été rachetés par Benjamin Bohin, donc l'usine qui reçoit
leur production après 1945 ne peut être que la sienne.

**Mais on ne fait pas semblant que la source le dise.** Ces trois liens sont
marqués comme une interprétation, pas comme une lecture littérale. Si quelqu'un
conteste, il verra tout de suite que c'est un choix et pourquoi il a été fait.

Un lien a été ajouté à la main : le programme l'avait écarté parce que la phrase
mélangeait une dépendance industrielle réelle et un titre de noblesse.

Un lien a été supprimé : l'usine citée est dans la Sarthe, donc hors sujet.

### Où c'est écrit

Toutes ces décisions sont dans un fichier à part, avec le motif de chacune. Rien
n'est modifié en douce : on peut retrouver qui a décidé quoi et pourquoi.

---

## Phase 10.A.1 — Inscrire les liens dans la base

**Fait le 29 juillet 2026.**

### Une erreur à corriger d'abord

J'avais écrit que la base ne contenait aucun lien entre sites. C'était faux.
Elle en contenait déjà cinq, posés pendant la phase 8 : des cités ouvrières
rattachées à leur mine, et une fenderie dépendant de sa forge. Et ce dernier
lien, que j'avais présenté comme rattrapé à la main, existait depuis un an.

### L'obstacle rencontré

Le modèle n'acceptait que cinq sortes de liens, toutes de **structure** : qui
appartient à quoi, qui succède à qui, qui dépend de qui.

Or ce qu'on venait de trouver était d'une autre nature : un **flux de matière**.
Un haut fourneau qui envoie sa fonte à une forge ne « dépend » pas d'elle et
n'en est pas un composant. Il lui vend quelque chose.

Quatorze des vingt liens étaient dans ce cas. Il n'y avait pas de case pour eux.

### La décision

Une sixième sorte de lien a été ajoutée : **approvisionne**. Ce lieu fournissait
une matière à cet autre.

L'alternative était de les ranger sous « dépend de ». On l'a écartée parce
qu'elle aurait mélangé deux choses très différentes : une cité ouvrière qui
dépend de sa mine, et une forge qui achète de la fonte à son voisin.

Un point de vocabulaire a été fixé au passage. Les notices disent tantôt
« alimentait la forge de la Roche », tantôt « alimentée en fer par la forge du
Champ-de-la-Pierre » — la même relation vue des deux bouts. On l'enregistre
toujours dans le même sens : du fournisseur vers celui qui reçoit.

### Comment les liens sont entrés

Pas à la main dans la base. Ils ont été écrits dans le fichier de décisions du
projet, puis toute la chaîne de fabrication a été rejouée : la mise au propre du
corpus, l'enrichissement, le calcul des distances au paysage, puis la
reconstruction complète.

C'est plus long, mais ça garantit qu'en relançant la fabrication dans six mois,
les liens seront toujours là. Une modification faite directement dans la base
aurait disparu à la première reconstruction.

### Ce qui s'est passé pendant

Quatre contrôles automatiques ont échoué, exactement comme ils devaient. Ils
vérifiaient qu'il y avait bien cinq liens, pas un de plus. C'est leur rôle :
empêcher qu'un changement passe inaperçu. On les a mis à jour en écrivant
pourquoi le nombre change.

Reconstruire le corpus a aussi effacé les tables de textes et d'images de la
phase 9. Elles ont été refabriquées dans la foulée, et leur propre contrôle
final est repassé au vert.

### Résultat

**Vingt-trois liens en base, reliant trente-six sites.**

La chaîne la plus complète est à Randonnai : un haut fourneau à Irai alimente
deux forges, qui alimentent une fenderie. Quatre usines, trois niveaux, tout
écrit dans les sources.

### Ce que ça change dans la publication

La carte peut maintenant tracer des traits entre les usines. Trente-six sites
sur trois cent dix-huit cessent d'être des points isolés : ils deviennent les
maillons de quelque chose.

---

## Phase 10.A.2 — Retrouver les dates

**Fait le 5 août 2026.**

### Le problème

Le corpus ne contient que **25 activités datées sur 403**. Autant dire rien : on
ne peut pas raconter une histoire dans le temps avec ça.

Sauf que les textes des fiches, eux, citent **plus de deux mille années**. Elles
étaient là depuis le début, dans des phrases comme « incendiée en 1877 » ou
« reconstruite en 1880 par Benjamin Bohin ». Simplement, personne ne les avait
sorties du texte.

### La décision qui change tout

On aurait pu se contenter de relever les années. Ça n'aurait servi à rien.

**Une année seule ne dit rien. Ce qui compte, c'est ce qui s'est passé cette
année-là.** On a donc extrait des *événements datés* : une date, ce qui est
arrivé, et la phrase qui le prouve.

Douze sortes d'événements ont été retenues : la création, la première mention
dans les archives, la reconstruction, l'agrandissement, l'installation d'une
machine, le rachat, le changement de métier, l'incendie ou la destruction,
l'autorisation administrative, la fermeture, les chiffres de production et les
effectifs.

### Les règles de datation

On n'a rien inventé : les règles existaient déjà depuis la phase 3.

« Vers 1850 » ne devient jamais 1850. Ça devient un intervalle de 1845 à 1855, et
le texte d'origine reste affiché. « Avant 1867 » n'a pas de date de début.
« Après 1945 » n'a pas de date de fin. Un siècle reste un siècle entier.

Et la formulation d'origine est toujours conservée à côté du calcul, pour qu'un
lecteur puisse vérifier.

### Ce qu'on a trouvé

**2 344 événements datés, sur 312 des 318 sites.**

Voici ce que ça donne pour une usine, la tréfilerie de La Fonte à
Saint-Sulpice-sur-Risle :

| Quand | Quoi |
| --- | --- |
| 1780 | Le marquis de L'Aigle établit la tréfilerie |
| vers 1830 | Une seconde roue hydraulique est installée |
| vers 1860 | Agrandissements |
| 1867 | 135 ouvriers, dont dix enfants |
| 1887 | Benjamin Bohin la rachète et la passe au laiton |
| vers 1891 | Nouveaux agrandissements |
| après 1945 | La production part chez Bohin, à deux kilomètres |

Sept lignes. Une vie d'usine, du marquis d'Ancien Régime à l'absorption par le
voisin. Tout vient du même paragraphe de la fiche, qu'aucun lecteur n'aurait lu
en entier.

### Un défaut corrigé en cours de route

En relisant la fiche de Bohin, dont je connaissais le texte, j'ai vu que
« reconstruite en 1880 » était classée comme une *création*. La raison est
bête : le mot « reconstruite » contient le mot « construit ».

Corrigé, avec deux autres défauts du même genre. Le nombre d'événements mal
classés est passé de 429 à 280 sur 2 344.

### Ce que ça change dans la publication

Le temps devient utilisable. On peut montrer la vie d'un lieu comme une frise,
et surtout comparer : quand les vallées se sont-elles équipées, quand les usines
ont-elles fermé, à quel moment les effectifs se sont effondrés.

C'est la dimension qu'on avait abandonnée faute de dates. Elle revient.

### Où on en est

Rien n'est encore inscrit dans la base. La liste attend une relecture.
