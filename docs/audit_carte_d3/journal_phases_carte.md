# Carte de la Risle — journal des phases d'amélioration

Branche `codex/carte-d3-modele-risle`, ouverte le 19 septembre 2026 depuis
l'essai D3 enregistré (`8097a53`).

**Objet.** Améliorer la carte de niveau ensemble, sur la Risle seule, qui sert
de modèle aux onze autres ensembles. Ce qui est établi ici comme règle sera
transposé ; ce qui est propre à cette vallée sera signalé comme tel.

**Règle de conduite.** Chaque phase se termine par une capture à 1440 px jugée
par le porteur. Rien ne s'empile sur une phase non validée. Aucune coordonnée,
aucune donnée source n'est modifiée par ces travaux.

## Décision du porteur — la végétation contemporaine est écartée (19 septembre 2026)

Question posée avant d'engager la phase 3 : une couche de forêt décrivant les
bois de 2006-2019 a-t-elle sa place dans une carte de patrimoine industriel
ancien ?

**Le constat qui a déplacé la question.** Tout ce que montre déjà la carte est
contemporain : les cours d'eau viennent des relevés actuels, les repères de
bourg d'adresses de mairie vérifiées cette année, et le sol posé en phase 1 est
celui des communes de 2026 — dont certaines sont des fusions récentes. La carte
est une carte d'aujourd'hui sur laquelle on situe des lieux d'hier. C'est
cohérent avec le sujet, qui est le patrimoine, donc une question du présent.

**Pourquoi la forêt n'a pas le même statut que la rivière.** La Risle a peu
changé en trois siècles : montrer la rivière d'aujourd'hui, c'est montrer à peu
près celle qui a fait naître les forges, et le lien de cause est vrai. La forêt,
elle, a beaucoup changé — et à cause de l'industrie cartographiée, les forges
consommant du charbon de bois. Un aplat de forêt actuelle derrière une forge de
1700 donnerait à lire « voilà le bois qui l'alimentait », ce qui serait faux.
Une mention en petits caractères ne corrige pas ce qu'une surface colorée fait
dire à l'œil. Le registre des sources du projet avait d'ailleurs déjà classé la
forêt actuelle en second rang et les forêts anciennes reconstruites vers 1850
en premier.

**Décision : la forêt contemporaine n'entre pas dans la carte.** Une couche de
végétation ne sera envisagée qu'à partir des forêts anciennes reconstruites vers
1850, sous réserve d'obtenir ces données en local et de confirmer leur licence.
La présence du territoire est recherchée d'abord par le relief, dont la
stabilité dans le temps est acquise ; sa source reste à trouver et à évaluer.
Les crédits de la carte indiquent que le fond — eau, communes, repères de bourg
— décrit la situation actuelle et non celle de la période industrielle, et
signalent que les aménagements hydrauliques disparus n'y figurent pas.

*Cette décision doit être reportée dans `docs/journal_decisions.md`, qui fait
foi ; la présente trace ne s'y substitue pas.*

---

**Cadre arrêté avec le porteur, 19 septembre 2026 :** quatre phases.

| Phase | Objet | État |
| --- | --- | --- |
| 0 | Correction du blocage d'affichage | Fait, à juger |
| 1 | Le cadre et le sol | Fait, à juger |
| 2 | Le dessin tenu par D3 | Fait, à juger |
| 3 | L'eau, les lieux, les liens (végétation écartée) | Fait, à juger |
| 4 | Le mouvement et l'approche | Fait, à juger |

---

## Phase 0 — Débloquer l'affichage (19 septembre 2026)

Non prévue au plan : découverte en ouvrant la carte dans un navigateur, ce qui
n'avait jamais été fait pour l'essai D3.

**Constat.** Le navigateur se figeait au premier affichage de la Risle. Mesure :
dessiner toute la carte coûtait 15 ms, placer les cinq noms de bourgs en coûtait
**480**. La recherche de placement essayait toutes les positions de la carte
contre environ 370 obstacles, à chaque changement de filtre et à chaque
redimensionnement de fenêtre.

**Fait.**

- L'occupation de la carte est rasterisée une fois par rendu, puis cumulée en
  tableau de sommes : tester une boîte devient quatre lectures. Les positions
  examinées et la règle de choix sont inchangées — le nom va toujours au plus
  près de ce qu'il désigne, et aucun nom n'est masqué.
- Les signes carrés de localité, laissés dans le groupe transformé par le zoom,
  grossissaient d'un facteur six. Ils sont compensés comme les points et les
  noms l'étaient déjà.
- Les 43 lieux, recopiés en double dans la page au format GeoJSON alors que le
  rendu reconstituait aussitôt leur forme d'origine, ne le sont plus.

**Mesuré, avant → après :** placement des noms 480 → 35 ms ; cycle complet
(changer de métier, revenir) figeait → 37 et 94 ms ; page 899 → 851 ko ;
carrés de localité à zoom 5 : six fois trop grands → taille constante,
vérifiée par mesure à k = 1 et k = 5,06 avec retour exact au cadrage initial.

**Limite acceptée.** La grille d'occupation réserve l'espace à deux unités près
au lieu du pixel exact. Trois des cinq noms se sont légèrement déplacés :
« L'Aigle » est passé sous son groupe de points, « Rai » à gauche de son carré.
Rien n'est coupé ni superposé. Le placement antérieur avait été validé sur
capture par le porteur : ce nouveau placement demande son jugement.

**Reste ouvert.** Les noms de bourgs sont calculés au cadrage initial et ne
suivent pas le zoom : en s'approchant, ils décrochent de leur signe et peuvent
sortir du cadre. Renvoyé à la phase 4.

---

## Phase 1 — Le cadre et le sol (19 septembre 2026)

**Constat corrigé en cours de route.** L'examen annonçait que la moitié du cadre
était vide et que resserrer ferait doubler la taille des points. La mesure a
démenti : les données occupent toute la largeur et 72 % de la hauteur, et la
carte s'étirant de toute façon à la largeur disponible, resserrer le cadre ne
grossit pas les points. Le resserrement reste utile — il supprime des bandes
vides — mais la taille des points est un paramètre libre, à régler pour
lui-même.

**Fait.**

- **Le cadre prend la proportion de ce qu'il montre**, entre deux bornes (360 et
  620 unités de haut) pour qu'il reste une carte et non un bandeau. Pour la
  Risle : 1000 × 560 → 1000 × 462. Ni les coordonnées ni la formule de
  projection ne changent ; l'emprise stable arbitrée le 18 septembre est
  conservée, calculée sur les mêmes 43 lieux et quatre bourgs.
- **Les points passent de 5,5 à 7 unités de rayon** (10 pour le lieu ouvert).
- **La carte reçoit un sol** : les contours communaux, dessinés sous l'eau, sous
  les liens et sous les lieux, en aplat clair avec une limite fine.

**Provenance du sol.** Contours communaux API Géo du 22 juillet 2026, déjà
présents dans le projet et déjà lus par le générateur pour la frontière
départementale. Aucune source nouvelle, aucun téléchargement, aucun droit à
demander. Appariement par le nom de commune.

**Décision de dessin, prise en cours de phase.** Le premier essai ne dessinait
que les dix communes portant un lieu. Résultat : une bande découpée au milieu du
blanc — et surtout une forme fermée que le lecteur pouvait prendre pour la
frontière de l'ensemble, ce que la méthode du projet interdit explicitement.
Toutes les communes qui touchent le cadre sont donc dessinées : 52 pour la
Risle. Le sol déborde volontairement du cadre pour qu'aucune limite communale ne
soit lue comme une limite de carte. Les communes portant un lieu sont marquées
dans les données mais ne reçoivent aucun traitement visuel distinct.

**Contrôles effectués.** Six contrôles du générateur vrais, aucun écart :
12 ensembles, 172 lieux en ensemble, 146 autres, Risle 43 lieux et 5 relations,
Crulai 7 lieux. Un sixième contrôle a été ajouté — `sol_complet` — qui fait
échouer la génération si une commune portant un lieu n'a pas de contour : un
trou dans le sol ne doit pas passer inaperçu. Il est vrai. Rendu vérifié dans un
navigateur réel à 1440 px : 52 communes dessinées, aucune commune manquante,
43 points, 650 tracés d'eau, cinq noms présents. Dessin 11,4 ms, noms 13,7 ms.

**Coût.** La page passe de 851 à 1014 ko : le sol pèse 163 ko. Ce dépassement
est assumé pour cette phase et doit être repris en phase 2 — le regroupement des
650 tracés d'eau et la suppression de leur recopie GeoJSON rendront davantage
que ce que le sol consomme.

**À juger par le porteur :** la capture à 1440 px, le ton du sol, la finesse des
limites communales, la taille des points, et la proportion du nouveau cadre.

**Non engagé dans cette phase :** la végétation, la hiérarchie de l'eau, le
traitement des liens, le mouvement. Aucune direction artistique.

---

## Phase 2 — Le dessin tenu par D3 (19 septembre 2026)

Phase sans effet visuel voulu : la carte doit être identique. Son objet est de
changer la façon dont elle est écrite, parce que les phases 3 et 4 en dépendent.

**Fait.**

- **La carte n'est plus effacée puis refaite à chaque geste.** Sa structure —
  sol, eau, relations, lieux — est posée une fois par ensemble ; chaque couche
  est ensuite mise à jour par D3, qui distingue ce qui entre, ce qui sort et ce
  qui reste. C'est la condition technique pour qu'un changement de métier puisse
  devenir un mouvement plutôt qu'un clignotement.
- **Un seul chemin de dessin.** La Risle était dessinée par un code, le
  département et Crulai par un autre ; les deux devaient être corrigés
  séparément. Il n'en reste qu'un, employé par les trois niveaux. C'est ce qui
  rend la Risle transposable aux onze autres ensembles.
- **L'eau est regroupée par catégorie** : deux tracés au lieu de six cent
  cinquante. Les identifiants des tronçons restent dans les données, où ils se
  vérifient ; ils n'ont jamais servi à l'affichage, l'eau n'étant pas
  interactive. Chaque tracé porte le nombre de tronçons qu'il réunit.
- **La recopie GeoJSON des tracés d'eau est supprimée.** Les mêmes données
  étaient transmises deux fois, sous deux formes. La forme GeoJSON attendue par
  D3 est désormais construite à l'affichage, à partir des données d'origine.

**Écart de comptage assumé et justifié.** Le nombre d'éléments de dessin de
l'eau passe de 650 à 2 pour la Risle et de 150 à 1 pour Crulai. Un contrôle qui
compterait les tracés dans la page verra donc un écart — il est voulu, et non
une perte. Les 650 tronçons restent intégralement présents : 254 principaux et
396 secondaires, vérifiés à l'écran par le nombre déclaré sur chaque tracé, soit
exactement les effectifs établis le 18 septembre. Crulai : 150 secondaires.

**Mesuré, avant → après :** éléments de dessin dans la carte 713 → 121 ;
dessin complet 11,4 → 6,3 ms ; page 1014 → 813 ko, soit sous les 851 ko d'avant
l'ajout du sol : le sol est payé.

**Contrôles effectués.** Six contrôles du générateur vrais, aucun écart.
`ruff` propre sur les outils. Syntaxe des deux scripts de la page vérifiée par
Node. Dans un navigateur réel, à 1440 px :

- Risle sans filtre : 52 communes, 2 tracés d'eau réunissant 254 + 396
  tronçons, 43 lieux, 5 relations.
- Filtre Métallurgie : 24 lieux, 4 relations — effectifs conformes. **Un point
  déjà présent avant le filtre est toujours le même élément après** : la preuve
  que la carte est mise à jour et non reconstruite.
- Retour à tous les métiers : 43 lieux, 5 relations, un seul groupe de repères
  et cinq noms — aucun empilement.
- Crulai : 7 lieux, un tracé d'eau réunissant 150 tronçons.
- Survol : l'étiquette apparaît avec les données réelles du lieu (« tréfilerie,
  Échauffour, Métallurgie et travail des métaux ») et disparaît à la sortie.
- Clavier : le focus pose son contour et l'étiquette ; Entrée ouvre la fiche ;
  Entrée sur une relation la sélectionne et ouvre son bloc de preuves.
- Zoom 3,38 : le point mesure toujours 7 à l'écran, le signe de localité 6 ;
  retour au cadrage initial exact.

**Reste ouvert.** Le mouvement lui-même — les transitions — n'est pas fait :
c'est la phase 4. Cette phase n'a fait que le rendre possible.

---

## Phase 3 — L'eau, les lieux, les liens (19 septembre 2026)

Réduite après la décision du porteur : la végétation en est retirée. Objet
restant, dans l'ordre de lecture d'une carte — d'abord le territoire, puis ce
qui s'y est implanté, puis ce qui relie.

**L'eau.** Chaque catégorie est désormais tracée deux fois : une gaine claire
qui la détache du sol, puis le trait. Toutes les gaines passent avant tous les
traits, sinon celle de la Risle effacerait ses propres affluents. La hiérarchie
est franchie : la rivière principale passe de 2,2 à 2,8 d'épaisseur et d'un bleu
moyen à un bleu plus profond ; les branches s'allègent de 1,3 à 1,2 et
s'éclaircissent. La Risle se distingue maintenant d'un coup d'œil de son réseau.

**Les lieux.** Le contour blanc passe de 1,4 à 1,9 : un point posé sur la
rivière ou sur une limite communale s'en détache au lieu de s'y fondre. Aucune
variation de taille selon les données n'a été introduite — faire varier un point
selon le nombre d'activités documentées reviendrait à faire lire une importance
que les sources n'établissent pas.

**Les liens.** Ils étaient des pointillés gris presque invisibles. Ils reçoivent
la même gaine claire que l'eau, passent de 1,6 à 2 d'épaisseur et d'un gris
neutre à un brun sombre. Le pointillé est conservé : une relation est établie
par une phrase, elle ne se mesure pas.

**Le sens des liens est affiché.** Les données disent lequel des deux lieux
travaillait pour l'autre, et le panneau l'affichait déjà ; la carte le taisait.
Une pointe est posée à 88 % de la courbe, orientée sur sa tangente, avant le
point d'arrivée pour ne pas le recouvrir. Elle garde sa taille d'écran au zoom,
comme les points et les noms. La légende l'explique : « lien établi par une
source, du premier lieu vers le second ».

**Les crédits disent enfin ce que le fond est.** Conformément à la décision
ci-dessus : le fond décrit la situation actuelle — cours d'eau, communes et
repères de bourg d'aujourd'hui — et non celle de la période industrielle ; les
biefs, canaux d'amenée et retenues de moulin qui faisaient tourner ces usines
ont disparu des relevés modernes et ne figurent pas sur la carte.

**Défaut corrigé au passage.** La légende de Crulai annonçait des liens alors
que Crulai n'en a aucun de documenté. Elle ne montre plus que des signes
réellement présents : « lieu industriel · cours d'eau » pour Crulai, la liste
complète pour la Risle. C'est un point de la passe 3 du suivi général.

**Contrôles effectués.** Six contrôles du générateur vrais, aucun écart.
`ruff` propre. Syntaxe JavaScript vérifiée par Node. Dans un navigateur réel,
à 1440 px :

- Risle : 4 éléments d'eau — deux gaines, deux traits — réunissant toujours
  254 tronçons principaux et 396 secondaires ; 43 lieux ; 5 liens, 5 gaines de
  lien et 5 pointes.
- Filtre Métallurgie : 24 lieux, 4 liens, 4 gaines, 4 pointes — la pointe suit
  son lien quand le filtre le retire.
- Retour à tous les métiers : 43 lieux, 5 liens, un seul groupe de repères.
- Crulai : 7 lieux, 150 tronçons secondaires, aucun lien, légende réduite.
- Sélection d'un lien au clavier : le lien passe en brun-rouge et sa pointe
  aussi ; le bloc de preuves s'ouvre.
- Zoom 5 : la pointe reste à taille d'écran constante et orientée juste.

**Poids :** 813 → 817 ko. La gaine et les pointes ne coûtent presque rien.

**Reste ouvert.** Le groupe dense de lieux autour de L'Aigle reste difficile à
viser : la lisibilité y gagne, le pointage non. Ce point était déjà réservé par
le suivi général ; il appelle une décision propre.

---

## Phase 4 — Le mouvement et l'approche (19 septembre 2026)

**Le mouvement.** Ce que la phase 2 avait rendu possible est fait. Un changement
de métier n'est plus un clignotement : les lieux qui entrent sortent de leur
point, ceux qui partent y rentrent, ceux qui restent glissent. Les liens, leurs
gaines et leurs pointes accompagnent les lieux qu'ils relient. Les commandes
« + », « − » et « Vue initiale » déplacent la carte au lieu de la faire sauter,
sur 420 millisecondes.

**La préférence système « moins d'animations » est respectée** : pour qui l'a
demandée, tout redevient instantané, sans perte de fonction. Vérifié dans le
code, non vérifié à l'écran faute de pouvoir changer ce réglage ici.

**L'approche.** En vue générale, la carte ne porte aucun nom d'usine : elle
reste sobre. Passé un zoom de 2,2, les lieux visibles à l'écran prennent leur
nom. Deux règles de sobriété : seuls les lieux réellement dans le cadre sont
nommés, et une étiquette qui recouvrirait un point ou une autre étiquette est
omise plutôt que superposée. Le lieu ouvert est servi en premier, puis de gauche
à droite, pour que l'ordre reste stable pendant le déplacement.

**Le décrochage des noms de bourgs est corrigé.** C'était le défaut ouvert
depuis la phase 0. Les noms quittent le groupe transformé par le zoom pour
vivre dans la couche de surface : leur position est celle de leur signe vue par
le zoom courant, plus un décalage constant à l'écran. Un nom dont le signe sort
du cadre est masqué. Le placement sans chevauchement reste calculé une seule
fois, au cadrage initial : le zoom ne le recalcule pas, ce qui aurait coûté
trop cher à chaque déplacement.

**Contrôles effectués.** Six contrôles du générateur vrais. Syntaxe JavaScript
vérifiée par Node. Dans un navigateur réel, à 1440 px :

- Les cinq noms de repères sont dans la couche de surface, aucun ne reste dans
  le groupe transformé.
- Seuil d'apparition : zoom 1,5 → aucun nom de lieu ; zoom 2,25 → 14 noms ;
  zoom 3,38 → 8 noms, le cadre contenant alors moins de lieux. Retour à la vue
  initiale → aucun nom.
- Distance d'un nom de bourg à son signe, de zoom 1 à zoom 1,5 : 40 → 40,
  51 → 51, 37 → 37, 22 → 22. Elle ne change plus. Seul
  Sainte-Gauburge-Sainte-Colombe passe de 20 à 50, son nom butant sur le bord
  du cadre — la garde de bord fait son travail plutôt que de le laisser sortir.
  À zoom 3,38 son signe quitte le cadre et son nom est masqué.
- Transition de filtre : 43 lieux encore présents 60 ms après le changement,
  24 lieux et 4 liens une fois la transition finie ; retour à 43 et 5.
- Parcours complet inchangé : survol, focus, Entrée vers la fiche, sélection
  d'une relation au clavier et ouverture de sa preuve, aller-retour
  département / Crulai / Risle, retour exact au cadrage initial.
- Crulai : 7 lieux, 150 tronçons secondaires, aucun nom de repère — ces repères
  restent propres à la Risle.

**Reste ouvert.** Le groupe dense de L'Aigle : en zoomant, les noms apparaissent
et se lisent, mais plusieurs points y restent sans nom faute de place, et viser
un point précis reste difficile. La difficulté a reculé, elle n'est pas résolue.

---

## Bloc A — La première impression (19 septembre 2026)

Premier bloc du plan actif, ouvert après la refonte du suivi. Objet : ce que
voit le lecteur qui arrive sur un ensemble.

**Le texte au-dessus de la carte est supprimé.** Décision du porteur, réaffirmée
après que la conservation d'une ligne courte a été proposée : ce texte ne sert
plus à rien. Les quatre lignes qui expliquaient ce qu'est un point, ce que
relient les traits et ce qu'un clic produit ont disparu, avec leur bloc et leur
style. Cette suppression rouvre en partie la décision du 14 août, qui avait posé
un mode d'emploi sur la page après qu'un lecteur n'avait pas compris ce qu'il
regardait ; le porteur a tranché en connaissance de cause.

**La légende quitte le dessus du cadre pour un cartouche dans la carte.** Elle
occupait une bande pleine largeur au-dessus de la carte, lue comme une ligne
technique. Elle est désormais dans un cartouche discret, posé dans le coin le
plus vide de la carte — mesuré à chaque rendu, pas réglé pour la Risle : une
autre vallée aura une autre diagonale et le cartouche ira ailleurs de lui-même.
Le coin haut-gauche est réservé aux commandes de zoom. Pour la Risle, le
cartouche choisit le bas-droite, qui est bien le coin libre.

**Une échelle est ajoutée**, dans le cartouche. Elle cherche la distance ronde
dont la barre approche une cible, recalculée à partir de la largeur réellement
affichée et du zoom courant : elle est donc juste à tout moment. La cible
s'adapte à la largeur de la carte, faute de quoi la barre occupait près de la
moitié d'une carte étroite.

**L'effet du filtre sort de la carte.** « Métallurgie et travail des métaux :
24 des 43 lieux » était posé en bas à gauche **sur** la carte : il couvrait le
territoire, tombait sur la partie basse de la vallée où il y a des points, et
faisait sauter la carte en apparaissant. Il se lit maintenant à droite du
sélecteur de métier — la cause et son effet côte à côte, au moment où le lecteur
s'y attend.

**Écran étroit, jamais vérifié jusqu'ici.** Deux défauts trouvés et corrigés :

- Le cartouche complet occupait 48 % de la carte à 380 pixels de large et 83 % à
  290. En dessous de 480 pixels il ne garde plus que l'échelle, et la légende
  descend sous la carte dans un bloc replié. Mesuré après correction : 6 % à
  380 pixels, 9 % à 290.
- Les points tombaient à 2,5 pixels de rayon sur une carte étroite, la carte
  s'étirant à la largeur disponible. Ils gardent désormais un rayon d'écran
  minimal de 5 pixels, sans rien changer sur écran large où le rayon naturel est
  déjà supérieur — 6,7 pixels à 952, inchangé.

**Contrôles effectués.** Six contrôles du générateur vrais. `ruff` propre.
Syntaxe JavaScript vérifiée par Node. Balise par balise, div ouvrants et
fermants équilibrés. Dans le navigateur, à quatre largeurs de carte — 952, 580,
380 et 290 pixels : cartouche jamais débordant, cinq noms de repères placés sans
chevauchement et aucun masqué, 43 lieux présents partout, échelle cohérente
(2 km à 952, 5 km en dessous, 20 km pour Crulai qui est plus resserré).
Département : cartouche masqué, bande de légende rétablie. Crulai : deux entrées
seulement, aucun lien annoncé.

**Incident de méthode à consigner.** En supprimant le style du texte retiré, une
coupe trop large a emporté environ soixante-dix lignes de CSS sans rapport —
cadre, commandes de zoom, annotation, fil d'ariane, panneau, filtres. Le défaut
a été vu immédiatement par comparaison avec la version enregistrée et réparé en
ne retirant que les règles visées, avec vérification de la présence de neuf
sélecteurs de contrôle. Rien n'a été perdu, mais la méthode — découper un
fichier entre deux repères textuels — est dangereuse et ne doit pas être
réemployée sans vérification immédiate.

**Correction d'un diagnostic erroné.** Il a d'abord été conclu que
l'observateur de redimensionnement ne se déclenchait pas faute d'être référencé.
La cause réelle est autre : **l'onglet de contrôle est passé en arrière-plan et
ne produisait plus aucune image** — zéro appel d'animation en une seconde,
`visibilityState` à `hidden`. Or la livraison des redimensionnements observés et
l'avancement des transitions dépendent toutes deux du cycle de rendu. Les deux
corrections apportées restent justes en elles-mêmes — un observateur sans
référence peut être ramassé par le navigateur, et l'observation porte désormais
sur le cadre plutôt que sur l'élément SVG — mais elles ne répondaient pas au
symptôme observé.

**Les crédits dépassaient la carte.** Mesure : à 380 pixels de carte, le bloc
des sources occupait 101 % de sa hauteur ; à 290 pixels, 173 % — près du double
de la carte qu'il documente. Sous 480 pixels, seule la ligne des sources reste
visible et les précisions passent dans un bloc replié. Rien n'est retiré, tout
reste atteignable. Après correction : 33 % à 380 pixels, 43 % à 290.

**Reprise des mesures, onglet toujours en arrière-plan.** Le porteur a remis la
fenêtre au premier plan ; la page continue de se déclarer masquée et de ne
produire aucune image. Les parcours dépendant d'une animation ont donc été
éprouvés autrement, sans transition :

- Zoom par commande, sans transition : 1,5 puis 2,25 puis 3,38, retour exact au
  cadrage initial et au `viewBox` 1000 × 462. Noms de lieux : aucun à 1,5,
  quatorze à 2,25, huit à 3,38. Échelle : 2 km à zoom 1, 1 km au-delà de 2,25.
  Point et signe de localité constants à 7 et 6 pixels d'écran à tous les zooms.
- Filtre Métallurgie : la mise à jour retient exactement **24 cercles sur 43**
  et **4 liens sur 5**, vérifié sur les données liées à chaque élément. Les 19
  cercles sortants restent dans la page faute d'images pour achever leur
  disparition — leur sélection est juste, leur retrait attend le rendu.

**Non vérifié, et il faut le savoir :**

- Le déclenchement automatique au redimensionnement de la fenêtre. La logique
  est juste — appelée directement, elle produit le bon résultat à toutes les
  largeurs — mais son déclencheur n'a pas pu être éprouvé, l'onglet ne
  produisant plus d'images. À reprendre avec une fenêtre au premier plan.
- Les transitions et le zoom n'ont pas pu être re-mesurés dans cette passe pour
  la même raison. Ils l'avaient été plus tôt dans la session, onglet visible :
  43 lieux pendant la transition puis 24 après, zoom à 1,5 puis 2,25 puis 3,38
  et retour exact.
- Le lecteur qui **arrive** sur un écran étroit reçoit la bonne mise en page
  sans dépendre de l'observateur : ce chemin-là est vérifié.

**Reste du bloc A :** la vérification dans une vraie fenêtre étroite, et le
jugement du porteur.

---

## Bloc B — Lire les liens d'un lieu (19 septembre 2026)

Engagé après un malentendu levé par le porteur : le bloc B reste au niveau de
l'ensemble. Quand un lieu s'ouvre, la carte ne change pas de niveau ni de
cadrage — elle reste la carte de la vallée, et c'est ce qu'elle fait à ce
moment-là qui est en jeu.

**Un lieu ouvert montre avec qui il travaillait.** Ses partenaires reçoivent un
anneau, les liens qui y mènent passent en trait plein et en couleur d'appui,
leurs pointes avec eux. Rien n'est atténué : la décision d'architecture interdit
d'affaiblir le reste, on renforce donc ce qui est lié. Quitter le lieu rétablit
l'état normal.

L'anneau est posé directement, hors animation : une désignation ne doit pas
dépendre d'un mouvement pour exister. Les libellés accessibles suivent — un
partenaire annonce « Lieu lié au lieu ouvert », le lieu ouvert annonce « Fiche
ouverte » au lieu de proposer de l'ouvrir.

**Vérifié sur deux lieux** : deux partenaires attendus, deux anneaux posés sur
les bons lieux, deux liens et deux pointes en avant ; puis trois attendus, trois
anneaux, trois liens, trois pointes. Cadrage inchangé à l'ouverture comme au
retour, conformément à l'arbitrage du 18 septembre. Retour à l'ensemble : plus
aucun anneau ni lien en avant.

### Le groupe dense de L'Aigle

**Aucun point n'est déplacé.** L'invariant l'interdit, et une carte qui écarte
ses lieux pour la commodité du pointage ment sur leur position. C'est la cible
qui s'élargit : un survol ou un clic désigne le lieu dont le centre est le plus
proche du curseur, dans une portée de 18 pixels, par un arbre de recherche
reconstruit à chaque rendu.

**Conséquence sur les gestes.** Le survol et le clic passent désormais par la
carte et non par chaque point. Sans cela le navigateur désignait le cercle du
dessus, c'est-à-dire le dernier dessiné, et non le plus proche du curseur —
précisément le défaut à corriger. Les points gardent leur accès clavier complet :
tabulation, contour de focus, étiquette d'identification et ouverture par Entrée.
Un clic sur un lien garde son comportement propre et ouvre sa preuve. Un
glissement de carte n'ouvre rien, la distance de clic étant contrôlée. Un clic
dans le vide, loin de tout lieu, n'ouvre rien non plus.

**La limite qui subsiste, chiffrée.** La difficulté n'est pas la désignation,
elle est la densité elle-même. Nombre de paires de lieux séparées de moins de
huit pixels à l'écran, donc impossibles à distinguer au doigt ou à la souris :

| Zoom | Paires indistinguables |
| --- | --- |
| 1 | 13 |
| 2 | 4 |
| 4 | 1 |
| 6 | 0 |

La paire la plus serrée — une filature et une usine de quincaillerie — est à
1,6 pixel à l'ouverture, et à 9,6 pixels au zoom maximal. Aucune coordonnée
n'est dupliquée : ce sont bien des lieux distincts, très proches. **Le zoom est
donc la réponse à cette densité, et il existe.** La liste du panneau reste
l'autre chemin, complet et ordonné, pour atteindre un lieu sans viser.

**Contrôles effectués.** Six contrôles du générateur vrais, `ruff` propre,
syntaxe JavaScript vérifiée par Node. Dans le navigateur : viser douze pixels à
côté d'un lieu isolé l'ouvre ; cliquer loin de tout n'ouvre rien ; les quinze
lieux du groupe de L'Aigle sont désignés chacun par le leur ; le focus clavier
affiche l'étiquette et Entrée ouvre la fiche ; un clic sur un lien sélectionne
le lien et ouvre sa preuve sans ouvrir de lieu.

**Non vérifié :** le toucher sur un appareil réel. Le clic passant désormais par
la carte, un appui tactile emprunte le même chemin que la souris, mais cela n'a
pas été éprouvé sur un appareil.

---

## Bloc C — Juger et transposer (19 septembre 2026)

Objet : savoir si la Risle est devenue un modèle ou reste une exception, et à
quel prix s'ouvre un ensemble de plus.

### Plus aucune ligne de code ne nomme la Risle

Le code réservait encore à cette vallée l'identification au survol, le zoom et
les noms de lieux à l'approche. Ces comportements ne lisent que des données
présentes pour les douze ensembles : rien ne justifiait la réserve. Les gardes
nommant `"risle"` sont supprimées, les fonctions et variables du zoom renommées
— elles décrivent la carte, pas une vallée — et la présence de repères de bourg
se lit désormais dans les données, jamais dans un nom. Un ensemble qui recevra
un jour des repères les affichera sans changement de code.

### Les deux ensembles côte à côte

| | Risle | Crulai |
| --- | --- | --- |
| Lieux, relations | 43 et 5 | 7 et 0 |
| Identification au survol | 5 lieux sur 5 justes | 5 sur 5 |
| Zoom et commandes | oui | oui |
| Noms de lieux au zoom 2,5 | 11 | 2 |
| Coin du cartouche | bas-droite | **haut-droite** |
| Entrées de légende | 5 | 2 |
| Échelle | 1 km | 500 m |
| Proportion du cadre | 1000 × 462 | 1000 × 620 |
| Repères de bourg | 4 | 0 |

Les différences sont toutes des conséquences des données, pas du code. Le
cartouche choisit un autre coin parce que Crulai n'a pas la même forme ; le
cadre prend une autre proportion pour la même raison ; l'échelle est deux fois
plus fine parce que l'emprise est plus petite ; la légende n'annonce ni rivière
principale ni relations parce que Crulai n'en a pas. **La seule différence de
fond est l'absence de repères de bourg**, qui est un manque de données et non un
manque de code.

### Le prix d'un ensemble de plus, mesuré

Sonde sur trois ensembles supplémentaires — Noireau, Flers, Argentan — sans rien
écrire ni publier :

| Ensemble | Lieux | Liens | Tracés d'eau | Communes du sol | Poids |
| --- | --- | --- | --- | --- | --- |
| Risle | 43 | 5 | 650 | 52 | 373 ko |
| Crulai | 7 | 0 | 150 | 20 | 98 ko |
| Noireau | 23 | 1 | 710 | 28 | 297 ko |
| Flers | 21 | 1 | 285 | 30 | 192 ko |
| Argentan | 7 | 0 | 365 | 28 | 168 ko |

**Ce qui est gratuit.** Les lieux, les relations, l'eau, le sol, la chronologie
et les chiffres du panneau se calculent sans intervention. Ouvrir un ensemble de
plus est, pour ces éléments, une ligne à ajouter au générateur.

**Ce qui coûte.** Deux choses.

*Le poids.* La page pèse 817 ko avec deux ensembles. Chaque ensemble
supplémentaire ajoute de 170 à 300 ko. Les douze porteraient la page à environ
**trois mégaoctets**. C'est tenable sur un poste de travail, lourd sur un
téléphone. La page entièrement autonome, sans chargement distant, ne tient pas
à douze ensembles : il faudra choisir entre l'autonomie et le poids. **Ce point
n'est pas tranché et sort du présent plan.**

*Les noms de communes.* Trois communes portées par des lieux n'ont pas de
contour dans les données actuelles : Athis-de-l'Orne et Frênes pour le Noireau,
Goulet pour Argentan. Les lieux portent le nom de commune de leur source
historique, tandis que les contours décrivent les communes d'aujourd'hui, où ces
trois-là ont fusionné. Le contrôle `sol_complet` ajouté au bloc A **fait échouer
la génération** dans ce cas : il fonctionne, et il faudra une table de
correspondance entre noms anciens et communes actuelles avant d'ouvrir ces deux
ensembles. C'est le premier vrai travail de données que la suite demande.

*Les repères de bourg.* Aucun des dix autres ensembles n'en a. Chacun demande de
retrouver l'adresse de la mairie dans l'annuaire officiel, de la faire géocoder
par le service de l'IGN en contraignant la commune, puis de trancher les cas où
le géocodeur ne trouve pas le numéro exact — ce qui s'est produit pour
Sainte-Gauburge. C'est un travail de vérification de sources, non automatisable,
et le choix des bourgs utiles relève du jugement éditorial. **Non engagé.**

### Contrôles effectués

Six contrôles du générateur vrais. `ruff` propre. Syntaxe JavaScript vérifiée
par Node. Dans le navigateur, sur les deux ensembles : survol juste cinq fois
sur cinq, zoom appliqué et retour exact au cadrage initial, commandes présentes,
noms de lieux apparaissant à l'approche, cartouche et échelle adaptés.

**Reste ouvert :** le jugement visuel du porteur sur le parcours complet, la
décision sur le poids de la page à douze ensembles, la table des communes
anciennes, et les repères de bourg.

---

## D1 — Le dessin du département tenu par D3 (19 septembre 2026)

Branche `codex/carte-departement-d3`. Premier temps du bloc D : supprimer le
second moteur de dessin. Aucun effet visible attendu.

**Fait.** La carte du département était effacée puis reconstruite à chaque
geste, élément par élément. Elle a désormais ses couches — contour, lieux hors
ensembles, ensembles — posées une fois et mises à jour par jointure, comme la
carte d'un ensemble. Les couches sont devenues paramétrables : chaque niveau
déclare les siennes, le mécanisme est commun.

Les noms d'ensembles passent dans la couche de surface, ancrés à leur bulle par
un décalage constant — la règle établie pour les repères de bourg. Le placement
qui leur était propre est remplacé par la grille d'occupation éprouvée sur les
ensembles. Le positionnement des noms ancrés devient une fonction commune aux
deux niveaux.

**Deux défauts corrigés au passage**, trouvés en mesurant les boîtes de texte :

- deux noms tombaient sur une bulle d'ensemble et deux paires se chevauchaient.
  Quatre positions candidates ne suffisaient pas dans le nord-ouest, où les
  ensembles se serrent ; il y en a vingt-quatre — huit directions à trois
  distances.
- les noms étaient servis du plus gros ensemble au plus petit, si bien que le
  nom le plus long arrivait en dernier et ne trouvait plus de place. Ils sont
  servis du plus long au plus court, règle déjà éprouvée sur les repères de
  bourg. « Bassin de Halouze · 13 » affichait « · 1 », son chiffre étant
  recouvert : il est lisible.

Les lieux hors ensembles gardent une taille d'écran minimale, comme ceux d'un
ensemble : à 2,6 unités ils disparaissaient sur écran étroit.

**Contrôles effectués.** Six contrôles du générateur vrais, `ruff` propre,
syntaxe JavaScript vérifiée par Node. Dans le navigateur :

- Sans filtre : 1 contour, 146 lieux hors ensembles, 12 bulles, 12 cibles
  cliquables, 12 noms. Éléments de dessin : 192.
- Sous Métallurgie, en lisant les données liées à chaque élément : 26 lieux hors
  ensembles retenus sur 26 attendus, 10 ensembles sur 10, 10 cibles, 10 noms.
  **Un élément présent avant le filtre est toujours le même après** : la carte
  est mise à jour, non reconstruite.
- Retour à tous les métiers : 12 ensembles, 12 noms, aucun empilement.
- Boîtes de texte mesurées sans filtre et sous trois métiers : aucun nom sur une
  bulle, aucun hors cadre.

**Limite qui subsiste.** Sans filtre, « Vallée du Noireau · 23 » et
« Flers · 21 » se touchent encore : deux ensembles voisins et importants dans le
coin le plus dense. Les deux restent entièrement lisibles et aucun n'est masqué.
Sous filtre, plus aucun chevauchement. Le remède — un trait de rappel entre un
nom éloigné et sa bulle — relève de la passe de présentation, pas de celle-ci.

**Incident de méthode.** Une première tentative a supprimé, en retirant
l'ancienne fonction, les déclarations partagées qui la suivaient dans le
fichier — bornes de découpe mal choisies. Le fichier a été restitué depuis la
version enregistrée et le travail refait en plaçant la fonction après ses
dépendances. Rien n'a été perdu ; c'est la deuxième fois dans la journée qu'un
découpage par repères textuels se révèle dangereux.

**Reste ouvert :** la validation du porteur. D2 apportera l'identification au
survol, le pointage du plus proche, le zoom et le cartouche.

---

## D2 — Donner au département ce que l'ensemble a déjà (19 septembre 2026)

**Une source unique de ce qui se désigne.** Chaque niveau déclare ses entités :
au département, les douze ensembles et les cent quarante-six lieux hors
ensembles — 158 en tout ; dans un ensemble, ses lieux. Chaque entité porte ses
lignes d'identification et dit si elle s'ouvre. L'étiquette de survol, l'arbre
de recherche du plus proche et les noms au zoom lisent tous cette même source.

**L'identification au survol existe au département.** Les douze bulles et les
cent quarante-six points gris ne disaient rien ; ils disent maintenant quelque
chose de vrai :

- sur une bulle : « Vallée de la Risle · 43 lieux recensés · Ouvrir cet
  ensemble », ou « Vue détaillée à venir » pour les dix ensembles non ouverts ;
- sur un point gris : « distillerie, cidrerie · Anceins · Agroalimentaire ».

**Le pointage du plus proche vaut aussi au département**, sans déplacer aucun
point. Un clic près d'une bulle ouvre son ensemble ; un clic près d'un lieu hors
ensemble n'ouvre rien, puisqu'il n'y a rien à ouvrir — et cela se lit dans
l'étiquette avant le clic.

**Le zoom et les commandes sont actifs.** Bulles, points gris et cibles
cliquables gardent leur taille d'écran : une bulle mesure 23 pixels à zoom 1
comme à zoom 2,5. Retour exact au cadrage initial.

**Les noms apparaissent en s'approchant.** Au-delà du seuil, les lieux hors
ensembles prennent leur nom — 42 à zoom 2,5 — tandis que les ensembles gardent
le leur en permanence. Le nombre d'étiquettes est borné à soixante, la carte du
département portant bien plus de lieux qu'un ensemble.

**Le cartouche remplace la bande de légende.** Il choisit son coin d'après le
contour départemental : **bas-gauche**, là où les ensembles choisissent
bas-droite. Trois entrées au lieu de cinq, et l'échelle du département.

**Un défaut ancien corrigé, qui touchait aussi les ensembles.** Le cartouche
était posé pendant le rendu de la légende, c'est-à-dire **avant** que la carte
soit dessinée — donc avant que l'échelle de projection de la vue affichée soit
connue. Au premier affichage d'une vue, la barre d'échelle manquait, ou pire,
reprenait celle de la vue précédente. Crulai annonçait ainsi 500 mètres au lieu
d'un kilomètre. Le cartouche est désormais posé après le dessin.

**Contrôles effectués.** Six contrôles du générateur vrais, `ruff` propre,
syntaxe JavaScript vérifiée par Node. Dans le navigateur :

| Vue | Coin du cartouche | Entrées | Échelle | Entités |
| --- | --- | --- | --- | --- |
| Département | bas-gauche | 3 | 20 km | 158 |
| Risle | bas-droite | 5 | 2 km | 43 |
| Crulai | bas-droite | 2 | 1 km | 7 |

Zoom 2,5 au département : échelle passée à 10 km, 42 noms de lieux apparus,
bulle constante à 23 pixels d'écran, retour exact. Quatre largeurs de carte —
952, 580, 380 et 290 pixels : le cartouche occupe de 6 à 17 % de la carte, se
réduit sous 480 pixels et la légende descend sous la carte ; les crédits restent
sous la hauteur de la carte ; les douze noms d'ensembles sont présents partout.

**Limite qui subsiste.** « Vallée du Noireau » et « Flers » se touchent à toutes
les largeurs, sans filtre. Les deux restent lisibles. C'est la même limite que
D1 ; elle appelle un trait de rappel, qui relève de la présentation.

**Reste ouvert :** la validation du porteur, et D3 — le passage du département à
un ensemble comme descente d'échelle.

---

## D3 — Le passage du département à un ensemble (19 septembre 2026)

**Le comportement examiné.** Ouvrir un ensemble remplaçait une carte par une
autre, d'un coup. Rien ne reliait ce que le lecteur quittait à ce qu'il ouvrait :
il changeait d'écran, il ne descendait pas dans un territoire.

**La descente d'échelle.** La carte du département s'approche désormais de la
bulle visée, puis celle de l'ensemble arrive de plus près et se pose sur son
cadrage. Le retour remonte symétriquement : le département repart de la bulle
que l'on quitte et s'élargit. Cela vaut quel que soit le chemin — clic sur la
bulle, touche Entrée depuis la carte, ou bouton de la liste du panneau.

**Trois garanties, parce qu'une animation ne doit jamais retenir un lecteur.**

- La préférence système « moins d'animations » rend le passage instantané, sans
  rien perdre.
- Une minuterie de sécurité achève toujours la navigation : si le navigateur ne
  produit pas d'images — onglet en arrière-plan — la transition n'aboutirait
  jamais et le lecteur resterait bloqué sur la carte de départ.
- Le retour au cadrage initial est **garanti, pas seulement demandé**. Sans
  cela, une transition interrompue laissait la carte agrandie sans que le
  lecteur l'ait voulu. Un geste de zoom volontaire annule ce repos en attente ;
  et le repos est également posé au retour de la page à l'écran, seul moment où
  un état resté agrandi commencerait à se voir.

**Contrôles effectués.** Six contrôles du générateur vrais, `ruff` propre,
syntaxe JavaScript vérifiée par Node. Dans le navigateur, en suivant le facteur
de zoom dans le temps :

- Descente vers la Risle : 1 → 2,40 → 1, puis stable. 43 lieux, cadre 1000 × 462.
- Remontée vers le département : 5 → 1, puis stable. 12 ensembles, 12 noms.
- Entrée au clavier depuis une bulle : arrive dans la Risle, 43 lieux.
- Entrée par la liste du panneau : arrive dans Crulai, 7 lieux.
- Ensemble non ouvert : la carte ne descend pas, et l'annonce le dit.
- Sous filtre Métallurgie : la descente conserve le filtre — 24 lieux retenus
  dans la Risle, 10 ensembles au retour.

**Constat qui n'était pas prévu et qu'il faut signaler.** La case demandait de
« préserver l'état partageable après le `#` ». **Cet état n'existe pas.** Le
prototype ne lit ni n'écrit aucune adresse : on ne peut donc pas partager un lien
vers un ensemble ou un lieu, et recharger la page ramène toujours au département.
C'est un écart avec une décision d'architecture arrêtée. Rien n'a été cassé par
D3 ; il n'y avait rien à préserver. Ce point appelle un travail à lui seul, hors
du bloc D.

**Correction de réception — la descente se jouait deux fois.** Le porteur a
signalé que l'ouverture d'un ensemble rejouait son animation une demi-seconde
plus tard, sur les deux ensembles ouverts. Cause : au département, la bulle
gardait son propre gestionnaire de clic **et** le clic remontait ensuite à la
carte, qui le traitait une seconde fois par la recherche du plus proche —
conséquence non vue de D2, qui avait fait passer le clic par la carte. Deux
appels, deux descentes.

Le gestionnaire de la bulle est retiré : le clic est traité une seule fois, au
niveau de la carte, comme pour les lieux d'un ensemble depuis le bloc B. Le
clavier garde son chemin propre. Un verrou de navigation est ajouté en second
filet : une descente déjà lancée ne se relance pas, quel que soit le geste.

Vérifié après correction, en comptant les appels réels : clic sur une bulle, une
seule ouverture ; touche Entrée, une seule ; bouton de la liste du panneau, une
seule. Les commandes de retour sont hors de la carte et n'ont pas ce risque.

**Seconde correction de réception — la descente restait fautive.** Après le
retrait du double clic, le porteur a constaté que le défaut subsistait et
s'aggravait : une trace parasite sur la Risle, et surtout un ensemble arrivant
démesurément réduit sur Crulai, points minuscules, carte inutilisable. Deux
causes, toutes deux dans la descente.

*La transition de départ n'était jamais coupée.* Quand la navigation s'achevait
par la minuterie de sécurité, l'animation du département continuait de tourner
et appliquait son zoom — calculé sur son cadre et ses coordonnées — à la carte
de l'ensemble qui venait d'apparaître. La vue sautait puis dérivait.

*La hauteur du cadre était celle de la vue quittée.* L'arrivée était calculée
avant le rendu de la nouvelle carte, alors que la hauteur du cadre change d'une
vue à l'autre : 520 au département, 462 sur la Risle, 620 sur Crulai. Le point
visé tombait à côté, et l'écart était le plus grand pour Crulai — ce qui
explique que ce soit là que le défaut était le pire.

Corrigé : la transition de départ est coupée avant toute chose, et l'arrivée
n'est calculée qu'après le rendu de la nouvelle vue. Le retour coupe également
toute transition en cours.

Vérifié après correction, dans le navigateur : Crulai arrive en 1000 × 620 avec
une transformation neutre, 7 lieux au rayon normal ; la Risle en 1000 × 462,
transformation neutre, 43 lieux, 5 liens, 4 tracés d'eau, 5 noms de repères,
échelle 2 km, et **aucun résidu de la couche départementale** — ni bulle, ni
point gris. Le retour au département revient en 1000 × 520, transformation
neutre, 12 bulles et 146 lieux.

**Reste ouvert :** la validation du porteur, et D4 — la vérification d'ensemble
aux trois niveaux, clavier et tactile compris.

---

## D4 — Vérification d'ensemble (19 septembre 2026)

Bloc de vérification : mesurer, ne pas ajouter. Deux défauts ont pourtant été
trouvés et corrigés, tous deux hérités de D2.

**Défaut 1 — un lieu masqué par le filtre restait désignable.** Sous Métallurgie,
la Risle dessinait 24 points mais déclarait 43 entités : survoler l'emplacement
d'un lieu masqué le nommait — « abattoir · L'Aigle · Agroalimentaire » — alors
que son point n'était pas à l'écran. Le filtre n'était pas appliqué à la source
commune des entités désignables. Il l'est désormais : 24 entités pour 24 points,
et survoler cet emplacement désigne le lieu visible le plus proche.

Le département n'était pas touché : ses entités étaient déjà filtrées. C'est
cette différence entre les deux niveaux qui a fait voir le défaut.

**Défaut 2 — le clavier perdait l'étiquette au département.** Le focus sur une
bulle posait son contour et annonçait son libellé, mais n'affichait pas
l'étiquette d'identification que le survol donne à la souris. Les lieux d'un
ensemble l'avaient, les ensembles non. Corrigé : le focus d'une bulle affiche la
même étiquette, y compris pour les dix ensembles non ouverts, qui annoncent
« Vue détaillée à venir ».

### Parcours vérifiés

| Vue | Entités | Dessiné | Cartouche | Échelle |
| --- | --- | --- | --- | --- |
| Département | 158 | 12 bulles, 146 lieux | bas-gauche, 3 entrées | 20 km |
| Département sous Métallurgie | 36 | 10 bulles, 26 lieux | bas-gauche | 20 km |
| Risle | 43 | 43 lieux, 5 liens, 4 tracés d'eau | bas-droite, 5 entrées | 2 km |
| Risle sous Métallurgie | 24 | 24 lieux, 4 liens | bas-droite | 2 km |
| Lieu ouvert | 43 | cadrage inchangé | bas-droite | 2 km |
| Crulai | 7 | 7 lieux, 0 lien | bas-droite, 2 entrées | 1 km |

**Clavier.** Au département, douze cibles atteignables ; dans un ensemble,
quarante-huit. Le focus pose son contour et son étiquette, Entrée ouvre, Espace
sur une relation la sélectionne et ouvre sa preuve, Entrée sur un lieu ouvre sa
fiche. Les libellés annoncent ce qui va se passer, y compris l'indisponibilité.

**Tactile.** Un appui — événements de pointeur de type `touch` — ouvre un
ensemble comme un clic. Le chemin est le même depuis le bloc B, où le clic est
passé au niveau de la carte. Essai simulé, non éprouvé sur un appareil réel.

**Écran étroit, aux trois niveaux.** À 380 et 290 pixels de carte : le cartouche
occupe de 6 à 10 % de la carte, ne déborde jamais, se réduit à l'échelle seule,
et la légende descend sous la carte. Les crédits restent sous la hauteur de la
carte. L'échelle s'adapte — 50 km au département, 5 km sur la Risle, 2 km sur
Crulai. Aucun débordement horizontal de la page. Les cinq noms de repères de la
Risle sont présents, Crulai n'en a toujours aucun.

### Les règles devenues communes aux trois niveaux

Elles ne sont plus propres à une vue : elles décrivent la carte.

1. Un seul chemin de dessin. Les couches sont posées une fois par vue et mises à
   jour ; rien n'est effacé tant qu'on ne change pas de vue.
2. Le cadre prend la proportion de ce qu'il montre.
3. Les signes gardent leur taille d'écran, au zoom comme au redimensionnement.
4. Ce qui ne doit pas grossir vit dans la couche non transformée ; un nom y est
   ancré à son signe par un décalage constant et se masque avec lui.
5. Une source unique déclare ce qui se désigne, et le filtre s'y applique comme
   au dessin. Le survol et le clic passent par elle, jamais par le signe dessiné
   en dernier. Aucun point n'est déplacé pour faciliter le pointage.
6. Le clavier obtient ce que la souris obtient : même étiquette, même contour,
   même ouverture.
7. La légende et l'échelle vivent dans un cartouche posé dans le coin le plus
   vide, mesuré à chaque rendu ; la légende ne montre que des signes présents.
8. Sous 480 pixels de carte, le cartouche se réduit à l'échelle, la légende et
   les précisions de crédits descendent sous la carte, repliées.
9. Toute animation cesse si le lecteur a demandé moins de mouvement ; et aucune
   animation ne peut retenir un lecteur — navigation et retour au cadrage sont
   garantis indépendamment des images produites.

### Ce qui reste ouvert

- **La validation du porteur**, sur les quatre sous-blocs.
- **L'état partageable après le `#`** : il n'existe pas. Écart avec une décision
  d'architecture, à traiter à part.
- **Le tactile sur un appareil réel**, jamais éprouvé.
- **« Vallée du Noireau » et « Flers »** se touchent encore au département, sans
  filtre. Les deux restent lisibles.
- **Le poids à douze ensembles** et **les communes d'archive sans contour**,
  tous deux hors du bloc D.

---

## Ce qui est déjà identifié comme règle transposable

À reprendre pour les onze autres ensembles.

- Le cadre prend la proportion de ce qu'il montre, entre deux bornes.
- Le sol couvre tout le cadre et déborde, jamais les seules communes de
  l'ensemble.
- Les signes qui ne doivent pas grossir au zoom vivent dans une couche non
  transformée, ou sont compensés par le facteur de zoom.
- Un seul chemin de dessin pour les trois niveaux : département, ensemble, lieu.
  Un ensemble traité en exception ne peut pas servir de modèle aux autres.
- Les couches se posent une fois et se mettent à jour ; la carte ne s'efface
  qu'en changeant d'ensemble.
- Les tracés d'eau se regroupent par catégorie pour l'affichage ; les
  identifiants se vérifient dans les données, pas dans la page.
- Une gaine claire sous l'eau et sous les liens les détache du sol. Toutes les
  gaines avant tous les traits.
- La légende ne montre que des signes réellement présents dans l'ensemble
  affiché.
- Aucun signe ne varie de taille selon une donnée qui n'établit pas ce qu'il
  ferait lire.
- Le sens d'un lien est porté par une pointe orientée sur la tangente de sa
  courbe, à taille d'écran constante.
- Les crédits disent que le fond est contemporain et nomment ce qui en est
  absent.
- Un nom vit dans la couche de surface, ancré à son signe par un décalage
  constant à l'écran ; il est masqué quand son signe quitte le cadre.
- Les noms de lieux n'apparaissent qu'au-delà d'un seuil de zoom, seulement
  pour les lieux réellement dans le cadre, et une étiquette qui en
  recouvrirait une autre est omise plutôt que superposée.
- Toute animation cesse si le lecteur a demandé moins de mouvement.

## Ce qui est propre à la Risle

- La hiérarchie rivière principale / branches secondaires : les données ne
  désignent aucun cours d'eau principal à Crulai. Cette règle ne se transpose
  pas telle quelle.
- Les quatre bourgs repères et le nom « La Risle » : vérifiés un par un, à
  refaire pour chaque ensemble.
