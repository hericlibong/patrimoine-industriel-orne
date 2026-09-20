# Mode lieu — journal des phases

Branche `codex/mode-lieu-l1`, ouverte le 20 septembre 2026 depuis `main`.
Plan : `roadmap_mode_lieu.md`. Diagnostic : `2026-09-20_analyse_mode_lieu.md`.

---

## L1 — Structure et navigation (20 septembre 2026)

**Objet.** Qu'ouvrir un lieu fasse réellement changer de mode.

### Fait

**Le panneau du lieu ne traîne plus le panneau de l'ensemble derrière lui.**
C'était la cause du panneau interminable : les deux étaient concaténés. Le
lecteur qui ouvrait un lieu recevait la vallée entière par-dessus sa fiche.

**Le retour et le choix d'un autre lieu sont redonnés dans le panneau du lieu.**
Sans cela, supprimer le panneau de l'ensemble aurait enfermé le lecteur dans la
fiche qu'il venait d'ouvrir. C'était le critère de réception de la phase.

**La liste suit le filtre en cours et dit ce qu'elle masque.** Sous Métallurgie,
elle annonce « 24 sur 43 » et ajoute « 19 lieux masqués par le filtre en
cours ». C'est la règle déjà en vigueur dans le panneau de l'ensemble et sur la
carte : rien ne disparaît en silence. **Décision appliquée sur recommandation,
le porteur ne l'ayant pas tranchée ; elle se change en une ligne.**

**Le lieu ouvert est amené à la vue** dès que la liste s'ouvre. Il était déjà
marqué d'un liseré, mais pouvait se trouver n'importe où dans une liste de
quarante-trois entrées à défilement propre : le marquer ne servait à rien si
rien n'y menait.

**Le sélecteur de métier disparaît en mode lieu, le filtre reste.** Le retour à
l'ensemble retrouve exactement la sélection quittée.

**Le titre de page nomme le lieu.** Il annonçait « Vallée de la Risle · 43 lieux
documentés » alors que le lecteur regardait un moulin. Il annonce désormais le
nom du lieu et, en dessous, sa commune et son lieu-dit. Le nom de l'ensemble
reste accessible par le fil de navigation et par le retour du panneau.

**Le libellé du retour a été corrigé avant livraison.** « Retour aux lieux de
Vallée de la Risle » est fautif : les douze ensembles ne prennent pas le même
article — « Flers », « Bassin de Halouze », « La Ferté-Macé ». Un tiret évite la
question : « ← Retour aux lieux — Vallée de la Risle ».

### Contrôles effectués

Six contrôles du générateur vrais, `ruff` propre, syntaxe JavaScript vérifiée
par Node. Dans le navigateur :

- Mode lieu sans filtre : titre « moulin à papier, tréfilerie », sous-titre
  « Aube · Moulin d'Aubette (Le) », sélecteur masqué, **aucun bloc de
  l'ensemble** sous la fiche, liste de 43 lieux, lieu courant marqué une fois.
- Mode lieu sous Métallurgie : liste de 24 lieux, compteur « 24 sur 43 », note
  « 19 lieux masqués », filtre conservé dans l'état.
- Liste ouverte : le lieu courant est bien dans la partie visible de la zone de
  défilement.
- Retour par le bouton : revient à l'ensemble, filtre restauré, sélecteur de
  nouveau visible, titre redevenu « Vallée de la Risle ». La carte retient bien
  24 lieux sur 43 — vérifié sur les données liées à chaque point, les 19 autres
  attendant une disparition que l'onglet de contrôle ne peut pas produire.
- Clavier : 46 éléments atteignables dans le panneau ; le retour prend le focus ;
  l'ordre est notice, retour, liste, lieux.

### Reste ouvert

- **La longueur du panneau.** Il mesure encore 1 223 pixels : l'historique et la
  chronologie sont toujours ouverts. C'est l'objet de L2, qui les repliera.
- **La zone vide à gauche** subsiste tant que la colonne n'est pas collante —
  objet de L3.
- **La validation du porteur.**

---

## L2 — Hiérarchie des contenus (20 septembre 2026)

**Objet.** Que le panneau se lise dans l'ordre où l'on comprend, et qu'il tienne
dans un écran — conséquence directe du choix « panneau court » du porteur.

### Fait

**Le panneau passe de 1 223 à 618 pixels.** Il tient désormais dans un écran
courant, sans rien perdre : tout ce qui était affiché reste atteignable, replié.

**L'ordre de lecture.** Identité ouverte ; historique documenté avec une amorce
visible et la suite dépliable ; chronologie repliée ; localisation et état des
connaissances repliés ; puis le retour et le choix d'un autre lieu.

**Les métiers sortent de la grille de chiffres.** Ils y figuraient en gras sous
l'étiquette « métier », dans une case conçue pour un nombre. Ils sont écrits en
clair sous le nom : « Bois, papier et imprimerie · Métallurgie et travail des
métaux ». La grille de chiffres disparaît entièrement.

**Les compteurs redondants partent.** Le nombre d'activités, que la liste des
activités donne déjà ; le nombre d'événements datés, qui reste seulement sur le
repli de la chronologie, où il sert d'indication de contenu.

**Deux zones de défilement internes supprimées.** La chronologie et le texte de
la notice en avaient chacune une, dans un panneau qui défilait déjà dans une
page qui défilait. Le repli les rend inutiles.

**L'amorce de l'historique coupe à une fin de phrase**, jamais au milieu d'un
mot. Sur le lieu de référence : « Moulin à papier construit en 1761. Exploité en
1824 par Jacques Marais. Consommait en 1826 11500 kg de drilles et produisait
460 rames. » La suite se déplie.

**Les libellés remplacés** : « Ce que dit la notice » devient « Historique
documenté · D'après la fiche d'inventaire, texte non réécrit » ; « Ce qui est
daté » et « Événements extraits du texte de la notice » deviennent
« Chronologie ». « Notice d'origine » devient « Voir la fiche d'inventaire ».

**La distance au cours d'eau descend dans le bloc secondaire**, avec une
formulation qui ferme la porte à la déduction : « 36 m. Une distance mesurée,
qui n'établit pas un usage de l'eau. »

### Deux défauts corrigés au passage

**Un code brut s'affichait au lecteur.** Le bloc de conservation montrait
`partiellement_conserve`. Le vocabulaire contrôlé du projet porte déjà le
libellé « Partiellement conservé », et le générateur le transmettait déjà : il
n'était simplement pas utilisé. Il l'est.

**Le mot « site » subsistait à quatre endroits de l'interface publique**, et non
à un seul comme annoncé dans l'analyse : le texte de précision, la méthode de la
carte du département, et deux phrases du pied de page. Les quatre sont corrigés.

### Décision appliquée sur recommandation

**Le bloc « Localisation et état des connaissances » s'ouvre quand la
conservation est documentée, et reste replié sinon.** Le porteur ne l'avait pas
tranchée. Vérifié sur les deux lieux de la Risle concernés — une affinerie
partiellement conservée, une usine de quincaillerie conservée — et sur un lieu
dont la conservation est inconnue. Elle se change en une ligne.

### Contrôles effectués

Six contrôles du générateur vrais, `ruff` propre, syntaxe JavaScript vérifiée
par Node. Dans le navigateur :

| Cas | Longueur de notice | Hauteur du panneau |
| --- | --- | --- |
| Lieu de référence | 700 caractères | 618 px |
| Notice la plus courte de la Risle | 122 caractères | 566 px |
| Notice la plus longue de la Risle | 1 259 caractères | 662 px |
| Conservation documentée, bloc ouvert | — | 799 px |

Aucune zone de défilement interne ne subsiste dans le panneau, hors la liste des
autres lieux, qui est repliée. Les quatre blocs repliables s'ouvrent au clic et
au clavier. Tous les lieux de la Risle et de Crulai ont un texte et des dates :
les cas « sans texte » et « sans date » n'existent pas dans les deux ensembles
ouverts et n'ont donc pas pu être éprouvés sur données réelles.

### Reste ouvert

- **La zone vide à gauche** — objet de L3.
- **La validation du porteur.**

---

## L3 — Comportement ordinateur et mobile (20 septembre 2026)

**Objet.** Que la carte cesse de laisser une demi-page blanche.

### Fait

**La colonne gauche est ancrée.** Sur ordinateur, la carte reste à l'écran
pendant que le panneau défile. C'était le défaut le plus visible du mode lieu :
la page étant une grille de deux colonnes alignées en haut, la colonne gauche
s'arrêtait dès que le panneau la dépassait, et le reste était blanc.

**Une sécurité de hauteur.** Si la fenêtre est plus courte que la colonne, celle-
ci reste atteignable au lieu d'être coupée. Elle ne se déclenche pas dans les
conditions courantes.

**L'ancrage ne s'applique pas sous 1180 pixels.** En une colonne, il n'y a rien
à retenir, et il enfermerait la carte en haut de l'écran devant le panneau.

### Contrôles effectués

Six contrôles du générateur vrais, `ruff` propre, syntaxe JavaScript vérifiée
par Node.

**Ancrage, sur les trois niveaux, tous blocs dépliés :**

| Vue | Hauteur du panneau | Défilement | Carte visible |
| --- | --- | --- | --- |
| Département | 603 px | 403 px | oui |
| Ensemble Risle | 1 204 px | 900 px | oui |
| Ensemble Crulai | 655 px | 455 px | oui |
| Lieu, tout déplié | 1 711 px | 1 249 px | oui |

Aucune des colonnes ne déborde de sa hauteur maximale.

**Écran étroit, en une colonne :**

| Largeur simulée | Carte | Cartouche | Crédits | Page |
| --- | --- | --- | --- | --- |
| 420 px | 356 × 164 | 7 %, réduit | repliés, 35 % | aucun débordement |
| 330 px | 266 × 123 | 11 %, réduit | repliés, 61 % | aucun débordement |

La carte ne mange pas l'écran avant le panneau : 164 et 123 pixels de haut sur
une fenêtre de 833. L'ancrage est bien désactivé. Le cartouche, l'échelle et les
crédits se comportent en mode lieu comme en mode ensemble.

### Limite relevée

Sur Crulai, dont le cadre est le plus haut des trois — 620 unités contre 462
pour la Risle et 520 pour le département —, le haut de la carte dépasse de
quelques dizaines de pixels lorsque la colonne est ancrée sur une fenêtre de
833 pixels. La carte reste visible et utilisable ; sur une fenêtre plus haute la
question ne se pose pas. À revoir si le porteur le juge gênant.

**Simulation, pas fenêtre réelle.** L'écran étroit a été éprouvé en contraignant
la largeur du conteneur, l'onglet de contrôle ne pouvant pas être redimensionné.
Le comportement d'une vraie fenêtre étroite reste à confirmer par le porteur.

### Reste ouvert

- **La validation du porteur.**
- L4, les médias, qui demandera de les transmettre au prototype.

---

## L4 — Médias (20 septembre 2026)

**Cadre posé par le porteur le 20 septembre.** Tout média inventorié est traité
comme publiable. Aucune condition de droits n'est appliquée par le code. Le
porteur décide seul, au moment qu'il choisit, de ce qui part en ligne.

### Ce qu'il a fallu établir avant d'afficher quoi que ce soit

**L'inventaire ne donne pas d'adresse d'image directe.** Le champ d'adresse
principal pointe vers une notice de la plateforme POP, pas vers un fichier. Le
chemin de fichier, lui, est **relatif pour 1 783 médias et complet pour 117**.

**La base n'est donc pas supposée, elle est lue dans les données.** Les 117
adresses complètes portent toutes le même hôte et la même forme de chemin que
les 1 783 relatives. La base en découle.

**Et elle a été vérifiée, pas déduite.** Trois fichiers chargés dans un
navigateur, dont deux reconstruits à partir d'une adresse relative : images
obtenues, 756 × 600 et 477 × 600. L'environnement local n'ayant pas d'accès
réseau, la vérification est passée par le navigateur.

### Fait

**Les médias sont transmis au prototype.** Ils n'y étaient pas du tout. Un média
par lieu : celui que la source signale comme image principale, à défaut le
premier. C'est la recommandation de la roadmap, **appliquée faute d'arbitrage du
porteur ; elle se change en une ligne.**

**Couverture réelle des deux ensembles ouverts :** 42 lieux sur 43 pour la
Risle, 7 sur 7 pour Crulai. Un seul lieu sans média, l'usine d'ébénisterie.

**L'image est affichée avec sa légende et son crédit**, sous les activités. Ce
sont des informations de provenance, pas des autorisations.

**Aucun cadre de remplacement** pour le lieu sans média : ni pictogramme, ni
mention « image indisponible ». Une absence n'est pas un manque à signaler.

**Une image qui échoue retire sa figure entière** et laisse le panneau intact.
Vérifié avec une adresse fautive.

**Le chargement n'est pas différé.** Il l'était d'abord ; le report dépend du
cycle de rendu et n'a jamais pu être éprouvé ici. Pour une seule image en tête
de panneau, il n'apporte rien et ajoute un mode d'échec.

### Contrôles effectués

Six contrôles du générateur vrais, `ruff` propre, syntaxe JavaScript vérifiée
par Node. Dans le navigateur :

| Cas | Résultat | Hauteur du panneau |
| --- | --- | --- |
| Lieu avec média | image chargée, 754 × 600, légende et crédit présents | 921 px |
| Autre lieu avec média | image chargée, 756 × 600 | 992 px |
| Lieu sans média | aucune figure, aucune mention d'absence | 679 px |
| Adresse fautive | figure retirée, panneau intact | — |

**Poids de la page :** 868 → 890 ko. Les médias de cinquante lieux coûtent 22 ko.

### Tension à arbitrer par le porteur

**Avec une image, le panneau ne tient plus dans un écran.** Il passait à 1 069
pixels ; la hauteur de l'image a été bornée à 230 pixels, ce qui le ramène entre
920 et 990. C'est encore au-dessus du critère de réception de L2, qui demandait
qu'il tienne sur un écran de 900 pixels.

L'image entière reste visible — aucun recadrage, rien de coupé — au prix de
bandes latérales sur les formats les plus allongés.

Trois issues possibles : accepter qu'un panneau avec photo dépasse légèrement ;
réduire encore la hauteur de l'image ; ou rendre la photo repliable comme les
autres blocs.

**Décision du porteur, 20 septembre 2026 : l'image est repliable.** Appliqué.
Le panneau retombe à 629 et 733 pixels selon la longueur de l'amorce, donc sous
le critère de L2. Déplié, il atteint 988 et 1 058 pixels — mais le lecteur l'a
demandé. La hauteur de l'image n'est plus bornée une fois dépliée : elle
s'affiche entière, sans bandes latérales.

Le repli s'intitule **« Voir l'image »** et non « la photographie ». La source
ne qualifie aucun des 1 900 médias — le champ de type vaut `image_non_qualifiee`
pour la totalité — et celui du moulin de Launay est un plan cadastral de 1831,
pas une photographie. Un lieu sans média n'a aucun repli.

### Reste ouvert

- **La validation du porteur**, et l'arbitrage ci-dessus.
- Le choix du média quand un lieu en compte plusieurs, appliqué sur
  recommandation.
- L5, le modèle de transformation des historiques.

## 2026-09-20 — Les cinquante historiques réécrits entrent dans la vue

Le modèle L5, arrêté et calibré le jour même sur dix lieux, est appliqué aux
cinquante lieux des deux ensembles ouverts : quarante-trois pour la Risle, sept
pour Crulai. Aucun autre lieu n'est touché — les 268 restants gardent le texte
brut de leur notice, conformément à la consigne de ne pas transformer
automatiquement les 318 notices.

**Où vivent les textes.** Dans `data/manual/`, que le projet réserve aux
corrections humaines documentées, jamais écrasées par un traitement automatique.
Les écrire dans la base aurait été une faute : `data/processed/` est déclaré
reproductible par script, donc une régénération les aurait effacés. Le fichier
n'est lu qu'en lecture par le générateur ; son absence ne bloque pas la
production de la vue.

**Le texte de la source ne disparaît pas.** Il est transmis à côté du texte
réécrit et reste accessible au lecteur, replié sous l'intitulé « Lire le texte
d'origine, tel qu'il est dans la source », mot pour mot. La règle du projet est
que le libellé source est conservé à côté de la valeur normalisée, jamais
remplacé : elle vaut aussi pour un paragraphe entier.

**La mention de provenance devient exacte.** « D'après la fiche d'inventaire,
texte non réécrit » était devenu faux pour ces cinquante lieux. Elle devient
« Réécrit à partir de la fiche d'inventaire, sans aucun fait ajouté ». Les 268
autres lieux gardent l'ancienne mention, qui reste vraie pour eux.

**Contrôles.** Le générateur compte les textes réécrits transmis (50) et vérifie
qu'aucun d'eux n'arrive sans son texte source — un texte réécrit orphelin ne
serait plus vérifiable. Dans le navigateur, les cinquante panneaux ont été
produits et comparés un à un : mention de provenance conforme, texte lu
identique au texte réécrit, texte d'origine présent et complet. Aucun écart.

**Cinquante-deux points relevés comme à vérifier**, inscrits à côté de chaque
texte. Ils ne sont pas des erreurs de réécriture mais des ambiguïtés de la
source, conservées au lieu d'être tranchées.

Deux questions restent pour le porteur du projet, l'une et l'autre nées de la
réécriture :

- **Le mot « site » dans les textes venus de la source.** L'interface dit
  « lieu », mais quelques notices emploient « site » dans leur propre phrase.
  Faut-il y toucher ? Relevé sur IA00061013.
- **Le présent sans date.** « subsiste », « aujourd'hui disparue »,
  « actuellement désaffecté » reviennent dans une douzaine de textes. Ces
  constats n'ont pas de date : ils renvoient à la rédaction de la notice, dont
  nous ne connaissons pas la date ici. La règle du projet veut que les
  observations contemporaines soient datées. L5 avait renvoyé la question au
  moment de l'affichage ; ce moment est arrivé.

Décision : **les cinquante historiques réécrits des ensembles ouverts sont
affichés, le texte d'origine reste accessible replié, et la mention de
provenance est corrigée ; le présent sans date reste en attente d'arbitrage.**

## 2026-09-20 — Le texte d'origine est retiré, « Lire la suite » rentre dans le fil

Deux décisions prises le matin même sont annulées le jour de leur mise en
œuvre, sur jugement du porteur du projet à l'écran.

**Le repli « Lire le texte d'origine » est supprimé.** Motif du porteur :
« Qu'est-ce qu'on en a à faire du texte d'origine ? […] c'est ce texte éditorial
qui va faire foi. On s'est cassé la tête pour transformer un texte qui n'était
pas lisible d'un point de vue lecteur, ce n'est pas pour le remettre après. »
Le raisonnement qui l'avait posé — la règle du projet qui veut que le libellé
source soit conservé à côté de la valeur normalisée — ne s'applique pas ici.
Cette règle protège la donnée, pas la prose : elle vaut pour un code de
vocabulaire contrôlé en regard de son libellé d'origine, et le texte source
reste conservé dans le corpus et accessible par la fiche d'inventaire, dont le
lien figure dans le même panneau. Rien n'est perdu. Ce qui était en cause,
c'est l'encombrement du panneau du lecteur par un doublon qu'il ne demande pas.

**« Lire la suite » cesse d'être un second bloc.** Motif du porteur : un texte
long ne se coupe pas en deux cartons. La fin du texte est maintenant masquée
dans le même paragraphe, derrière des points de suspension suivis du lien
« Lire la suite » ; au clic, les points et le lien disparaissent et la phrase
continue là où elle s'était arrêtée. Un seul bloc, un seul texte. C'est la
forme courante et attendue, et l'ancienne ne l'était pas.

Quarante-cinq des cinquante historiques sont assez longs pour être coupés,
cinq tiennent entiers. Les cinquante panneaux ont été produits et comparés un à
un : un seul paragraphe par historique, aucun bloc replié restant, aucune
mention du texte d'origine, et le texte déplié strictement identique au texte
réécrit. Le clic a été déclenché pour de vrai sur le cas le plus long, la
tréfilerie de Rai.

Décision : **le texte d'origine ne figure plus dans le panneau du lieu, et la
suite d'un historique long se déplie dans le fil du texte, sans second bloc.**

## 2026-09-20 — Le panneau du lieu est nettoyé de ce qui ne s'adresse pas au lecteur

Jugement du porteur du projet à l'écran, sur la forme du panneau. Le reproche
est unique et il porte : plusieurs éléments du panneau parlent du travail fait
sur la donnée, pas du lieu. Ils s'adressent à celui qui a construit la fiche,
pas à celui qui la lit.

**« Historique documenté » devient « Historique ».** Un titre nomme une chose.
« Documenté » ne nomme rien de plus : il rassure sur la méthode, dans un
emplacement réservé à l'orientation du lecteur.

**La mention de provenance est supprimée.** Elle disait « Réécrit à partir de
la fiche d'inventaire, sans aucun fait ajouté » — posée le matin même, jugée
sans utilité pour le lecteur. Le lien vers la fiche d'inventaire, quelques
lignes plus haut dans le même panneau, dit d'où vient le texte. Le texte
commence maintenant directement.

**« Voir plus » et « Voir moins », au lieu de « Lire la suite ».** Le chemin
manquait dans un sens : un historique long déplié occupe la page, et rien ne
permettait de le replier sans quitter le lieu. Le même lien fait l'aller et le
retour ; le libellé change avec l'état, et l'état est annoncé aux lecteurs
d'écran. Quarante-cinq historiques sur cinquante sont concernés. Aller-retour
vérifié sur le plus long, la tréfilerie de Rai : 201 caractères visibles
repliés, 1 348 dépliés, retour à l'identique au second clic.

**Le bloc « Localisation et état des connaissances » est supprimé.** Motif du
porteur, qui en prend explicitement la responsabilité : dans son état, il ne
sert à rien et on n'y comprend rien. « Le point situe le lieu à ce niveau de
précision et ne représente pas son emprise » et « une distance mesurée qui
n'établit pas un usage de l'eau » sont des précautions écrites pour se
prémunir, pas des phrases qui apprennent quelque chose. Elles énoncent ce que
la donnée n'est pas, jamais ce qu'elle est.

Ce qui disparaît de l'écran ne disparaît pas du corpus : la précision de
localisation, la distance au cours d'eau et l'état de conservation restent des
champs du corpus, produits et contrôlés comme avant. Seul leur affichage est
retiré. Les invariants du domaine ne sont pas touchés : la précision reste un
champ distinct des coordonnées, aucun point n'est déplacé, aucune précision
n'est relevée.

**À reprendre plus tard, noté ici pour ne pas être perdu.**

1. **Refaire le bloc des limites, ou renoncer.** Ces trois informations ont une
   valeur réelle pour qui veut savoir ce qu'on sait d'un lieu. Ce qui a échoué,
   c'est leur formulation, pas leur existence. Une reprise devra dire ce que
   l'on sait, dans les mots de quelqu'un qui raconte — « on connaît l'adresse,
   pas les murs » plutôt que « le point ne représente pas son emprise ». Tant
   qu'une telle formulation n'existe pas, le bloc reste supprimé.
2. **L'avertissement de fin de chronologie devient une note.** « Une date
   imprécise reste un intervalle. Une période documentée n'est pas une preuve
   d'activité continue » reste exact et utile, mais posé en fin de liste il a
   le poids d'une conclusion alors qu'il n'en est pas une. Demande du porteur :
   une petite étoile à côté de ce qui est concerné, renvoyant à une note. Son
   emplacement reste à décider. Laissé en l'état pour l'instant.

Décision : **le panneau du lieu ne porte plus que ce qui parle au lecteur : le
titre « Historique » sans qualificatif, le texte sans mention de provenance, un
« Voir plus / Voir moins » réversible, et plus de bloc de localisation.**

## 2026-09-20 — L'image du lieu est posée, plus jamais repliée

Le repli « Voir l'image » avait été posé le 20 septembre à la demande du
porteur — « rends la photo repliable » — pour un motif de hauteur : une image
en portrait faisait passer le panneau de 618 à 1 069 pixels et rompait le
« panneau court ». Le porteur revient sur cette demande le même jour, après
l'avoir vue à l'écran, et le motif qu'il donne l'emporte : c'est l'image qui
fait exister le lieu à l'arrivée. Un repli lui retire son effet avant même
qu'elle ait servi. Le lecteur ouvre un lieu, il voit son image.

Le problème de hauteur, lui, n'a pas disparu — il était réel, c'est la réponse
qui était mauvaise. Il est traité là où il se pose, dans la mise en page : la
hauteur de l'image est bornée à 300 pixels. La borne porte sur la boîte de
l'image et non sur son contenu, de sorte que l'image garde sa forme, n'est
jamais recadrée, et ne traîne aucune bande latérale : un portrait est
simplement moins large, et centré.

Mesuré dans le navigateur sur les cinquante panneaux, image chargée et décodée :
le plus haut atteint 772 pixels, contre 618 quand l'image était repliée. Le
critère du panneau court — tenir sans débordement sur un écran de 900 pixels de
haut — reste satisfait. Trois exemples : une image en portrait de 471 × 600 est
affichée en 236 × 300, une de 476 × 600 en 238 × 300, un paysage de 756 × 600
en 377 × 300. Aucune image n'est agrandie au-delà de sa taille d'origine, ce
qui l'aurait rendue floue. Quarante-neuf des cinquante lieux ont une image.

Aucune image n'est téléchargée ni copiée : le panneau pointe l'adresse du
média, comme avant. Une image dont l'adresse ne répond pas retire sa propre
figure du panneau plutôt que d'afficher un cadre vide.

**Point laissé au jugement du porteur.** Les images de la source mesurent
600 pixels de haut au maximum. La borne à 300 leur en laisse la moitié. Monter
la borne donnerait une image plus présente, au prix d'un panneau plus long ;
c'est un seul nombre à changer, et cela se juge à l'œil, pas au calcul.

Décision : **l'image du lieu est posée, visible dès l'ouverture, bornée à 300
pixels de haut et jamais recadrée.**

## 2026-09-20 — L6, le mode lieu éprouvé sur les cinquante lieux publiables

Relevé complet dans `docs/F10_site/L6_releve_essai.md`. Trois points méritent
d'être inscrits ici.

**La feuille de route visait des cas difficiles qui n'existent pas.** Elle
prévoyait cinq lieux couvrant la notice absente, l'absence d'événement daté, le
lieu sans média, les activités multiples. Vérification faite sur les cinquante
lieux des deux ensembles ouverts : aucun lieu sans historique, aucun sans
événement daté, un seul sans image, un seul à trois activités. La Risle est une
vallée bien documentée, et c'est précisément pour cela qu'elle sert de modèle.
L'essai a donc porté sur les six lieux réels qui en forment les extrêmes, puis
sur un contrôle de robustesse où les informations manquantes ont été simulées
en mémoire dans le navigateur, sans qu'aucune donnée soit touchée.

**Une erreur de mesure de ma part, corrigée.** Les hauteurs de panneau
annoncées plus tôt dans la journée — 618 pixels image repliée, 772 image
posée — étaient mesurées sur la colonne de la carte et non sur le panneau du
lieu. Les vraies valeurs, mesurées sur les cinquante panneaux à 1440 pixels :
médiane 789, maximum 885, minimum 490. La conclusion ne change pas — le critère
du panneau court de L2, tenir sous 900 pixels, est tenu par les cinquante — mais
la marge est plus faible qu'annoncée, et cela a une conséquence : monter la
borne de hauteur de l'image, que le porteur envisage, ferait passer une partie
des lieux au-dessus du critère. Les deux décisions sont liées.

**Le panneau tient même quand tout manque.** En retirant une à une l'historique,
les dates, les activités, le lien vers la fiche et l'image, puis toutes
ensemble, le panneau continue de se tenir : il donne le nom et la commune, dit
honnêtement ce qu'il ignore, et laisse repartir vers l'ensemble et vers les
autres lieux. Une image dont l'adresse ne répond pas retire sa propre figure
plutôt que d'afficher un cadre cassé. Aucun code technique n'apparaît à
l'écran dans aucun des essais.

**Les captures n'ont pas pu être faites.** L'onglet piloté par l'assistant ne
produit aucune image : les mesures et la lecture du contenu affiché tiennent
lieu de preuve. Le manque vaut aussi règle : une capture du panneau d'un lieu
incorpore la photographie de l'inventaire, et le dépôt exclut depuis le 17 août
2026 les rendus qui en incorporent. L'examen visuel revient au porteur, et c'est
le premier point de L7.

Décision : **L6 est éprouvé et consigné ; les cinq critères de réception sont
tenus ; l'examen visuel du porteur reste à faire avant d'ouvrir L7.**
