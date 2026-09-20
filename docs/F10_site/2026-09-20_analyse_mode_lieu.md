# Analyse — le mode lieu

**20 septembre 2026. Mission d'analyse, sans modification du prototype.**
Aucune branche, aucun code, aucune donnée touchés.

---

## 1. Diagnostic de l'état actuel

### La cause du panneau interminable tient en une ligne

Le panneau de droite est assemblé ainsi : au niveau département, le panneau du
département ; au niveau ensemble, le panneau de l'ensemble ; **au niveau lieu,
le panneau du lieu suivi du panneau de l'ensemble**. Les deux sont simplement
concaténés.

Ce n'est donc pas un défaut d'organisation du contenu, c'est un assemblage
délibéré qui n'a jamais été revu. Le lecteur qui ouvre un lieu reçoit tout ce
qu'il avait avant, plus la fiche par-dessus.

Conséquence mesurée sur les captures : après la fiche viennent « L'ensemble en
quelques repères », les 43 lieux, les 10 communes, les années documentées, la
liste des sept activités de la vallée, « Explorer les lieux » et « Relations
entre les lieux ».

### La grande zone vide à gauche a une cause distincte

La page est une grille de deux colonnes — la gauche souple, la droite fixe à
360 pixels — avec un alignement en haut. Chaque colonne a sa propre hauteur et
**rien ne retient la carte** : dès que le panneau dépasse, la carte s'arrête et
le reste de la colonne gauche est vide. C'est ce que montrent les deuxième et
troisième captures : une demi-page blanche à gauche.

Sous 1180 pixels de large, la grille passe à une colonne et tout s'empile — le
comportement mobile existe déjà et n'est pas en cause.

### Le lieu ouvert est marqué, mais pas trouvable

La liste « Explorer les lieux » marque bien le lieu courant — il porte un
attribut d'état et un liseré visible sur la troisième capture. Mais la liste a
sa propre zone de défilement interne, et le lieu ouvert peut s'y trouver
n'importe où. Rien ne l'y amène.

### Trois défauts de détail relevés en lisant

- **Le mot « site » apparaît dans l'interface publique**, dans le texte de
  précision de localisation : « Le point situe le site à ce niveau de précision ».
  C'est contraire à la règle de vocabulaire.
- **Les métiers sont affichés dans une case de chiffre.** La grille d'entrée
  accueille quatre valeurs : 2, 11, 15 m, puis « Bois, papier et imprimerie,
  Métallurgie et travail des métaux » en gras avec l'étiquette « métier ». Un
  texte long dans un emplacement conçu pour un nombre.
- **La chronologie a sa propre zone de défilement**, dans un panneau qui défile
  déjà lui-même dans une page qui défile.

### Ce qui fonctionne déjà et ne doit pas être refait

Le lieu ouvert est mis en évidence sur la carte, ses partenaires reçoivent un
anneau et les liens qui y mènent passent en trait plein. Le cadrage ne bouge pas
à l'ouverture. L'accès aux preuves des relations fonctionne au clic comme au
clavier. Tout cela date du bloc B et n'a pas à être repris.

---

## 2. Appréciation de la proposition

### Ce qui est juste, et techniquement simple

**Faire du mode lieu un vrai mode.** Supprimer la concaténation est une ligne.
Le reste du travail consiste à redonner dans le panneau du lieu ce que le
panneau de l'ensemble fournissait : le retour à l'ensemble et le choix d'un
autre lieu.

**La carte maintenue à gauche.** Un ancrage collant de la colonne gauche résout
la zone vide sans toucher à la carte elle-même. C'est du style, pas de la
logique.

**Masquer le sélecteur de métier et mémoriser le filtre.** Le filtre est déjà un
état global conservé lors de la navigation ; il n'y a rien à mémoriser, juste à
ne pas l'effacer et à masquer la commande.

**L'historique avant la chronologie.** Juste. On comprend une histoire avant de
la dater.

**Retirer les compteurs redondants.** Le nombre d'événements datés est répété
par la chronologie elle-même ; le nombre d'activités est répété par la liste des
activités.

**La distance au cours d'eau en bloc secondaire, sans en faire une preuve.**
Conforme à un invariant du projet. Le texte actuel ne l'affirme pas — il ne
faudra pas l'introduire en le déplaçant.

### Ce qui pose problème

**Le média n'a aucune chance de s'afficher, pour aucun lieu.** L'inventaire
compte 1 900 relations média–lieu couvrant 316 des 318 lieux. Mais :

| Champ | Valeur | Nombre |
| --- | --- | --- |
| Sélection | `non_evalue` | **1 900 sur 1 900** |
| Autorisation | `a_demander` | **1 900 sur 1 900** |
| Usage | `prototype_prive` / `reference_interne` | 1 783 / 117 |
| Droits | `protege` / `inconnus` | 1 783 / 117 |

Aucun média n'a été sélectionné, aucune autorisation n'a été demandée, et
l'usage déclaré est interne pour la totalité. La condition posée par la
proposition — « seulement lorsqu'un média a été sélectionné et que son usage est
permis » — est donc **juste, et jamais satisfaite**. Écrire ce bloc aujourd'hui
revient à écrire du code qui ne s'exécutera pour aucun lieu.

Ce n'est pas un problème d'interface : c'est un travail de droits, qui suppose
une revue humaine de sélection puis des demandes d'autorisation. À traiter comme
tel, et non comme une phase de développement.

**La proposition entre en tension avec une structure déjà arrêtée.** Le document
de méthode des fiches définit un panneau de détail en huit éléments — repère,
identité, image, phrase factuelle courte, activités, situation actuelle,
localisation, actions — avec deux règles explicites : « le panneau doit tenir
dans un écran courant » et « le panneau n'est pas un mini-article ».

Or la proposition place dans le panneau l'historique documenté complet, c'est-à-
dire le texte entier de la notice, plus la chronologie. Sur le lieu des captures,
c'est un paragraphe de douze lignes et onze événements datés. Le panneau ne
tiendra pas dans un écran et sera, précisément, un mini-article.

Ce n'est pas nécessairement une erreur : la méthode prévoyait une **page
éditoriale « Les lieux »** distincte, qui n'existe pas dans le prototype. La
proposition fusionne de fait le panneau court et la page longue. **Il faut le
dire et le décider**, pas le laisser arriver par accident.

**Deux points de la proposition se contredisent légèrement.** Il est demandé de
conserver honnêtement ce qui est connu ou inconnu sur la conservation, tout en
la reléguant dans un bloc replié. Or pour 315 des 318 lieux du corpus, l'état de
conservation est inconnu — c'est le rapport de qualité du projet qui l'établit.
Replier une information absente est sans risque ; mais si un jour elle est
connue pour un lieu, la replier devient un choix discutable. Une règle
conditionnelle vaudra mieux qu'une règle fixe.

### Ce qui manque à la proposition

**Rien n'est dit du titre de page ni du fil de navigation.** Sur la première
capture, le lecteur qui a ouvert un lieu voit toujours « Vallée de la Risle » et
« 43 lieux documentés » en titre de page. En mode lieu, le titre devrait parler
du lieu.

**Rien n'est dit de ce que devient la carte.** Elle reste, mais faut-il qu'elle
recadre, qu'elle se réduise, qu'elle conserve exactement son état ? La décision
du 18 septembre impose déjà de ne pas recadrer à l'ouverture d'une fiche. Il
suffit de le rappeler, mais il faut le rappeler.

**Rien n'est dit de l'adresse.** Le prototype ne lit ni n'écrit aucune adresse :
on ne peut pas partager un lien vers un lieu, et recharger ramène au
département. C'est un écart connu avec une décision d'architecture, signalé le
19 septembre. Le mode lieu est le niveau où ce manque se voit le plus.

---

## 3. Décisions qui reviennent au porteur

Elles sont cinq, et aucune ne peut être tranchée par le code.

**1. Le mode lieu est-il un panneau court ou une page longue ?** La méthode
prévoyait les deux séparément : un panneau tenant dans un écran, et une page
éditoriale pour les lieux qui la méritent. La proposition les fusionne. Il faut
choisir, car tout le reste en dépend : si c'est un panneau court, l'historique
complet et la chronologie n'y tiennent pas et doivent être repliés ou déportés.

**2. La liste « Choisir un autre lieu » respecte-t-elle le filtre métier ?**
Trois règles possibles : suivre le filtre, ce qui est cohérent avec la carte
mais peut cacher le voisin immédiat ; ignorer le filtre, ce qui donne accès à
tout mais ne correspond plus à ce que la carte montre ; suivre le filtre en
indiquant combien de lieux sont masqués, comme le fait déjà le panneau de
l'ensemble. **Recommandation : la troisième** — c'est la règle déjà en vigueur
dans le projet, et elle ne cache rien en silence.

**3. Le bloc média est-il écrit maintenant ou plus tard ?** Puisqu'il ne
s'affichera pour aucun lieu, **recommandation : plus tard**, après la revue des
droits. Écrire un emplacement vide invite à le remplir.

**4. La conservation est-elle toujours repliée, ou seulement quand elle est
inconnue ?** Recommandation : repliée quand elle est inconnue — le cas de 315
lieux sur 318 — et visible quand elle est documentée.

**5. L'adresse partageable entre-t-elle dans ce chantier ?** Elle n'est pas dans
la proposition. Recommandation : non, mais la traiter juste après, car c'est au
niveau du lieu qu'elle manque le plus.

---

## 4. Architecture cible proposée

### Sur ordinateur

Deux colonnes, comme aujourd'hui. **La colonne gauche devient collante** : la
carte reste visible pendant que le panneau défile. La colonne droite défile
naturellement avec la page.

En-tête de page : le nom du lieu, sa commune, et un retour explicite vers
l'ensemble. Le sélecteur de métier disparaît, son état est conservé.

Panneau, dans cet ordre :

1. **Identité** — nom, commune et lieu-dit, activités écrites en clair, lien
   vers la fiche d'inventaire.
2. **Historique documenté** — le texte de la notice, avec sa provenance.
3. **Chronologie** — repliable, sans zone de défilement propre.
4. **Localisation et état des connaissances** — repliable : précision
   géographique, distance au cours d'eau, conservation.
5. **Choisir un autre lieu** — replié, en dernier, avec le lieu courant amené à
   la vue à l'ouverture.

### Sur mobile

L'empilement existe déjà sous 1180 pixels et n'a pas à être refait. Deux points
à vérifier seulement : que l'ancrage collant ne s'y applique pas, et que la
carte ne mange pas tout l'écran avant le panneau.

---

## 5. Le périmètre proposé pour la première mission tient-il ?

**Oui**, et c'est même le seul périmètre raisonnable. Il ne dépend d'aucune
donnée nouvelle, d'aucun droit, d'aucune réécriture. Il touche trois choses :
l'assemblage du panneau, le style de la colonne gauche, et le contenu du panneau
du lieu.

Une réserve toutefois : **supprimer la concaténation retire aussi le retour à
l'ensemble et la liste des lieux**. Ces deux fonctions doivent être redonnées
dans le même mouvement, sans quoi le lecteur se retrouve dans un cul-de-sac.
C'est inclus dans la proposition, mais il faut le traiter comme une condition de
réception, pas comme une amélioration.

Deuxième réserve : la première mission ne peut pas être jugée sans une capture,
et l'environnement de contrôle ne produit pas d'images. Le jugement du porteur
sera, comme pour la carte, le seul examen visuel réel.

---

## 6. Ce que cette analyse n'a pas fait

Aucun code n'a été lu au-delà du panneau du lieu, du panneau de l'ensemble, de
leur assemblage et de la mise en page. Aucune donnée n'a été modifiée. Les
médias n'ont été lus que pour compter ce qui est disponible. Aucune notice n'a
été transformée. Les recherches sur des personnes ou des entreprises n'ont pas
été abordées.
