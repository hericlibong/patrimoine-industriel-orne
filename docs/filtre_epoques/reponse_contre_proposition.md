# Réponse à la contre-proposition sur le filtre temporel

**21 septembre 2026 — décision finale avant révision.** Cette réponse porte sur
`docs/phase10_filtre_temporel.md`, version 2. Elle ne déclenche encore aucun
développement.

**La proposition révisée est acceptée dans son principe. Deux objections
seulement restent à corriger.** Les précautions méthodologiques appartiennent à
la documentation et aux sources ; elles ne doivent pas transformer l'interface
en langage de spécialiste.

## Décision générale

L'idée d'un filtre temporel est retenue et doit être traitée avant la direction
artistique. L'analyse produite est solide : elle distingue correctement les
périodes d'activité, les siècles documentaires, les événements datés et la
situation contemporaine. Elle montre aussi que le libellé « Période d'activité
documentée » ne peut pas couvrir honnêtement les 29 lieux initialement annoncés.

Les choix suivants sont acceptés comme base de travail :

- rouvrir 10.D pour ce complément fonctionnel, en inscrivant le motif au
  journal ;
- conserver les périodes historiques déjà définies dans
  `config/classifications.yml` ;
- retirer provisoirement « Depuis 2001 », qui ne produit aucun résultat utile ;
- commencer avec une seule époque sélectionnée à la fois ;
- rendre visibles les lieux insuffisamment datés dans les explications et les
  compteurs, sans jamais transformer leur absence documentaire en absence
  historique ;
- conserver l'état du filtre pendant la navigation ;
- faire réagir la carte, les listes et les ensembles ;
- réserver l'habillage définitif à 10.E.

## Principe de simplicité pour l'interface

Le lecteur n'a pas besoin de lire constamment « documenté », « attesté » ou
« suffisamment daté ». Les dates viennent des notices et les sources restent
accessibles. L'interface doit donc rester directe :

- sélecteur : **« Époque »** ;
- choix initial : **« Toutes les époques »** ;
- résultat : **« 71 lieux »**, ou le nombre réellement obtenu ;
- filtres actifs : **« Métallurgie · 1850–1913 »** ;
- résultat vide : **« Aucun lieu pour cette époque »** ;
- données manquantes : **« 4 lieux sans date »**.

Aucune phrase explicative permanente n'est nécessaire sous le sélecteur. Une
explication courte peut rester accessible dans la méthode. Le compteur combiné
n'a pas à former une phrase longue : les deux sélecteurs visibles donnent déjà
le contexte du nombre.

## Point central rejeté : l'intervalle entre la première et la dernière date

La règle proposée consiste à faire apparaître un lieu dans toutes les périodes
comprises entre sa première et sa dernière date attestées. Elle n'est pas
retenue.

Un lieu mentionné en 1700 puis en 1900 n'est pas pour autant attesté entre 1789
et 1849. Nous savons seulement que deux faits sont documentés à deux moments
éloignés. Faire apparaître le lieu pendant toutes les périodes intermédiaires
produirait une continuité documentaire qui n'existe pas dans la source.

Le remplacement du mot « actif » par « attesté » ne résout pas ce problème :
le lieu n'est précisément pas attesté dans la période intermédiaire. Les
intervalles atteignant plusieurs siècles montrent que cette erreur ne serait
pas marginale ; elle structurerait une grande partie des résultats.

Les intervalles première–dernière date peuvent rester des indicateurs internes
de l'étendue chronologique d'un dossier. Ils ne doivent pas servir de règle de
sélection publique.

## Règle de remplacement proposée : les événements réellement datés

La chronologie contient 2 360 événements datés concernant 314 lieux. Cette
source offre une couverture large sans remplir artificiellement les silences.

Le filtre recommandé devient :

**Nom court :** « Époque »  
**Explication :** « Lieux pour lesquels un fait est documenté à cette époque »

Un lieu apparaît lorsqu'au moins un événement réellement daté de sa
chronologie chevauche l'époque sélectionnée. Le chevauchement porte uniquement
sur l'intervalle propre à cet événement — date exacte, date approximative,
siècle, décennie ou intervalle indiqué par la source. Il ne porte jamais sur
l'espace séparant deux événements distincts.

Ainsi, un lieu documenté en 1700 et en 1900 apparaît dans les périodes qui
contiennent ces événements. Il n'apparaît pas automatiquement dans toutes les
périodes intermédiaires.

Tous les types d'événements sont admis, y compris les 209 classés
« indéterminés » : leur classement interne est incertain, pas leur existence ni
leur date. Ce point est tranché et ne demande plus d'arbitrage.

## Objection 1 — ne pas inventer une date pour une borne ouverte

Dans la version 2 de `docs/phase10_filtre_temporel.md`, cette objection concerne
précisément :

- la fin de la section **« Les types d'événements admis »** ;
- la section **4.3 — La règle de correspondance** ;
- **T1 — Établir les époques de chaque lieu** ;
- l'arbitrage **2 — Les événements à borne ouverte**.

La recommandation « après 1920 compte comme 1921 » et « avant 1900 compte comme
1899 » est refusée. Elle fabrique une année absente de la source.

Les 103 événements « après » et les 14 événements « avant » doivent être
écartés du calcul de ce filtre. Ils restent naturellement présents, avec leur
formulation originale, dans la chronologie du lieu. Les effectifs par époque,
par ensemble et par métier doivent être recalculés après cette exclusion.

## Objection 2 — corriger le nombre d'ensembles vides avant 1789

Dans la version 2, cette objection concerne précisément :

- la fin de la section **4.4 — Les effectifs, recalculés** ;
- la section **4.7 — Le comportement aux trois niveaux** ;
- l'arbitrage **5 — Les cases vides**.

Le tableau donne six ensembles sans résultat avant 1789 : Noireau, Flers,
Alençon, La Ferté-Macé, Tinchebray et Crulai. Les deux mentions de « cinq »
doivent donc devenir **« six »**.

## Combinaison avec le métier

Le filtre métier et le filtre d'époque peuvent être combinés au niveau du lieu.
La combinaison est acceptée pour la première version. Elle n'a pas besoin d'une
phrase explicative longue dans le compteur : les contrôles affichent
« Métallurgie » et « 1850–1913 », puis le résultat indique simplement le nombre
de lieux.

La méthode conserve la nuance suivante : ce croisement ne date pas
nécessairement l'activité métallurgique elle-même. Le filtre strict d'une phase
d'activité reste une option future, séparée.

## Effet recherché sur les trajectoires longues

Un lieu peut apparaître dans plusieurs époques s'il possède des événements
réellement datés dans chacune d'elles. Cela permet de montrer les lieux dont
l'histoire traverse plusieurs périodes sans prétendre qu'ils ont fonctionné
continûment entre ces événements.

Le panneau du lieu pourra, plus tard, distinguer :

- les faits datés de sa chronologie ;
- les véritables phases d'activité datées lorsqu'elles existent ;
- les siècles documentaires de la source.

Ces trois niveaux ne doivent pas être fusionnés.

## Révision demandée

Avant toute implémentation, reprendre `docs/phase10_filtre_temporel.md` afin de :

1. exclure du filtre les 103 événements « après » et les 14 événements
   « avant », sans modifier leurs données ni leur affichage dans les
   chronologies ;
2. recalculer après cette exclusion tous les effectifs par époque, ensemble et
   métier ;
3. corriger « cinq ensembles » en **« six ensembles »** aux trois emplacements
   indiqués ;
4. simplifier les libellés visibles selon la section « Principe de simplicité
   pour l'interface » ;
5. conserver la combinaison métier–époque et l'option future séparée du filtre
   strict par phase d'activité ;
6. adapter T1 et les contrôles à ces décisions.

## Statut

L'idée du filtre est validée. La version 2 fondée sur les événements réellement
datés est retenue. La combinaison métier–époque et tous les types d'événements
sont acceptés. Il reste uniquement les deux corrections décrites ci-dessus :
les bornes ouvertes et le nombre d'ensembles vides avant 1789.

Aucun développement ne doit commencer avant la mise à jour du document et la
confirmation que les effectifs ont été recalculés. Après cette correction, T1
pourra être lancé sans nouvelle contre-proposition générale.
