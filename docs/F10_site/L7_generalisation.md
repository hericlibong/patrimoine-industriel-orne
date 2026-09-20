# L7 — Ce que le mode lieu coûte à généraliser

**20 septembre 2026.** Trois des quatre points de L7 sont traités ici : les
règles devenues communes, le coût chiffré de la généralisation, et ce qu'il
faut pour ouvrir un ensemble de plus. **Le quatrième — l'examen visuel des
lieux d'essai — revient au porteur du projet et n'est pas fait.**

---

## 1. Les règles devenues communes

Elles sont sorties du travail des phases L1 à L6 et des corrections du
20 septembre. Elles valent maintenant pour tout lieu, comme les règles de la
carte valent pour tout ensemble.

**Sur ce qu'on écrit au lecteur**

1. **Un titre nomme, il ne qualifie pas.** « Historique », pas « Historique
   documenté ». Le qualificatif rassure sur la méthode dans un emplacement
   réservé à l'orientation du lecteur.
2. **Rien de ce qui parle du travail fait sur la donnée ne s'affiche.** Pas de
   mention de provenance quand le lien vers la source est déjà dans le panneau,
   pas de précaution qui énonce ce que la donnée n'est pas.
3. **Une information qu'on ne sait pas expliquer ne s'affiche pas.** C'est la
   règle qui a fait supprimer le bloc des limites : ses trois informations sont
   justes, leur formulation ne l'était pas.
4. **Un manque se dit en clair.** « Aucun texte historique dans la source »,
   « Activité non précisée par la source ». Jamais un blanc, jamais un code
   technique, jamais un bloc vide.
5. **Le mot du lecteur est « lieu ».** « Site » reste réservé aux noms
   techniques internes.

**Sur la forme**

6. **Un texte long ne se coupe pas en deux blocs.** Il reste un seul texte dont
   la fin est masquée derrière des points de suspension et un lien, et le chemin
   existe dans les deux sens : « Voir plus », « Voir moins ».
7. **L'image est posée, jamais repliée.** C'est elle qui fait exister le lieu à
   l'arrivée.
8. **Une image se borne par sa boîte, jamais par recadrage.** Rien n'est coupé,
   aucune bande latérale, aucun agrandissement au-delà de la taille d'origine.
9. **Le panneau tient sous 900 pixels au repos.** Le seul dépassement autorisé
   est celui que le lecteur a demandé en dépliant.

**Sur la navigation**

10. **Jamais de cul-de-sac.** Depuis un lieu, on atteint toujours son ensemble
    et un autre lieu.
11. **Le filtre survit au changement de niveau.** Entrer dans un lieu puis
    revenir rend l'ensemble exactement dans l'état où on l'avait laissé.
12. **Tout ce qui se clique s'atteint au clavier.**

---

## 2. Ce que la généralisation coûte

### Le poids de la page

| | Aujourd'hui, deux ensembles | Les douze ensembles |
| --- | --- | --- |
| Page entière | 899 ko | 2 356 ko |
| Une fois compressée, comme en ligne | 247 ko | environ 565 ko |
| Part des données dans la page | 57 % | 83 % |

**Ce que ces chiffres disent.** La page ferait deux fois et demie son poids
actuel. Compressée — ce que fait tout serveur — elle passerait de 247 à environ
565 kilo-octets. C'est le poids d'une page d'actualité ordinaire avec ses
photos. Ce n'est pas un obstacle, mais ce n'est plus négligeable sur une
connexion lente.

### Le coût par ensemble, et d'où il vient

| Ensemble | Lieux | Poids | Part prise par la carte |
| --- | --- | --- | --- |
| Risle | 43 | 380 ko | 70 % |
| Noireau | 23 | 280 ko | 83 % |
| Halouze | 13 | 218 ko | 88 % |
| Flers | 21 | 183 ko | 77 % |
| Argentan | 7 | 155 ko | 92 % |
| La Ferté-Macé | 12 | 126 ko | 78 % |
| La Ferrière | 7 | 117 ko | 87 % |
| Tinchebray | 9 | 108 ko | 84 % |
| Randonnai | 9 | 98 ko | 81 % |
| Crulai | 7 | 94 ko | 86 % |
| Alençon | 13 | 87 ko | 74 % |
| Malétable | 8 | 86 ko | 80 % |

**Le constat qui compte : le poids ne vient pas des lieux, il vient de la
carte.** De 70 à 92 % du poids de chaque ensemble est le fond de carte — les
contours de communes et le tracé des rivières. Argentan, avec sept lieux, pèse
155 ko quand Alençon, avec treize, en pèse 87 : ce n'est pas le nombre de lieux
qui décide, c'est l'étendue du territoire à dessiner. Alléger la page, si un
jour il le faut, se fera sur la géographie, pas sur le contenu.

### Le travail éditorial restant

Les douze ensembles rassemblent **172 lieux**. Cinquante sont réécrits, **122
restent à faire** : 66 700 caractères de notices, d'une longueur médiane de
508 caractères — la moitié de celle des textes déjà traités. À la cadence de la
calibration, c'est un travail de plusieurs séances, pas d'un après-midi, et il
ne doit pas être automatique.

### L'obstacle qui n'était pas connu

**Sept ensembles sur douze ont des communes dont le contour manque.**

| Ensemble | Communes sans contour |
| --- | --- |
| Noireau | Athis-de-l'Orne, Frênes |
| Halouze | Larchamp |
| La Ferté-Macé | La Ferté-Macé |
| Tinchebray | Tinchebray |
| Randonnai | Normandel, Randonnai |
| Malétable | Longny-au-Perche, Malétable, Saint-Victor-de-Réno, Tourouvre |
| Argentan | Goulet |

Ce sont des noms de communes qui ont fusionné ou changé de nom ; le fond de
carte actuel ne les connaît plus sous ce nom. Le générateur **refuse de
produire la vue** tant qu'un contour manque, et c'est voulu : une carte avec un
trou se verrait, mais une carte dont il manque une commune au milieu ne se voit
pas. Trois de ces noms étaient repérés depuis le 19 septembre ; l'inventaire
complet, fait ici, en compte onze dans sept ensembles.

**Trois ensembles seulement sont ouvrables sans rien résoudre :** Flers,
Alençon et La Ferrière. Les sept du tableau demandent d'abord ce travail de
rapprochement des noms de communes.

### Les 146 lieux qui n'ont pas d'ensemble

Sur les 318 lieux du corpus, **172 appartiennent à un ensemble et 146 n'en ont
aucun**. Ces 146 existent sur la carte du département comme points, mais la vue
ne transmet d'eux que six informations — nom, commune, activités et
coordonnées. Ni historique, ni chronologie, ni image, ni lien vers la fiche.

**Ouvrir les douze ensembles ne donne donc pas le mode lieu aux 318 lieux, mais
à 172.** Les 146 autres demandent une décision qui n'a jamais été prise : ou
bien on leur donne un mode lieu sans ensemble d'appartenance, ou bien on
accepte qu'ils restent des points sur la carte du département.

---

## 3. Ce qu'il faut pour ouvrir un ensemble de plus

Décrit, non développé, comme le prévoit la feuille de route.

1. **Une ligne de code.** Le nom de l'ensemble s'ajoute à la liste de ceux qui
   sont détaillés. Tout le reste est déjà générique.
2. **Résoudre ses communes sans contour**, pour sept ensembles sur dix. C'est le
   seul vrai travail technique, et il est en amont : il faut rapprocher les noms
   de communes de l'inventaire des noms actuels du fond de carte. Une commune
   fusionnée n'est pas une commune disparue ; le rapprochement est une décision
   documentée, pas une substitution automatique.
3. **Réécrire ses notices**, ou accepter le texte brut. Un ensemble ouvert sans
   réécriture fonctionne : le panneau affiche la notice telle quelle. Le mélange
   de lieux réécrits et de lieux bruts dans la même vue est possible mais se
   verrait.
4. **Décider de ses repères.** La Risle est le seul ensemble à avoir des points
   nommés le long de la rivière pour orienter le lecteur. Les onze autres n'en
   ont pas, et rien ne les produit automatiquement : c'est un choix éditorial
   par ensemble.
5. **Vérifier la carte sur sa propre géographie.** Le cadre s'ajuste tout seul à
   ce qu'il montre, mais le placement des noms et la densité des points se
   jugent à l'œil, ensemble par ensemble. Le cas de L'Aigle, où treize paires de
   points se touchent au zoom initial, est déjà connu.

**Ce qui ne demande rien du tout** : le panneau du lieu, la navigation, le
filtre, le clavier, le comportement sur écran étroit. Tout cela est générique et
a été éprouvé en L6.

---

## 4. Ce qui reste au porteur du projet

**L'examen visuel des lieux d'essai**, premier point de L7, n'est pas fait :
l'assistant ne peut pas photographier la page, l'onglet piloté ne produisant
aucune image. Les six lieux de L6 sont à regarder dans un navigateur ordinaire.

**Trois décisions attendent, et deux d'entre elles se prennent ensemble :**

1. **La hauteur de l'image.** Le panneau le plus haut est à 885 pixels, le
   critère est 900. Monter la borne de l'image ferait passer une partie des
   lieux au-dessus. Il faut choisir entre l'image plus présente et le panneau
   court.
2. **Le présent sans date** — « subsiste », « aujourd'hui disparue »,
   « actuellement désaffecté » — dans une douzaine de textes réécrits. Trois
   options : afficher tel quel, attribuer à la notice, ou signaler comme non
   daté.
3. **Les 146 lieux sans ensemble.** Leur donner un mode lieu, ou les laisser
   points sur la carte.

**Et une décision de cap :** ouvrir les dix autres ensembles, ou approfondir les
deux qui le sont. Les chiffres ci-dessus permettent de trancher ; ils ne
tranchent pas.
