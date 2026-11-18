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
