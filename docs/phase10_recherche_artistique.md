# Phase 10.E — Chantier de recherche artistique

**Version :** 0.9 — 20 novembre 2026
**Statut :** composition « édition » retenue ; survol des deux ensembles validé ; Risle : liens entre établissements et zone chiffrée, soumis au jugement.
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

**Statut :** carte retenue à titre provisoire (topographique, A′, carrés) ; deux expérimentations de composition soumises au jugement.
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

## 10. Empreinte écartée ; affinement de Gravure et de Carmin (18 novembre 2026)

**Le jugement du porteur sur D, Empreinte.** Pas convaincu. Le regard
extérieur qu'il transmet précise : graduations, contours multiples et ombres
ajoutent de la complexité sans ajouter de force ; répétés 149 fois, les
symboles composés créent une texture agitée ; les graduations ne portent en
pratique aucune information lisible. « Plus sophistiqué » a été compris comme
« plus détaillé ». Ce qu'on cherche : une carte mieux dessinée, pas plus
décorée. D est classée derrière A et B et n'est pas retenue comme base.

**Ce qui est demandé.** Deux affinements distincts, sans nouvelle famille
graphique : A′, qui garde l'élégance de Gravure et donne plus d'autorité aux
données ; B′, qui garde le contraste de Carmin et gagne en finesse. Ni contour
superflu, ni texture, ni ombre, ni effet de gravure.

**Ce qui est fait.** Les deux variantes partagent la même règle de dessin. Seule
la couleur change, bleu d'encre pour A′, carmin pour B′, avec des noms en
italique pour B′.

- **Lieux hors ensemble :** un disque plein, un peu plus grand que dans A (rayon
  3,3 pixels à l'échelle du département), détaché du fond par un simple liseré
  couleur papier. Une seule forme : plus de rond creux ni de losange.
- **Ensembles :** cercles un peu plus grands que dans A, toujours
  proportionnels à la racine du nombre de lieux. Les deux pilotes sont pleins,
  avec le chiffre en blanc ; les dix autres sont couleur papier, cerclés d'un
  trait de 1,6 pixel, avec le chiffre de la couleur du trait. Le chiffre est en
  romain gras, à chasse fixe. Aucune ombre, aucun second cercle.
- **Noms d'ensembles :** plus grands qu'avant (15,5 pixels pour les pilotes,
  13,5 pour les autres), centrés sur la hauteur du cercle, à sa droite, sinon à
  gauche, dessous ou dessus.

**Vérifié** à 1440 pixels, version topographique, sans erreur dans la console.
Non vérifié : mobile.

## 11. A′ retenue ; dernière passe sur le signe des lieux isolés (18 novembre 2026)

**Ce que dit le porteur.** A′ « Gravure affinée » devient la direction de
référence pour la carte topographique : meilleur équilibre entre sobriété,
élégance et cohérence avec le fond. B′ reste lisible, mais le carmin domine trop.
On ne multiplie plus les variantes générales. Il reste un seul point : les lieux
hors ensemble. Les petits disques bleu d'encre manquent de présence, se fondent
par endroits dans le fond et forment des amas là où ils se touchent. Les douze
ensembles, leurs cercles, leurs chiffres, leurs noms et la distinction provisoire
entre pilotes et autres ne sont pas concernés. Le fond ne change pas. Les lieux
des ensembles restent masqués.

**Ce qui a été constaté avant de dessiner.**

- À l'échelle du département, à 1440 pixels, 29 paires de lieux isolés sont à
  moins de 9 pixels l'une de l'autre (calcul fait dans la page sur les 149 lieux
  hors ensemble). Les vrais amas sont autour d'Écouché (cinq lieux, dont deux
  usines à chaux à 2,7 pixels l'une de l'autre) et de Longny-au-Perche (trois
  lieux). Dès qu'on zoome franchement, ils se séparent. Le problème est donc
  celui de la vue d'ensemble.
- Une partie des amas ne tient pas à la forme. Dans A′, tous les liserés papier
  étaient tracés d'abord, puis tous les disques par-dessus : quand deux points se
  touchent, le liseré qui les séparait disparaît sous le disque voisin, et les
  deux points fusionnent en une tache.

**Ce qui est fait.** Un sélecteur, visible seulement sur A′, offre quatre
signes, tous de même surface et de même couleur, avec le même liseré papier :

- **A′ actuel** : la version jugée, intacte, pour comparer ;
- **disque** : la même forme, mais chaque signe est détouré à son tour, du nord
  au sud. Deux voisins restent séparés par un filet papier ;
- **carré** : même détourage, carré droit ;
- **losange** : même détourage, carré posé sur la pointe.

Deux boutons recadrent sur Écouché et Longny avec un zoom léger (×2), qui
conserve les chevauchements de la vue départementale. Aucune coordonnée n'est
déplacée.

**Évaluation**, faite à 1440 pixels, version topographique, en agrandissant la
vue départementale sans zoomer la carte :

| | Sur le relief, les forêts, les rivières | Présence au département | Amas d'Écouché | Avec les cercles des ensembles |
|---|---|---|---|---|
| A′ actuel | se perd près des rivières bleues | faible | une seule tache | même famille ronde |
| disque détouré | identique | faible | cinq points distincts | même famille ronde |
| carré | se détache : seule forme droite sur un fond tout en courbes | nette | cinq carrés distincts, empilement lisible | contraste franc : le lieu n'est pas un ensemble |
| losange | se détache | nette | distinct, mais les pointes s'imbriquent et s'agitent | contraste, un peu « marqueur » |

**Recommandation : le carré détouré.** C'est la seule forme droite sur une carte
faite de courbes : rivières, relief, lisières et cercles des ensembles. Il
gagne en présence sans changer de couleur ni grossir. Il sépare aussi sans
légende le lieu de l'ensemble. Enfin, c'est le signe que les cartes
topographiques donnent depuis longtemps au bâti.

**La nuance.** Ce dernier argument est aussi la réserve : un carré peut se lire
comme « ce bâtiment-ci, exactement ici ». Or beaucoup de nos points restent des
emplacements approximatifs. À 6 pixels, le risque est faible, mais la fiche du
lieu devra continuer d'afficher la précision géographique. Si le porteur juge ce
risque trop grand, le disque détouré est le repli sûr. Le détourage, lui, vaut
pour toutes les formes et devrait être conservé quel que soit le choix.

**Remarque hors périmètre.** À Longny, le nom « Mortagne-au-Perche » du fond
passe sur les signes. Ce sont les noms de villes qu'il faudra placer en
évitant les lieux, plus tard ; le fond n'est pas touché ici.

**Vérifié** à 1440 pixels, version topographique, sans erreur dans la console.
Non vérifié : mobile, thèmes encre et nuit.

## 12. Carte retenue ; passage à la composition générale (18 novembre 2026)

**Ce que décide le porteur.** La recherche cartographique est close à titre
provisoire. Sont retenus :

- le fond topographique ;
- la direction A′ « Gravure affinée » ;
- de petits carrés bleu d'encre pour les lieux hors ensemble ;
- les cercles numérotés pour les douze ensembles.

La validation reste provisoire : la carte doit être éprouvée avec les
interactions, filtres par époque et par métier compris.

**Ce qui est demandé.** Intégrer cette carte dans une vraie publication. L'esquisse
D reste la référence de fonctionnement : navigation, filtres combinables,
recherche, transitions et fiches. Sa grande colonne latérale permanente ne
convient pas. Deux pistes à expérimenter, indépendantes l'une de l'autre :

1. une carte immersive ;
2. un récit cartographique.

La réserve du porteur : avec des carrés aussi petits, l'effet des filtres risque
d'être peu perceptible. Il faut l'observer, sans refaire les symboles pour
l'instant. Les fiches, les infobulles et le récit complet ne sont pas à finaliser.

**Ce qui est fait.** Un dossier `prototype/composition/` à trois parties :

- `carte_a.js` : la carte retenue, dessinée exactement comme dans la carte seule
  et partagée par les deux pages.
- `mecanique.js` : la mécanique de l'esquisse D, reprise sans toucher à
  l'esquisse : état dans l'adresse, comptes, recherche, contenu des fiches.
  S'y ajoute une phrase calculée qui dit en texte ce que la carte montre.
- les deux pages, `immersive.html` et `recit.html`.

Les esquisses, la carte seule et ses variantes restent intactes.

*Composition 1, la carte immersive.* La carte occupe tout l'écran. Le titre et un
texte d'arrivée sont posés à gauche, sur la carte. Le texte se replie dès la
première action et peut être rouvert. En bas, un pupitre flottant réunit :

- la phrase calculée ;
- six colonnes d'époque, chacune avec une petite barre proportionnelle à son
  nombre de lieux ;
- un sélecteur de métier qui s'ouvre au-dessus.

La recherche est en haut à droite, le zoom à droite et une légende courte en bas
à gauche. Ouvrir la Risle ou Crulai fait descendre la carte sur l'ensemble et y
fait apparaître ses lieux. Sa présentation remplace alors le texte d'arrivée.

*Composition 2, le récit cartographique.* La page s'ouvre sur une une
éditoriale : grand titre, chapô, texte d'introduction et trois chiffres. La carte
vient ensuite, en pleine planche, à la hauteur de l'écran. Un cartouche, en haut
à gauche, donne le titre de la vue et la phrase calculée ; il change avec les
filtres. Une bande en pied de planche lit les époques comme une règle graduée,
avec une jauge par époque, et les métiers comme un index. Sous la carte viennent
les douze ensembles, présentés en index, puis la façon de lire la carte et les
sources. Pour ne pas piéger le défilement de la page, la molette ne zoome la
carte que lorsque la planche occupe l'écran.

**Ce que les filtres font sur la carte, dans les deux pages.** Les choix de
représentation sont les suivants :

- un carré écarté par le filtre s'efface à 14 % d'opacité ;
- un cercle d'ensemble se resserre sur son nouvel effectif, et son chiffre
  change ;
- un filet pointillé garde la taille entière du cercle ;
- un ensemble vide ne garde que son filet, et son nom s'estompe.

Tout est animé en un peu plus d'une demi-seconde. Ce sont des choix de
comportement, pas une refonte des symboles.

**Premier constat sur la réserve du porteur**, observé à 1440 pixels. Exemple :
textile, entre 1850 et 1913, dans la population des 321 lieux. La phrase annonce
65 lieux, dont 14 hors ensemble. Le changement se lit d'abord dans les cercles,
qui rétrécissent et changent de chiffre. Les carrés retenus restent lisibles,
mais leur petit nombre et leur taille rendent leur disparition moins
spectaculaire que celle des cercles. C'est une observation, pas un jugement :
c'est au porteur d'en juger dans la page.

**Vérifié** à 1440 pixels sur les deux pages, sans erreur dans la console :

- filtres par époque et par métier, et leur combinaison ;
- adresse partageable ;
- descente dans la Risle et ouverture d'une fiche ;
- index des ensembles du récit.

Non vérifié : mobile, clavier de bout en bout, lecteur d'écran.

## 13. Les deux compositions écartées ; proposition « édition » (18 novembre 2026)

**Le jugement du porteur.** Aucune des deux compositions n'est retenue en l'état.

- La carte immersive est jugée déséquilibrée. Ses blocs de texte sont
  rectangulaires et la carte y est mal intégrée. Le bandeau de filtres est
  imposant, et les éléments flottants paraissent posés les uns à côté des
  autres.
- Le récit a une intention éditoriale plus nette. Mais il sépare trop
  l'introduction, la carte et l'exploration. Les métiers y deviennent presque
  invisibles et les époques sont peu mises en valeur. Les ensembles y sont
  relégués dans une présentation de répertoire.
- Dans les deux cas, la qualité artistique reste en dessous des attentes.

**Le constat le plus grave : une régression.** Plusieurs acquis de l'esquisse D
ont été perdus. Le plus net touche la navigation vers les ensembles. Dans les
deux compositions, ouvrir la Risle ne faisait qu'agrandir la carte de l'Orne.
Dans l'esquisse D, on quittait l'Orne pour une carte propre à l'ensemble :
autre relief, communes, eau orientée, bourgs et relations, avec un cadrage
borné. C'est une erreur de notre part : la mécanique de D avait été reprise
pour les filtres, pas pour la descente d'échelle.

**Ce qui est demandé.**

- Une nouvelle proposition, indépendante des précédentes. Elle part de la
  logique de D et de la carte topographique.
- La descente d'échelle de D est rétablie.
- Les époques et les métiers retrouvent une présentation travaillée.
- Le changement doit se voir quand on choisit une époque.
- Une composition, pas un assemblage de composants.
- Bureau seulement ; le mobile viendra plus tard.

**La proposition** est dans `prototype/edition/` et compte trois fichiers :

- `carte_departement.js`, la carte A′ ;
- `carte_ensemble.js`, la vue propre d'un ensemble ;
- `index.html`, la page.

Elle lit les mêmes données que les esquisses. Elle ne touche ni aux esquisses,
ni à la carte seule, ni aux deux compositions précédentes.

*Une seule surface.* La marge de texte et la carte ne sont plus deux blocs. La
page a une couleur de papier unique, et la carte n'a pas de cadre :

- hors du département, le relief passe sous un voile de la couleur de la page ;
- sur la gauche, la page s'éclaircit progressivement jusqu'à la marge ;
- en bas, elle laisse place à la frise ;
- en haut, elle s'efface légèrement sous la légende.

Le texte se pose sur le papier, sans encadré ni fond blanc. Rien ne flotte
au-dessus de la carte à part la légende et les trois boutons de cadrage. Le
nom d'un lieu survolé ou choisi s'écrit sur la carte même, sans bulle.

*La marge* est le texte de ce que la carte montre, quel que soit le niveau.

- Département. On y trouve la recherche, le titre et un chapô court. Vient
  ensuite la phrase calculée, ouverte par un grand chiffre, puis l'index des
  métiers. Les deux ensembles construits sont nommés dans la phrase d'arrivée,
  avec un lien vers chacun.
- Ensemble. La présentation, trois repères chiffrés, la phrase calculée,
  l'index des métiers de l'ensemble et les relations documentées, chacune en
  toutes lettres. Un clic sur une relation la met en évidence sur la carte.
- Lieu. Une note sommaire : métier, nom, commune, époques documentées,
  texte, précision de localisation et lien vers le dossier. Un fil de retour
  la précède : l'Orne, puis l'ensemble. Il n'y a plus de fiche flottante sur
  la carte.

*Les métiers* sont un index. Chaque ligne porte un trait fin à la longueur de
son nombre de lieux. Quand une époque est choisie, la part de cette époque
s.encre sur le trait et le nombre devient, par exemple, « 36 / 76 » pour le textile
entre 1789 et 1849.

*Les époques* forment une frise sous la carte. Chaque époque est une colonne de
petits carrés, **un carré par lieu**, du même signe que les lieux de la carte.
Choisir un métier encre les carrés qui le concernent, et le reste demeure en
gris clair. La colonne choisie s'encre en entier, avec un axe épaissi ; les
autres pâlissent. Un bouton « Traverser le temps » fait défiler les six
époques. Les comptes se lisent ainsi : dans la population des 321 lieux, de 67
lieux avant 1789 à 261 entre 1850 et 1913. Un lieu documenté sur plusieurs
périodes compte dans chacune.

*Ce qui change pour les lieux isolés quand on filtre.* Les symboles ne sont pas
refaits, mais leur comportement change :

- un lieu écarté ne s'efface plus : il se réduit à une petite trace pâle, qui
  garde la mémoire de sa place ;
- un lieu qui entre dans la sélection est signalé par une onde brève, un carré
  qui s'élargit et s'éteint.

On voit ainsi ce qui apparaît et ce qui se retire d'une époque à l'autre. Les
cercles d'ensemble gardent leur comportement : ils se resserrent sur leur
effectif, et un filet garde leur taille entière.

*La vue d'ensemble*, pour la Risle et pour Crulai et Chandai, est une autre
carte. Au clic, la carte de l'Orne plonge vers l'ensemble et s'efface ; la vue
de l'ensemble s'approche et apparaît. Elle montre :

- le relief de l'ensemble, plus fin que celui du département, dans les mêmes
  teintes que la carte A′ ;
- les forêts publiques ;
- les communes qui portent un lieu, en pleine lumière, le reste sous un voile ;
- les limites communales en pointillé ;
- l'eau, orientée vers l'aval d'après le relief ;
- les bourgs et les lieux, du même signe carré ;
- les relations documentées, en pointillé couleur rouille.

Le cadrage et les déplacements restent bornés au territoire de l'ensemble,
comme dans D. La carte de l'Orne et les autres ensembles ne sont plus visibles.

*Au fil de la Risle.* Pour la Risle seulement, le courant est animé, comme dans
les esquisses B et D, et un rail permet de descendre la vallée de l'amont vers
l'aval. Ce rail se manipule au bouton, au glisser ou aux flèches du clavier. La
caméra suit l'axe de la vallée, et le lieu le plus proche est nommé sur la
carte et décrit dans la marge. Le sens amont-aval est calculé depuis le relief.
Crulai et Chandai n'a pas cette animation : le porteur ne demande pas de la
généraliser.

**Vérifié** à 1440 × 900 pixels, sans erreur dans la console :

- l'arrivée sur la carte de l'Orne, la marge tenant dans la hauteur ;
- les filtres par métier, par époque et combinés. Exemple : textile entre 1850
  et 1913 donne 65 lieux, dont 14 hors ensemble, dans la population des 321
  lieux ;
- l'adresse partageable ;
- l'ouverture de la Risle et de Crulai dans leur vue propre, puis le retour à
  l'Orne avec les filtres conservés ;
- l'ouverture d'un ensemble à venir ;
- un lieu isolé ;
- un lieu de la Risle ouvert depuis l'Orne alors qu'un filtre l'écartait : les
  filtres se lèvent ;
- la descente de la Risle ;
- la traversée du temps.

**Non vérifié.** Les transitions n'ont pas été observées en mouvement : le
navigateur de contrôle suspendait les animations quand son panneau n'était pas
au premier plan. Seuls leurs états de départ et d'arrivée ont été contrôlés. Ne
sont pas vérifiés non plus le mobile (hors champ), le clavier de bout en bout et
le lecteur d'écran.

## 14. « Édition » retenue comme base ; affinement de la page d'accueil (19 novembre 2026)

**Le jugement du porteur.** La proposition « édition » est retenue comme base de
travail. La marge sans séparation rigide fonctionne. La carte reste dominante,
la recherche est bien placée et la frise est bien intégrée. Il manque encore du
contraste et du dynamisme. Plusieurs commandes ressemblent à de l'information
imprimée et ne se lisent pas comme des commandes.

**Périmètre strict** : la page d'accueil, dans sa vue départementale. Les vues
d'ensemble, les fiches de lieux et leurs interactions ne sont pas touchées. Une
seule réserve : l'index des métiers et la frise des époques sont communs à
toutes les vues. Leur nouveau traitement apparaît donc aussi dans les vues de
la Risle et de Crulai, sans autre changement à ces vues.

**Version de référence.** L'état d'avant la passe est conservé tel quel dans
`prototype/edition_reference/`, pour la comparaison.

**Ce qui a changé.**

*Une couleur d'accent.* Un rouge brique discret (`#b0482a`), proche de celui
des relations documentées, marque ce qui est interactif et ce qui est choisi.
Il ne sert jamais à la carte elle-même.

*L'introduction.* Elle est courte à l'arrivée, avec un lien « Lire la suite »
qui déplie le reste sans déplacer la composition. Le texte reste provisoire et
sera réécrit plus tard. La mention « deux ensembles ont déjà leur propre carte »
est retirée : c'était une information de développement.

*Le corpus en chiffres.* Une bande légèrement teintée, sans cadre, porte trois
chiffres, calculés sur la sélection dans la population des 321 sites :

- les sites industriels ;
- les ensembles qui en comptent au moins un ;
- les sites hors ensemble.

Sans sélection, on lit 321, 12 et 149. Avec le textile entre 1850 et 1913, on
lit 65 « sur 321 », 8 et 14. Quand un chiffre change, il défile jusqu'à sa
nouvelle valeur en une demi-seconde et s'éclaire un instant en brique. Sous les
chiffres, la sélection en cours s'affiche en pastilles. Chaque pastille se
retire d'un clic, et la ligne nomme l'ensemble le plus fourni. Sans sélection,
une phrase invite à choisir.

*Les métiers.* Chaque état se distingue désormais :

- au repos, une courte invitation : « Choisir un métier pour le voir sur la
  carte » ;
- au survol, un fond léger et un carré qui se teinte ;
- une fois choisi, un fond plus soutenu, un filet brique à gauche, un carré
  plein et le trait de proportion en brique, les autres métiers pâlissant ;
- un lien « × tous les métiers » ramène à l'ensemble.

Le fonctionnement des filtres combinés est inchangé.

*La frise.*

- L'en-tête invite : « Choisir une période pour la voir sur la carte, ou »,
  suivi d'un bouton « Traverser le temps » à pastille brique.
- Les colonnes sont plus hautes et les effectifs plus grands : la différence de
  volume entre les périodes, de 67 à 261 sites, se voit mieux.
- Les dates sont en encre pleine.
- Au survol, une colonne prend un fond léger et ses carrés s'encrent.
- La colonne choisie garde un fond plus soutenu, avec un axe et un effectif en
  brique.

*La légende.* Elle devient un vrai bloc, titré « Légende », avec des symboles
plus grands :

- « Site industriel », un carré bleu d'encre. L'expression « lieu isolé »,
  propre à notre classement interne, n'est plus employée.
- « Ensemble », deux cercles numérotés : plusieurs sites proches, et le chiffre
  donne leur nombre.

Un bouton « ? » ouvre une aide. Elle explique qu'à l'échelle du département,
des sites très proches se superposeraient, et qu'ils sont donc réunis sous un
cercle. Elle précise qu'un ensemble est un regroupement fait pour la lecture de
la carte, pas forcément une organisation industrielle de l'époque. Les mentions
techniques (ensemble ouvert ou à venir, lieu écarté par la sélection) sont
retirées.

*Les sites sur la carte.* Le fond n'est pas touché. Les carrés sont un peu plus
grands, de 3,3 à 3,6 unités de base. Quand un filtre est actif, les sites
retenus grossissent encore d'un cinquième et les traces des sites écartés
pâlissent un peu plus. Les sites retenus tiennent ainsi face au fond. Les
transitions, onde comprise, sont conservées.

**Une remarque laissée au porteur.** Sur la carte, les cercles de la Risle et de
Crulai sont pleins, les dix autres sont clairs. Cette différence traduit l'état
de développement : seules deux vues sont construites. La légende ne l'explique
plus, et c'est voulu. Mais la carte la montre encore. Il faudra décider
d'unifier ces cercles quand les douze vues existeront, ou dès maintenant.

**Vérifié** à 1440 × 900 pixels, sans erreur dans la console :

- la marge tient dans la hauteur, sauf les crédits, qui demandent un
  défilement ;
- les chiffres, les pastilles et leur retrait ;
- les états des métiers et de la frise ;
- l'aide de la légende ;
- le retour depuis la Risle avec la sélection conservée ;
- une adresse partagée qui ouvre directement une période.

**Non vérifié.** L'animation des chiffres n'a été vue qu'à ses deux bouts : le
navigateur de contrôle ralentissait le rendu quand son panneau n'était pas au
premier plan. Le clavier de bout en bout et le lecteur d'écran ne sont pas
vérifiés non plus.

## 15. Continuité du fond topographique (19 novembre 2026)

**Le constat du porteur.** L'affinement de l'accueil est conservé. Il reste un
défaut. Hors de l'Orne, le relief, les rivières et les forêts s'arrêtent sur les
bords d'un rectangle visible, et cette coupure sépare la carte de la page.

**Pourquoi.** La carte seule avait extrait ses données sur une emprise juste
autour du département, de 0,98° ouest à 1,07° est et de 48,10° à 49,05° nord. La
composition « édition » affiche bien davantage, puisque la carte remplit toute
la page derrière la marge et la frise. Le bord de l'emprise venait donc à
l'écran.

**Deux solutions, et le choix.** Le porteur préfère prolonger le fond plutôt que
de le limiter au contour. Pour le prolonger sans étirer le relief, il fallait de
vraies données sur une emprise plus large. Ces données ont été demandées aux
mêmes sources IGN :

- le RGE ALTI, au même pas de 0,0075° ;
- la BD TOPO V3 : les rivières d'ordre 4 et plus, ainsi que les forêts
  publiques.

La nouvelle emprise va de 2,15° ouest à 1,80° est et de 47,60° à 49,45° nord. Le
relief passe ainsi de 274 × 127 à 528 × 247 cases. La grille est calée sur
l'ancienne : à l'intérieur, les altitudes déjà extraites sont reprises case pour
case. Il n'y a donc ni raccord ni recalcul, et rien n'est extrapolé.

- Le script `tools/fond_etendu_extraire.py` produit
  `prototype/edition/fond_etendu.js`, d'environ 3,5 Mo.
- Les réponses brutes sont archivées dans `data/raw/ign_fond_etendu/`, non
  versionné, avec leur empreinte.
- Les données de la carte seule ne sont pas modifiées.
- Sur le prolongement, on compte 21 680 tronçons de rivière et 183 forêts. Les
  rivières d'ordre 3 n'y sont pas reprises : elles n'apparaissent qu'à fort
  grossissement, quand on est dans l'Orne.

**Ce qui change à l'écran.**

- Le fond couvre toute la surface visible, sous le même voile couleur de page
  qu'avant. Le contour de l'Orne garde son trait et sa lisibilité.
- Le déplacement est borné à l'emprise des données. En glissant ou en
  éloignant au maximum, le bord n'arrive pas à l'écran.
- Par précaution, les quatre bords de l'emprise se fondent dans la page sur 90
  pixels.
- Les noms de forêts restent ceux de la carte seule : aucun nom n'apparaît hors
  du département.

**Ce qui ne change pas.** Le reste n'est pas touché : la direction artistique du
fond, les filtres, la frise, les métiers, la légende et les vues d'ensemble.
L'état d'avant cette correction est conservé dans
`prototype/edition_reference_affinage/`.

**Vérifié** à 1440 × 900 pixels, sans erreur dans la console :

- au cadrage d'arrivée ;
- au plus grand éloignement ;
- en faisant glisser la carte jusqu'à ses limites, vers le haut à droite puis
  vers le bas à gauche.

Aucune coupure rectangulaire n'apparaît.

**Limite.** Les déplacements programmés, comme le survol vers un ensemble à
venir, ne passent pas par cette borne. Ils restent dans le département, donc
loin des bords. Le chargement est un peu plus lourd.

## 16. La vallée de la Risle : découvrir les lieux sur la carte (20 novembre 2026)

**La demande du porteur.** La composition générale est retenue. On passe à
l'exploration des ensembles, en commençant par la Risle. Le défaut principal :
choisir un site remplaçait la présentation de la vallée, dans la marge, par la
fiche du lieu. Le porteur veut que la marge présente la vallée et que la
découverte des établissements se fasse sur la carte. Il demande aussi :

- de retrouver les photographies documentaires ;
- de rendre la descente de la rivière plus lisible et plus expressive ;
- d'articuler la descente avec la traversée du temps ;
- de rendre accessibles les sites serrés autour de L'Aigle.

Ni l'accueil ni les autres ensembles ne doivent changer.

**Version de référence.** L'état d'avant cette passe est conservé dans
`prototype/edition_reference_fond/`.

**Ce qui a changé, pour la seule Risle.** Le comportement est réservé à une
liste de vues, qui ne contient que la Risle. Crulai et Chandai garde son
fonctionnement antérieur.

*La marge reste à la vallée.* Titre, nom de travail, introduction courte avec
« Lire la suite », repères chiffrés, phrase calculée, métiers et relations
documentées. Le texte reste provisoire. Choisir un site ne la remplace plus.

*Deux niveaux sur la carte.*

- **Au survol**, une petite bulle donne une vignette, le métier, le nom et la
  commune. Si plusieurs sites sont superposés sous le pointeur, elle annonce
  « 3 sites ici » et invite à cliquer.
- **Au clic**, une fiche se pose à côté du lieu, du côté où elle tient. Elle ne
  déborde ni sur la marge, ni sur la frise, ni sur la ligne de la rivière. Elle
  se déplace avec la carte. Elle contient :
  - la photographie avec sa légende, son crédit et le lien vers sa notice ;
  - les métiers, le nom, la commune et le lieu-dit ;
  - les dates extrêmes trouvées dans les sources, par exemple « de 1825 à
    1968 » pour la tréfilerie d'Échauffour ;
  - la barre des époques et le nombre d'activités successives ;
  - l'historique, avec « Lire la suite » ;
  - les relations documentées qui concernent ce site ;
  - la chronologie sourcée, repliée ;
  - le lien vers le dossier d'inventaire et la précision de localisation.
- **Sans photographie** (un seul site de la Risle sur 43), la fiche commence
  directement par le texte, sans image de remplacement.
- **Au clavier**, la liste textuelle des lieux ouvre la même fiche. Le focus
  va au bouton de fermeture, Échap ferme la fiche et rend le focus.

*Les photographies.* Ce sont les médias documentaires déjà inventoriés pour 42
des 43 sites, tous de la Région Normandie, Inventaire général, publiés sur la
plateforme POP du ministère de la Culture. Ils sont affichés comme aperçus
distants crédités, avec la mention « aperçu à usage interne ». Aucune image
n'est téléchargée ni versionnée, conformément à la règle du projet : une image
en ligne n'est pas une autorisation. Une publication demandera de documenter
les droits de chaque photographie.

*Les sites serrés autour de L'Aigle.* Rien n'est déplacé.

- Le grossissement maximal passe de 6 à 16 fois le cadrage de l'ensemble, et le
  double clic rapproche.
- Un clic sur plusieurs sites superposés ouvre une liste de choix, par exemple
  six sites à L'Aigle au cadrage initial.
- Le bouton « Rapprocher pour les distinguer » calcule le grossissement qui
  sépare les deux sites les plus proches du groupe. À L'Aigle, la filature et
  la manufacture de quincaillerie sont à 38 mètres l'une de l'autre. Il faut
  donc aller jusqu'au maximum, et les six sites deviennent alors cliquables un à
  un, à 15 pixels au moins d'écart.

*La descente de la Risle.* La réglette du haut devient une ligne de rivière.

- Chaque site y est une étape, à pas égal, de l'amont vers l'aval. Les communes
  sont nommées sous leurs étapes quand la place le permet. La partie parcourue
  est d'un bleu plein, et l'étape courante est marquée en brique.
- La descente va de site en site, au lieu d'un glissement continu. La carte se
  rapproche du site, l'entoure d'un anneau brique et ouvre une bulle d'étape :
  photographie, métier, nom, commune, première phrase de l'historique,
  « Ouvrir la fiche » et « Site suivant ». Après environ 3,6 secondes, elle
  passe au site suivant.
- Les commandes permettent de démarrer, d'interrompre, de reprendre, d'aller au
  site précédent ou suivant, et de quitter. Un clic sur une étape de la ligne y
  conduit.
- Ce pas à pas évite les à-coups du glissement continu de l'esquisse B, qui
  recalculait la caméra à chaque image. Le courant animé de la rivière est
  conservé.

*Une seule lecture automatique à la fois.*

- Lancer « Traverser le temps » met la descente en pause et ferme sa bulle. La
  descente reste à sa place.
- Reprendre la descente arrête la traversée du temps. La période où celle-ci
  s'est arrêtée reste choisie.
- La descente ne visite que les sites retenus par les filtres, par exemple « 33
  sites » entre 1789 et 1849. Si le site courant sort de la sélection, elle se
  place sur le site retenu suivant en aval. La ligne grise les étapes écartées.
- Il n'y a jamais qu'une bulle à la fois. Ouvrir une fiche met la descente en
  pause, et Échap referme dans l'ordre : le choix, la fiche, la descente, puis
  la vue.

*Placement.* La légende de la Risle descend en bas à droite pour laisser le haut
à la ligne de la rivière.

*Largeur réduite.* Sous 1 280 pixels, la frise des époques se resserre au lieu de
déborder. Cette règle vaut aussi pour l'accueil.

**Vérifié** à 1440 × 900 et à 1100 × 760 pixels, sans erreur dans la console :

- l'arrivée dans la Risle ;
- le survol, avec sa vignette ;
- le clic et la fiche complète, avec et sans photographie ;
- le groupe de L'Aigle et son rapprochement ;
- la descente : démarrage, pause pendant un trajet, reprise, fiche ouverte
  depuis une étape, Échap ;
- le passage de la descente à la traversée du temps, puis le retour ;
- le retour à l'Orne et Crulai inchangé.

**Non vérifié.** Les écrans tactiles, le lecteur d'écran et le mobile (hors
champ) ne sont pas testés. L'animation des déplacements n'a été vue que par
instantanés.

## 17. Risle : descente allégée, survol fiabilisé (20 novembre 2026)

**La demande du porteur.** Deux corrections seulement.

- La descente est plus lisible, mais son cadre, ses cercles et sa ligne droite
  la rendent rigide et utilitaire.
- Certains sites ne réagissent pas au survol.

Le reste ne change pas. La version d'avant est conservée dans
`prototype/edition_reference_risle/`.

**Le survol : deux causes trouvées.**

1. **Le délai d'apparition repartait de zéro** à chaque mouvement de souris.
   Tant que le pointeur bougeait, même d'un pixel, la bulle n'apparaissait pas.
   Les sites où l'on s'arrête net semblaient marcher, les autres non. Désormais,
   la carte ne prévient la page que lorsque ce qui est sous le pointeur change.
   Une bulle déjà ouverte se met à jour aussitôt. L'attente de 60 millisecondes,
   qui évite d'allumer une bulle quand le pointeur ne fait que traverser, n'est
   plus relancée quand on passe d'un site à son voisin dans un groupe serré.
2. **Une règle masquait la bulle** dès que le lieu approchait du bord de la zone
   libre de la carte. Après un zoom, c'était le cas de nombreux sites. La bulle
   n'est désormais masquée que si le lieu sort de la fenêtre ; elle reste par
   ailleurs recadrée pour ne pas être coupée.

**Le reste du comportement.**

- Un filtre referme la bulle de survol et la liste de choix en cours. Les sites
  écartés ne sont jamais détectés sous le pointeur.
- Pendant un glisser, le survol se tait.
- Le curseur devient une main pointée sur un site et une main fermée pendant le
  glisser. Il reste la flèche ordinaire sur les zones non interactives, au lieu
  de la main ouverte permanente d'avant.

**Mesure du survol.** Elle simule un pointeur qui s'approche, puis bouge encore
un peu sur le site.

| Cas | Sites visibles testés | Bulle affichée | Avant la correction |
| --- | --- | --- | --- |
| Cadrage d'arrivée | 43 | 43 | 35 |
| Zoom ×5 sur L'Aigle | 21 | 21 | 20 |
| Rapprochement maximal à L'Aigle | 14 | 14 | non mesuré |
| Filtre textile | 6 | 6 | non mesuré |

Les huit échecs d'avant, au cadrage d'arrivée, étaient tous dans les groupes
serrés de L'Aigle. Sous filtre, aucun des sites écartés ne réagit au survol :
19 sites testés avec le filtre métallurgie, 34 avec la période d'avant 1789.
Après un survol, le clic ouvre la fiche et ferme la bulle courte. Un contrôle
avec la vraie souris confirme le comportement.

**La descente allégée.** L'ordre des lieux, les commandes et la logique de
progression ne changent pas.

- Plus de cadre ni d'ombre : un voile de papier très doux, qui s'efface sur les
  bords, assure seulement la lisibilité au-dessus de la carte.
- Le bouton de lecture devient un petit cercle brique au trait fin, plein
  quand la lecture tourne.
- Le titre et l'état tiennent sur une ligne, et les commandes deviennent du
  texte : « ‹ précédent · suivant › · quitter ».
- La ligne ondule doucement, comme l'eau, avec une amplitude de 3 pixels. Elle
  est fine et pâle en entier ; la partie parcourue est d'un bleu plus épais.
- Les étapes deviennent de petits points sans contour : encre atténuée à
  venir, bleu une fois passées, à peine visibles si les filtres les écartent.
  L'étape courante est un point brique avec un halo fin. Le nom de sa commune
  se renforce.
- À la fin, la lecture s'arrête sur « fin de la descente », et le bouton
  propose de recommencer.

**Vérifié** à 1440 × 900 pixels, sans erreur dans la console :

- la descente du début à la fin ;
- la pause et la reprise ;
- le survol et le clic le long de la vallée, autour de L'Aigle, et après un
  filtre par époque et par métier.

**Non vérifié.** Les écrans tactiles et le lecteur d'écran.

## 18. Risle : la vraie cause de la panne du survol (20 novembre 2026)

**Le retour du porteur.** Le survol à la souris ne marche que pour un ou deux
sites, alors que les points de la ligne de la rivière répondent bien.

**Ce que la section 17 avait manqué.** Les deux défauts qu'elle a corrigés
étaient réels, mais ce n'était pas la panne principale.

- **La panne.** Un clic sur un point où plusieurs sites se superposent ouvre une
  liste de choix. Tant que cette liste restait ouverte, le survol était coupé
  sur toute la carte, et rien ne la refermait si l'on allait ailleurs. Au
  cadrage d'arrivée, 18 survols sur 43 tombent sur de tels groupes : le premier
  clic un peu au hasard suffisait à tout bloquer. Les mesures de la section 17
  survolaient sans jamais cliquer d'abord, ce qui a masqué le défaut.
- **Un facteur aggravant.** Le serveur local ne disait rien du cache, si bien
  que le navigateur pouvait garder d'anciennes copies des scripts après une
  modification. La panne a d'ailleurs été reproduite ainsi : une ancienne
  version restée en cache, puis un clic sur le groupe de L'Aigle, puis plus
  aucune bulle.

**Les corrections.**

- Une liste de choix ouverte ne bloque plus que le survol de ses propres sites.
- La bulle courte s'ouvre aussitôt, sans minuterie que le navigateur pourrait
  retarder.
- Les scripts de la page portent un numéro de version, et un serveur local qui
  interdit le cache est ajouté : `tools/serveur_prototypes.py`.

**Vérifié** à 1440 × 900 pixels, à la vraie souris puis par pointeur simulé sur
chaque site visible :

| Situation | Sites survolés | Bulle affichée |
| --- | --- | --- |
| Rien d'ouvert | 43 | 43 |
| Liste de choix ouverte | 18 | 18 |
| Fiche ouverte | 10 | 9 |
| Descente en pause | 29 | 28 |

Ne sont pas comptés les sites couverts par la bulle ouverte. Les deux seuls
sites sans bulle de survol sont ceux qui ont déjà leur fiche ou leur bulle
d'étape à l'écran, ce qui est voulu.

## 19. Risle : le décalage entre les carrés visibles et la souris (20 novembre 2026)

**Le retour du porteur.** Même après la section 18, poser le curseur sur un
carré ne déclenche rien.

**La cause, trouvée dans le Chrome du porteur.** La carte de la Risle était
dessinée sur une surface plus petite de 7 % que l'écran, puis étirée pour le
remplir.

- **D'où vient l'écart.** L'arrivée dans un ensemble est animée par un léger
  rapprochement en CSS : la vue part de 93 % de sa taille. Or la carte mesurait
  sa surface de dessin avec la taille affichée, réduite à 93 %, au lieu de sa
  taille de mise en page. Elle le faisait une fois pour toutes, à sa création,
  pendant que la vue était encore réduite.
- **Ce que voyait le porteur.** Les carrés apparaissaient environ 7 % plus loin
  du coin supérieur gauche que l'endroit où la page attendait la souris. Près de
  ce coin, l'écart était nul ; ailleurs, il dépassait la zone de détection.
  D'où « un ou deux sites » qui répondaient.
- **Pourquoi les vérifications précédentes ne l'ont pas vu.** Elles visaient
  les positions calculées par la page elle-même : elles étaient cohérentes avec
  la détection, mais pas avec le dessin. Elles prouvaient donc la cohérence du
  code avec lui-même, pas ce que voit le lecteur. Les sections 17 et 18
  annonçaient à tort un survol réparé. Leurs corrections restent utiles, mais
  ne traitaient pas la panne vue par le porteur.

**La correction.** Les deux cartes, celle de l'Orne et celle de l'ensemble,
mesurent désormais leur surface sur la taille de mise en page, que les effets
de zoom en CSS ne modifient pas. La position de la souris est ramenée dans le
repère de dessin, même pendant une animation. Les scripts passent à la version
`20261120d`.

**Vérifié dans le Chrome du porteur**, en 1664 × 921 pixels.

- La surface de dessin mesure maintenant 1664 pixels, comme l'écran, contre
  1548 avant. C'est vrai à l'arrivée directe comme à l'arrivée par un clic
  depuis l'Orne.
- Les carrés ont été repérés à l'œil sur une capture, sans passer par les
  calculs de la page, puis survolés avec la vraie souris. La tuilerie, en
  haut de la vallée, et l'usine Eurofac de Rai ont réagi : bulle affichée et
  curseur en main.

C'est désormais la règle : un contrôle d'interaction vise ce qui est visible à
l'écran, pas une position fournie par le code contrôlé.

## 20. Crulai et Chandai rejoint le fonctionnement de la Risle (20 novembre 2026)

**La demande du porteur.** Les deux ensembles en test doivent fonctionner de la
même façon. Dans Crulai et Chandai, le survol encadrait bien le carré, mais
aucune bulle n'apparaissait : cet ensemble avait été laissé hors de la passe de
la Risle, à la demande du 20 novembre.

**Ce qui change.** Crulai et Chandai entre dans la liste des vues où la
découverte se fait sur la carte. Il reçoit :

- la bulle au survol ;
- la fiche au clic, posée près du lieu ;
- la liste de choix pour les sites superposés ;
- l'introduction courte avec « Lire la suite » ;
- la légende en bas à droite.

Ses sept sites ont tous une photographie documentaire, affichée comme aperçu
crédité à usage interne. La descente au fil de l'eau reste propre à la Risle :
le porteur avait demandé de ne pas la généraliser.

**Vérifié dans le Chrome du porteur**, en 1664 × 921 pixels. Les sept carrés ont
été repérés à l'œil sur une capture, puis survolés à la vraie souris : 7 bulles
sur 7. Le clic sur la tréfilerie dite la Fabrique, à Chandai, ouvre sa fiche
sur la carte, et la marge reste à l'ensemble.

## 21. Risle : les liens entre établissements, la zone chiffrée (20 novembre 2026)

Le porteur valide le survol. Il demande deux améliorations sur la Risle.

- Les relations documentées doivent devenir des portes d'entrée
  cartographiques.
- La zone chiffrée doit reprendre le langage de l'accueil, sans faire bouger la
  colonne.

L'état d'avant est conservé dans `prototype/edition_reference_crulai/`.

**Les données vérifiées.** La Risle compte cinq relations, relues avec la
décision du 29 juillet 2026 sur l'extraction des relations.

| Lien | De | Vers | Fiabilité |
| --- | --- | --- | --- |
| Approvisionnement | tréfilerie Boisthorel, Rai | usine Eurofac, Rai | forte |
| Approvisionnement | tréfilerie Boisthorel, Rai | usine de matériel d'équipement industriel, Rai | forte |
| Transfert de production | tréfilerie de la Fonte, Saint-Sulpice | « l'usine de Saint-Sulpice » | moyenne |
| Transfert de production | laminoir du Moulin à Tan, Saint-Sulpice | « l'usine de Saint-Sulpice » | moyenne |
| Transfert de production | tréfilerie des Bouviers, Saint-Sulpice | « l'usine de Saint-Sulpice » | moyenne |

Les trois transferts sont enregistrés vers l'usine de quincaillerie. Mais le
journal du 29 juillet les marque comme interprétés : la source dit « l'usine de
Saint-Sulpice-sur-Risle » sans la nommer, et la commune compte cinq sites. **La
carte les traçait pourtant comme des liens certains**, en trait vers une usine
précise. C'est corrigé.

**Ce que fait un lien choisi.**

- Dans la colonne, la ligne prend le fond et le filet brique des métiers
  choisis, et les autres liens pâlissent.
- La carte se cadre sur les établissements concernés, avec un grossissement
  adapté à leur écart. Elle va jusqu'à dix fois le cadrage de l'ensemble pour
  Boisthorel et ses deux voisines de Rai.
- **Lien attesté** : un trait brique plein relie les deux établissements, avec
  une pointe de flèche orientée du fournisseur vers le destinataire, selon la
  règle d'orientation du projet. Les deux sites sont cerclés et nommés.
- **Destinataire incertain** : aucun trait. Le site d'origine est cerclé en
  plein, et les quatre autres établissements de Saint-Sulpice-sur-Risle,
  destinataires possibles, sont cerclés en pointillé. La colonne l'explique en
  toutes lettres. La règle est appliquée à toute relation de fiabilité autre
  que forte. Pour la Risle, ce sont exactement les trois liens marqués comme
  interprétés.
- Le reste de la carte s'atténue sans disparaître. Les bulles et les fiches
  restent accessibles, y compris sur les sites de la relation, qui reste alors
  affichée.
- **Sortie** : recliquer le lien, le bouton « × toute la vallée » ou Échap.
  La vallée revient alors en entier.
- La descente de la Risle et la sélection d'un lien ne coexistent pas : lancer
  la descente efface le lien, et choisir un lien met la descente en pause.
- Si un filtre écarte un des établissements, la ligne le signale, sans changer
  de hauteur.

**Le titre.** « Ce que les sources relient » devient « Les liens entre
établissements ». Une ligne le suit : « Tels que les sources les décrivent ».
Chaque lien porte sa nature (approvisionnement, transfert de production) et son
degré de certitude (lien attesté, destinataire incertain), pour ne pas laisser
croire que toutes les relations prouvent la même chose. « D'un établissement à
l'autre » a été écarté : la formule suggère un flux même pour un simple
transfert dont la cible est inconnue.

**La zone chiffrée.** Elle reprend la bande teintée, les chiffres et les
pastilles de l'accueil.

- **Les repères fixes** — 43 lieux documentés, 10 communes, première date
  connue 1440 — passent sur une ligne discrète au-dessus de la bande. Ils ne
  changent jamais.
- **Les chiffres recalculés** suivent les filtres avec le même défilement et le
  même éclat brique : les sites retenus (« sur 43 »), les communes concernées et
  les métiers représentés. Exemple : métallurgie entre 1850 et 1913 donne 23
  sites, 7 communes et 4 métiers.
- **Les métiers représentés** comptent tous les métiers des sites retenus. Un
  site peut en avoir plusieurs, d'où 4 métiers même avec le seul filtre
  métallurgie.
- **Les pastilles** des filtres actifs se retirent une à une. Une ligne nomme la
  commune la plus fournie, par exemple « L'Aigle (6) ».

**La stabilité de la colonne.** La bande garde une hauteur minimale, et l'aide
des métiers garde sa place quand un métier est choisi, au lieu de disparaître.
Cette seconde règle vaut aussi pour l'accueil. Mesure dans Chrome sur six
états successifs (sans filtre, période, période et métier, retrait de l'un,
puis de l'autre, métier seul) : la zone chiffrée ne bouge pas, et la liste des
métiers comme celle des liens ne se déplacent pas de plus d'un pixel.

**Vérifié dans Chrome**, en 1664 × 921 pixels, sur les écrans réellement
affichés :

- les cinq liens, dont les cadrages et les tracés ont été vus à l'image ;
- le survol et le clic sur le laminoir pendant qu'un lien est choisi ;
- la sortie par Échap ;
- les six états de filtres.

Crulai et Chandai n'a pas de relation documentée et ne reçoit pas encore la
zone chiffrée : le porteur a demandé de commencer par la Risle.

## 22. Liens entre établissements : retour à la version d'avant, plus le zoom (20 novembre 2026)

**Le jugement du porteur.** Il rejette la partie « liens » de la section 21.

- Elle a supprimé des tracés qui fonctionnaient.
- Elle a remplacé des pointillés par des cercles.
- Elle a ajouté des textes que le lecteur n'a pas à lire : « la source ne nomme
  pas l'usine destinataire… », « Tels que les sources les décrivent », les
  étiquettes de nature et de certitude.

Les « sources » sont des notes de travail du projet, pas du contenu pour le
lecteur. La demande était seulement de zoomer sur le lien choisi. La consultation
des décisions du projet ne servait qu'à choisir le titre de la rubrique.

**Ce qui est rétabli, à l'identique de l'état d'avant la section 21.**

- Les cinq liens sont tracés en pointillé, le lien choisi en trait plein et les
  autres atténués.
- Chaque ligne de la liste reprend son texte d'origine, seul.
- Il n'y a plus de cercles, de pointe de flèche, d'atténuation des sites,
  d'étiquettes ni d'explications.

**Ce qui est gardé.**

- Le titre « Les liens entre établissements », accepté par le porteur, suivi de
  la seule consigne « Choisir un lien pour le voir sur la carte. ».
- La ligne choisie mise en évidence dans la colonne.
- Le zoom : un clic cadre la carte sur les deux établissements du lien.
- La sortie : recliquer le lien, le bouton « × toute la vallée » ou Échap.

La zone chiffrée de la section 21 n'est pas concernée et reste en place.

**Retiré de la section 21.** Le tableau des cinq liens et la remarque sur les
trois transferts vers Saint-Sulpice-sur-Risle restent dans cette section comme
constat de travail. Ils n'entraînent aucun changement d'affichage. S'il faut
rectifier ces liens, le porteur le décidera plus tard.

**Vérifié dans Chrome :**

- la liste et son titre ;
- les cinq tracés d'origine visibles au cadrage d'arrivée ;
- le zoom sur un lien de Rai et sur un lien de Saint-Sulpice-sur-Risle, vus à
  l'image.
