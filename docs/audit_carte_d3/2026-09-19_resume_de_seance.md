# Séance du 19 septembre 2026 — résumé

Branche `codex/carte-d3-modele-risle`, ouverte ce jour depuis l'essai D3 figé.
Six enregistrements. Rien n'est envoyé au dépôt distant.

## Le point de départ

La carte des ensembles n'avançait plus. Un examen a été demandé avant de
poursuivre. Ouverte dans un navigateur — ce qui n'avait jamais été fait pour
l'essai D3 — la carte **figeait à l'affichage de la Risle**.

La mesure a donné la cause : dessiner toute la carte coûtait 15 millisecondes,
placer les cinq noms de bourgs en coûtait 480. Trente fois le reste de la carte,
pour cinq mots.

L'examen a montré autre chose, plus grave : **D3 était dans la page mais ne
tenait pas le dessin.** Sept appels sur environ 1 350 lignes, pour trois
services. La Risle était dessinée par un code distinct, désigné par son nom, à
côté de celui du département et de Crulai. Un ensemble traité par exception ne
pouvait pas servir de modèle aux onze autres.

## Ce qui a été fait

**Phase 0 — débloquer l'affichage.** Rasterisation de l'occupation de la carte :
480 ms → 35 ms. Signes de localité compensés au zoom. Recopie inutile des lieux
supprimée.

**Phase 1 — le cadre et le sol.** Le cadre prend la proportion de ce qu'il
montre. Les points passent de 5,5 à 7. La carte reçoit un sol : toutes les
communes touchant le cadre, jamais les seules communes de l'ensemble — une forme
fermée se lirait comme une frontière, ce que la méthode interdit.

**Phase 2 — le dessin tenu par D3.** La carte n'est plus effacée puis refaite à
chaque geste ; ses couches sont posées une fois et mises à jour. Un seul chemin
de dessin pour les trois niveaux. Éléments de dessin 713 → 121, page 1014 →
813 ko.

**Phase 3 — l'eau, les lieux, les liens.** Gaine claire sous l'eau et les liens,
hiérarchie de la rivière franchie, contour des lieux épaissi. Le sens des liens,
présent dans les données, est porté sur la carte par une pointe orientée. Les
crédits disent que le fond est contemporain.

**Phase 4 — le mouvement et l'approche.** Le changement de métier devient un
mouvement. Passé un zoom de 2,2, les lieux prennent leur nom sans se recouvrir.
Les noms de bourgs cessent de décrocher au zoom.

**Bloc A — la première impression.** Le texte de quatre lignes au-dessus de la
carte supprimé. La légende descendue dans un cartouche posé dans le coin le plus
vide, choisi à chaque rendu. Une échelle ajoutée. L'effet du filtre sorti de la
carte, à côté du sélecteur. Quatre défauts d'écran étroit trouvés et corrigés.

**Bloc B — lire les liens d'un lieu.** Un lieu ouvert montre ses partenaires par
un anneau et ses liens en trait plein. Le groupe dense de L'Aigle est rendu
atteignable **sans déplacer aucun point** : la cible s'élargit, le survol et le
clic désignent le lieu le plus proche du curseur.

**Bloc C — juger et transposer.** Plus aucune ligne de code ne nomme la Risle.
Crulai reçoit d'un coup tout ce qui a été construit. Le coût d'ouverture d'un
ensemble de plus est chiffré.

## Ce que cela a coûté et rapporté

| | Avant | Après |
| --- | --- | --- |
| Affichage de la Risle | figeait le navigateur | 6 ms |
| Placement des cinq noms | 480 ms | 35 ms |
| Éléments de dessin | 713 | 121 |
| Poids de la page | 356 ko puis 899 | 857 ko, sol compris |
| Cartouche sur carte étroite | 83 % de la carte | 9 % |
| Crédits sur carte étroite | 173 % de sa hauteur | 43 % |
| Rayon des points, carte étroite | 2,5 px | 5 px |

## Les décisions prises

Quatre entrées ont été ajoutées au journal des décisions, à cette date.

1. **La Risle est écrite comme cas général, non comme exception.** Un seul
   chemin de dessin pour les trois niveaux. L'essai D3 antérieur est conservé
   figé sur sa branche.
2. **Le cadre prend la proportion de ce qu'il montre ; le sol couvre tout le
   cadre et déborde.** Réouverture assumée de l'arbitrage du 18 septembre sur
   les dimensions ; l'emprise et la projection sont inchangées.
3. **La végétation contemporaine n'entre pas dans la carte.** La forêt de
   2006-2019 derrière une forge de 1700 ferait lire un lien de cause faux. Seules
   les forêts anciennes reconstruites vers 1850 seront envisagées ; le relief est
   la piste à instruire d'abord.
4. **Les crédits disent que le fond est contemporain** et signalent que les
   biefs et retenues de moulin n'y figurent pas.

Une cinquième décision, prise par le porteur en cours de séance : **le texte
au-dessus de la carte est supprimé entièrement**, et non raccourci. Elle rouvre
en partie la décision du 14 août sur le mode d'emploi.

## Le suivi de la carte a été refondu

Les sept phases du plan d'expérimentation D3, dont l'objet est atteint, sont
versées à l'historique du document et remplacées par trois blocs. Le second
plan, « Développement SVG », est marqué comme historique. La référence de
travail annoncée dans le document est actualisée.

## Ce qui reste ouvert

**Jugements du porteur.** Aucun bloc n'est validé : les cases de validation des
blocs A, B et C sont décochées, ainsi que celles des quatre phases.

**Vérifications non faites.**

- L'essai dans une vraie fenêtre étroite. L'onglet de contrôle s'est mis en
  arrière-plan en cours de séance et a cessé de produire des images ; le
  déclenchement automatique au redimensionnement n'a donc pas pu être éprouvé.
  Le lecteur qui arrive sur un écran étroit reçoit la bonne mise en page sans en
  dépendre, et ce chemin est vérifié.
- Le toucher sur un appareil réel.

**Questions de données et d'arbitrage.**

- **Le poids à douze ensembles.** Chaque ensemble ajoute de 170 à 300 ko ; les
  douze porteraient la page à environ trois mégaoctets. Il faudra choisir entre
  le fichier unique autonome et le chargement de chaque vallée à l'ouverture.
- **Les communes d'archive sans contour actuel.** Trois noms, neuf lieux, deux
  ensembles bloqués. Note dédiée : `note_communes_anciennes.md`.
- **Les repères de bourg** pour les dix autres ensembles. Travail de
  vérification de sources, non automatisable, avec un choix éditorial à chaque
  vallée.
- **Les petits ensembles.** Crulai est presque vide : sept lieux, aucune
  relation, aucun repère. La carte fonctionne mais dit peu. Le porteur a
  constaté que le remède viendrait des données plus que du dessin.

**Difficultés acceptées.**

- La densité autour de L'Aigle subsiste à faible zoom : 13 paires de lieux à
  moins de huit pixels l'une de l'autre à l'ouverture, aucune au zoom 6. Le zoom
  est la réponse, la liste du panneau est l'autre chemin.

## Incidents de méthode consignés

- Une suppression de style a d'abord emporté environ soixante-dix lignes de CSS
  sans rapport, réparées immédiatement par comparaison avec la version
  enregistrée.
- Un diagnostic erroné a été rendu puis corrigé : l'observateur de largeur était
  accusé de ne pas se déclencher faute de référence, alors que l'onglet ne
  produisait plus d'images.
- Une affirmation de l'examen initial s'est révélée fausse à la mesure : le cadre
  n'était pas vide à moitié et le resserrer ne grossit pas les points. Corrigé
  dans le journal des décisions.

## Documents produits

| Fichier | Objet |
| --- | --- |
| `2026-09-19_examen_essai_d3.md` | l'examen initial et son diagnostic |
| `journal_phases_carte.md` | le détail, les mesures et les limites de chaque phase |
| `note_communes_anciennes.md` | note de recherche sur les trois communes disparues |
| `2026-09-19_resume_de_seance.md` | le présent résumé |
