# Phase 10.E — Chantier de recherche artistique

**Version :** 0.1 — 17 novembre 2026
**Statut :** brainstorming ouvert. Aucune décision de direction artistique.
**Branche :** `claude/recherche-artistique`, ouverte depuis
`claude/esquisses-direction-artistique`. Les esquisses A, B, C et D restent
intactes sur leur branche ; elles servent d'inspiration et de référence de
fonctionnement.

## 1. Ce que dit le porteur (17 novembre 2026)

Il a mis du temps à formuler sa gêne devant l'esquisse D. Ce n'est pas un
détail : **tout est d'un bloc**. Une colonne-bloc à gauche, une carte-bloc à
droite, et le lecteur se débrouille. Le résultat est jugé grossier, binaire
visuellement. Il manque de subtilité, de sophistication, de recherche, de
couleur, de diversité et de finesse.

Il demande d'ouvrir un autre chantier, sur une autre branche, sans jeter ce qui
a été fait.

## 2. Ce que retient le regard extérieur

Le porteur a soumis l'esquisse D à un autre assistant. Ses deux retours sont
résumés ici ; ce sont des avis, pas des décisions.

**Le diagnostic.** L'esquisse D a une sophistication fonctionnelle, pas encore
plastique ni éditoriale. Quatre causes sont avancées :

- toutes les informations ont le même poids visuel : rien ne dit quoi regarder
  en premier ;
- la carte est chargée de signes mais pauvre en géographie perceptible — ni
  vallées, ni forêts, ni rivières, ni villes qui structurent l'espace ;
- les effets sont trop explicites et s'additionnent (trame, cercles orange,
  police étroite, papier vieilli) ;
- les nombres sont exacts mais ne sont pas mis en forme : six époques de même
  hauteur ne montrent pas l'écart entre 67 et 261 lieux.

**Les pistes proposées.**

- Une carte contemporaine travaillée : relief réel discret, eau beaucoup plus
  présente, forêts actuelles signalées comme actuelles, bourgs.
- Les cartes anciennes (Cassini, état-major, photographies aériennes) en couches
  consultables, jamais en fond qui change seul avec l'époque. La date d'une carte
  n'est pas la date d'une activité. Licences à vérifier.
- Plus de colonne fixe : une carte qui occupe l'écran, des commandes discrètes,
  des séquences de récit facultatives à l'entrée d'un ensemble.
- Les époques et les métiers dessinés comme des données : barres
  proportionnelles, mots et effectifs plutôt que pictogrammes abstraits.
  Précautions notées : périodes de durées inégales, un lieu peut compter dans
  plusieurs périodes.
- Une palette ardoise, bleu d'eau, sauge, encre ; une couleur vive réservée à la
  mise en évidence. Deux familles de caractères simples, l'une à empattements
  pour le texte, l'autre sans empattements pour les données.
- Une fiche de lieu en deux temps : un aperçu court, puis une présentation ample
  où la photographie respire.
- Une architecture commune, mais un traitement propre à certains ensembles : la
  Risle suit l'eau, Crulai regarde de près, Flers montre la densité. Hypothèses
  à vérifier sur les notices.
- Un mot ajouté : **la surprise** — des moments de découverte, pas des effets.
- Une mise en garde : demander « plus artistique » à une IA produit plus
  d'effets, pas plus de justesse. Il faut des références analysées, des
  intentions écrites, des essais par fragments, et le jugement du porteur.

**La méthode proposée.** Pas d'esquisse E qui rhabillerait D. Trois essais
ciblés, dans l'ordre : la carte seule ; la carte dans deux compositions sans
colonne ; la place des données (temps, métiers, fiche) sur la Risle et Crulai.

## 3. Évaluation de ces retours

**D'accord sur l'essentiel.** Le « tout d'un bloc » du porteur et le « même
poids visuel pour tout » du regard extérieur désignent le même défaut. L'esquisse
D a été construite pour prouver que le parcours fonctionne ; elle a été habillée
ensuite. Le rappel au principe ancien « partir du paysage pour révéler ce qu'il
cache » est juste : D l'avait perdu.

**Commencer par la carte, seule, est la bonne porte.** Tant que la carte ne tient
pas sans interface, tout le reste est de l'habillage.

**Trois réserves.**

- **Les forêts et l'eau détaillée demandent de nouvelles données.** Le projet n'a
  aujourd'hui que le contour, le relief et les cours d'eau des deux ensembles.
  Forêts, réseau hydrographique complet et bourgs du département viendraient de
  sources IGN ouvertes, à extraire et archiver selon nos conventions. C'est
  faisable, mais c'est du travail de données, pas de dessin.
- **Les images de référence citées ne sont pas des modèles à copier**, et
  plusieurs sont des œuvres protégées. Elles servent à nommer des qualités, pas à
  reproduire un style.
- **Les photographies de l'Inventaire restent des aperçus internes.** Une fiche
  « où la photo respire » ne change rien à la question des droits, qui reste
  ouverte avant toute publication.

## 4. Question ouverte

Par quoi commence le chantier ? Recommandation : **la carte de l'Orne seule**,
sans colonne ni filtre, jugée à 1440 pixels, avec deux ou trois traitements
comparés côte à côte. À trancher par le porteur.

## 5. Premier essai — la carte seule (17 novembre 2026)

Décision du porteur : on commence par la carte de l'Orne seule.

**Fichier :** `prototype/recherche/carte.html`, servi par un serveur local
(`python -m http.server 8771 --bind 127.0.0.1 --directory prototype`, puis
`/recherche/carte.html`). Les touches 1, 2 et 3 changent de traitement.

**Ce qui est nouveau dans les données.** Pour la première fois, la carte montre
la géographie du département, toute de source IGN, Licence ouverte :

- les rivières : 17 292 tronçons de la BD TOPO, d'ordre 3 et plus, dont
  l'épaisseur suit l'ordre de la rivière (un ruisseau est fin, l'Orne est
  épaisse) ;
- les forêts publiques actuelles : 58 forêts domaniales et communales. Ce sont
  les forêts d'aujourd'hui, et la carte le dit ;
- les 25 communes de plus de 2 000 habitants ;
- un relief quatre fois plus fin que dans l'esquisse D (pas de 0,0075°, environ
  800 m).

Script : `tools/carte_seule_extraire.py`. Réponses brutes archivées dans
`data/raw/ign_carte_seule/` avec leur empreinte. Lieux et ensembles : ceux des
esquisses, 321 lieux.

**Les trois traitements.**

1. **Topographique** — relief ombré et teintes douces selon l'altitude, eau
   bleue, forêts en vert sauge, lieux en rouge sombre.
2. **Encre** — fond clair, relief en courbes de niveau tous les 20 m, forêts
   hachurées, eau bleu d'encre, lieux en noir.
3. **Nuit** — fond ardoise, relief en lumière rasante, eau claire, lieux en
   points de lumière chaude : le patrimoine apparaît comme des lumières dans le
   paysage.

Aucune colonne, aucun filtre : seulement le titre posé sur la carte, le zoom, et
le nom d'un lieu au survol. Hors du département, la géographie continue sous un
voile, pour que l'Orne ne flotte pas dans le vide.

**Vérifié** à 1440 pixels dans le navigateur intégré, sur les trois traitements.
Non vérifié : mobile, et la fluidité dans un navigateur ordinaire.

## 6. Retour sur la carte seule (18 novembre 2026)

**Statut :** noté. Ce retour est une évaluation, pas une demande de modification.
Les trois traitements restent en place.

**Résumé du retour, transmis par le porteur.**

- Le progrès par rapport à l'esquisse D est net : le département a enfin une
  présence géographique.
- **Topographique** est la direction à privilégier. Ses réserves : le relief
  paraît uniforme, voire froissé, par endroits ; les forêts sont mal accordées au
  relief ; les lieux sont trop petits ; les ensembles ne sont pas structurés.
- **Encre** est élégante, mais elle apporte moins de géographie, et ses courbes
  s'agitent dans les zones accidentées. On la garde comme référence secondaire :
  finesse des traits, sobriété des noms.
- **Nuit** n'est pas retenue comme carte principale. Les lumières peuvent faire
  croire à des établissements actifs aujourd'hui, et les halos sont trop
  spectaculaires pour un propos documentaire. On la garde comme expérience,
  pour une éventuelle séquence de révélation.
- **Priorité : les lieux.** Le fond attire plus l'œil que le patrimoine. Il faut
  des points plus présents sans tout encombrer, adaptés au zoom, et qui
  distinguent les lieux isolés des concentrations.
- **Les douze ensembles.** À l'échelle de l'Orne, seuls les lieux hors ensemble
  sont des points ; chaque ensemble a sa propre forme, avec son nom et son
  effectif. La Risle et Crulai, déjà explorables, ont un traitement plus
  affirmé ; les dix autres, un traitement plus discret. Deux formes sont à
  comparer : le cercle proportionnel, comme dans D, et une enveloppe souple qui
  suit les lieux, sans jamais suggérer une frontière.
- **Hiérarchie.** Il faut distinguer quatre niveaux : le territoire, les
  ensembles, les lieux, puis le contexte (villes, rivières, forêts). Les noms de
  rivières sont aujourd'hui trop présents.
- **Bulle de survol.** Elle est trop pauvre, mais ce chantier vient plus tard.
- **Suite proposée :** travailler la finesse de la seule version topographique,
  pas une nouvelle ambiance.

**Évaluation.** Ce retour est juste, et il relève une erreur de l'essai, à
corriger avant tout. Sur la carte, les lieux de la Risle et de Crulai sont
dessinés un par un, alors que ceux des dix autres ensembles ne le sont pas, et
qu'aucun ensemble n'a de forme. Résultat : 199 points visibles, alors que le
titre annonce 321 lieux. La carte mélange deux échelles et sous-représente dix
ensembles sans le dire. La règle de l'esquisse D, rappelée par le retour, doit
s'appliquer : un ensemble est une forme, et ses lieux n'apparaissent qu'à
l'intérieur.

Deux points de méthode :

- l'enveloppe souple se calcule à partir des seuls lieux de l'ensemble, et la
  légende doit dire qu'elle n'est qu'un regroupement de proximité ;
- pour les dix ensembles non construits, les coordonnées de leurs lieux ne sont
  pas dans les données des esquisses. Le cercle est faisable tout de suite ;
  l'enveloppe demande de reprendre ces coordonnées dans la base du corpus.

## 7. Correction de la carte seule — les ensembles à leur place (18 novembre 2026)

**Ce que précise le porteur.** On ne complique pas : on expérimente ce qui est
expérimentable. Les lieux hors ensemble restent des points. Les lieux qui
appartiennent à un ensemble n'apparaissent pas sur la carte de l'Orne, ni pour
la Risle ni pour Crulai : ils n'apparaîtront qu'à l'ouverture d'un ensemble. Sur
la carte de l'Orne, on voit les ensembles eux-mêmes. L'enveloppe souple n'est
qu'un test visuel sur les deux pilotes ; si elle ne convient pas, on revient aux
ronds de l'esquisse D.

**Ce qui est fait.**

- Les 50 points de la Risle et de Crulai sont retirés. La carte montre 149 lieux
  hors ensemble en points et les douze ensembles en formes, chacune avec son nom
  et son nombre de lieux. Le total fait bien 321.
- Les deux pilotes ont une forme pleine, teintée, au trait continu. Les dix
  autres ont un rond proportionnel, plus pâle, au trait pointillé.
- Un bouton en haut à droite fait passer les deux pilotes de l'enveloppe au
  rond, pour comparer. L'enveloppe est calculée sur les seuls lieux de
  l'ensemble, élargis d'environ 1,3 km. La note de bas de page dit qu'elle n'est
  pas une frontière.
- Les noms d'ensembles passent avant ceux des villes, des rivières et des forêts.

**Vérifié** à 1440 pixels, version topographique, dans les deux modes. La Risle
dessine une longue bande le long de la vallée ; Crulai, une bande plus courte au
sud-est de L'Aigle.

## 8. Redonner de l'autorité aux données — trois variantes (18 novembre 2026)

**Ce que demande le porteur.** Le fond topographique est une bonne base, mais
les données s'y noient : les lieux sont de minuscules points et les ensembles
ressemblent à des points un peu plus gros. L'esquisse D, malgré ses défauts,
donnait plus d'autorité aux données. Il retient **le cercle** pour les
ensembles et écarte l'enveloppe. Il demande plusieurs traitements réellement
différents des lieux hors ensemble et des ensembles, sans toucher au fond, à la
navigation ni au reste. La version précédente reste comme référence.

**Ce qui est fait.** Un sélecteur en haut à droite (ou les touches 0, A, B, C)
fait passer d'une variante à l'autre. La référence garde son bouton enveloppe ou
rond.

- **A — Gravure.** Lieux : petit rond blanc cerclé d'encre avec un point
  central, comme un symbole de carte imprimée. Ensembles : disque proportionnel
  avec le nombre de lieux inscrit dedans. Les deux pilotes sont pleins, bleu
  d'encre, avec une ombre légère : on comprend qu'ils s'ouvrent. Les dix autres
  sont blancs, cerclés. Noms en romain, à côté du disque.
- **B — Carmin.** Lieux : petits losanges carmin bordés de blanc. Ensembles :
  anneaux carmin qui éclaircissent le paysage sous eux, nombre au centre. Les
  pilotes ont un anneau épais doublé d'un filet ; les dix autres, un anneau fin.
  Noms en italique.
- **C — Métiers.** Lieux : couleur du métier principal, six familles. Ensembles :
  couronne qui montre la part de chaque métier, nombre au centre. Les pilotes
  sont entourés d'un filet et en pleine couleur ; les dix autres sont atténués.
  Une courte légende apparaît en bas à gauche. Population de référence : les
  métiers par ensemble sont ceux de la vue de référence ; un lieu à plusieurs
  métiers compte dans chacun, la couronne montre donc des parts d'activités, pas
  de lieux.

Dans les trois, les rayons suivent la racine du nombre de lieux, comme dans
l'esquisse D. Les noms d'ensembles passent avant ceux des villes, des rivières et
des forêts. Les lieux grossissent un peu avec le zoom.

**Vérifié** à 1440 pixels, version topographique, sur les quatre états, sans
erreur dans la console. Non vérifié : mobile, et les variantes sur les fonds
encre et nuit, qui ne sont pas réglées pour elles.

## 9. Quatrième variante — D « Empreinte » (18 novembre 2026)

**Le retour du porteur sur A, B et C.** A, Gravure, est la préférée : la plus
cohérente avec le fond, sobre et fine. Mais ses lieux se confondent parfois avec
les détails géographiques. B, Carmin, a la meilleure visibilité, mais ses
losanges sont raides. C, Métiers, prouve que la carte supporte plusieurs
couleurs, mais ses petits anneaux chargent l'image. Il demande une quatrième
proposition, plus aboutie et plus singulière, qui parte de Gravure sans s'y
enfermer. Le fond, les cercles, les lieux masqués des ensembles et la
distinction entre les deux pilotes et les dix autres restent en place. Les trois
variantes et la référence sont conservées.

**L'idée.** Les données impriment le paysage. Ce n'est pas un symbole posé sur
la carte, c'est une trace laissée dans la terre.

- **Le lavis.** Sous chaque lieu et chaque ensemble, un lavis de couleur garance
  (rouge brun, éteint) se fond dans le relief par multiplication, comme une
  encre sur un papier. Là où les lieux se rapprochent, les lavis se superposent
  et la terre fonce d'elle-même. Les concentrations se lisent sans qu'on les
  dessine : c'est la réponse à la demande de distinguer lieux isolés et
  concentrations.
- **Les lieux hors ensemble.** Un repère gravé : un anneau d'encre fin, une
  réserve blanche qui le détache des rivières et du relief, un cœur garance. On
  garde la finesse de Gravure et on gagne la présence de Carmin, sans losange.
- **Les ensembles, comme des sceaux.** Le disque porte une graduation par lieu :
  43 traits pour la Risle, 7 pour Crulai, qu'on peut compter. Le nombre est
  inscrit au centre. Les deux pilotes sont pleins, bleu d'encre, avec des
  graduations blanches, un second filet et une ombre ; les dix autres sont
  couleur papier, avec des graduations d'encre et un filet intérieur.
- **Les noms.** En capitales romaines espacées, reliés au sceau par un filet
  fin, comme sur une carte gravée.
- **Les couleurs.** Deux seulement en plus du fond : l'encre et la garance. La
  variété vient de la superposition des lavis, pas de la palette.

**Vérifié** à 1440 pixels, en vue d'ensemble et zoomée sur la Risle, sans
erreur dans la console. Non vérifié : mobile. La finesse des graduations n'a pu
être jugée qu'à la résolution réduite des captures du navigateur intégré ; elle
reste à juger par le porteur sur un écran réel.

## 10. Empreinte écartée, affinement de A et B (18 novembre 2026)

**Le retour sur D, Empreinte.** Le porteur n'est pas convaincu, et le regard
extérieur non plus. Les graduations, les contours multiples et les ombres
ajoutent de la complexité sans ajouter de force : la carte paraît plus décorée,
pas mieux dessinée. Répétés cent cinquante fois, les petits symboles à trois
éléments donnent une texture agitée. Les graduations évoquent un instrument de
mesure, sans rapport avec le fond. D passe derrière A et B. Elle reste dans la
page pour mémoire.

**Ce que j'en retiens.** J'ai lu « plus sophistiqué » comme « plus détaillé ».
La demande était l'inverse : sélectionner, proportionner, retirer.

**La consigne.** Pas de nouvelle famille graphique. On fait deux évolutions
abouties : A′, à partir de Gravure, pour donner plus d'autorité aux données ; B′,
à partir de Carmin, pour gagner en finesse. Aucun contour superflu, aucune
texture, ombre ni effet de gravure. Le fond, les cercles, les lieux masqués des
ensembles et la distinction des pilotes sont conservés, et les variantes
existantes aussi.

**Le parti pris commun.** Un seul élément par symbole. Ce qui détache un symbole
du fond n'est pas un contour de plus, mais une **réserve** couleur papier, comme
sur une carte imprimée où l'on interrompt le fond autour d'un signe.

- **Lieux hors ensemble.** Un disque plein, un peu plus grand que dans A et B (un
  peu plus de 3 pixels de rayon), entouré d'une réserve fine. Il n'y a plus ni
  point central ni anneau dans A, ni losange dans B.
- **Ensembles.** Un disque proportionnel un peu plus grand, une réserve, et le
  nombre de lieux en chiffres romains de texte, proportionnés au disque. Les
  pilotes sont pleins ; les dix autres sont couleur papier, cerclés d'un trait
  unique. Il n'y a ni ombre, ni double filet, ni graduation.
- **Noms.** Centrés sur la hauteur du disque, à sa droite, à défaut à gauche,
  dessous ou dessus. Les noms des pilotes sont en demi-gras.

**Ce qui distingue les deux.**

- **A′, Gravure affinée** : tout en encre bleu-noir, noms en romain.
- **B′, Carmin affiné** : tout en carmin un peu plus profond que dans B, trait
  des ensembles légèrement plus épais, noms en italique couleur encre chaude.

**Vérifié** à 1440 pixels, en vue d'ensemble, sans erreur dans la console. Non
vérifié : mobile ; finesse des réserves à juger sur un écran réel.
