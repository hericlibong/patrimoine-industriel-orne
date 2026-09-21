# T5 — Épreuve du filtre d'époque

**21 septembre 2026.** Dernière tâche du filtre temporel. Le filtre est éprouvé
sur les deux ensembles ouverts, sur trois ensembles fermés, sur ordinateur et
sur mobile, au clavier. Les contrôles sont ceux de L6, appliqués au filtre.

---

## Les ensembles fermés comptent juste

Un ensemble fermé n'a pas de vue détaillée : il n'existe, pour le filtre, que
par la pastille de la carte et la ligne de la liste. Son décompte vient d'un
calcul préparé à la génération, et non d'une liste de lieux. Il fallait vérifier
que ce raccourci ne ment pas.

| Ensemble | Av. 1789 | 1789‑1849 | 1850‑1913 | 1914‑1945 | 1946‑1975 | 1976‑2000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Vallée du Noireau | — | 16 | 18 | 11 | 12 | 3 |
| Flers | — | 3 | 15 | 13 | 17 | 11 |
| Argentan | 1 | 3 | 5 | 3 | 4 | 3 |

**Ces dix-huit nombres sont exactement ceux du relevé de T1**, et ce sont aussi
ceux que la liste affiche à l'écran. Les deux chemins — le décompte préparé et
l'affichage — ont été comparés séparément au relevé.

---

## Le parcours complet

Quatre états du métier — aucun, métallurgie, agroalimentaire, textile — croisés
avec les sept états de l'époque. Pour chacune des vingt-huit combinaisons :
le niveau départemental, puis l'entrée dans la Risle et dans Crulai, puis
l'ouverture d'un lieu quand il en reste un, puis le retour.

**125 cas parcourus. Aucune erreur, aucun problème.**

| Contrôle | Résultat |
| --- | --- |
| Aucune erreur JavaScript | tenu |
| Aucun ensemble listé sans contenu | tenu |
| Aucun panneau vide | tenu |
| La liste compte comme la règle | tenu |
| Aucun cul-de-sac : le retour existe toujours | tenu |
| L'état du filtre survit au passage dans un lieu | tenu |
| Aucun code technique ni mention parasite à l'écran | tenu |
| Un ensemble vidé le dit au lieu de rester muet | tenu |

---

## Les hauteurs

Le panneau le plus haut atteint **603 pixels** au niveau département et
ensemble, sous n'importe quelle combinaison de filtres. Le critère du panneau
court de L2 — tenir sous 900 — est tenu.

Le panneau d'un lieu mesure **829 pixels avec son image, filtre actif ou non,
au pixel près**. Le filtre ne touche pas au panneau du lieu, et il ne devait pas
y toucher.

---

## Mobile

À 390 pixels de large, les sept états de l'époque parcourus, les deux ensembles
ouverts visités, un lieu ouvert à chaque fois :

- **Aucun débordement horizontal**, nulle part.
- Les deux sélecteurs s'empilent et prennent toute la largeur.
- Le compteur « 2 lieux sans date » reste lisible.
- Les filtres sont bien masqués pendant la lecture d'un lieu.

**Une réserve, et c'est la seule de T5.** La barre des filtres passe de 149 à
**207 pixels** dès qu'une époque est choisie — deux étiquettes, deux sélecteurs
empilés et le compteur, avant que la carte commence. C'est beaucoup sur un
téléphone. Le problème est d'habillage, non de structure : il revient à 10.E.

---

## Clavier

Le parcours complet a été fait au seul clavier : choisir une époque, entrer dans
un ensemble, ouvrir un lieu, remonter par Échap jusqu'au département. Vingt et
un éléments focalisables au département, quatre-vingt-quinze dans un ensemble,
quatre-vingt-douze dans un lieu. Les deux sélecteurs sont atteignables, Échap
remonte d'un niveau à chaque appui, et le filtre est intact au bout du parcours.

### Un défaut trouvé et corrigé

**Après un choix, le focus n'était pas rendu au sélecteur.** Une personne
naviguant au clavier se retrouvait sans point de retour, rejetée au début du
document.

La cause est une condition que j'avais ajoutée en généralisant la fermeture aux
deux sélecteurs : elle ne rendait le focus que si le sélecteur était encore
marqué comme ouvert. Or l'affichage est reconstruit avant la fermeture, et il
avait déjà remis cette marque à faux. La condition n'était donc jamais vraie.

Corrigé : quand un sélecteur est nommé, le focus lui est rendu sans condition.
Vérifié ensuite sur les deux sélecteurs, au clavier et à la souris.

---

## Ce qui reste connu et assumé

| Point | Statut |
| --- | --- |
| La barre des filtres fait 207 pixels sur mobile | Habillage, renvoyé à 10.E |
| Le compteur annonce 2 lieux sans date et non 4 | Décidé : il dit ce qu'il montre ; la méthode dira ce que porte le corpus |
| Le cadre de la Risle ne se recadre pas | Comportement décidé pour ses repères de bourgs, antérieur au filtre |
| Le filtre strict par phase d'activité | Option future, séparée, hors première version |
| « Depuis 2001 » | Retirée du filtre, conservée dans le vocabulaire |

---

**T5 est fait. Les cinq tâches du filtre temporel sont closes. La phase 10.D
peut être reclose.**
