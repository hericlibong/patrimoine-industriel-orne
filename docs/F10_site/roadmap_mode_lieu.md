# Mode lieu — roadmap

**Document de préparation, 20 septembre 2026.** Il ne remplace ni ne modifie le
suivi de la carte des ensembles, qui reste le document de la carte.

**Objet.** Ce que voit le lecteur lorsqu'il ouvre un lieu. Aujourd'hui, le
panneau du lieu est suivi du panneau de l'ensemble : le lecteur qui voulait
comprendre un lieu reçoit par-dessus tout ce qui concerne la vallée, la page
défile sans fin et la carte disparaît en laissant une demi-page blanche.

Le diagnostic complet est dans `2026-09-20_analyse_mode_lieu.md`.

---

## Décisions déjà prises par le porteur

| Décision | Date | Conséquence |
| --- | --- | --- |
| **Le mode lieu est un panneau court**, pas une page longue | 20 septembre | L'historique complet et la chronologie ne peuvent pas être ouverts par défaut |
| **Tout média inventorié est traité comme publiable** | 20 septembre | Le bloc média devient une phase de développement ordinaire ; la question des droits est tranchée par le porteur seul, au moment qu'il choisit |
| Le mot « lieu » dans l'interface, « site » réservé au technique | antérieure | Un écart subsiste à corriger, voir L2 |

**Conséquence directe du panneau court, à retenir pour tout le plan.** Sur le
lieu des captures, le texte de la notice fait douze lignes et la chronologie
onze événements. Seuls l'identité, le média et une amorce d'historique restent
ouverts ; tout le reste est replié.

## Décisions encore à prendre

Elles sont posées dans la phase où elles se jouent, avec une recommandation.
Aucune n'est tranchée par le code.

1. La liste « Choisir un autre lieu » suit-elle le filtre métier ? — phase L1.
2. La conservation est-elle toujours repliée, ou seulement quand elle est
   inconnue ? — phase L2.
3. Quel média s'affiche quand un lieu en compte plusieurs ? — phase L4.
4. L'adresse partageable entre-t-elle dans ce chantier ? — hors plan, voir fin.

---

## L1 — Structure et navigation du mode lieu

**Objectif.** Qu'ouvrir un lieu fasse réellement changer de mode : le panneau ne
parle plus que de ce lieu, et le lecteur peut en sortir.

- [x] Cesser d'ajouter le panneau de l'ensemble derrière le panneau du lieu.
- [x] Redonner dans le panneau du lieu un retour explicite vers l'ensemble,
      libellé avec le nom de l'ensemble. Formulation corrigée avant livraison :
      « ← Retour aux lieux — Vallée de la Risle », les douze ensembles ne
      prenant pas le même article.
- [x] Redonner l'accès aux autres lieux, en bloc replié et en dernier, avec le
      lieu courant amené à la vue à l'ouverture.
- [x] Masquer le sélecteur de métier en mode lieu, sans effacer le filtre en
      cours ; le retour à l'ensemble le rétablit tel quel.
- [x] Mettre le nom du lieu en titre de page, avec sa commune et son lieu-dit en
      sous-titre.
- [x] Vérifier que le cadrage de la carte ne bouge pas à l'ouverture d'un lieu.

**Bilan L1 — 20 septembre 2026.** Fait et mesuré dans un navigateur ; détail
dans `journal_mode_lieu.md`. La liste des autres lieux suit le filtre et indique
combien de lieux il masque — décision appliquée sur recommandation, le porteur
ne l'ayant pas tranchée ; elle se change en une ligne. Le panneau mesure encore
1 223 pixels : l'historique et la chronologie restent ouverts, c'est l'objet de
L2.

**Décision attendue du porteur :** la liste « Choisir un autre lieu » suit-elle
le filtre métier ? Trois règles possibles — suivre le filtre ; l'ignorer ;
le suivre en indiquant combien de lieux sont masqués. **Recommandation : la
troisième**, déjà en vigueur dans le panneau de l'ensemble, qui ne cache rien en
silence.

**Fichiers concernés :** `tools/vue_reference_gabarit.html` — assemblage du
panneau, `panneauSite`, `panneauSysteme` ; `prototype/vue_reference/index.html`
régénéré.

**Livrable visible.** Ouvrir un lieu affiche un panneau qui ne parle que de lui,
avec un retour nommé vers l'ensemble et un accès replié aux autres lieux.

**Critères de réception.**

- Plus aucun bloc de l'ensemble sous la fiche : ni repères, ni activités de la
  vallée, ni relations générales.
- Le retour à l'ensemble fonctionne au clic et au clavier, et restaure le filtre.
- Aucun cul-de-sac : depuis un lieu, on atteint toujours l'ensemble et un autre
  lieu.

**Contrôles.** Six contrôles du générateur vrais ; `ruff` propre ; syntaxe
JavaScript vérifiée par Node ; dans le navigateur, parcours ensemble → lieu →
autre lieu → retour, sans filtre et sous filtre.

- [x] **Validation du porteur, 20 septembre 2026.**

---

## L2 — Hiérarchie des contenus

**Objectif.** Que le panneau se lise dans l'ordre où l'on comprend : qui, puis
quoi, puis quand, puis avec quelles limites.

- [x] **Identité** — nom, commune et lieu-dit, activités écrites en clair, lien
      vers la fiche d'inventaire. Ouvert.
- [x] Sortir les activités de la grille de chiffres : un métier n'est pas un
      nombre et n'a pas sa place dans une case conçue pour un nombre.
- [x] Retirer les compteurs redondants : le nombre d'événements datés, répété
      par la chronologie, et le nombre d'activités, répété par leur liste.
- [x] **Historique documenté** — remplace « Ce que dit la notice ». Amorce
      visible, suite dépliable. Provenance discrète et honnête, du type
      « D'après la fiche d'inventaire », tant que le texte n'est pas réécrit.
- [x] **Chronologie** — après l'historique, repliée, sans zone de défilement
      propre. Remplace « Ce qui est daté » et « Événements extraits du texte de
      la notice ».
- [x] **Localisation et état des connaissances** — replié : précision
      géographique en formulation courte, distance au cours d'eau, conservation.
- [x] Ne jamais présenter la distance au cours d'eau comme une preuve d'usage de
      l'eau ; vérifier que le déplacement ne l'introduit pas.
- [x] Corriger le mot « site » dans le texte de précision de localisation, seul
      endroit de l'interface publique où il subsiste.

**Bilan L2 — 20 septembre 2026.** Fait et mesuré ; détail dans
`journal_mode_lieu.md`. Le panneau passe de 1 223 à 618 pixels. Deux défauts
corrigés au passage : un code brut `partiellement_conserve` affiché au lecteur,
et le mot « site » subsistant à quatre endroits de l'interface publique et non à
un seul. Le bloc de localisation s'ouvre quand la conservation est documentée —
décision appliquée sur recommandation, le porteur ne l'ayant pas tranchée.

**Décision attendue du porteur :** la conservation est-elle toujours repliée, ou
visible quand elle est documentée ? **Recommandation : repliée quand elle est
inconnue** — le cas de 315 lieux sur 318 — **et visible quand elle est connue**,
parce qu'une information établie mérite mieux qu'un pli.

**Fichiers concernés :** `tools/vue_reference_gabarit.html` — `panneauSite` et
les styles du panneau.

**Livrable visible.** Un panneau qui tient dans un écran courant à l'ouverture,
et se déplie à la demande.

**Critères de réception.**

- À l'ouverture, sur un écran de 900 pixels de haut, le panneau ne dépasse pas
  sans défilement interne autre que celui de la page.
- Chaque bloc replié s'ouvre au clic et au clavier, et son état est visible.
- Aucune information du panneau actuel n'a disparu : tout est atteignable.

**Contrôles.** Mesure de la hauteur du panneau replié, sur trois lieux de
longueurs de notice différentes ; parcours clavier de tous les blocs.

- [x] **Validation du porteur, 20 septembre 2026.**

---

## L3 — Comportement ordinateur et mobile

**Objectif.** Que la carte cesse de laisser une demi-page blanche, et que le
mode lieu reste lisible sur écran étroit.

- [x] Rendre la colonne gauche collante sur ordinateur : la carte reste visible
      pendant que le panneau défile.
- [x] Vérifier que l'ancrage collant ne s'applique pas sous 1180 pixels, où la
      page passe déjà à une colonne.
- [x] Vérifier sur écran étroit que la carte ne mange pas l'écran avant le
      panneau, et que l'ordre d'empilement sert la lecture.
- [x] Vérifier que le cartouche, l'échelle et les crédits de la carte se
      comportent en mode lieu comme en mode ensemble.

**Bilan L3 — 20 septembre 2026.** Fait et mesuré ; détail dans
`journal_mode_lieu.md`. La carte reste visible aux trois niveaux, panneau
entièrement déplié : 1 711 pixels de panneau, 1 249 de défilement, carte
toujours à l'écran. L'écran étroit a été éprouvé par contrainte de largeur, pas
dans une vraie fenêtre. Limite relevée : sur Crulai, dont le cadre est le plus
haut, le haut de la carte dépasse de quelques dizaines de pixels sur une fenêtre
de 833.

**Fichiers concernés :** `tools/vue_reference_gabarit.html` — mise en page de
`main` et de la colonne gauche.

**Livrable visible.** La carte accompagne la lecture du lieu au lieu de
disparaître ; plus aucune zone vide à gauche.

**Critères de réception.**

- Sur ordinateur, la carte reste visible quelle que soit la longueur du panneau.
- Sur écran étroit, aucun débordement horizontal, aucun élément coupé.
- Les parcours de la carte — survol, zoom, sélection — ne sont pas affectés.

**Contrôles.** Quatre largeurs de carte, comme pour le bloc D : 952, 580, 380 et
290 pixels. Vérification que rien de la carte n'a régressé.

- [ ] **Validation du porteur avant L4.**

---

## L4 — Médias

**Objectif.** Afficher une image lorsqu'un lieu en a une.

**Cadre posé par le porteur.** Tout média inventorié est traité comme publiable.
Aucune condition de droits n'est appliquée par le code. Le porteur décide seul,
au moment qu'il choisit, de ce qui part en ligne.

- [x] Transmettre les médias au prototype : ils ne sont pas dans les données
      générées aujourd'hui. C'est le vrai travail technique de cette phase.
- [x] Afficher un média dans le panneau lorsqu'il en existe un pour le lieu.
- [x] Afficher la légende et le crédit avec l'image — information, non
      autorisation.
- [x] N'afficher aucun cadre de remplacement, aucun pictogramme et aucun texte
      « image indisponible » pour les lieux sans média. Deux lieux sur 318 sont
      dans ce cas.
- [x] Vérifier qu'une image absente ou en erreur ne casse pas le panneau.

**Bilan L4 — 20 septembre 2026.** Fait et mesuré ; détail dans
`journal_mode_lieu.md`. Couverture : 42 lieux sur 43 pour la Risle, 7 sur 7 pour
Crulai. La base des adresses d'images n'était pas documentée : elle a été lue
dans les 117 adresses complètes de l'inventaire, puis vérifiée dans un
navigateur sur trois fichiers.

**Tension tranchée par le porteur, 20 septembre 2026 : l'image est repliable.**
Avec une image affichée, le panneau passait de 618 à près de 1 000 pixels et ne
tenait plus dans un écran. Repliée, il retombe à 629-733 pixels, sous le critère
de L2 ; dépliée, l'image s'affiche entière, sans borne de hauteur.

**Décision attendue du porteur :** quel média s'affiche quand un lieu en compte
plusieurs ? L'inventaire compte 1 900 médias pour 316 lieux, soit six ou sept
par lieu en moyenne. **Recommandation : celui que la source signale comme image
principale, avec repli sur le premier disponible** si la source n'en désigne
aucune.

**Fichiers concernés :** `tools/generer_vue_reference.py` — transmission des
médias ; `data/exports/medias_sites_v1.csv` — inventaire, en lecture seule ;
`tools/vue_reference_gabarit.html` — affichage.

**Livrable visible.** Une image en haut du panneau, avec sa légende et son
crédit, pour les lieux qui en ont une.

**Critères de réception.**

- Un lieu avec média l'affiche ; un lieu sans média ne montre aucun vide signalé.
- Légende et crédit sont présents dès qu'une image est affichée.
- Le panneau reste court : l'image ne repousse pas l'identité hors de l'écran.

**Contrôles.** Un lieu avec média, un lieu sans, un média dont l'adresse échoue.
Vérification que le poids de la page reste tenable.

**Point matériel à surveiller.** Le dépôt distant est public et exclut depuis le
17 août les images de tiers et les rendus qui les incorporent. Le prototype avec
images fonctionne donc en local et en démonstration sans que rien ne parte en
ligne — c'est déjà en place, il n'y a rien à faire, mais il faut le savoir avant
de s'étonner qu'une capture ne se versionne pas.

- [ ] **Validation du porteur avant L5.**

---

## L5 — Modèle de transformation des historiques

**Objectif.** Définir comment un texte de notice devient un texte lisible, sans
transformer quoi que ce soit.

**Cette phase ne produit pas de code.** Elle produit un modèle écrit et des
exemples, à valider avant toute application.

- [ ] Relever ce que contient réellement un texte de notice : sur le lieu des
      captures, quinze faits enchaînés sans liaison — construction, exploitation
      par une personne nommée, consommations, productions chiffrées,
      reconstruction, inactivité, mention d'une autre activité, réaménagement,
      cessation, effectifs, existence d'un fonds d'archives.
- [ ] Choisir ce qui reste dans l'amorce visible et ce qui va dans la suite.
- [ ] Définir la règle de provenance : ce qui est cité, ce qui est reformulé, et
      comment le lecteur fait la différence.
- [ ] Poser les règles de prudence déjà établies par le projet : une date
      imprécise reste un intervalle, une période documentée n'est pas une preuve
      d'activité continue, une contradiction entre sources ne s'efface pas.
- [x] Écrire des exemples complets. **Dix notices réelles réécrites et
      contrôlées** le 20 septembre, une par catégorie de difficulté, neuf issues
      des ensembles ouverts. Résultats dans `L5_calibration.md`.
- [x] Contrôle en deux passes retenu par le porteur le 20 septembre.

**Fichiers concernés :** `docs/phase10_fiches_sites_methode.md` — méthode
existante à confronter ; le présent dossier pour le modèle produit.

**Livrable.** Un modèle écrit et des exemples, jugés côte à côte avec les
textes d'origine.

**Calibration faite le 20 septembre 2026** — `L5_calibration.md`. Le contrôle
n'a laissé passer aucun ajout, aucune perte, aucun renforcement de certitude,
aucune tendance inventée : les six défauts qui avaient motivé la démarche sont
absents des dix notices. Cinq verdicts « à reprendre » portent tous sur le même
mot, « puis », entre deux faits que la source ordonne déjà — deux fois repris de
la source elle-même. **Le seuil de huit sur dix n'était donc pas le bon
indicateur** : il comptait les verdicts, pas les défauts. **Le porteur a retenu
le 20 septembre un contrôle à deux niveaux** — ajouté, perdu et renforcé
bloquent ; relié et déplacé se signalent. Verdicts recalculés : **dix notices
sur dix sans écart bloquant**, cinq à relire pour un connecteur.

Deux difficultés remontent vers le corpus et non vers la réécriture : deux
notices emploient le présent sans le dater — « subsiste le four », « elle
utilise aujourd'hui » — et une source porte une mesure corrompue, citée telle
quelle. **Cinq décisions attendent le porteur avant de clore L5.**

**Contre-proposition préparée le 20 septembre 2026**, en réponse à
`proposition_L5.md`, dans `L5_modele_transformation_historiques.md` : diagnostic
de la proposition initiale, prompt de réécriture ramené à sept règles absolues,
protocole de contrôle en deux passes, cas d'essai réécrit avec sa rubrique
« À vérifier », plan de calibration en dix catégories, et six arbitrages
attendus du porteur. **En attente de validation ; L5 n'est pas close.**

**Critères de réception.** Le modèle tient sur une page, il est applicable sans
interprétation, et aucun exemple n'ajoute un fait absent de la source.

- [ ] **Validation du porteur avant L6.**

---

## L6 — Essai sur quelques lieux représentatifs

**Objectif.** Éprouver le mode lieu sur des cas qui ne se ressemblent pas, avant
toute généralisation.

- [ ] Choisir cinq lieux couvrant les cas difficiles : notice longue, notice
      courte ou absente, plusieurs activités, aucun événement daté, lieu sans
      média.
- [ ] Parcourir chacun entièrement, sur écran large et étroit.
- [ ] Consigner ce qui tient et ce qui casse, lieu par lieu.

**Livrable.** Un relevé par lieu, avec captures, et la liste des défauts.

**Critères de réception.** Aucun lieu ne produit un panneau vide, un bloc
incohérent ou un cul-de-sac de navigation.

- [ ] **Validation du porteur avant L7.**

---

## L7 — Validation et généralisation

**Objectif.** Décider si le mode lieu vaut pour les 318 lieux, et à quel prix.

- [ ] Examen visuel complet du porteur sur les cinq lieux d'essai.
- [ ] Consigner les règles devenues communes, comme pour la carte.
- [ ] Mesurer ce que la généralisation coûte : poids de la page, données
      supplémentaires à transmettre, travail éditorial restant.
- [ ] Décrire ce qu'il faut pour ouvrir le mode lieu sur un ensemble de plus,
      sans le développer.

**Livrable.** Mode lieu jugé, règles écrites, coût de généralisation chiffré.

- [ ] **Décision du porteur.**

---

## Hors de ce plan

**L'adresse partageable après le `#`.** Le prototype ne lit ni n'écrit aucune
adresse : on ne peut pas partager un lien vers un lieu, et recharger ramène au
département. C'est un écart avec une décision d'architecture, signalé le
19 septembre. Le mode lieu est le niveau où ce manque se voit le plus, mais le
traiter demande un travail propre. **Recommandation : juste après L3.**

**La réécriture effective des 318 notices.** L5 définit le modèle ; l'appliquer
est une mission distincte, qui ne doit pas être automatique.

**Les recherches sur les personnes et les entreprises** citées dans les notices.
Enrichissement ultérieur, à ne pas mêler à la restructuration de l'interface.

**La direction artistique.** Palette, typographie, habillage : phase 10.E.

**La carte des ensembles.** Ce qui fonctionne n'est pas rouvert.

---

## Première mission recommandée

**L1 seule.** Structure et navigation, rien d'autre.

C'est le seul périmètre qui ne dépend d'aucune donnée nouvelle, d'aucun droit et
d'aucune réécriture. Il produit immédiatement le changement le plus visible :
le panneau cesse de parler de l'ensemble.

**Sa condition de réception tient en une phrase :** supprimer le panneau de
l'ensemble retire aussi le retour et la liste des lieux ; les deux doivent être
redonnés dans le même geste, sinon le lecteur est enfermé dans le lieu qu'il
vient d'ouvrir.
