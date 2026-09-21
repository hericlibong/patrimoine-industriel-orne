# Filtre temporel — évaluation et proposition révisée

**Version 3, 21 septembre 2026.** Intègre les deux corrections de la décision
finale du porteur : **les événements à borne ouverte sont écartés du calcul**, et
le nombre d'ensembles sans résultat avant 1789 est **six**, non cinq. Tous les
effectifs ont été recalculés après exclusion. Les libellés de l'interface sont
ramenés au principe de simplicité posé par le porteur.

Rappel des versions. La version 1 retenait un lieu sur l'intervalle entre sa
première et sa dernière date : règle retirée, elle fabriquait une continuité
absente de la source. La version 2 l'a remplacée par les événements réellement
datés, mais ancrait les bornes ouvertes sur une année inventée : correction
apportée ici.

Aucun code, aucune donnée modifiée, aucune branche, aucun développement lancé.
Tous les chiffres ont été recalculés depuis les exports du corpus.

---

## 0. Ce qui change depuis la version 1, et pourquoi

**La règle de l'intervalle première–dernière date était fausse.** Un lieu
mentionné en 1700 puis en 1900 n'est pas attesté entre 1789 et 1849 : deux faits
sont documentés à deux moments éloignés, et rien n'est documenté entre les deux.
Remplacer « actif » par « attesté » ne réparait rien, puisque le lieu n'est
précisément pas attesté dans l'intervalle. Et l'erreur n'aurait pas été
marginale : vingt-huit lieux couvraient plus de trois siècles et seraient
apparus presque partout.

**La règle retenue est celle du porteur :** un lieu apparaît quand au moins un
événement réellement daté de sa chronologie chevauche l'époque choisie. Le
chevauchement porte sur l'intervalle propre de l'événement — année, année
approximative, siècle, décennie, quart de siècle, intervalle indiqué par la
source — et jamais sur l'espace séparant deux événements.

**Elle couvre mieux que celle qu'elle remplace.** L'intervalle donnait 225 lieux
sur 318 ; les événements datés en donnent **314**, bornes ouvertes exclues. La
règle la plus fidèle est aussi la plus large : c'est rare, et cela clôt la
discussion.

| | Version 1, retirée | Version 3, retenue |
| --- | ---: | ---: |
| Lieux couverts | 225 | **314** |
| Lieux d'ensemble couverts | — | **170 sur 172** |
| 1976–2000 | 30 lieux | **103 lieux** |
| Continuité supposée entre deux faits | Oui, et c'est le défaut | **Aucune** |
| Année inventée pour une borne ouverte | — | **Aucune** |

L'intervalle première–dernière date reste utile comme indicateur interne de
l'étendue chronologique d'un dossier. Il ne sert pas à sélectionner.

---

## 1. Analyse de l'idée

### Ce que le filtre permet de comprendre

Il répond à une question qu'aucun autre levier ne pose : **quand ?** Le métier
dit ce qu'on faisait, la carte dit où, la proximité de l'eau dit avec quelle
force motrice. Rien ne dit à quel moment. Or le corpus couvre neuf siècles — le
plus ancien événement daté remonte à 1101, le plus récent à 2001.

Il permet surtout de montrer que **le patrimoine industriel de l'Orne n'est pas
un bloc**. Les chiffres révisés le disent d'eux-mêmes : neuf lieux de la Risle
portent un fait documenté avant 1789, aucun à Flers ni à Crulai. Onze lieux de
Flers en portent un après 1976, aucun à La Ferrière. Ces écarts sont de la
matière éditoriale, pas des défauts de données.

### Ce qu'il ne permet pas d'affirmer

**Qu'un lieu était actif.** Un fait daté est un fait, pas une activité. « Deux
groupes électrogènes à vapeur en 1919 » dit qu'on a documenté un équipement, pas
que l'usine tournait.

**Qu'un lieu était actif entre deux faits.** C'est l'erreur de la version 1, et
la règle retenue l'élimine par construction : un lieu n'apparaît que dans les
époques où un événement tombe.

**Qu'un lieu absent d'une époque n'y existait pas.** Une absence de datation
n'est pas une absence historique. C'est le risque qui subsiste, et il se traite
par les compteurs, non par la règle.

### Avant ou après la direction artistique

**Avant.** Un filtre est une structure : il change ce que la carte montre, ce
que les listes comptent, ce que les ensembles affichent. Le découvrir après
avoir habillé l'application obligerait à re-habiller.

Cela rouvre 10.D, close la veille. Le porteur l'a accepté et l'inscrit au
journal avec son motif.

### L'impact sur les trois niveaux

| Niveau | Ce que le filtre y fait |
| --- | --- |
| Département | Réduit les points, recadre la carte, **et réduit la liste des ensembles** : un ensemble sans lieu dans l'époque disparaît, comme avec le métier |
| Ensemble | Réduit les lieux, efface les liens dont une extrémité disparaît, recadre |
| Lieu | Ne filtre rien — un lieu ouvert reste entier — mais l'état du filtre survit à l'aller-retour |

Faire réagir les ensembles suppose que chaque ensemble sache quelles époques il
couvre. C'est une donnée à transmettre, traitée en T2 de la roadmap.

---

## 2. Analyse de la proposition initiale

### Le chiffre de 29 lieux recouvrait deux choses différentes

| Origine | Phases | Lieux | Ce que c'est |
| --- | ---: | ---: | --- |
| `chronologie_phase` | 25 | **12** | Une vraie période d'activité, calculée depuis des bornes documentées |
| `siecles_source_site` | 17 | **17** | Un repérage depuis le champ des siècles, **sans preuve de continuité d'activité** |
| **Total** | 42 | **29** | |

La proposition initiale les étiquetait « période d'activité documentée ». Pour
17 d'entre eux ce libellé est faux, et le dictionnaire du projet le dit :
« sans preuve automatique de continuité de l'activité ». Ce point n'est pas
contesté par la réponse du porteur ; il est acté.

### Pourquoi le filtre strict reste inutilisable comme filtre général

Sur les 172 lieux des douze ensembles, **cinq** ont une vraie période
d'activité : quatre dans la Risle, un à Alençon. Cinq ensembles sur douze n'ont
rien. Sur les deux ensembles ouverts, le filtre strict laisserait quatre lieux
sur cinquante et viderait entièrement Crulai.

Il reste néanmoins une **option future distincte**, maintenue séparée comme le
demande la réponse : voir la section 4.9.

### Règle par règle, après révision

| Règle proposée | Verdict |
| --- | --- |
| Les sept périodes existent dans `classifications.yml` | **Exact.** Codes et bornes vérifiés |
| « Toutes les époques » par défaut | **Retenu** |
| Une seule époque à la fois | **Retenu** |
| Un lieu apparaît si une phase chevauche | **Remplacé** : si un **événement daté** chevauche |
| Un élément chevauchant plusieurs époques appartient à chacune | **Retenu et nécessaire** |
| Lieux insuffisamment datés visibles quand le filtre est vide | **Retenu** |
| Lieux insuffisamment datés retirés quand une époque est choisie | **Retenu, à condition d'être comptés à l'écran** |
| Message « 29 lieux suffisamment datés » | **Chiffre remplacé** : 314 lieux portent au moins un fait daté |
| Filtre aux trois niveaux | **Retenu** |
| État conservé pendant la navigation | **Retenu** — le mécanisme du filtre métier existe déjà |
| Ensembles vides retirés de la liste | **Retenu et désormais sans danger** : voir 4.7 |
| Métier et époque sur la même phase | **Impossible en général** — 10 % du corpus. Voir 4.5 |
| Déduplication par lieu | **Retenu et obligatoire** |
| Clavier et écran étroit | **Retenu** |
| Aucun style avant 10.E | **Retenu** |

### La période « Depuis 2001 »

**Un seul lieu**, pour un seul événement de toute la chronologie. Retirée du
filtre, conservée dans le vocabulaire — conformément à la décision du porteur.

### Siècles ou demi-siècles

Les six périodes nommées portent un sens historique : la Révolution, le rail et
la vapeur, les guerres, les Trente Glorieuses, les reconversions. Des siècles ou
des demi-siècles seraient plus réguliers et diraient moins. **Périodes nommées
conservées.**

---

## 3. Les sources temporelles comparées

| Source | Couverture | Ce qu'elle prouve | Ce qu'elle ne prouve pas | Filtre public | Libellé honnête |
| --- | ---: | --- | --- | --- | --- |
| **Événements datés à bornes connues** | **314 lieux**, 2 243 événements | Qu'un fait précis est documenté à un moment | Rien entre deux faits | **Oui — règle retenue** | « Un fait documenté à cette époque » |
| **Événements à borne ouverte** | 117 événements | Qu'un fait est antérieur ou postérieur à une date | À quelle époque le rattacher | Non — écartés du calcul, conservés à l'affichage | « après 1920 », tel quel |
| **Phase d'activité** | 12 lieux, 25 phases | Qu'une activité a eu des bornes documentées | Rien au-delà | Non, trop rare ; option future | « Période d'activité documentée » |
| **Siècles documentaires** | 318 lieux | Que la source situe le lieu dans ces siècles | Ni l'activité, ni sa continuité | Non retenu | « Siècles mentionnés par la source » |
| **Intervalle première–dernière date** | 225 lieux | L'étendue d'un dossier | **Pas l'attestation entre les deux** | **Refusé** | Usage interne seulement |
| **Situation actuelle** | 318 lieux | Un état — conservé, dégradé, détruit | Une période d'activité | Non, ce n'est pas du temps | — |

Ces sources ne doivent jamais être fusionnées. Le panneau du lieu pourra les
distinguer, comme le prévoit la réponse du porteur ; c'est hors de la première
version.

### Les types d'événements admis

La réponse demande de confirmer les types admis ou de documenter les exclusions.

| Type | Nombre | Admis | Motif |
| --- | ---: | --- | --- |
| emploi | 361 | Oui | Un effectif relevé une année est un fait daté |
| creation | 339 | Oui | |
| cessation | 276 | Oui | |
| production | 221 | Oui | |
| equipement | 217 | Oui | |
| attestation | 212 | Oui | |
| **indetermine** | **209** | **Oui** | Voir ci-dessous |
| agrandissement | 97 | Oui | |
| reconstruction | 97 | Oui | |
| reglementation | 93 | Oui | Un arrêté daté documente le lieu à cette date |
| exploitation | 66 | Oui | |
| conversion | 63 | Oui | |
| acquisition | 59 | Oui | |
| destruction | 50 | Oui | |

**Aucune exclusion par type, et les 209 « indéterminés » sont admis.** La
vérification faite pour ce document est sans ambiguïté : leur type est inconnu,
leur date ne l'est pas. Quelques-uns, mot pour mot :

> « Exploitation démarrée en 1910 » · « 1 800 000 camemberts produits en 1970 »
> · « Modernisation du site en 1933 » · « augmentée d'une cidrerie en 1914 »

Ce sont des faits datés parfaitement utiles au lecteur. Les exclure retirerait
116 lieux d'une ou plusieurs époques pour un motif de classement interne.

**Une seule exclusion, et elle porte sur la précision, pas sur le type.** Les
103 événements de précision « après » et les 14 de précision « avant » ont une
borne ouverte : « après 1920 » ne dit pas jusqu'à quand, « avant 1900 » ne dit
pas depuis quand.

La version 2 proposait de les ancrer sur leur seule borne connue — 1921, 1899.
**Le porteur l'a refusé, et le motif est juste : cela fabrique une année absente
de la source.** Une source qui dit « après 1920 » ne dit pas 1921.

**Ces 117 événements sont donc écartés du calcul du filtre.** Ils ne sont ni
modifiés ni masqués : ils restent dans la chronologie du lieu, avec leur
formulation d'origine, et le lecteur les y lit normalement. Le filtre travaille
sur les **2 243 événements** dont les deux bornes sont connues. Aucun lieu n'est
perdu par cette exclusion : les lieux couverts restent 314 sur 318.

---

## 4. Proposition révisée

### 4.1 Le nom et l'explication

**Nom court : « Époque ».** Rien d'autre à l'écran.

La phrase « Lieux pour lesquels un fait est documenté à cette époque » définit
la règle, mais **elle n'est pas affichée en permanence** : elle vit dans la
méthode, accessible en un clic. Principe posé par le porteur : le lecteur n'a
pas à lire « documenté », « attesté » ou « suffisamment daté » à chaque écran.
Les dates viennent des notices, et les sources restent atteignables.

Le mot « actif » n'apparaît nulle part.

### 4.2 Les époques

Six, sans « Depuis 2001 » :

Avant 1789 · 1789–1849 · 1850–1913 · 1914–1945 · 1946–1975 · 1976–2000

### 4.3 La règle de correspondance

Un lieu apparaît si **au moins un événement daté de sa chronologie a son propre
intervalle qui chevauche l'époque choisie.**

L'intervalle est celui que la source donne à cet événement, déjà présent dans le
corpus : « 1949 » donne 1949–1949, « vers 1920 » donne 1915–1925, « 19e siècle »
donne 1801–1900, « années 1950 » donne 1950–1959, « entre 1950 et 1956 » donne
1950–1956. **Aucun calcul ne relie deux événements.**

**Un événement dont une borne est ouverte n'entre pas dans le calcul.** « Après
1920 » et « avant 1900 » ne désignent aucune époque : les rattacher à l'une
d'elles supposerait une année que la source ne donne pas. Ces 117 événements
restent affichés dans la chronologie du lieu ; ils ne servent pas à le
sélectionner.

Un lieu peut apparaître dans plusieurs époques s'il a des faits datés dans
chacune. C'est l'effet recherché : montrer les trajectoires longues sans
prétendre à une continuité.

### 4.4 Les effectifs, recalculés

Calculés sur les 2 243 événements à bornes connues, les 117 événements à borne
ouverte étant écartés.

**Par époque, sur les 318 lieux du corpus :**

| Époque | Lieux |
| --- | ---: |
| Avant 1789 | 67 |
| 1789–1849 | 176 |
| 1850–1913 | 258 |
| 1914–1945 | 168 |
| 1946–1975 | 154 |
| 1976–2000 | 103 |

**Par ensemble :**

| Ensemble | Lieux | Datés | Av. 1789 | 1789‑1849 | 1850‑1913 | 1914‑1945 | 1946‑1975 | 1976‑2000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Risle | 43 | 43 | 9 | 33 | 39 | 27 | 14 | 10 |
| Noireau | 23 | 23 | — | 16 | 18 | 11 | 12 | 3 |
| Flers | 21 | 21 | — | 3 | 15 | 13 | 17 | 11 |
| Halouze | 13 | 13 | 5 | 5 | 12 | 5 | 6 | 6 |
| Alençon | 13 | 11 | — | 3 | 6 | 9 | 10 | 5 |
| La Ferté-Macé | 12 | 12 | — | 1 | 11 | 8 | 5 | 5 |
| Tinchebray | 9 | 9 | — | 3 | 5 | 5 | 8 | 8 |
| Randonnai | 9 | 9 | 5 | 6 | 8 | 2 | 1 | 3 |
| Malétable | 8 | 8 | 5 | 8 | 7 | 4 | 3 | 2 |
| La Ferrière | 7 | 7 | 1 | 1 | 5 | 3 | 4 | — |
| Argentan | 7 | 7 | 1 | 3 | 5 | 3 | 4 | 3 |
| Crulai | 7 | 7 | — | 6 | 7 | — | 1 | — |
| **Total** | **172** | **170** | **26** | **88** | **138** | **90** | **85** | **56** |

**Les cases vides sont des résultats, pas des pannes.** Neuf couples ensemble ×
époque sur soixante-douze sont vides. **Six d'entre eux sont « Avant 1789 »** :
Noireau, Flers, Alençon, La Ferté-Macé, Tinchebray et Crulai n'ont aucun fait
documenté avant la Révolution. Deux sont « 1976–2000 » : La Ferrière et Crulai.
Le neuvième est Crulai sur « 1914–1945 ». C'est de l'information éditoriale.

**Trajectoires :** 5 lieux traversent les six époques, 20 en traversent cinq,
70 en traversent quatre, 104 en traversent trois, 89 deux, et 26 une seule.

**Les lieux sans aucun fait daté sont quatre** — une scierie à
Saint-Germain-de-Clairefeuille, deux tanneries à Vimoutiers et Alençon, une
imprimerie à Alençon. Deux d'entre eux appartiennent à un ensemble, tous deux à
Alençon.

### 4.5 La combinaison avec le métier

**Autorisée, croisée au niveau du lieu, et dite honnêtement.**

Le croisement au niveau de l'activité — un métier et sa propre période — n'est
vérifiable que sur les 42 phases datées, soit 10 % du corpus. Il est hors de
portée comme règle générale.

**La combinaison est acceptée pour la première version**, et le compteur reste
court : les deux contrôles affichent « Métallurgie » et « 1850–1913 », le
résultat indique « 70 lieux ». Les sélecteurs visibles donnent le contexte du
nombre ; aucune phrase longue n'est nécessaire.

La nuance — ce croisement ne date pas l'activité métallurgique elle-même —
appartient à la méthode, pas au compteur.

Les effectifs croisés sont substantiels et le filtre y gagne son intérêt : la
métallurgie compte 42 lieux avec un fait documenté avant 1789 et 18 après
1976 ; l'agroalimentaire, l'inverse — 23 avant 1789, 92 entre 1850 et 1913.
C'est exactement ce que le projet veut montrer.

| Métier | Lieux | Av. 1789 | 1789‑1849 | 1850‑1913 | 1914‑1945 | 1946‑1975 | 1976‑2000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Agroalimentaire | 113 | 23 | 81 | 92 | 61 | 57 | 38 |
| Métallurgie | 79 | 42 | 61 | 70 | 31 | 23 | 18 |
| Textile, habillement, cuir | 76 | 5 | 36 | 65 | 43 | 43 | 23 |
| Bois, papier, imprimerie | 32 | 7 | 12 | 24 | 22 | 22 | 16 |

Le filtre strict d'une phase d'activité reste une option future, séparée : voir
la section 4.9.

### 4.6 Les libellés

Ramenés au principe de simplicité posé par le porteur : des mots courts, aucune
phrase explicative permanente.

| Emplacement | Texte |
| --- | --- |
| Le sélecteur | **Époque** |
| Choix par défaut | Toutes les époques |
| Filtres actifs | Métallurgie · 1850–1913 |
| Résultat | 258 lieux |
| Résultat vide | Aucun lieu pour cette époque |
| Données manquantes | 4 lieux sans date |
| Panneau de l'ensemble | 39 lieux sur 43 |
| Panneau du lieu | Faits datés : 1825, vers 1850, 1867, 1963 |
| Panneau du lieu, si aucune date | Aucune date dans la source |
| Dans la méthode, atteignable en un clic | Lieux pour lesquels un fait est documenté à cette époque |

**« 4 lieux sans date » reste obligatoire** quand une époque est choisie. C'est
la mention la plus courte qui empêche le lecteur de conclure qu'il ne s'est rien
passé ailleurs. Elle est courte parce qu'elle est permanente.

### 4.7 Le comportement aux trois niveaux

**Département.** Les points se réduisent, la carte se recadre, la liste des
ensembles se réduit. Un ensemble reste affiché s'il compte au moins un lieu avec
un fait documenté à l'époque choisie. **Six ensembles disparaissent sur « Avant
1789 »** — Noireau, Flers, Alençon, La Ferté-Macé, Tinchebray et Crulai — deux
sur « 1976–2000 » — La Ferrière et Crulai — et Crulai seul sur « 1914–1945 ».
Les quatre autres époques n'en font disparaître aucun. Dans tous les cas c'est
un fait historique, pas un défaut.

**Ensemble.** Les lieux se réduisent, les liens dont une extrémité disparaît
s'effacent — comme le filtre métier le fait déjà. La carte se recadre. Le
panneau annonce combien de lieux sont masqués et combien n'ont aucune date.

**Lieu.** Rien n'est filtré. Le sélecteur est masqué pendant la lecture, comme
celui du métier, et restauré au retour.

### 4.8 L'explication méthodologique

Rien n'est posé sur la page. Le texte vit dans la méthode, atteignable en un
clic depuis le compteur :

> Les dates viennent des fiches d'inventaire. Un lieu apparaît ici quand un fait
> daté — une construction, un effectif, un arrêt — y est documenté. Entre deux
> faits, la source ne dit rien, et nous non plus. Les faits que la source situe
> seulement « avant » ou « après » une date ne servent pas à ce filtre ; ils
> restent lisibles dans la chronologie du lieu.

### 4.9 L'option future, maintenue séparée

Le filtre strict par phase d'activité — 12 lieux, 25 phases — **n'est pas
abandonné, il est mis de côté.** Il redeviendra pertinent si le nombre de phases
structurées augmente. Il ne se mélange pas au filtre d'époque et ne doit jamais
partager son sélecteur.

Sa place naturelle est le panneau du lieu, où une phrase peut dire
« Tréfilerie documentée de 1807 à 1926 » sans être confondue avec un compteur.
Hors de la première version.

### 4.10 Ce qui appartient à 10.D et ce qui attend 10.E

| À faire dans 10.D | À laisser à 10.E |
| --- | --- |
| Calculer les époques de chaque lieu depuis ses événements | L'apparence du sélecteur |
| Transmettre les époques couvertes par chaque ensemble | Le dessin des points filtrés |
| Le sélecteur, ses six époques, son état conservé | L'animation du recadrage |
| La réaction des trois niveaux, ensembles compris | La mise en page des compteurs |
| Les compteurs, y compris le décompte des non datés | La typographie |
| Les libellés courts, arrêtés dans les mots | |
| La note de méthode et son accès depuis le compteur | Sa forme |

---

## 5. Mini-roadmap

Aucune tâche n'est lancée. Aucune phase ne calcule de continuité entre deux
événements.

### T1 — Établir les époques de chaque lieu — **fait le 21 septembre 2026**

Outil : `tools/epoques_lieux.py`. Relevé :
`docs/filtre_epoques/T1_releve_epoques.md`. Les six contrôles passent et les
effectifs sont conformes à ceux des sections 4.4 et 4.5.

- Pour chaque lieu, retenir les époques traversées par l'intervalle propre de
  chacun de ses événements datés. Aucune donnée du corpus n'est modifiée.
- **Écarter du calcul les 117 événements à borne ouverte**, sans les modifier ni
  les retirer de la chronologie du lieu.
- Produire le décompte par époque, par ensemble et par métier.

**Livrable :** un relevé chiffré reproductible.
**Contrôles :** les totaux se recoupent avec les 318 lieux et avec les tableaux
de la section 4.4 ; les quatre lieux sans date sont nommés ; aucun lieu ne
reçoit une époque sans événement qui la justifie ; un contrôle vérifie
qu'aucune époque intermédiaire n'est ajoutée entre deux faits ; un second
vérifie qu'aucune année n'est inventée pour un événement à borne ouverte, et
que ces 117 événements restent affichables.
**Validation du porteur avant T2.**

### T2 — Transmettre les époques au prototype — **fait le 21 septembre 2026**

Fait dans `tools/generer_vue_reference.py`, qui appelle le module de T1 plutôt
que de réécrire la règle. Trois contrôles ajoutés au générateur. Poids : la page
passe de 898,9 à 921,4 ko, soit +2,5 %, et +1,2 ko une fois compressée.

**Écart relevé, à trancher en T3 :** la vue ne transmet que 196 lieux en points.
Sur les quatre lieux sans date du corpus, deux seulement sont visibles ; les
deux autres sont à Alençon, ensemble fermé. Le compteur devra dire ce qu'il
compte, ou compter ce qu'il montre.

- Ajouter à chaque lieu la liste de ses époques, pour les lieux d'ensemble et
  pour les 146 lieux hors ensemble.
- Ajouter à chaque ensemble les époques qu'il couvre, sans quoi la liste des
  ensembles ne peut pas réagir.
- Mesurer le poids ajouté.

**Livrable :** les données du filtre présentes dans la vue, rien d'affiché.
**Contrôles :** effectifs inchangés ; le générateur sort en erreur si un
décompte ne correspond pas ; poids mesuré avant et après.
**Validation du porteur avant T3.**

### T3 — Le sélecteur et les compteurs — **fait le 21 septembre 2026**

Un seul jeu de fonctions sert les deux sélecteurs. **Le compteur annonce
« 2 lieux sans date » et non quatre** : les deux autres sont à Alençon, ensemble
fermé, et ne sont pas des points affichés — le compteur dit ce qu'il montre, la
note de méthode dira ce que porte le corpus. Clavier, conservation de l'état et
écran étroit vérifiés. À 390 pixels la barre des filtres atteint 207 pixels
avant la carte : question d'habillage, renvoyée à 10.E.

- Poser le sélecteur à côté de celui du métier, avec ses six époques.
- Écrire les compteurs, y compris le décompte des lieux sans date.
- Conserver l'état pendant la navigation.

**Livrable :** le filtre visible et fonctionnel au niveau département.
**Contrôles :** effectifs de la carte et de la liste identiques ; clavier ;
écran étroit.
**Validation du porteur avant T4.**

### T4 — La réaction des trois niveaux — **fait le 21 septembre 2026**

Neuf tests qui n'interrogeaient que le métier sont devenus un test unique. Un
ensemble vidé affiche « Aucun lieu pour cette époque » et laisse repartir. 125
cas parcourus — quatre états du métier croisés avec sept états de l'époque,
puis entrée dans les deux ensembles ouverts, ouverture d'un lieu et retour :
aucune erreur, aucun cul-de-sac, aucune perte d'état.

- Réduire la liste des ensembles au département.
- Réduire lieux et liens dans l'ensemble, recadrer.
- Masquer le sélecteur en mode lieu et le restaurer au retour.
- Combiner avec le métier, les deux sélecteurs restant visibles côte à côte.

**Livrable :** le filtre agit aux trois niveaux.
**Contrôles :** parcours complet sous chacune des six époques ; croisement avec
trois métiers ; aucun cul-de-sac ; aucun ensemble affiché vide ; vérification
que les neuf couples ensemble × époque vides produisent « Aucun lieu pour cette
époque » et non une page morte.
**Validation du porteur avant T5.**

### T5 — Épreuve et clôture

- Éprouver sur les deux ensembles ouverts et sur un ensemble fermé.
- Vérifier ordinateur, mobile et clavier.
- Consigner, puis reclore 10.D.

**Livrable :** relevé d'épreuve et clôture réinscrite au journal.
**Contrôles :** ceux de L6, appliqués au filtre.
**Décision du porteur.**

---

## 6. Arbitrages attendus

**Tout ce qui était en suspens est tranché.** Rappel de ce que la décision
finale du porteur a fixé, et qui ne se rediscute plus :

| Point | Décision |
| --- | --- |
| La règle de sélection | Les événements réellement datés, jamais l'intervalle entre deux faits |
| Les types d'événements | Tous admis, y compris les 209 « indéterminés » |
| Les événements à borne ouverte | Écartés du calcul, conservés à l'affichage |
| La combinaison avec le métier | Acceptée en première version, compteur court |
| Les libellés | Mots courts, aucune phrase permanente sous le sélecteur |
| « Depuis 2001 » | Retirée du filtre, conservée dans le vocabulaire |
| Une seule époque à la fois | Oui |
| Le filtre strict par phase d'activité | Option future, séparée |
| La réouverture de 10.D | Acceptée, motif à inscrire au journal |

**Il ne reste qu'une chose à faire avant T1 :** confirmer que les effectifs de
ce document, recalculés après l'exclusion des bornes ouvertes, sont ceux sur
lesquels le travail s'engage. Ce sont ceux des sections 4.4 et 4.5.
