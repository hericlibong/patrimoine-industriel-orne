# Phase 10 — Direction artistique rejetée : Atlas industriel vivant

**Version :** 0.1 — proposition à arbitrer
**Statut :** rejetée après revue éditoriale du 27 juillet 2026 ; conservée pour
mémoire du processus de conception

## Objet

Ce document transforme le cadrage éditorial et le storyboard du bloc 2 en une
forme visible. Il ne définit pas encore l'architecture technique de
l'application et ne crée pas une bibliothèque de composants générale.

La direction doit servir quatre usages déjà décidés :

1. faire entrer dans le sujet par une proposition visuelle et journalistique ;
2. porter le data storytelling sans reléguer les données au rang
   d'illustrations ;
3. permettre une exploration cartographique précise sans produire un
   catalogue ;
4. donner aux études de cas une place suffisante pour les images, les
   chronologies, les sources et les incertitudes.

## Références limitées

Le benchmark ne sert pas à choisir un modèle à copier. Cinq références ont été
retenues pour un mécanisme précis.

| Référence | Ce qui est utile | Ce qui n'est pas repris |
| --- | --- | --- |
| [The Pudding — A People Map of the UK](https://pudding.cool/2019/06/people-map-uk/) | Une proposition cartographique immédiatement compréhensible, une exploration directe et une méthode accessible dans la même expérience | La carte comme produit autonome et la dépendance au survol |
| [Kontinentalist — Map-driven stories](https://kontinentalist.com/craft/map-driven) | L'intégration de cartes, textes, images et chapitres dans de véritables récits visuels | La spectacularisation graphique et les transitions qui ne servent pas une preuve |
| [ONS — How we build scrollytelling articles](https://digitalblog.ons.gov.uk/2021/06/02/how-we-build-scrollytelling-articles/) | Le principe texte + visualisation persistante, avec une attention explicite à l'accessibilité et à la compatibilité | La reprise d'un gabarit technique avant validation de la forme |
| [Historic England — 100 Places for 100 Years of the BBC](https://historicengland.org.uk/whats-new/news/bbc-centenary-map-100-uk-buildings-places) | Le lien simple entre lieu, image et récit court dans une carte patrimoniale | L'accumulation de marqueurs et le fonctionnement de catalogue de lieux |
| [Bassin minier Nord–Pas-de-Calais — carte interactive](https://bassinminier-patrimoinemondial.org/la-carte-interactive/) | La proximité thématique : patrimoine industriel, identité territoriale, fiches illustrées et carte | L'adresse touristique ou institutionnelle et la fiche comme destination systématique |

### Conclusion du benchmark

La publication doit être plus éditoriale qu'un SIG public, plus démonstrative
qu'un portail patrimonial et plus exploratoire qu'un long format linéaire. La
carte ne constitue donc ni un fond décoratif ni un répertoire : elle change de
rôle selon la question journalistique.

## Trois directions possibles

### A — Atlas industriel vivant

**Principe :** un atlas éditorial contemporain, sur fond papier chaud, où les
cartes, les chiffres et les documents d'archives partagent la même hiérarchie.
La dimension industrielle apparaît par la précision des tracés, les
annotations, la couleur oxyde et une typographie de travail, sans imiter un
manuel ancien.

**Caractère :** documenté, tactile, précis, dense par endroits mais jamais
administratif.

**Forces :**

- équilibre naturel entre journalisme, cartographie et photographie ;
- compatible avec des documents d'époques et de formats très différents ;
- permet une forte identité sans assombrir l'ensemble de la lecture ;
- prolonge la carte interne existante tout en lui donnant une véritable voix.

**Risque à contrôler :** le papier chaud et l'oxyde peuvent devenir un cliché
« patrimoine ». Ils restent donc des accents ; les données et les grilles
gardent une facture contemporaine.

### B — Dossier d'atelier

**Principe :** fond graphite, filets clairs, annotations monospaces, cadrages
serrés et orange de signalisation. L'interface évoque une table lumineuse, un
plan d'atelier ou un dossier technique.

**Caractère :** industriel, frontal, technique, nocturne.

**Forces :**

- identité très reconnaissable ;
- excellente présence des schémas, chronologies et documents techniques ;
- convient aux chapitres sur les transformations et les flux.

**Risques :**

- fatigue sur un récit long ;
- photographies anciennes souvent trop sombres ou écrasées ;
- tonalité potentiellement trop masculine, mécanique et attendue ;
- carte libre moins lisible et impression de « poste de contrôle ».

### C — Paysage productif

**Principe :** grandes photographies, blancs généreux, verts et bleus
territoriaux, typographie humaniste. Les cartes sont légères et les récits de
lieux occupent le premier plan.

**Caractère :** sensible, ouvert, territorial, presque documentaire
photographique.

**Forces :**

- très bonne entrée par les lieux et les traces ;
- respiration favorable à la lecture longue ;
- images contemporaines et paysages bien valorisés.

**Risques :**

- affaiblissement du positionnement datajournalistique ;
- difficulté à faire cohabiter les vues denses du corpus avec une esthétique
  très aérée ;
- glissement possible vers un magazine de patrimoine ou une communication
  touristique.

## Direction recommandée

La recommandation est la direction **A — Atlas industriel vivant**.

Elle répond le mieux à l'intention décidée : une enquête datajournalistique
qui utilise le patrimoine industriel comme objet, et non un site patrimonial
auquel on aurait ajouté quelques graphiques. Elle peut accueillir les sept
familles de visualisations du bloc 2, les images, les documents et les textes
sans qu'un média annule les autres.

Cette recommandation est appliquée aux trois écrans de référence pour permettre
un arbitrage visuel. Elle ne devient la direction définitive qu'après
validation.

## Principes visuels de la direction A

### Palette

| Rôle | Nom | Valeur | Usage |
| --- | --- | --- | --- |
| Fond principal | Papier | `#F3EFE6` | pages, fonds de récit |
| Fond élevé | Craie | `#FFFDF8` | cartes, panneaux, fiches |
| Texte | Encre | `#171A1C` | texte principal, traits forts |
| Texte secondaire | Ardoise | `#5E6568` | métadonnées, repères |
| Accent éditorial | Oxyde | `#9B3F2B` | appels, sélection, chiffres clés |
| Géographie | Eau | `#2F6F8F` | hydrographie, liens spatiaux |
| Donnée secondaire | Laiton | `#A66E16` | mise en évidence complémentaire |
| Incertitude | Violet grisé | `#74638F` | états inconnus ou incomplets |
| Filets | Poussière | `#CBC4B8` | séparateurs, fonds cartographiques |

L'oxyde ne code pas un secteur. C'est la couleur de la voix éditoriale et de
la sélection. Le bleu est réservé à l'eau et aux relations géographiques qui
l'utilisent réellement. L'incertitude n'est jamais indiquée par une simple
baisse d'opacité.

### Typographies

- **Titres et citations : Newsreader**, serif variable, pour la présence
  éditoriale et les grands nombres.
- **Texte, navigation et interface : IBM Plex Sans**, pour une lecture nette
  et une tonalité technique contenue.
- **Données, sources et repères : IBM Plex Mono**, uniquement pour les
  identifiants, dates courtes, valeurs et légendes techniques.

Si une police distante ne peut pas être servie de façon fiable, les familles
de repli sont respectivement `Georgia`, `Arial` et `Consolas`. Le système ne
prévoit pas de quatrième famille.

### Échelle typographique de départ

| Niveau | Bureau | Mobile | Usage |
| --- | ---: | ---: | --- |
| Titre d'ouverture | 72–88 px | 44–52 px | un seul par entrée |
| Titre de chapitre | 48–56 px | 36–42 px | question éditoriale |
| Titre de portrait | 56–64 px | 40–46 px | nom du site |
| Intertitre | 28–32 px | 24–28 px | étape ou preuve |
| Chapô | 22–24 px | 19–21 px | promesse, idée principale |
| Corps | 18 px / 1,55 | 17 px / 1,55 | récit |
| Interface | 15–16 px | 16 px | boutons, filtres |
| Source et légende | 13–14 px | 14 px | crédit, provenance |

### Grille et rythme

- largeur de contenu maximale : **1 280 px** ;
- grille bureau : **12 colonnes**, gouttières de 24 px ;
- marge extérieure : 48 à 72 px selon la largeur ;
- unité d'espacement : **8 px** ;
- espacements réellement utilisés : 8, 16, 24, 40, 64 et 96 px ;
- largeur de lecture courante : 620 à 720 px ;
- récit scrollytelling : 4 colonnes de texte et 8 de visualisation ;
- exploration : 3 colonnes de filtres/liste, 6 de carte, 3 de détail ;
- portrait : image ou visualisation sur 7 à 8 colonnes, récit sur 4 à 5.

Le rythme alterne trois densités : entrée ample, preuve dense, respiration
photographique. Il n'est pas construit par une succession uniforme de cartes
de contenu.

### Hiérarchie

Chaque écran doit permettre de repérer, dans cet ordre :

1. la question ou le lieu traité ;
2. la preuve visuelle principale ;
3. l'action possible ;
4. la source, la précision ou la limite.

Une information secondaire ne reçoit pas un cadre simplement pour la rendre
visible. Les filets, aplats et encadrés sont réservés aux changements de rôle :
interaction, méthode, source ou incertitude.

## Langage cartographique

### Fond de carte

- fond clair, sans imagerie satellite par défaut ;
- limites départementales nettes et communes très discrètes ;
- hydrographie simplifiée en bleu lorsque la question la mobilise ;
- routes, relief et lieux non utiles masqués ;
- noms de communes affichés avec parcimonie, en fonction du niveau de zoom ;
- sources cartographiques toujours visibles sous la carte.

### Sites et secteurs

La carte générale ne donne pas une couleur sectorielle définitive à chaque
site. Un site peut avoir plusieurs activités et plusieurs secteurs.

- état neutre : point encre à centre craie ;
- secteur choisi : points correspondants colorés, autres points maintenus en
  contexte ;
- site multi-secteurs : il apparaît dans chaque filtre correspondant, sans
  création d'un « secteur principal » artificiel ;
- sélection : double contour oxyde et halo non transparent ;
- regroupement à petite échelle : agrégat chiffré, jamais simple amas de
  points.

La palette sectorielle détaillée sera définie au bloc 4 avec les filtres
publics, afin de ne pas fabriquer neuf couleurs sans avoir validé leurs
libellés et leurs combinaisons.

### Précision et incertitude

| État | Symbole | Formulation publique |
| --- | --- | --- |
| Point approximatif | point plein entouré d'un cercle pointillé | « Position approximative » |
| Zone documentaire | polygone hachuré et contour continu | « Emprise documentaire » |
| Information contemporaine inconnue | motif violet grisé + libellé explicite | « Situation actuelle non documentée » |
| Date imprécise | borne ouverte ou intervalle hachuré | « Vers… », « avant… », « après… » |
| Relation historique documentée | trait continu avec source accessible | « Relation mentionnée par la source » |
| Proximité calculée | trait pointillé, valeur de distance | « Proximité mesurée, sans causalité déduite » |

La forme, le motif et le texte portent ensemble l'état. La couleur seule ne
doit jamais suffire.

## Images et documents

### Photographies

- pas de filtre sépia ni de colorisation automatique ;
- cadrage éditorial autorisé, mais l'image complète reste accessible ;
- les photographies historiques et contemporaines sont identifiées comme
  telles ;
- une image principale peut occuper une grande largeur si elle apporte une
  information, pas seulement une ambiance ;
- les mosaïques sont limitées à deux ou trois images ayant une fonction
  comparative ;
- aucun carrousel automatique.

### Documents graphiques

- plans, cartes anciennes, dessins et pages imprimées conservent leur ratio ;
- fond craie et marge légère pour distinguer le document de la page ;
- zoom disponible quand l'information l'exige ;
- les ajouts éditoriaux sont visuellement séparés de l'original ;
- aucune reconstitution n'est présentée comme un document source.

### Légendes, crédits et droits

Sous chaque média sélectionné, un bloc unique affiche :

1. une légende factuelle ;
2. la date ou la période si elle est connue ;
3. l'auteur ou le producteur ;
4. le crédit exact ;
5. un lien vers la notice ou la source ;
6. l'identifiant du média lorsque celui-ci est utile à la vérification.

Le crédit n'est jamais dissimulé dans une infobulle. La preuve d'autorisation
reste dans le registre de production ; elle n'alourdit pas l'interface
publique. Les visuels présents dans les maquettes sont des emplacements de
travail : ils matérialisent le traitement prévu, mais ne constituent pas une
sélection éditoriale ou juridique.

## Trois écrans de référence

Les maquettes sont disponibles en SVG et en PNG :

- `docs/design/phase10/01_accueil_atlas_industriel.svg`
- `docs/design/phase10/01_accueil_atlas_industriel.png`
- `docs/design/phase10/02_exploration_atlas_industriel.svg`
- `docs/design/phase10/02_exploration_atlas_industriel.png`
- `docs/design/phase10/03_portrait_abadie_atlas_industriel.svg`
- `docs/design/phase10/03_portrait_abadie_atlas_industriel.png`

### Écran 1 — Accueil

L'accueil ne commence pas par une liste de fonctionnalités. Il montre
simultanément :

- le titre et l'angle journalistique ;
- une carte de l'Orne où la géographie industrielle commence à apparaître ;
- les deux nombres d'entrée, 318 sites et 403 phases d'activité ;
- trois portes : commencer le récit, explorer la carte, rechercher un lieu ;
- une image de travail qui annonce que la matière visuelle fait partie du
  projet final.

### Écran 2 — Exploration

L'exploration est un espace de travail public en trois zones :

- filtres et résultats à gauche ;
- carte dominante au centre ;
- détail contextuel du site sélectionné à droite.

Le panneau de droite n'est pas une page de catalogue. Il répond à une
sélection sur la carte ou dans la liste, montre les informations indispensables
et propose un portrait seulement lorsqu'il existe.

### Écran 3 — Portrait Abadie

Le portrait montre comment une étude de cas peut articuler :

- une image principale et son crédit visible ;
- une thèse courte sur le rôle du site dans le récit ;
- une chronologie structurée ;
- une carte de flux documentés ;
- des liens de retour vers le chapitre et l'exploration ;
- des sources et limites accessibles sans casser la lecture.

Il ne représente pas le gabarit des 318 sites. C'est un format enrichi réservé
aux études de cas sélectionnées.

## Système visuel minimal

Le premier système comporte seulement les éléments visibles dans les trois
écrans et nécessaires au storyboard :

1. en-tête principal ;
2. lien, bouton primaire et bouton secondaire ;
3. titre éditorial, chapô, corps, légende et source ;
4. compteur ou chiffre clé ;
5. filtre sous forme de groupe dépliable ;
6. champ de recherche ;
7. élément de résultat ;
8. panneau de détail lié à la carte ;
9. marqueur neutre, actif, approximatif et zone documentaire ;
10. légende cartographique ;
11. média avec légende et crédit ;
12. chronologie de site ;
13. appel vers un chapitre, un portrait ou la méthode ;
14. bloc de limite ou d'incertitude ;
15. pied de page documentaire.

Ne sont pas créés à ce stade : système de cartes génériques, modales
universelles, notifications, comptes, favoris, tableaux de bord, carrousels,
menus à plusieurs niveaux ou variantes spéculatives.

## Points à arbitrer

La validation du bloc 3 demande seulement trois décisions :

1. retenir, corriger ou écarter la direction **Atlas industriel vivant** ;
2. confirmer le trio typographique et la tonalité papier–encre–oxyde ;
3. confirmer que les trois écrans donnent le bon équilibre entre données,
   carte, texte et image.

Les détails d'interaction de la carte et les couleurs sectorielles restent au
bloc 4. Le contenu détaillé du panneau et du portrait reste au bloc 5.
