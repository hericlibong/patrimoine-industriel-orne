# Examen de l'essai D3 sur la carte d'ensemble — 19 septembre 2026

**Nature du document :** examen préalable, à la demande du porteur. Aucun code
n'est modifié, aucune décision n'est prise ici. Ce document ne remplace ni le
suivi de la carte, ni le journal des décisions : il les alimente.

**Périmètre examiné :** la carte de niveau ensemble dans la vue de référence,
l'état actuel de la branche d'essai D3 (travail non enregistré), et le plan
inscrit en tête du suivi de la carte.

---

## 1. Les faits nus

L'essai D3 est réel et il fonctionne. Trois choses ont été faites :

| Ce qui a été ajouté | Où cela agit | État |
| --- | --- | --- |
| La bibliothèque D3 (version 7.9.0) embarquée dans la page, sans appel distant | Toute la page | Fait |
| Les 43 lieux et les 650 tracés d'eau de la Risle recopiés au format GeoJSON | Uniquement la Risle | Fait |
| Un zoom et un déplacement avec trois commandes (« + », « − », « Vue initiale ») | Uniquement la Risle | Fait, une correction déjà appliquée |

Ce qui n'a pas bougé : la carte du département, la carte de Crulai, les données,
les fiches, les preuves documentaires, les filtres par métier et les retours.
Elles continuent de fonctionner exactement comme avant, par l'ancien chemin de
dessin, qui n'a pas été retiré.

Deux chiffres résument la situation matérielle : la page produite pesait
356 kilo-octets avant l'essai, elle en pèse **899** aujourd'hui. La bibliothèque
en explique 280 ; les **263 restants sont de la donnée recopiée en double**
(voir § 3.2).

---

## 2. Le constat central

> **D3 est présent dans la page, mais la carte n'est pas construite avec D3.**

C'est, à mon avis, l'explication exacte du sentiment du porteur : « on n'arrive
pas à tirer le potentiel ». Ce n'est pas un problème de compétence de l'agent
précédent, ni un problème d'ambition graphique. C'est un problème de **place**
donnée à l'outil.

Sur les quelque 1 350 lignes du gabarit, D3 est appelé à **sept endroits**, pour
trois services seulement : convertir une forme géographique en trait de dessin,
gérer le zoom, et remettre le zoom à zéro. Tout le reste — créer les points,
les traits, les noms, les réagencer quand on change de métier, gérer le survol,
le clavier, les couleurs, les tailles — reste écrit à la main, élément par
élément, exactement comme avant l'arrivée de D3.

Autrement dit : **la bibliothèque a été posée à côté du dessin, pas dessous.**
Tant qu'elle reste à côté, elle ne peut rien apporter d'autre que ce qu'elle
apporte aujourd'hui, c'est-à-dire un zoom et un convertisseur de tracés. Tout
enrichissement demandé à partir de là coûtera le prix fort, parce qu'il faudra
l'écrire à la main.

### Ce que « construire avec D3 » veut dire concrètement

La différence tient en une phrase. Aujourd'hui, quand le lecteur change de
métier, **la carte entière est effacée puis redessinée de zéro**. Avec D3 employé
pour ce qu'il est, on dirait plutôt : « voici les lieux à montrer maintenant » —
et la bibliothèque se charge d'ajouter ceux qui manquent, de retirer ceux qui
partent et de faire bouger ceux qui restent.

Cette différence n'est pas cosmétique, elle décide de tout ce qui suit :

- On ne peut pas **animer** une carte qu'on efface. Or « la carte se recadre au
  lieu d'atténuer » est une décision arrêtée de l'architecture : un recadrage qui
  se voit se fait par un mouvement, pas par un clignotement.
- On ne peut pas **faire apparaître les noms au zoom** (phase 3 du plan) si
  chaque redessin repart de rien.
- On ne peut pas **mettre en évidence les lieux liés au lieu ouvert** (phase 4)
  sans reconstruire toute la carte à chaque clic.

Les phases 3 et 4 du plan actif buteront donc sur le même mur, l'une après
l'autre, tant que ce point n'est pas tranché.

---

## 3. Ce qui est fragile dans l'état actuel

Les points ci-dessous ont été vérifiés dans le code. Ils sont classés du plus
structurant au plus local.

### 3.1 Deux chemins de dessin coexistent

La Risle est dessinée par un chemin, le département et Crulai par un autre. Les
deux produisent aujourd'hui le même résultat, mais ils devront être corrigés
deux fois à chaque évolution, et ils divergeront. C'est le coût caché le plus
sûr de l'état actuel.

### 3.2 Toutes les données de la Risle existent maintenant en double

Les 43 lieux sont présents deux fois dans la page : sous leur forme d'origine, et
recopiés dans le format GeoJSON avec **l'intégralité de leurs propriétés**. Le
code de dessin lit ensuite la copie GeoJSON… **pour en reconstituer aussitôt la
forme d'origine**. Le détour ne sert à rien. Les 650 tracés d'eau sont dans le
même cas.

Ce doublement est la cause des 263 kilo-octets évoqués plus haut. Pour les
tracés d'eau, le format GeoJSON est utile (il alimente vraiment le convertisseur
D3) ; pour les lieux, il est aujourd'hui purement décoratif.

### 3.3 Les 650 tracés d'eau produisent 650 éléments de dessin

Chacun est créé un par un, à chaque redessin. C'est le poste le plus lourd de la
carte. D3 sait dessiner une collection entière de tracés **en un seul élément par
catégorie** — ici deux, la Risle principale et les branches secondaires. Le gain
serait immédiat et sans effet visible sur le rendu.

### 3.4 Les repères de bourg grossissent avec le zoom

Le porteur avait déjà signalé ce défaut pour la bulle d'identification ; il a été
corrigé pour elle. Il subsiste, non corrigé, pour **les quatre petits carrés des
localités** : ils sont placés dans le groupe que le zoom agrandit, et la
compensation de taille ne traite que les points industriels et les noms. À zoom
maximal, ils sont six fois trop grands.

Par ailleurs, les noms de bourgs sont positionnés une fois pour toutes au
cadrage initial : dès qu'on zoome, ils s'éloignent du bourg qu'ils désignent, et
le travail d'évitement des chevauchements ne vaut plus.

### 3.5 Le placement des noms est très coûteux

Pour poser les cinq noms sans chevauchement, le code essaie **toutes les
positions possibles** sur la carte, par pas de quelques unités, et vérifie
chacune contre environ 370 obstacles. Cela représente de l'ordre de plusieurs
dizaines de millions de comparaisons — refaites à chaque changement de filtre et
à chaque redimensionnement de la fenêtre. C'est la cause probable de lenteurs
ressenties au redimensionnement. Là encore, D3 propose un outil fait pour ça.

### 3.6 Le zoom est réinstallé à chaque rendu et la molette est désactivée

Réinstaller le comportement de zoom à chaque affichage est inutile et fait le
lit de doublons d'écoute. Surtout, la molette et le double-clic ont été
volontairement neutralisés : sur une carte, ce sont les deux gestes que tout
lecteur essaie en premier. Le choix est défendable (éviter de capturer le
défilement de la page) mais il devrait être un arbitrage explicite du porteur,
pas un effet de bord ; des solutions intermédiaires existent (molette avec
touche, ou zoom à la molette une fois la carte « saisie »).

Enfin, les trois commandes agissent instantanément, sans mouvement : le lecteur
perd le lien entre l'avant et l'après. C'est précisément ce qu'une transition
règle en une ligne.

---

## 4. Ce que D3 pourrait apporter, sans « carte sophistiquée »

Le porteur demande explicitement de ne pas viser la prouesse. Voici donc, classé
par rapport bénéfice/effort, ce que l'outil donne presque gratuitement **une fois
qu'il tient réellement le dessin** — et à quoi chaque élément sert dans la
publication.

| Apport | Ce que le lecteur y gagne | Phase du plan concernée |
| --- | --- | --- |
| Mise à jour au lieu de redessin | Le changement de métier devient un mouvement lisible, pas un clignotement | Structure — préalable à tout le reste |
| Transitions de zoom et de recadrage | On ne perd pas le fil quand la carte bouge ; on comprend d'où l'on vient | Phase 2, finition |
| Apparition des noms selon le zoom | Vue générale sobre, détails en s'approchant | Phase 3, telle quelle |
| Mise en évidence d'un lieu et de ses liens | Voir immédiatement qui est relié à qui | Phase 4, telle quelle |
| Détection du point le plus proche du curseur | **Règle le problème des points serrés autour de L'Aigle** sans déplacer aucune coordonnée : on vise une zone, pas un cercle de 5 unités | Difficulté signalée par le porteur, encore ouverte |
| Placement de noms par répulsion | Remplace la recherche exhaustive du § 3.5, et tient au zoom | Phases 3 et 6 |
| Échelles de taille et de couleur | La légende devient une conséquence du code, plus une liste tenue à la main | Phase 6 |
| Dessin de n'importe quelle couche géographique | Forêts, relief : le même mécanisme que l'eau, déjà éprouvé | Phase 5 |

Le point à retenir : **six des sept phases restantes du plan reposent sur le même
préalable**. Ce préalable n'est pas une nouvelle fonctionnalité, c'est un
changement de la façon dont la carte est écrite.

---

## 5. Un problème de méthode, distinct du code

Il faut le dire clairement, parce qu'il pèse plus lourd que tout le reste.

**Aucune des étapes de l'essai D3 n'a été vue dans un navigateur.** Le suivi le
répète honnêtement à chaque bilan : « contrôle simulé », « aucune capture »,
« aucun navigateur disponible dans cette session ». Les contrôles effectués sont
sérieux — ils comparent des coordonnées, des nombres, des identifiants — mais
ils ne peuvent rien dire de ce qui est justement en jeu : la lisibilité.

Conséquence visible dans le document : **toutes les cases « validation du
porteur » sont décochées, sur les deux phases déclarées faites.** Le travail
avance techniquement, mais aucune boucle de jugement ne se referme. Le défaut de
la bulle qui grossissait n'a pas été trouvé par un contrôle, il a été trouvé par
le porteur — et son jumeau, les carrés de localité, est toujours là (§ 3.4).

C'est réparable : l'environnement de travail actuel dispose d'un navigateur
pilotable. Le rendu réel peut être ouvert, mesuré et capturé à chaque étape.

**Second point de méthode :** le document de suivi porte aujourd'hui **deux plans
actifs qui se contredisent**. En tête, le plan D3, dont la phase 2 est marquée
« À FAIRE MAINTENANT » alors que toutes ses cases de réalisation sont cochées.
Plus bas, le plan « Développement SVG », dont l'étape 4 est annoncée comme la
prochaine à exécuter. Les deux ne peuvent pas être vrais en même temps. Un
lecteur — humain ou agent — qui ouvre ce fichier ne peut pas savoir quoi faire.

---

## 6. Recommandation

**Une seule question à trancher :** D3 doit-il tenir le dessin de la carte, ou
rester un outil d'appoint posé à côté ?

**Ma recommandation : qu'il le tienne.** Trois raisons courtes.

1. Six des sept phases restantes en dépendent ; le mur sera le même à chaque
   fois, et de plus en plus cher à franchir.
2. Deux chemins de dessin coexistent aujourd'hui ; les garder tous les deux
   coûte davantage que d'en avoir un seul.
3. Cela ne demande aucune sophistication graphique — c'est une réécriture **à
   résultat visuel identique**, vérifiable par les contrôles existants, qui
   comparent précisément les nombres, les coordonnées et les parcours.

**La nuance**, clairement séparée : cette réécriture touche le cœur d'une carte
déjà validée sur trois points par le porteur (l'eau, les localités,
l'identification au survol). Elle ne doit donc pas être engagée sans un moyen de
prouver que rien n'a bougé. Ce moyen existe déjà pour les nombres ; il manque
pour l'image. Il faut donc **d'abord rétablir le contrôle visuel réel**, et
seulement ensuite toucher au dessin.

### Ordre proposé

1. **Voir l'existant.** Ouvrir la vue actuelle dans un navigateur, à 1440 px puis
   en écran étroit, et fixer par des captures l'état de référence : sans filtre,
   sous Métallurgie, à zoom 1, 3 et 6. Rien n'est modifié à cette étape.
2. **Corriger les deux défauts avérés** du § 3.4 — les carrés de localité et les
   noms qui dérivent au zoom. Petits, isolés, vérifiables immédiatement.
3. **Supprimer la donnée en double** du § 3.2. Sans effet visuel ; la page
   retrouve environ 260 kilo-octets.
4. **Réécrire le dessin de la Risle avec D3, à résultat identique**, en
   regroupant les tracés d'eau (§ 3.3). Comparaison avant/après par captures et
   par les contrôles chiffrés existants.
5. **Étendre le même chemin** au département et à Crulai, pour n'en garder qu'un.
6. Seulement alors, reprendre les phases 3 et 4 du plan, qui deviennent des
   ajouts simples.

### Décision à rédiger, si le porteur suit cette recommandation

> **Décision : la carte d'ensemble est réécrite pour que D3 tienne son dessin,
> avant toute nouvelle fonctionnalité.** Cette réécriture se fait à résultat
> visuel identique et doit être prouvée par un contrôle dans un navigateur réel,
> à 1440 px et sur écran étroit, avant et après. Le plan D3 en tête du suivi
> devient le seul plan actif ; le plan « Développement SVG » est versé à
> l'historique, ses étapes 4 à 6 restant à reprendre après la réécriture. La
> molette de zoom, aujourd'hui neutralisée, fait l'objet d'un arbitrage séparé.

---

## Annexe technique — repères pour l'exécution

*Cette annexe nomme les fichiers et les fonctions ; elle ne fait pas partie de
l'explication ci-dessus.*

**Fichiers concernés :** `tools/vue_reference_gabarit.html` (gabarit, 1 354
lignes), `tools/generer_vue_reference.py` (générateur, 620 lignes),
`prototype/vue_reference/index.html` (produit, régénéré), `tools/vendor/d3.v7.9.0.min.js`
(non versionné à ce jour, avec sa licence ISC).

**Les sept appels D3 recensés :** `d3.zoomIdentity` (l. 375, 1088, 1101),
`d3.geoTransform` (l. 397), `d3.geoPath` (l. 553), `d3.select` (l. 835, 852, 866,
872), `d3.zoom` (l. 837).

**Points de code cités dans le rapport :**

| § | Emplacement |
| --- | --- |
| 3.1 | `dessinerSysteme`, branche `if(code === "risle" && detail.geojson …)` l. 552-571 |
| 3.2 | `geojson_systeme` (générateur, l. 413-440) ; consommation l. 527-533 |
| 3.3 | boucle `for(const feature of detail.geojson.eau.features)` l. 554 |
| 3.4 | `ajusterTailleZoom` l. 813-825 ne traite que `circle.site` et `text[data-repere]` ; les `rect[data-bourg]` créés l. 677 sont dans `contenuCarte` |
| 3.5 | double boucle de recherche de placement, l. 715-722 |
| 3.6 | `installerZoomRisle` l. 834-849 ; filtre excluant `wheel` et `dblclick` l. 842-843 |

**Ce qui est correctement fait et ne doit pas être défait :** la projection
maison de `cadrer()` (l. 383-403) garantit l'emprise stable arbitrée le
18 septembre — si elle est remplacée par une projection D3, l'équivalence doit
être démontrée coordonnée par coordonnée ; le repositionnement de la bulle
d'identification par `zoomRisle.apply()` (l. 757) est la bonne méthode et sert
de modèle pour le correctif du § 3.4 ; la couche d'interface non transformée
(`coucheInterface`) est le bon dispositif et doit accueillir tout ce qui ne doit
pas grossir ; l'accès clavier des points et des relations, avec `role="button"`
et gestion d'Entrée/Espace, est complet et doit survivre à la réécriture.
