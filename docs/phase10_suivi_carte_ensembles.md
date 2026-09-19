# Carte des ensembles — Plan et suivi des passes

## Le socle technique est acquis — 19 septembre 2026

Le plan d'expérimentation D3 qui occupait cette place avait un seul objet :
faire fonctionner D3 dans la carte. C'est fait. Ses sept phases décrivaient le
chemin pour y parvenir ; elles n'ont plus d'objet comme plan et sont versées à
l'historique du document. **La carte telle qu'elle est aujourd'hui est la
référence.**

Ce qui est acquis, et qui ne se rediscute pas sans passer par le journal :

- D3 est embarqué localement, sans appel distant, et **tient le dessin** de la
  carte. Un seul chemin de dessin sert les trois niveaux — département,
  ensemble, lieu. La Risle n'est plus une exception : c'est le cas général.
- Les couches sont posées une fois par ensemble puis mises à jour. Un
  changement de métier est un mouvement, pas un clignotement.
- Le cadre prend la proportion de ce qu'il montre. Le sol est formé de toutes
  les communes touchant le cadre, et déborde.
- L'eau est hiérarchisée et détachée du sol par une gaine ; les liens sont
  lisibles et portent leur sens ; les lieux se détachent du fond.
- Zoom et déplacement bornés, avec retour exact au cadrage initial. Les noms de
  repères suivent leur signe. Passé un zoom de 2,2, les lieux prennent leur nom
  sans se recouvrir. Toute animation cesse si le lecteur a demandé moins de
  mouvement.
- La végétation contemporaine est écartée par décision du 19 septembre.

Le détail de ces travaux, leurs mesures et leurs limites sont dans
`docs/audit_carte_d3/journal_phases_carte.md`. Les décisions correspondantes
sont au journal, à la date du 19 septembre.

## Ce qui reste — plan actif

Quatre blocs. Les trois premiers portent sur la carte d'un ensemble ; le
quatrième, ouvert le 19 septembre, aligne la carte du département sur ce qui a
été établi là.

### BLOC A — La première impression — faite, en attente de jugement

**Question à juger :** en arrivant sur un ensemble, le lecteur comprend-il ce
qu'il regarde sans avoir à lire un paragraphe ?

- [x] **Supprimer** le texte au-dessus de la carte. Une consigne courte avait
  été proposée à la place ; le porteur a tranché pour la suppression complète,
  ce texte ne servant plus à rien.
- [x] Sortir la légende du dessus du cadre : elle est dans un cartouche posé
  dans le coin le plus vide de la carte, choisi à chaque rendu.
- [x] Ajouter une échelle calculée, adaptée à la largeur affichée et au zoom
  courant.
- [x] Sortir de la carte l'effet du filtre métier, qui couvrait le territoire ;
  il se lit à côté du sélecteur.
- [-] Vérifier la lisibilité sur écran étroit. Vérifiée à quatre largeurs de
  carte par contrainte de la largeur du conteneur ; **pas dans une vraie fenêtre
  étroite**, l'onglet de contrôle ne produisant plus d'images.
- [x] Vérifier que les crédits et les sources restent lisibles sans occuper plus
  de place que la carte.
- [ ] Validation du porteur.

**Livrable :** un écran d'ensemble qui se comprend d'un coup d'œil, sur écran
large et sur écran étroit.

**Acquis à conserver :** le fond est déjà teinté par le sol communal — ce point
du plan précédent est fait. La légende ne montre déjà que des signes réellement
présents.

**Bilan du bloc A — 19 septembre 2026.** Réalisation faite et mesurée dans un
navigateur ; détail, chiffres et limites dans
`docs/audit_carte_d3/journal_phases_carte.md`. Deux défauts d'écran étroit
trouvés et corrigés : le cartouche occupait jusqu'à 83 % de la carte, ramené à
9 % ; les crédits occupaient jusqu'à 173 % de sa hauteur, ramenés à 43 % par un
repli. Deux autres défauts trouvés au passage et corrigés : les points tombaient
à 2,5 pixels de rayon sur carte étroite, ils gardent désormais 5 pixels
minimum ; l'observateur de largeur n'était pas retenu et portait sur l'élément
SVG. La validation du porteur reste ouverte, ainsi que l'essai dans une vraie
fenêtre étroite.

### BLOC B — Lire les liens d'un lieu — fait, en attente de jugement

**Question à juger :** quand un lieu est ouvert, voit-on avec qui il
travaillait ?

- [x] Ouvrir un lieu met en évidence les lieux liés et les traits qui y mènent ;
  quitter le lieu rétablit l'état normal. Rien n'est atténué : ce qui est lié
  est renforcé.
- [x] Accès aux preuves inchangé : un clic sur un lien le sélectionne et ouvre
  sa phrase justificative, sans ouvrir de lieu.
- [x] Traiter le groupe dense autour de L'Aigle : la cible s'élargit, aucun
  point n'est déplacé. Le survol et le clic désignent le lieu le plus proche du
  curseur au lieu du cercle dessiné en dernier.
- [-] La densité elle-même subsiste à faible zoom : 13 paires de lieux sont à
  moins de huit pixels l'une de l'autre à l'ouverture, 4 au zoom 2, une seule au
  zoom 4, aucune au zoom 6. Le zoom est la réponse ; la liste du panneau est
  l'autre chemin.
- [ ] Validation du porteur.

**Livrable :** comprendre visuellement à qui un lieu est relié, et pouvoir
atteindre un lieu même dans l'amas de L'Aigle.

**Acquis à conserver :** les liens sont déjà lisibles et portent déjà leur sens
par une pointe orientée.

**Bilan du bloc B — 19 septembre 2026.** Réalisation faite et mesurée dans un
navigateur ; détail et chiffres dans
`docs/audit_carte_d3/journal_phases_carte.md`. Deux lieux éprouvés : deux
partenaires attendus, deux anneaux posés sur les bons lieux ; puis trois
attendus, trois posés. Cadrage inchangé à l'ouverture comme au retour. Les
quinze lieux du groupe de L'Aigle sont désignés chacun par le leur. Le clavier
conserve son parcours complet. Reste ouvert : le toucher sur appareil réel, et
la validation du porteur.

### BLOC C — Juger et transposer — fait, en attente de jugement

**Question à juger :** cette carte est-elle la bonne, et que faut-il pour la
onzième vallée ?

- [x] Vérifier la liste des règles transposables sur Crulai. Plus aucune ligne
  de code ne nomme la Risle : identification au survol, zoom et noms de lieux
  valent pour tout ensemble, et la présence de repères de bourg se lit dans les
  données. Les différences entre les deux cartes sont toutes des conséquences
  des données.
- [x] Chiffrer ce qu'il faut pour ouvrir un ensemble de plus, sans le
  développer. Sonde sur Noireau, Flers et Argentan : lieux, relations, eau et
  sol se calculent sans intervention ; chaque ensemble ajoute de 170 à 300 ko.
- [ ] **Décision à prendre : le poids.** Les douze ensembles porteraient la page
  à environ trois mégaoctets. La page entièrement autonome ne tient pas à douze ;
  il faudra choisir entre l'autonomie et le poids. Hors du présent plan.
- [ ] **Travail de données préalable :** trois communes portées par des lieux
  n'ont pas de contour — Athis-de-l'Orne et Frênes pour le Noireau, Goulet pour
  Argentan. Les lieux portent des noms de communes anciennes, fusionnées depuis.
  Une table de correspondance est nécessaire avant d'ouvrir ces ensembles.
- [ ] Examen visuel complet par le porteur, sur écran large et étroit :
  parcours carte → lieu ou lien → retour, sous filtre et sans filtre, sur la
  Risle et sur Crulai.
- [ ] Décision du porteur.

**Livrable :** carte de référence jugée, et règles d'adaptation explicites pour
les onze autres ensembles.

**Remplace la phase de comparaison D3 / SVG du plan précédent**, devenue sans
objet : le choix a été tranché le 19 septembre, D3 tient le dessin. La
référence SVG antérieure reste consultable sur sa branche.

### BLOC D — Harmoniser la carte du département — fait, en attente de jugement

**Question à juger :** la carte d'arrivée, celle sur laquelle le lecteur clique
pour entrer dans un ensemble, se comporte-t-elle comme celles qu'elle ouvre ?

**Constat qui ouvre ce bloc, 19 septembre 2026.** Deux moteurs coexistent. La
carte des ensembles tourne sur l'architecture D3 : couches posées une fois,
jointures de données, transitions, zoom, comportements génériques. La carte du
département est restée en SVG écrit à la main, effacée et reconstruite à chaque
geste. Écart relevé dans le code :

| | Ensemble | Département |
| --- | --- | --- |
| Couches persistantes et jointures | oui | non |
| Transitions au changement de métier | oui | non |
| Zoom et déplacement | oui | non |
| Cartouche, légende et échelle dans la carte | oui | non, bande au-dessus |
| Identification au survol | oui | non |
| Pointage du lieu le plus proche | oui | non |
| Taille d'écran minimale des points | oui | non |

#### D1 — Le dessin du département tenu par D3, à résultat identique

- [x] Poser les couches une fois — contour, autres lieux, ensembles, étiquettes —
  et les mettre à jour au lieu d'effacer la carte à chaque changement de métier.
  Les couches sont paramétrables ; chaque niveau déclare les siennes.
- [x] Remplacer le placement d'étiquettes maison par le mécanisme déjà éprouvé
  sur les ensembles, en conservant la règle : un nom n'est jamais masqué. Les
  noms passent en surface, ancrés à leur bulle par un décalage constant.
- [x] Vérifier que rien n'a bougé : 12 ensembles, 146 autres lieux, 26 lieux et
  10 ensembles retenus sous Métallurgie, mêmes coordonnées, même cadrage. Un
  élément présent avant le filtre est toujours le même après.
- [-] Deux défauts corrigés au passage : deux noms tombaient sur une bulle et
  « Bassin de Halouze · 13 » affichait « · 1 », son chiffre recouvert. Il
  subsiste un chevauchement sans filtre entre « Vallée du Noireau » et
  « Flers », deux voisins dans le coin le plus dense ; les deux restent
  lisibles. Le trait de rappel relève de la présentation.
- [ ] Validation du porteur.

**Livrable :** aucun changement visible, un seul moteur de dessin pour les trois
niveaux.

#### D2 — Donner au département ce que l'ensemble a déjà

- [x] Identification au survol : nom de l'ensemble, effectif et disponibilité ;
  nom, commune et activités pour les lieux hors ensembles, qui ne disaient rien.
  Une source unique des entités désignables sert les trois niveaux.
- [x] Pointage du lieu le plus proche, sans déplacer aucun point. Un clic près
  d'une bulle ouvre son ensemble ; près d'un lieu hors ensemble, rien ne s'ouvre
  puisqu'il n'y a rien à ouvrir, et l'étiquette le dit avant le clic.
- [x] Zoom et déplacement bornés, avec retour exact au cadrage initial. Bulles,
  points gris et cibles gardent leur taille d'écran.
- [x] Cartouche dans la carte, avec légende et échelle, à la place de la bande
  au-dessus du cadre. Il choisit bas-gauche au département, là où les ensembles
  choisissent bas-droite.
- [x] Taille d'écran minimale des points. Les noms des lieux hors ensembles
  apparaissent aussi au zoom, bornés à soixante étiquettes.
- [x] Vérifier la lisibilité sur écran large et étroit : quatre largeurs de
  carte, cartouche de 6 à 17 % de la carte, réduit sous 480 pixels, crédits sous
  la hauteur de la carte.
- [-] Un défaut ancien corrigé au passage, qui touchait aussi les ensembles : le
  cartouche était posé avant le dessin, donc avant que l'échelle de projection
  soit connue — Crulai annonçait 500 mètres au lieu d'un kilomètre. Il subsiste
  un chevauchement entre « Vallée du Noireau » et « Flers » à toutes les
  largeurs ; les deux restent lisibles.
- [ ] Validation du porteur.

**Livrable :** une carte d'arrivée qui se manipule comme celles qu'elle ouvre.

**À décider en cours de bloc, et à consigner :** le sol communal. Les ensembles
reposent sur les contours des communes qui touchent leur cadre ; à l'échelle du
département cela ferait 381 communes, donc un poids et une densité de traits à
évaluer avant d'engager quoi que ce soit. Le contour départemental seul est
peut-être suffisant.

#### D3 — Le passage du département à un ensemble

- [x] Examiner le comportement actuel : la carte était remplacée d'un coup, sans
  lien visible entre ce qu'on quitte et ce qu'on ouvre.
- [x] Descente d'échelle : la carte du département s'approche de la bulle visée,
  puis celle de l'ensemble arrive de plus près et se pose. Vaut par le clic, par
  Entrée depuis la carte et par la liste du panneau.
- [x] Le retour remonte symétriquement : le département repart de la bulle
  quittée et s'élargit. Vérifié, 5 → 1 puis stable.
- [x] Parcours clavier préservés ; le filtre est conservé à l'aller comme au
  retour — 24 lieux dans la Risle, 10 ensembles au département.
- [x] Trois garanties : la préférence « moins d'animations » rend le passage
  instantané ; une minuterie achève toujours la navigation ; le retour au
  cadrage initial est garanti, y compris au retour de la page à l'écran.
- [ ] **L'état partageable après le `#` n'existe pas.** Le prototype ne lit ni
  n'écrit aucune adresse : on ne peut pas partager un lien vers un ensemble, et
  recharger ramène au département. Écart avec une décision d'architecture
  arrêtée ; rien n'a été cassé par D3, il n'y avait rien à préserver. Appelle un
  travail à lui seul, hors du bloc D.
- [ ] Validation du porteur.

**Livrable :** le lecteur comprend qu'il descend dans le même territoire, au
lieu de changer d'écran.

#### D4 — Vérification d'ensemble

- [x] Parcours complet aux trois niveaux, sous filtre et sans filtre, sur écran
  large et étroit. Six vues mesurées ; à 380 et 290 pixels de carte le cartouche
  occupe de 6 à 10 %, ne déborde jamais, et les crédits restent sous la hauteur
  de la carte.
- [x] Contrôle clavier complet : 12 cibles au département, 48 dans un ensemble ;
  focus, contour, étiquette, Entrée et Espace vérifiés. Essai tactile simulé.
- [x] Consigner les règles devenues communes aux trois niveaux : neuf règles,
  dans `docs/audit_carte_d3/journal_phases_carte.md`.
- [-] Deux défauts trouvés et corrigés, tous deux hérités de D2 : un lieu masqué
  par le filtre restait désignable au survol dans un ensemble ; et le focus
  clavier sur une bulle du département n'affichait pas l'étiquette que le survol
  donne à la souris.
- [ ] Le tactile n'est pas éprouvé sur un appareil réel.
- [ ] Décision du porteur.

**Livrable :** un seul moteur, trois niveaux, règles communes écrites.

**Hors de ce bloc :** le niveau du lieu lui-même — ce que voit le lecteur une
fois entré dans une fiche — qui relève d'un plan distinct.

## Instruit séparément, hors des blocs

**Le relief.** Retenu le 19 septembre comme la façon honnête de donner de la
présence au territoire : la forme du terrain n'a pas changé depuis la période
industrielle, et elle explique l'implantation. Aucune donnée d'altitude n'est
présente dans le projet. À instruire : disponibilité, provenance, droits,
volume, et compatibilité avec une carte sans moteur cartographique.

**Les forêts anciennes.** Seule couche de végétation envisageable, reconstruite
à partir de cartes des environs de 1850. Déclarée au registre des sources mais
absente du projet, diffusée comme service distant, licence à confirmer au
moment de l'usage. À instruire avant toute proposition.

**Les aménagements hydrauliques disparus.** Biefs, canaux d'amenée et retenues
de moulin ne figurent pas dans les relevés modernes et ne sont donc pas sur la
carte ; les crédits le disent. Une représentation demanderait une source propre.

## Hors de ce plan

Pictogrammes métiers, palette, typographie et finition artistique relèvent de
la direction artistique, phase 10.E. Les blocs ci-dessus portent sur la
lisibilité et la compréhension, pas sur l'identité visuelle.

## Situation

**Référence de travail depuis le 19 septembre 2026 :
`codex/carte-d3-modele-risle`.** La carte y est dessinée par D3 sur les trois
niveaux ; c'est elle qui fait foi. Les deux états antérieurs restent consultables
sur leurs branches : `codex/carte-svg-narrative` pour la référence SVG et
`codex/test-d3-risle` pour l'essai D3 figé. Le paragraphe ci-dessous décrit la
situation au 18 septembre et n'est pas réécrit.

**Référence de travail : `codex/carte-svg-narrative` (18 septembre 2026).**
La carte SVG immédiatement antérieure à la passe 1 est rétablie pour Risle et
Crulai, avec ses branches hydrographiques, points, relations, cadrage sous
filtre et interactions. Les améliorations actuelles des panneaux sont conservées.
**SVG-1 — Eau validée visuellement par le porteur sur les captures fournies.**
SVG-2 est validée visuellement par le porteur sur la capture fournie, avec le
cadrage stable autorisé. La vérification sur écran étroit reste ouverte.
L'identification des points de la Risle au survol est validée par le porteur.
La mise en évidence du lieu dont la fiche est ouverte existe déjà selon le
porteur ; son éventuelle amélioration esthétique est reportée à la direction
artistique. Prochaine étape : lire les liens entre lieux.

**IGN suspendu**, conservé sur `codex/test-fond-ign-risle`, commit local de
sauvegarde `ca487ba`. Aucun merge ou push. Les essais refusés de la passe 1
restent historiques ; leurs cases ne décrivent pas la réalisation actuelle.

La nouvelle branche part de `origin/main` disponible localement, commit
`cf51f35810576b5436a779d4c814bc68ec0bc4dc`. La branche principale réelle est
`main` ; sa référence locale, ancienne (`e7d607e`), reste intacte. Aucun accès
réseau ni mise à jour de la branche principale n'a été effectué.

Le dessin SVG et le cadrage proviennent de `cf51f35`, dont les fonctions de
projection, de cadrage et de dessin d'ensemble sont identiques à celles
conservées dans la sauvegarde IGN, hors vocabulaire « lieux » et ouverture du
panneau de preuve. Aucun repère, nom d'eau supplémentaire ou changement de
cadrage issu des essais refusés n'est récupéré. La mention IGN des crédits
hydrographiques désigne la provenance des données locales, sans fond distant.

## Règles de suivi

- Une case de réalisation est cochée après exécution et vérification.
- La case de validation est cochée seulement après accord du porteur.
- Après chaque passe, consigner en bas de sa section les fichiers modifiés,
  contrôles effectués, retours et points restant ouverts.
- Conception et arbitrages dans 00 ; modifications par la CLI sur consignes
  courtes et précises. Aucune capture automatique.
- Préserver les données, les filtres, les relations et leurs réserves,
  les sources, les fiches et les parcours de retour.

## Développement SVG — historique

**Plan antérieur au passage à D3, conservé pour la traçabilité.** Ses étapes 4
à 6 annoncées comme à faire sont reprises, sous une autre forme, par les blocs A
à C du plan actif en tête du document. Il n'est plus une consigne d'exécution.

### Parcours à suivre — lecture rapide

Les cases ci-dessous indiquent les étapes acceptées par le porteur. Les détails
techniques et les anciens essais sont conservés plus bas pour la traçabilité.
Les identifiants SVG servent uniquement aux consignes de la CLI.

| Étape | Ce que le lecteur doit voir ou pouvoir faire | Avancement |
| --- | --- | --- |
| 1. Lire l'eau | Distinguer la Risle et conserver ses branches visibles. | Validée |
| 2. Se situer | Lire « La Risle » et les quatre localités repères. | Validée |
| 3. Identifier un lieu | Survoler un point et lire son nom, sa commune et ses activités. | Validée |
| 4. Repérer le lieu ouvert | Ouvrir une fiche et reconnaître immédiatement son point sur la carte. | **Prochaine étape** |
| 5. Lire les liens entre lieux | Distinguer un lien, le sélectionner et accéder à sa preuve. | À préciser avant exécution |
| 6. Vérifier le parcours complet | Vérifier carte, filtres, fiches et retours ; tester Crulai et consigner l'adaptation aux autres ensembles. | À faire |

- [x] Étape 1 — Eau (SVG-1).
- [x] Étape 2 — Localités et nom de rivière (SVG-2).
- [x] Étape 3 — Étiquette d'identification (SVG-3A).
- [ ] Étape 4 — Point du lieu ouvert mis en évidence (SVG-3B).
- [ ] Étape 5 — Liens entre lieux (SVG-4).
- [ ] Étape 6 — Vérification d'ensemble et adaptations (SVG-5).

**À faire maintenant : étape 4, sur la Risle uniquement.** Un clic sur un point
ou sur un lieu dans la liste ouvre sa fiche et entoure le point correspondant
d'un halo visible. En quittant la fiche, les points retrouvent leur aspect
normal. La carte garde le même cadrage. Si ce comportement existe déjà et est
lisible, le vérifier et le conserver plutôt que le réécrire.

**Plus tard, en direction artistique :** apparence des étiquettes, palette,
typographie et habillage de la carte. Les contrôles sur écran étroit encore
ouverts restent à effectuer à l'étape 6.

### 1. Eau

- [x] SVG-1.1 : relever le nombre et les identifiants des tracés existants de
  Risle et Crulai avant modification, pour contrôler leur conservation.
- [x] SVG-1.2 : identifier les tronçons de la Risle dans les propriétés des
  données hydrographiques locales ; consigner la règle et les éventuels manques.
- [x] SVG-1.3 : transmettre une catégorie principale/secondaire au rendu sans
  supprimer, déplacer ou simplifier davantage les tracés actuels.
- [x] SVG-1.4 : rendre la Risle plus visible ; garder toutes les branches
  secondaires visibles et discrètes. Aucun nouveau nom affiché.
- [x] SVG-1.5 : conserver Crulai sans rivière principale imposée ; vérifier que
  son réseau secondaire reste visible.
- [x] SVG-1.6 : adapter la légende seulement aux catégories réellement utilisées.
- [x] SVG-1.7 : vérifier génération, syntaxe JavaScript, conservation des tracés,
  filtres et parcours existants. Consigner les contrôles réellement effectués.
- [x] SVG-1.8 : examen visuel par le porteur sur Risle et Crulai ; retours consignés.
- [x] SVG-1.9 : corrections éventuelles appliquées, puis accord du porteur avant SVG-2.

**Livrable :** hydrographie SVG hiérarchisée et limites documentées.

**Critère de réception :** distinguer immédiatement la rivière principale de
la Risle, tout en retrouvant les branches de la carte initiale et des points
industriels lisibles. Aucun changement de cadrage ou ajout d'autre couche.

**Bilan SVG-1 — 18 septembre 2026 : réalisation technique vérifiée ; validation
visuelle du porteur reçue avant SVG-2.** Le porteur indique avoir validé la couche
Eau sur les captures fournies et autorise SVG-2. Aucune correction de SVG-1 n'est
demandée dans ce retour. Cet accord du porteur est distinct des contrôles simulés
effectués par la CLI ; aucune nouvelle capture n'est réalisée dans cette mission.

Avant toute modification, relevé des 650 tracés de Risle et des 150 de Crulai.
L'ancien HTML embarquait leurs coordonnées sans identifiants ; les `cleabs`
ont été retrouvés en rejouant exactement la sélection et la déduplication du
générateur avant modification, avec égalité de toutes les géométries embarquées.
Le relevé local de contrôle est conservé dans `.venv/svg1_avant.json`
(identifiants ordonnés, géométries, données et gabarit avant intervention).

**Règle d'identification :** dans l'ensemble Risle uniquement, le champ source
`cpx_toponyme_de_cours_d_eau`, après retrait des espaces externes et comparaison
sans distinction de casse, doit être exactement « la Risle ». Ce nom figure
sur 254 tronçons sélectionnés : 218 liés à `COURDEAU0000002000844950` et 36 à
`COURDEAU0000002491711065`. Ces liens corroborent le relevé ; ils ne servent pas
à extrapoler l'appartenance d'un tronçon sans nom. Le code BD Carthage varie et
n'est pas utilisé seul. Aucune appartenance n'est déduite de la proximité des
lieux industriels ; le critère de proximité préexistant sélectionne toujours
le même réseau, sans intervenir dans sa classification.

**Limites :** 147 des 650 tronçons de Risle n'ont pas de nom ; ils restent
secondaires, sans extrapolation topologique. Les noms différents restent aussi
secondaires. Aucune contradiction de propriétés entre occurrences d'un même
identifiant n'a été relevée dans les fichiers locaux sélectionnés ; le code
laisse néanmoins secondaire un identifiant dont les occurrences conduiraient
à des catégories contradictoires. Aucun filtrage selon la présence d'un nom.

**Résultat :** Risle 254 principaux / 396 secondaires, total 650 ; Crulai
0 principal / 150 secondaires, total 150. Les objets embarqués portent
`id`, `points` et `categorie`. Les principaux utilisent `#4f8fac`, épaisseur
2.2, opacité 0.85 ; les secondaires gardent `#8fb4cc`, 1.3 et 0.55.
L'eau reste dessinée sous les relations et les points. La légende montre
une entrée par catégorie présente : principale et secondaire pour Risle,
seulement cours d'eau pour Crulai. Aucun nom de rivière ou de bourg ajouté.

**Contrôles effectués :** cinq contrôles existants du générateur vrais,
aucun écart ; syntaxe JavaScript vérifiée par Node (`vm.Script`). Comparaison
avant/après stricte des listes ordonnées d'identifiants et de coordonnées,
des nombres et des chemins SVG projetés, sans nouvelle simplification.
Toutes les données embarquées hors métadonnées hydrographiques sont identiques.
Dans le contrôle DOM simulé réutilisant le harnais existant sans dépendance :
attributs de cadrage, points, relations et contenu des panneaux inchangés ;
Risle 43 lieux/5 relations, Métallurgie 24 lieux/4 relations, Crulai 7 lieux ;
réseau intégral sous filtre, preuve ouverte au clavier, fiches et retours
préservés. Styles, ordre de dessin et absence de doublon dans la légende vérifiés.
Ces contrôles ne constituent pas un examen visuel. SVG-1.8 et SVG-1.9 ont ensuite
été cochées sur le retour explicite du porteur, avant SVG-2.

**Fichiers modifiés pour SVG-1 :** `tools/generer_vue_reference.py`,
`tools/vue_reference_gabarit.html`, `prototype/vue_reference/index.html`
régénéré et le présent suivi. Modifications locales préexistantes conservées ;
aucune autre couche engagée, aucun changement de branche, commit, merge ou push.
Résultat : `http://127.0.0.1:8765/`, réponse locale HTTP 200 et SHA-256 identique
à l'HTML régénéré ; aucun redémarrage du serveur. Aucune capture automatique.

### 2. Repères

- [x] SVG-2.1 : examiner les ressources locales, puis vérifier les positions des
  quatre bourgs par des recherches officielles ciblées ; consigner leur provenance.
- [x] SVG-2.2 : contrôler les positions dans le cadrage préexistant, sans filtre
  et avec chaque métier représenté dans la Risle ; signaler les repères hors cadre.
- [x] SVG-2.3 : placer une seule occurrence de « La Risle » près d'un tronçon
  principal vérifié et dégagé, en bleu et italique.
- [x] SVG-2.4 : afficher L'Aigle, Rai, Aube et Sainte-Gauburge-Sainte-Colombe,
  avec un petit signe de localité distinct des points industriels ; garder les
  coordonnées vérifiées des signes et décaler uniquement les textes sombres.
- [x] SVG-2.5 : contrôler numériquement les cinq noms sans chevauchement ni boîte
  coupée, sans recouvrir les points ou les relations, sous filtre et à largeur
  étroite (mesures de texte estimées dans la simulation).
- [ ] SVG-2.5b : vérifier réellement dans un navigateur le placement, les polices
  et la lisibilité sur écran étroit ; consigner les limites éventuelles.
- [x] SVG-2.6 : adapter la légende et les crédits uniquement aux signes ajoutés.
- [x] SVG-2.7 : régénérer depuis le générateur et le gabarit, puis vérifier les
  contrôles existants, la syntaxe JavaScript, les cinq noms sur Risle, Crulai
  inchangé, l'eau validée, les lieux, relations, filtres, fiches, preuves et retours.
- [x] SVG-2.8 : examen visuel et retours du porteur sur la carte Risle.
- [x] SVG-2.9 : corrections éventuelles puis validation du porteur avant SVG-3.

**Livrable :** carte Risle portant exactement ces cinq noms lisibles, positions
et provenance consignées ; aucune modification de Crulai.

**Critères de réception actualisés après arbitrage :** aucun autre nom, aucun
centroïde communal utilisé comme centre de bourg. Pour Risle seulement, cadrage
stable calculé sur les 43 lieux et les quatre bourgs vérifiés, avec une marge
suffisante et sans élargissement supplémentaire. Aucun changement de dimensions
ou de formule de projection ; Crulai inchangé. Eau, points et relations
intégralement préservés. Les cinq noms
doivent rester lisibles sous filtre et sur écran étroit. Validation du porteur
reçue sur la capture fournie ; contrôle sur écran étroit toujours ouvert.

**Bilan initial SVG-2 — préparation du 18 septembre 2026 : blocage avant intégration,
ensuite levé par l'arbitrage explicite ci-dessous.**

Branche vérifiée : `codex/carte-svg-narrative`. Modifications présentes conservées.
L'état avant intervention (données, gabarit, générateur) est relevé dans
`.venv/svg2_avant.json`, pour les comparaisons après une intégration autorisée.
La couche Eau validée n'est pas modifiée.

**Ressources locales examinées :** contours API Géo du 22 juillet pour les codes
61008, 61214, 61342 et 61389, sans calcul de centroïde ; archives BAN du 21 juillet,
qui fournissent seulement des adresses à L'Aigle pour les bourgs demandés. Ces
adresses concernent des lieux industriels et ne sont pas retenues comme signes
de localité. Les mentions BAN des anciens essais ne suffisent pas à reconstituer
une provenance vérifiable pour les quatre positions actuelles.

**Positions préparées (longitude, latitude, WGS84) :** repères ponctuels d'adresse
ou de place de mairie, sans prétendre localiser un centre géométrique du bourg.
Les adresses sont vérifiées dans l'Annuaire Service Public ; les coordonnées
proviennent de requêtes au géocodage officiel IGN, index `address`, contraintes
par code INSEE, le 18 septembre 2026. Aucun résultat de type `municipality` retenu.

| Bourg | Longitude | Latitude | Repère géocodé et identifiant BAN | Provenance de l'adresse |
| --- | --- | --- | --- | --- |
| L'Aigle | 0.628894 | 48.764938 | Place Fulbert de Beina ; `61214_0475` ; type `street` | [Annuaire Service Public](https://lannuaire.service-public.gouv.fr/normandie/orne/9c9c4887-670f-4aef-9b00-24d6e4bab37f) |
| Rai | 0.579159 | 48.750466 | 12b Rue Trémont de Boisthorel ; `61342_0067_00012_b` ; type `housenumber` | [Annuaire Service Public](https://lannuaire.service-public.gouv.fr/normandie/orne/734b8da9-e754-4598-af21-0f1241b90cea) |
| Aube | 0.545120 | 48.740366 | 89 Route de Paris ; `61008_0060_00089` ; type `housenumber` | [Annuaire Service Public](https://lannuaire.service-public.gouv.fr/normandie/orne/3ca1f823-6000-4d0d-a080-7afa400749cd) |
| Sainte-Gauburge-Sainte-Colombe | 0.431513 | 48.716061 | Place de la Mairie ; `61389_0128` ; type `locality` (place nommée, pas commune) | [Annuaire Service Public](https://lannuaire.service-public.gouv.fr/normandie/orne/0fd678a5-aa06-440f-96da-93a1bb72ed27) |

Réponses officielles conservées localement dans `.venv/svg2_ban_aigle.json`,
`.venv/svg2_ban_rai.json`, `.venv/svg2_ban_aube.json` et
`.venv/svg2_ban_gauburge.json`. Les requêtes sont reproductibles à
`https://data.geopf.fr/geocodage/search`, paramètres `index=address`, `limit=3`,
`citycode` égal au code INSEE indiqué et `q` égal à l'adresse de mairie et au bourg.
Pour Sainte-Gauburge, le numéro 1 indiqué par l'annuaire n'est pas fourni par la
BAN : la place est localisée, sans prétendre avoir vérifié le bâtiment au numéro 1.

**Blocage de cadrage :** calcul ciblé avec les formules inchangées de `cadrer()`
et les lieux actuellement retenus par chaque filtre. Dans la carte de 1000 × 560
unités, les quatre signes se projettent à l'intérieur sans filtre et sous
Métallurgie (24 lieux). Ils tiennent aussi sous Agroalimentaire. En revanche :

| Filtre | Lieux | Bourgs hors de la carte actuelle |
| --- | --- | --- |
| Bois, papier, imprimerie | 4 | L'Aigle (1046.4, 83.3) ; Sainte-Gauburge (-386.3, 621.3) |
| Énergie | 2 | Aube (-79.8, 543.1) ; Sainte-Gauburge (-1454.6, 989.2) |
| Mécanique, électrique | 2 | L'Aigle (1018.4, 96.4) ; Aube (-243.0, 657.6) ; Sainte-Gauburge (-1953.6, 1212.7) |
| Textile, habillement, cuir | 9 | Sainte-Gauburge (-371.7, 627.8) |
| Verre, céramique, matériaux de construction | 1 | Les quatre bourgs : le recadrage sur un seul lieu produit une échelle incompatible avec ces repères |

Ces valeurs sont des coordonnées projetées SVG, pas des coordonnées déplacées
des bourgs. Décaler seulement les textes ne peut pas ramener les signes réels
dans la carte. Garder les cinq noms avec leurs signes visibles sous tous les
filtres demanderait un arbitrage explicite sur le cadrage, interdit dans la
mission actuelle ; aucune modification de cadrage n'est effectuée. Aucun nom
n'est masqué ou supprimé pour contourner la difficulté. L'intégration SVG-2
s'arrête avant modification du générateur, du gabarit ou de l'HTML.

**Contrôles réalisés :** positions et types de résultats officiels vérifiés,
calcul de projection sans filtre et sous les sept métiers représentés (dont
Métallurgie). Il s'agit d'un contrôle numérique préalable, pas d'une validation
visuelle ni d'un contrôle de chevauchement des textes. Aucun navigateur
disponible via l'outil de contrôle dans cette session ; aucune vérification
réelle sur écran étroit, aucune capture automatique. Génération, syntaxe et
parcours SVG-2 non testés puisqu'aucune intégration n'est réalisée.

**Fichier modifié :** le présent suivi seulement, plus les relevés locaux de
contrôle dans `.venv/` non versionnée. Prototype inchangé à
`http://127.0.0.1:8765/`. Aucune validation SVG-2 cochée, aucune autre couche
engagée, aucun changement de branche, merge ou publication.

**Arbitrage du porteur — poursuite de SVG-2, 18 septembre 2026.** Le porteur
autorise un cadrage stable de la Risle calculé sur les 43 lieux industriels et
les quatre bourgs vérifiés, avec une marge minimale suffisante pour les signes
et les noms. Un métier modifie les lieux et relations affichés, sans recalculer
l'emprise ; une fiche conserve ce même cadrage. Dimensions, coordonnées,
hiérarchie de l'eau et Crulai restent inchangés. La validation visuelle SVG-2
reste ouverte. Cet arbitrage remplace uniquement l'interdiction initiale de
modifier le cadrage Risle ; les constats du blocage initial sont conservés.

**Bilan après réalisation — 18 septembre 2026.**

- Cadrage calculé à chaque rendu sur la même liste fixe de 47 positions, sans
  dépendre du métier ou de la fiche. Les quatre bourgs se trouvent déjà à
  l'intérieur des extrema des 43 lieux : la vue sans filtre garde donc son
  cadrage antérieur. La marge existante de 30 unités SVG est conservée ; les
  textes sont placés à l'intérieur. Aucune emprise élargie au-delà du nécessaire.
- Quatre signes carrés sombres de 6 unités SVG, centrés aux coordonnées
  vérifiées consignées dans le tableau ci-dessus. Seuls les textes sont décalés.
  Une entrée de légende « localité — repère d'adresse ou de place » et un crédit
  Annuaire Service Public / IGN-BAN sont ajoutés uniquement dans la Risle.
- Une seule étiquette « La Risle », bleue et italique, ancrée au sommet 6 du
  tronçon principal `TRON_EAU0000000019049392`, soit (0.50695, 48.73358). Cette
  position reprend exactement un sommet simplifié déjà embarqué et sa catégorie
  principale validée. Aucun tracé d'eau modifié, déplacé ou filtré davantage.
- Placement des noms tenant compte des lieux, des courbes de relations, des
  signes de localité, des autres noms et de l'annotation du filtre. La police
  reste au moins à 12 pixels affichés ; Sainte-Gauburge-Sainte-Colombe occupe
  une seule étiquette sur deux lignes sous 480 pixels de largeur de carte.
  Un changement de largeur recalcule seulement le placement des textes et
  conserve les mêmes coordonnées et le cadrage stable de la Risle.

**Contrôles automatisés effectués :** régénération, cinq contrôles existants
vrais, aucun écart ; syntaxe JavaScript par Node (`vm.Script`). Comparaison
stricte avec le relevé avant SVG-2 : toutes les données précédentes identiques,
seul `detail.risle.reperes` ajouté. Hydrographie Risle 650 tracés (254 principaux,
396 secondaires) et Crulai 150 secondaires, géométries et ordre conservés.
Le rendu SVG hydrographique sans filtre est strictement identique au précédent.

Contrôle DOM simulé sans dépendance, consigné dans `.venv/svg2_controles.cjs` :
54 combinaisons de largeur et de métier (six largeurs de carte : 1000, 700, 480,
375, 294 et 254 pixels ; sans filtre, sept métiers représentés et un métier sans
résultat). Cinq noms et quatre signes présents à chaque état, coordonnées des
signes exactes ; boîtes de texte dans le SVG, sans recouvrement mutuel ni des
points ou relations. Ce contrôle utilise des mesures de texte conservatrices
estimées, pas les polices d'un navigateur réel. Cadrage et hydrographie identiques
sous filtre et dans les fiches ; Risle 43 lieux/5 relations, Métallurgie
24 lieux/4 relations ; preuves activées au clavier, ouverture des fiches et
retours préservés. Crulai : données, attributs du dessin SVG, panneaux, légende
et crédits strictement identiques au relevé antérieur, 7 lieux/150 tracés d'eau.

**Vérifications réelles dans un navigateur : aucune.** Le navigateur est
indisponible dans cette session ; aucune capture automatique n'est faite.
SVG-2.5b, SVG-2.8 et SVG-2.9 restent décochées. Le placement numérique vérifié
ne vaut pas validation visuelle ; les libellés et leur rattachement aux signes
doivent encore être jugés par le porteur sur écran large et étroit.

**Fichiers modifiés :** `tools/generer_vue_reference.py`,
`tools/vue_reference_gabarit.html`, `prototype/vue_reference/index.html`
régénéré et le présent suivi. Les relevés de contrôle `.venv/` restent locaux
et non versionnés. Modifications préexistantes conservées, aucun changement de
branche, commit, merge ou publication ; SVG-3 non engagée.
Prototype actualisé : `http://127.0.0.1:8765/`, réponse locale HTTP 200,
SHA-256 identique à l'HTML régénéré. `git diff --check` sans erreur.

### 3. Lieux industriels

**Accord du porteur — 18 septembre 2026 :** SVG-2 jugée acceptable sur la
capture fournie ; passage à SVG-3 autorisé. Cet accord ne coche pas SVG-2.5b :
le contrôle réel sur écran étroit n'est pas attesté. Le protocole ci-dessous
est approuvé ; première mission limitée à SVG-3A, sur la Risle uniquement.

#### Étape 3 — Identifier un lieu au survol (SVG-3A, validée)

- [x] SVG-3A.1 : réutiliser le nom du lieu, sa commune et toutes ses activités
  présentes dans les données ; aucun métier principal déduit, aucune donnée inventée.
- [x] SVG-3A.2 : au survol d'un point, afficher une petite étiquette temporaire
  avec ces informations ; aucun nom de lieu affiché en permanence.
- [x] SVG-3A.3 : au focus clavier, afficher la même étiquette et un contour
  clairement visible autour du point ; Entrée ouvre la fiche existante.
- [x] SVG-3A.4 : garder l'étiquette dans le cadre, lisible près des bords,
  sans intercepter le clic ; la retirer à la sortie du survol/focus et lors
  d'une ouverture de fiche ou d'un changement de filtre/vue.
- [x] SVG-3A.5 : régénérer le prototype et vérifier de manière ciblée les
  données affichées, les filtres et l'ouverture/retour des fiches ; préserver
  eau, repères, coordonnées, cadrage et relations. Crulai reste inchangé.
- [x] SVG-3A.6 : examen visuel et validation du porteur avant SVG-3B.

**Livrable SVG-3A :** sur la carte Risle, passer la souris sur un point ou
l'atteindre au clavier fait apparaître son nom, sa commune et ses activités.
Quitter le point retire l'étiquette. Le clic ou Entrée ouvre la fiche actuelle.
Sur mobile, le toucher conserve l'ouverture directe actuelle de la fiche.

**Réception :** juger un point isolé, un point dans le groupe dense de L'Aigle
et un point près du bord, puis refaire un essai sous filtre Métallurgie.
Les informations correspondent aux données du lieu, sans texte coupé ni
modification de la carte validée. Pas de capture automatique.

**Bilan SVG-3A — 18 septembre 2026 :** réalisation technique effectuée sur la
Risle uniquement. Le gabarit ajoute une étiquette temporaire non interactive
au survol et au focus : nom du lieu, commune et liste complète des activités
présentes dans les données. Le focus ajoute la classe `identifie-focus` et son
contour ; Entrée conserve l'ouverture de fiche, comme le clic et le toucher.
Une seule étiquette est maintenue : le focus prend la priorité sur le survol,
puis le survol reprend à la sortie du focus. Elle est supprimée à la sortie,
à l'ouverture d'une fiche et dans chaque nouveau rendu de filtre ou de vue.

Le cadre de l'étiquette est borné au `viewBox` 1000 × 560 ; le groupe porte
`pointer-events:none`, donc il ne bloque pas les clics. Crulai ne reçoit aucun
de ces comportements. Aucun libellé permanent, pictogramme métier, donnée,
coordonnée, eau, repère, relation ou état de sélection n'est changé.

**Contrôles réalisés :** génération avec les cinq contrôles existants vraie,
syntaxe JavaScript vérifiée par Node (`vm.Script`), et contrôle DOM simulé
réutilisant l'outil local `.venv/svg2_controles.cjs` : contenu nom/commune/
activités, survol puis sortie, focus puis sortie, contour déclaré, Entrée et
clic vers la fiche, disparition à l'ouverture, filtre Métallurgie (24 lieux,
4 relations) et retour. Les 54 états SVG-2 précédents restent contrôlés ;
Crulai garde ses 7 lieux et 150 tracés d'eau. Le prototype servi localement
répond HTTP 200 et son SHA-256 correspond à l'HTML régénéré ; `git diff --check`
est propre.

Le contrôle est simulé : aucun navigateur réel ni écran étroit n'est disponible
dans cette session, donc aucune vérification visuelle n'est affirmée. SVG-3A.6
et la validation globale SVG-3 restent décochées. Fichiers modifiés :
`tools/vue_reference_gabarit.html`, `prototype/vue_reference/index.html`
régénéré et le présent suivi ; le générateur n'a pas besoin de changement pour
ces données déjà embarquées. Aucun commit, fusion, publication, dépendance ou
capture automatique.

**Retour du porteur :** fonctionnement jugé bon sur la capture fournie ;
SVG-3A validée. La mise en évidence du lieu ouvert existe déjà selon le porteur.
Son éventuelle amélioration esthétique est reportée à la direction artistique.
Ce retour n'atteste pas d'un essai clavier ou mobile supplémentaire.

#### Étape 4 — Mettre en évidence le point du lieu ouvert (SVG-3B, prochaine étape)

- [ ] SVG-3B.1 : après validation de SVG-3A, vérifier les états existants avant
  de modifier : clic sur le point ou ouverture depuis la liste doivent
  désigner le même lieu et mettre clairement en évidence son point.
- [ ] SVG-3B.2 : rendre le point sélectionné reconnaissable par sa taille ou
  un halo ; au retour à l'ensemble, rétablir l'état normal des points.
- [ ] SVG-3B.3 : vérifier le parcours point/liste → fiche → retour sous filtre,
  puis obtenir la validation visuelle du porteur.

**Livrable visible :** ouvrir un lieu depuis la carte ou la liste affiche sa
fiche et un halo autour de son point, sans déplacer le point ni recadrer la
carte. Quitter la fiche retire le halo. Réutiliser une mise en évidence
existante si elle répond déjà à ce besoin.

**À juger :** ouvrir un lieu isolé, puis un lieu près de L'Aigle, revenir à
l'ensemble, et refaire un essai depuis la liste sous filtre Métallurgie.
Aucun changement des étiquettes, de l'eau, des localités ou des relations.
Mission de code non lancée.

### 4. Relations

- [x] Vérifier que les cinq relations de la Risle sont dessinées comme chemins
  SVG, avec leurs extrémités conservées et sans changement de géométrie.
- [x] Vérifier la sélection par clic et par Entrée/Espace au focus ; la
  sélection met en évidence le lien et ouvre le bloc « Relations entre les lieux ».
- [x] Vérifier la preuve : phrase justificative, type de relation et niveau de
  fiabilité sont affichés. Les réserves présentes dans les données sont portées
  par la phrase source (par exemple « la source ne nomme pas la cible ») ; il
  n'existe pas de champ de réserve séparé à afficher.
- [x] Vérifier le filtrage : un lien dont une extrémité est masquée disparaît de
  la carte et de la liste, tandis que le panneau indique le nombre de relations
  masquées ; le retour à « Tous les métiers » les rend à nouveau accessibles.
- [x] Vérifier l'ouverture d'une fiche et le retour à l'ensemble sans modifier
  les relations, leurs preuves ou les accordéons.
- [ ] Examen visuel réel et validation du porteur.

**Livrable :** déjà présent dans la référence : relations lisibles et accès à
leur documentation. **Aucune implémentation supplémentaire nécessaire.**

**Diagnostic ciblé — 18 septembre 2026 :** le générateur transmet les cinq
relations Risle avec `de`, `vers`, `type`, `fiabilite` et `phrase`. Le gabarit
dessine chaque relation en chemin SVG `role="button"`, avec activation souris
et clavier. La liste de preuves reprend les communes des deux lieux, la phrase,
le type et la fiabilité ; le texte source conserve les réserves formulées dans
la donnée. Les liens restent sous les points, et le filtre exige que les deux
extrémités soient visibles. Le contrôle local existant
`.venv/svg2_controles.cjs` est passé : syntaxe, 43 lieux/5 relations sans
filtre, 24 lieux/4 relations sous Métallurgie, sélection clavier, preuve,
filtrage, fiche et retours simulés. Aucun examen visuel réel n'a été effectué.

**Point séparé — chevauchement autour de L'Aigle :** difficulté signalée par le
porteur autour des points denses ; elle concerne la lisibilité générale des
points, pas une panne des relations. La solution reste à décider ultérieurement
dans la direction artistique. Aucun zoom n'est implémenté maintenant.

### 5. Validation

- [ ] Technique : vérifier Risle et Crulai avec les filtres et les parcours.
- [ ] Technique : consigner les règles communes et les ajustements propres aux
  autres ensembles, sans imposer les particularités de Risle.
- [ ] Validation du porteur : valider Risle et Crulai, les règles communes et
  les adaptations à appliquer ensuite aux autres ensembles.

**Livrable :** référence SVG jugée par le porteur et règles d'adaptation explicites.

## Historique des essais et ancien plan

Les sections suivantes sont conservées comme historique. Les cases cochées
attestent des opérations effectuées dans les essais de l'époque, y compris les
essais refusés ou suspendus ; elles ne valent ni maintien dans le prototype
actuel, ni validation du porteur. Les anciennes passes non engagées sont
supplantées par le mini-plan « Développement SVG » ci-dessus.

## Passe 1 — Se situer (historique : deux essais refusés, 10.D)

**Question à juger :** reconnaît-on le territoire et comprend-on où sont les lieux ?

### Sous-tâches

- [x] Définir le périmètre : Risle et Crulai, localités repères et hydrographie.
- [x] Vérifier la présence de ressources locales : noms des cours d'eau dans
  les fichiers hydrographiques, noms et contours dans les données communales.
- [x] Choisir un petit nombre de localités utiles pour situer chaque ensemble,
  y compris aux alentours lorsque cela aide ; sélection confirmée par le porteur
  le 17 septembre 2026.
- [x] Déterminer des positions de libellés représentant correctement les
  localités ; coordonnées de bourgs vérifiées par BAN, sans centroïde communal.
- [x] Identifier la rivière principale et les affluents utiles à nommer à partir
  des données ; la Risle est hiérarchisée pour Risle, aucun principal imposé pour
  Crulai-Chandai, et seuls les tronçons nommés sont conservés.
- [x] Transmettre au SVG les noms et les informations nécessaires à une
  hiérarchie simple entre rivière principale et cours d'eau secondaires.
- [x] Afficher les localités et les noms des cours d'eau avec un traitement
  provisoire lisible, sans masquer les lieux industriels ou les relations.
- [ ] Vérifier le placement, les chevauchements et le comportement des repères
  lorsque le filtre métier recadre la carte ; ne pas changer la règle de filtre.
- [x] Actualiser la légende et les crédits uniquement pour les éléments ajoutés.
- [x] Régénérer le prototype et vérifier les contrôles existants.
- [ ] Vérifier les parcours et la lisibilité sur écran large et étroit.
- [ ] Faire examiner les deux cartes par le porteur ; consigner et appliquer
  les corrections nécessaires.
- [ ] Obtenir la validation de la passe 1.

**Hors périmètre :** relief, forêts, pictogrammes métiers, zoom, nouvelle palette
définitive et refonte du moteur cartographique. Aucun contour d'ensemble ne
doit suggérer une frontière historique établie.

**Livrable :** cartes Risle et Crulai enrichies de repères géographiques dans le
prototype de référence, sélection des repères et provenance consignées,
contrôles et jugement du porteur renseignés ci-dessous.

**Bilan — deux essais refusés ; carte antérieure à la passe 1 restaurée ; enrichissement suspendu (17 septembre 2026) :**
le premier résultat a été refusé pour surcharge hydrographique, chevauchements,
libellés coupés et contexte géographique insuffisant. La reprise limite les
repères visibles à trois par carte : L'Aigle, Aube et Rai pour la Risle ; Crulai,
Chandai et L'Aigle comme repère extérieur pour Crulai-Chandai. La Risle est le
seul cours d'eau nommé ; les autres tracés restent disponibles sans libellé.
La reprise a elle aussi été refusée ; l'enrichissement de la carte est donc
suspendu et la version immédiatement antérieure à la passe 1 est restaurée.

Les données locales
ont été examinées, sans modification du prototype. Les contours communaux sont
disponibles dans `data/raw/api_geo/2026/2026-07-22/communes_orne_contours.geojson`.
L'hydrographie locale provient des tronçons BD TOPO archivés dans
`data/raw/hydrographie/2026/2026-07-23/`. Les fichiers hydrographiques portent
des noms de cours d'eau, mais ne fournissent pas toujours une toponymie continue
ou un point de bourg.

### Sélection proposée puis confirmée

Pour la Risle, la sélection confirmée est limitée à **L'Aigle**, **Aube** et
**Rai**, repères urbain, amont industriel et pôle des activités de la fin du
parcours.

Pour Crulai et Chandai, la sélection confirmée est **Crulai**, **Chandai** et
**L'Aigle** comme repère extérieur de la vallée industrielle principale. Aucun de
ces libellés ne suggère une emprise historique commune.

Pour l'eau, proposer **la Risle** comme rivière principale de l'ensemble Risle.
Pour Crulai et Chandai, aucun cours d'eau principal ne ressort avec la même
évidence dans les données de proximité des sept lieux ; proposer de ne nommer
que les tronçons effectivement nommés par les données, après vérification de
leur continuité, plutôt que d'imposer un affluent. À titre de repères à examiner
dans les fichiers : la Risle est attestée pour la vallée ; les autres noms
doivent être retenus seulement si leur tracé couvre lisiblement l'emprise de la
carte (les noms de fossés et de ruisseaux locaux seront écartés par défaut).

**Provenance et limite de positionnement.** Les noms de communes viennent du
champ `nom` des contours communaux API Géo ; les noms d'eau viennent de
`cpx_toponyme_de_cours_d_eau` dans les objets hydrographiques et du contexte
territorial calculé. Ces ressources ne localisent pas le centre bâti d'un bourg.
La passe d'intégration devra donc employer des positions de repère clairement
indicatives, sans appeler un centroïde communal « centre du bourg », et signaler
les cas où aucune position suffisamment fiable n'est disponible.

**Intégration historique des essais ensuite refusés (absente de la référence actuelle).** Les coordonnées BAN et
leur provenance sont consignées dans `tools/generer_vue_reference.py`. Le SVG
porte les repères sélectionnés, les noms d'eau disponibles et une hiérarchie
provisoire (Risle principale, autres tronçons secondaires). L'emprise est stable
sur l'ensemble complet lors d'un changement de filtre. Le contrôle de placement
fin, notamment les chevauchements sous filtre et sur les deux formats, reste à
examiner visuellement. La validation de la passe 1 reste ouverte.

### Test isolé Plan IGN — Risle uniquement (18 septembre 2026)

Branche : `codex/test-fond-ign-risle`, créée depuis l'état courant sans stash,
reset ni restauration globale ; toutes les modifications préexistantes sont
conservées. Aucun commit, merge ou publication. Cette autorisation ponctuelle
ne valide ni un changement général de moteur ni la direction artistique.

Solution : Leaflet **1.9.4 stable**, JS/CSS locaux et licence BSD-2-Clause dans
`prototype/vue_reference/vendor/leaflet-1.9.4/`. Fond WMTS Géoplateforme,
`https://data.geopf.fr/wmts`, couche `GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2`,
style `normal`, PNG, pyramide actuelle **PM_0_19** (niveaux 0–19), confirmés par
le GetCapabilities courant. Aucune copie massive ou archive de tuiles.

Références officielles vérifiées le 17 septembre 2026 :

- [Diffusion WMTS IGN/Géoplateforme](https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/diffusion/wmts/)
- [Plan IGN, catalogue publié par l'IGN](https://www.data.gouv.fr/datasets/plan-ign)
- [Licence Ouverte 2.0](https://www.data.gouv.fr/pages/legal/licences/etalab-2.0)
- [Version stable Leaflet](https://leafletjs.com/download.html)

La Licence Ouverte autorise la réutilisation en mentionnant source et mise à
jour. Crédits visibles : IGN, Plan IGN, édition juillet 2026 et lien vers la
licence. Précision « Fond géographique actuel », pour ne pas présenter ce fond
contemporain comme une reconstitution historique.

Le fond est réservé au niveau ensemble Risle et à ses fiches. Les 43 points
utilisent leurs coordonnées géographiques existantes ; les cinq relations
sont reprojetées en courbes Leaflet, fléchées, avec cible élargie et activation
par Entrée/Espace pour ouvrir l'accordéon et lire les phrases sources. Les
réserves et les panneaux actuels sont conservés. Aucun SVG superposé, aucun
ancien libellé ou tracé hydrographique ajouté sur le fond IGN.

Cadrage initial : tous les lieux et le contexte de L'Aigle (position de bourg
déjà vérifiée), marge 13 % et 24 px, zoom initial au plus 12. Il reste stable
au filtrage et à l'ouverture d'une fiche ; zoom/déplacement standards,
molette désactivée, bouton « Revenir à la vue d'ensemble ». Département et
Crulai gardent leur SVG et leur comportement précédent.

Contrôles réellement effectués :

- [x] Régénération : cinq contrôles du générateur vrais, aucun écart.
- [x] Syntaxe du JavaScript généré vérifiée par Node.
- [x] Une tuile du service actuel vérifiée : HTTP 200, `image/png`.
- [x] Test d'état/rendu **simulé** sans dépendance par
  `node tests/test_vue_reference_ign.cjs` : 43 lieux/5 relations ; Métallurgie
  24 lieux/4 relations selon les mêmes règles ; cadrage non recalculé ; preuve
  activée au clavier, ouverture d'un lieu, retour et remise à la vue d'ensemble.
- [x] Dans cette simulation : panneau/accordéons conservés, département SVG,
  Crulai 7 points/150 tracés et absence de rubrique relations ; erreurs de
  tuiles et absence de Leaflet affichent un message sans supprimer les listes.
- [x] Comparaison avec HEAD : sites, relations et hydrographie Risle/Crulai
  strictement identiques ; aucune donnée source modifiée.
- [x] Serveur `http://127.0.0.1:8765/` : HTTP 200 et SHA-256 identique à
  `prototype/vue_reference/index.html` régénéré ; aucun redémarrage nécessaire.
- [ ] Parcours dans un navigateur réel, contrôle clavier complet et lisibilité
  aux formats large/étroit : aucun navigateur de contrôle disponible dans
  cette session. CSS adaptatif conservé, mais cela ne vaut pas examen visuel.
- [ ] Validation du porteur.

Fichiers de ce test : gabarit, HTML régénéré, fichiers Leaflet/licence,
test ciblé, présent suivi, journal et note dans la roadmap. Le générateur n'a
pas besoin d'être modifié pour cette intégration ; ses modifications
préexistantes sont conservées.

Limites : connexion réseau indispensable au fond ; fonctionnement effectif
des tuiles dans le navigateur et lisibilité des relations courtes restent à
examiner. Message explicite en cas de fond indisponible/incomplet ; listes,
fiches et preuves locales utilisables. Le SVG antérieur n'est pas effacé et
les données hydrographiques restent dans le corpus. Enrichissement SVG de la
passe 1 toujours suspendu, validation non cochée.

### Vérification Épuré / Niveaux de gris et bascule SVG (18 septembre 2026)

Branche vérifiée avant modification : `codex/test-fond-ign-risle`. État local
préexistant conservé ; aucun commit, merge ou publication.

**Blocage de la comparaison dans le périmètre autorisé.** Les styles officiels
existent, mais ne sont pas des variantes PNG de la couche WMTS actuelle.
Le GetCapabilities courant de `https://data.geopf.fr/wmts` annonce uniquement
`STYLE=normal` pour `GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2` (ainsi que sa variante
L93). Les accès officiels vérifiés, réponses JSON valides obtenues :

- [Épuré](https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/epure.json) :
  style version 8, 321 couches de rendu.
- [Niveaux de gris](https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/gris.json) :
  style version 8, 425 couches de rendu.

Ces deux fichiers déclarent la source vectorielle `plan_ign`, tuiles PBF
`https://data.geopf.fr/tms/1.0.0/PLAN.IGN/{z}/{x}/{y}.pbf`, métadonnées
`https://data.geopf.fr/tms/1.0.0/PLAN.IGN/metadata.json` (format `pbf`,
EPSG:3857, niveaux 0–18).
La [documentation officielle TMS](https://cartes.gouv.fr/aide/fr/guides-utilisateur/utiliser-les-services-de-la-geoplateforme/diffusion/tms/)
confirme la diffusion de ces styles vectoriels ; la
[fiche officielle Plan IGN](https://cartes.gouv.fr/aide/fr/partenaires/ign/representations-cartographiques-souveraines/plan-ign/plan-ign-web/)
confirme les deux déclinaisons. Il faudrait ajouter un moteur capable de rendre
ces styles JSON et leurs symboles/toponymes, ou une adaptation importante :
arrêt avant cette intégration conformément à la consigne. Aucun paramètre
`STYLE` supposé, URL de tuile inventée, substitution CSS ou sélecteur factice.
**Style réellement intégré : Plan IGN standard PNG uniquement**, inchangé.

**Défaut de bascule identifié et corrigé.** La précédente instruction
`CARTE.hidden = utiliseIGN` affectait une propriété JavaScript du SVG sans
poser l'attribut utilisé par `svg.carte[hidden]{display:none}`. Le SVG
départemental pouvait donc rester au-dessus de Leaflet. Le gabarit pose
désormais explicitement l'attribut `hidden` sur le SVG dans Risle et le retire
pour département/Crulai. Aucun changement de disposition, dimensions, points,
relations, hydrographie, zoom ou cadrage.

Contrôles :

- [x] Générateur : cinq contrôles vrais, aucun écart, Risle 43 lieux/5 relations.
- [x] Syntaxe JavaScript du prototype régénéré.
- [x] Test ciblé simulé : attribut de masquage SVG présent sur Risle, retiré
  sur département/Crulai ; Métallurgie 24 lieux/4 relations, ouverture par
  point, preuve au clavier et retour, cadrage stable.
- [ ] Changement de style à vue constante : non réalisé, intégration bloquée.
- [ ] Vérification visuelle dans un navigateur réel et validation du porteur.

Fichiers : gabarit, HTML régénéré, test ciblé, présent suivi, journal et note
roadmap. Fond distant et gestion existante des erreurs préservés. Prototype
servi à `http://127.0.0.1:8765/`, version régénérée vérifiée par SHA-256.

### Essai réversible du fond standard désaturé (18 septembre 2026)

**Essai du fond standard désaturé ; styles vectoriels officiels non intégrés.**
Branche vérifiée avant modification : `codex/test-fond-ign-risle`.

Commande temporaire « Fond : Standard / Standard grisé », avec Standard grisé
par défaut. Le filtre `grayscale(100%)` s'applique uniquement au pane Leaflet
`fondIGN`, contenant les tuiles PNG du fond standard existant. Les points,
relations, commandes et panneaux restent hors de ce pane, donc non désaturés.
La bascule change uniquement son filtre visuel, sans recréer/recharger la
carte ou les tuiles et sans modifier centre, zoom, cadrage ou dimensions.
Attributions et gestion des erreurs réseau inchangées. Le choix reste conservé
pendant le filtrage et les parcours ; aucun nouveau moteur ou style vectoriel.

Contrôles réellement effectués :

- [x] Régénération : cinq contrôles du générateur vrais, aucun écart.
- [x] Syntaxe JavaScript vérifiée.
- [x] Test ciblé simulé : grisé initial, bascule vers Standard et retour au
  grisé ; même instance de carte, de fond et de couches, aucun recadrage.
  Pane dédié uniquement aux tuiles ; points et relations dans leurs panes
  habituels. Risle 43 lieux/5 relations ; Métallurgie 24 lieux/4 relations ;
  preuves, fiches et retours préservés, département/Crulai toujours en SVG.
- [x] HTML servi sur `http://127.0.0.1:8765/` identique au fichier régénéré
  (SHA-256).
- [ ] Examen dans un navigateur réel et validation visuelle du porteur.

Fichiers : gabarit, HTML régénéré, test ciblé, suivi, journal et note roadmap.
Aucune nouvelle dépendance, capture, fusion ou publication. Cet essai CSS
explicitement autorisé n'est **pas** le style officiel IGN « Niveaux de gris ».

## Passe 2 — Identifier et explorer (10.D)

**Question à juger :** peut-on identifier un lieu ou une relation avant d'ouvrir son détail ?

- [ ] Définir l'information d'identification : nom, commune et activités connues,
  sans inventer un métier principal pour les lieux à activités multiples.
- [ ] Rendre cette information accessible au survol et au focus clavier ;
  définir un accès adapté au tactile sans dépendance au survol.
- [ ] Clarifier les états de focus, de survol et de sélection avec un traitement provisoire.
- [ ] Faciliter le ciblage des points et des relations sans déplacer leurs coordonnées.
- [ ] Préserver l'ouverture des fiches et des preuves documentaires.
- [ ] Vérifier les interactions souris, clavier et tactile sur les deux ensembles.
- [ ] Recueillir les retours et obtenir la validation de la passe 2.

**Livrable :** identification et interactions compréhensibles dans le prototype,
avec comportement ordinateur/mobile et contrôles consignés.

**Bilan :** non engagée.

## Passe 3 — Consolider la carte de référence (10.D)

**Question à juger :** la carte reste-t-elle compréhensible dans les deux ensembles
et avec les différents filtres ?

- [ ] Corriger les chevauchements qui subsistent et les éléments coupés par le cadrage.
- [ ] Vérifier les cas denses, peu denses et sans résultat sous filtre.
- [ ] Faire correspondre la légende aux signes réellement affichés.
- [ ] Vérifier le parcours carte → lieu ou relation → retour, sur écran large
  et étroit, avec contrôle clavier ciblé.
- [ ] Consigner les limites acceptées et les points reportés à 10.E ou à l'audit.
- [ ] Obtenir la validation de la carte pour 10.D.

**Livrable :** carte fonctionnelle de référence validée sur Risle et Crulai,
avec liste explicite des limites et points reportés. Cette validation ne clôt
pas à elle seule 10.D : le niveau lieu et le parcours complet restent à juger.

**Bilan :** non engagée.

## Passe 4 — Donner une personnalité à la carte (10.E)

**Question à juger :** le territoire gagne-t-il en présence sans masquer les données ?

- [ ] Définir la palette, la typographie cartographique et la hiérarchie des signes.
- [ ] Choisir une famille cohérente de pictogrammes et leur usage conditionnel,
  avec une règle explicite pour les lieux à activités multiples.
- [ ] Évaluer des données de relief et de masses boisées : disponibilité,
  provenance, droits, volume et compatibilité avec le prototype SVG.
- [ ] Tester un relief discret et des masses boisées atténuées uniquement à
  partir de données géographiques réelles.
- [ ] Adapter la légende et les crédits au traitement retenu.
- [ ] Vérifier la lisibilité sur les formats cibles et obtenir la validation.

**Livrable :** carte habillée selon la direction artistique retenue, avec
ressources utilisées, crédits et choix acceptés ou écartés consignés.

**Bilan :** non engagée ; données supplémentaires à évaluer pour relief et forêts.

## Passe 5 — Zoom et déplacement, si nécessaires

**Question à juger :** ces interactions résolvent-elles une difficulté réelle d'exploration ?

- [ ] Identifier un besoin persistant que les passes précédentes ne résolvent pas.
- [ ] Décider explicitement d'engager ou de reporter cette passe.
- [ ] Si engagée, définir zoom, déplacement, limites et retour au cadrage initial.
- [ ] Définir la taille des signes et le comportement des libellés pendant le zoom.
- [ ] Préserver les interactions clavier, tactile, filtre et ouverture des détails.
- [ ] Vérifier les deux ensembles et obtenir la validation.

**Livrable :** soit une décision motivée de report, soit une navigation
cartographique vérifiée dans le prototype, avec ses limites consignées.

**Bilan :** optionnelle, non engagée.

## Gestion des missions de code

Luna 5.6 Medium reste le point de départ envisagé pour une sous-tâche limitée
et précisément cadrée. Un traitement complexe des libellés, du relief ou du
zoom, ou une difficulté persistante, justifiera de réévaluer le modèle avant
de poursuivre. Aucun modèle ne garantit à lui seul la bonne exécution.

Ne pas envoyer les cinq passes dans une seule mission. La première consigne
doit porter uniquement sur la passe 1 ou une sous-tâche de celle-ci.

## Préparation de la branche SVG — 18 septembre 2026

Sauvegarde IGN : 11 fichiers explicitement examinés et ajoutés, aucun ajout
global. Les données brutes, médias, `.claude/`, `docs/pilotage/` et la note
non versionnée restent hors commit et sont laissés en place. Avant sauvegarde,
aucun commit propre à IGN par rapport à `origin/main` ; après sauvegarde,
`ca487ba` est le seul commit propre à cette branche.

Récupérés depuis la sauvegarde, uniquement sur la nouvelle branche :
`config/phase10_systemes.yml` (présentations courtes),
`tools/generer_vue_reference.py` (transmission de ces présentations),
`tools/vue_reference_gabarit.html` (entrée, filtres et panneaux actuels) et
le présent suivi. L'HTML `prototype/vue_reference/index.html` est régénéré.
Le gabarit est débarrassé de Leaflet, du fond IGN et de ses commandes ; les
fichiers vendor et le test IGN restent exclusivement dans la branche IGN.
Les activités par ligne, blocs repliables, ordre lieux puis relations et
masquage de la rubrique sans relations sont conservés. L'ouverture d'une
preuve depuis une relation SVG tient compte du bloc repliable avant le rendu.

Contrôles limités effectués :

- [x] Régénération : cinq contrôles existants vrais, aucun écart ; 12 ensembles,
  172 lieux dans les ensembles et 146 autres lieux.
- [x] Syntaxe JavaScript : compilation du script généré par Node (`vm.Script`).
- [x] SVG rétabli : données des lieux, relations et hydrographie strictement
  identiques à `cf51f35` pour Risle et Crulai, y compris toutes les branches.
  Simulation du dessin : Risle 43 points, 5 relations, 650 tracés d'eau ;
  Crulai 7 points, aucune relation, 150 tracés d'eau.
- [x] Absence de chargement IGN/Leaflet et de leurs commandes dans le gabarit
  et l'HTML régénéré ; aucun fichier vendor récupéré.
- [x] Contrôle local simulé, en réutilisant le harnais DOM du test IGN sans
  fichier supplémentaire ni dépendance : activités par ligne, blocs repliables,
  lieux avant relations, preuve ouverte au clavier et conservée sous filtre,
  Métallurgie Risle 24 points/4 relations, fiche et retour, Crulai sans rubrique
  relations, retour au département.
- [x] `git diff --check` sans erreur ; branche `main` intacte.
- [ ] Examen visuel et validation du porteur : non effectués dans cette préparation.

Les quatre fichiers récupérés et l'HTML régénéré sont laissés en modifications
locales sur `codex/carte-svg-narrative` ; aucun commit supplémentaire n'est créé.
Ces modifications non committées ne sont pas isolées par le seul nom de branche :
les conserver ou les enregistrer explicitement avant une future bascule.

Aucune capture, recherche web, dépendance, sous-agent, fusion ou publication.
Aucune couche du nouveau plan commencée ; examen visuel et validation du
porteur restent distincts des contrôles techniques.

## Plan d'expérimentation D3 — historique (17-18 septembre 2026)

Conservé tel quel. Ses sept phases décrivaient le chemin pour faire
fonctionner D3 dans la carte ; leur objet est atteint et le plan actif est
désormais en tête du document. Les cases cochées attestent des opérations de
l'époque ; certains bilans sont devenus faux depuis le 19 septembre — notamment
les 650 tracés d'eau embarqués en GeoJSON, l'affirmation que le département et
Crulai restent sur leur rendu antérieur, et celle que les repères sont
compensés au zoom, qui ne valait pas pour les signes de localité.

### PHASE 0 — Préparation

- [x] Travail SVG actuel sauvegardé localement sans perdre les modifications.
- [x] Branche `codex/test-d3-risle` créée depuis cet état.
- [x] Fonctions existantes repérées : filtres, identification, sélection du lieu, fiches, preuves et retours.
- [x] Données nécessaires localisées : 43 lieux, 5 relations, réseau d'eau actuel, quatre localités et nom La Risle.
- [x] Point d'intégration D3 identifié et méthode de conservation du cadrage décrite brièvement.
- [x] Plan détaillé inscrit en tête du suivi.

Point d'intégration prévu : la génération des données de `D.detail.risle` dans
`tools/generer_vue_reference.py`, puis le rendu de `dessinerSysteme("risle")`
dans `tools/vue_reference_gabarit.html`. La projection, l'emprise stable et
les états d'interaction seront conservés lors de la phase 1 ; aucune conversion
ni modification du prototype n'est engagée en phase 0.

**Livrable :** branche prête et intégration cadrée ; prototype inchangé.

- [ ] Validation du porteur.

**Bilan de la PHASE 0 :** la sauvegarde locale est le commit `15cb793`
(`chore: sauvegarder la reference SVG avant l essai D3`) et la branche active
`codex/test-d3-risle` en est issue. Les fichiers sans rapport restent non
suivis et préservés ; aucun ajout global n'a été effectué. D3 n'est pas ajouté,
les données ne sont pas converties et le prototype reste inchangé pour cet
essai. La décision technique encore ouverte concerne seulement le choix des
outils D3/GeoJSON à la phase 1.

### PHASE 1 — Base D3

- [x] Ajouter D3 localement, sans dépendance à un CDN à l'affichage.
- [x] Représenter les données géographiques nécessaires en GeoJSON, sans altérer les coordonnées, identifiants ou informations.
- [x] Générer les tracés géographiques avec D3.
- [x] Conserver les 43 lieux, les 5 relations et tous les tracés d'eau actuellement affichés.
- [x] Conserver la distinction Risle principale / branches secondaires.
- [x] Conserver les quatre localités et le nom La Risle.
- [x] Retrouver une emprise et une occupation de la carte comparables au SVG actuel, avec cadrage stable sous filtre.
- [x] Conserver les interactions existantes : étiquette au survol/focus, sélection, fiches, preuves et retours.
- [x] Laisser la vue départementale et Crulai inchangés.
- [x] Contrôler la génération, la syntaxe et les parcours ciblés.
- [ ] Validation visuelle du porteur.

**Bilan de la PHASE 1 :** le générateur embarque D3 v7.9.0 depuis
`tools/vendor/d3.v7.9.0.min.js`, et la vue régénérée utilise les 43 lieux et
les 650 tracés d'eau GeoJSON pour Risle. Les coordonnées et identifiants ont
été comparés à la représentation historique ; les 5 relations, les quatre
localités et `La Risle` sont présents. La génération passe ses contrôles
existants ; les deux scripts inline passent la vérification de syntaxe
JavaScript. Les contrôles ciblés confirment les handlers de survol/focus,
sélection, filtre, fiche, preuve et retour, ainsi que l'absence de script
externe ou de chargement distant de données. Crulai et la vue départementale
restent sur leurs données et leur chemin de rendu antérieurs. Le contrôle
visuel du porteur n'est pas réalisé dans cette passe et reste décoché ; aucune
capture n'a été produite.

**Livrable :** carte Risle rendue avec D3, comparable à la référence, sans perte fonctionnelle.

### PHASE 2 — Zoom et déplacement maîtrisés

*Cette phase portait la mention « À FAIRE MAINTENANT » alors que toutes ses
cases de réalisation étaient cochées. La contradiction est levée ici : la phase
est faite, et son bilan est partiellement faux — les signes de localité
n'étaient pas compensés au zoom, défaut trouvé et corrigé le 19 septembre.*

- [x] Commandes « + », « − » et « Vue initiale ».
- [x] Zoom centré et limité.
- [x] Déplacement de la carte agrandie avec limites.
- [x] Points, textes et liens lisibles au zoom.
- [x] Survol, fiches, preuves et filtres préservés.
- [x] Retour exact au cadrage initial.
- [x] Contrôles ciblés et limites consignées.
- [ ] Validation visuelle du porteur.

**Livrable :** explorer les points serrés près de L'Aigle et revenir simplement à toute la vallée.

**Bilan de la PHASE 2 :** l'essai est implémenté dans le gabarit et régénéré
dans le prototype. D3 limite le zoom à 1–6, centre les commandes par facteur
1,5, borne la translation, désactive molette et double-clic et distingue le
glissement du clic par une distance de clic. Le groupe cartographique est le
seul transformé ; les commandes restent fixes. Les tailles de points et de
repères sont compensées par le facteur de zoom et les traits gardent leur
épaisseur. Les contrôles statiques ciblés passent pour le filtre Métallurgie,
la fiche, la preuve et les retours. La validation visuelle du porteur reste
ouverte ; aucune capture n'a été produite.

Le zoom ne déplace ni ne sépare artificiellement les coordonnées. Aucun doublon
de coordonnées exactes n'a été trouvé parmi les 43 lieux ; les points très
proches ou superposés visuellement restent donc à traiter par le futur cadrage
de la phase 3, sans nouvelle règle engagée ici.

**Correction de réception :** le porteur a signalé que la bulle d'identification
grossissait avec le zoom. La cause était son insertion dans `contenuCarte`, le
groupe géographique transformé par D3. Elle est désormais rendue dans
`coucheInterface`, une couche sœur non transformée ; son ancrage est calculé
par la transformation D3 courante, puis recalculé à chaque zoom ou déplacement.
La bulle reste pointer-events:none, bascule de côté près des bords et est
masquée lorsque le point sort du cadre. Les points, noms, contours de focus et
épaisseurs de traits gardent également une taille d'écran constante par
compensation ou `vector-effect`. Les contrôles mathématiques et structurels
passent ; la vérification des dimensions réellement rendues à zoom 1, 1,5, 3
et 6 reste à faire dans un navigateur, ainsi que la validation du porteur.

### PHASE 3 — Informations selon le zoom — NON ENGAGÉE

- [ ] Sélectionner les informations existantes utiles en vue rapprochée.
- [ ] Définir les seuils d'apparition des noms.
- [ ] Éviter les collisions et conserver une vue générale sobre.
- [ ] Validation du porteur.

**Livrable :** davantage de repères en zoomant, sans surcharge au départ.

Aucune nouvelle donnée ou règle d'affichage n'est implémentée avant le cadrage
de cette phase.

### PHASE 4 — Mise en évidence des relations — NON ENGAGÉE

- [ ] Examiner le comportement existant.
- [ ] Proposer comment distinguer les partenaires et liens d'un lieu sélectionné.
- [ ] Après accord, réaliser uniquement l'amélioration utile, sans refaire l'accès aux preuves.
- [ ] Validation du porteur.

**Livrable :** comprendre visuellement quels lieux sont liés au lieu sélectionné.

### PHASE 5 — Présence du territoire — NON ENGAGÉE

- [ ] Vérifier la disponibilité et la provenance de données forestières et d'altitude.
- [ ] Présenter l'effort et les limites avant intégration.
- [ ] Choisir avec le porteur un essai de masses forestières ou de relief discret.
- [ ] Tester la couche choisie sans masquer eau, sites et liens.
- [ ] Validation du porteur.

**Livrable :** enrichissement géographique réel, discret et évalué visuellement.

### PHASE 6 — Présentation — SUSPENDUE

- [ ] Retirer le long paragraphe et conserver une consigne courte.
- [ ] Intégrer une légende compacte sans masquer les données.
- [ ] Teinter légèrement le fond.
- [ ] Ajouter une échelle calculée, adaptée au zoom.
- [ ] Vérifier sources et lisibilité sur écran étroit.
- [ ] Validation du porteur.

**Livrable :** composition clarifiée, après évaluation des apports techniques.

### PHASE 7 — Comparaison et décision

- [ ] Comparer l'essai D3 à la référence SVG.
- [ ] Consigner gains, pertes et difficultés restantes.
- [ ] Vérifier les parcours ciblés.
- [ ] Décrire les adaptations aux autres ensembles sans les développer.
- [ ] Décision du porteur.

**Livrable :** choix explicite de la solution à poursuivre.

## HORS DE CET ESSAI

Végétation, relief, nouveaux noms d'affluents, pictogrammes et finition artistique
ne sont pas engagés ; ils seront décidés après comparaison.
