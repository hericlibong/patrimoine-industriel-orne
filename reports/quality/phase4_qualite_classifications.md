# Phase 4 — qualité des classifications

Date du contrôle : 21 juillet 2026.

## Résultat

Le bloc est validé techniquement. Les classements sectoriels, contemporains et
de qualité ont été rejoués avec les mêmes entrées dans un ordre inversé. Les
sorties sont identiques et possèdent une empreinte SHA-256 stable.

Cette validation prouve la reproductibilité du traitement automatique. Elle ne
prouve pas encore que deux personnes classeront de la même façon un cas ambigu :
ce contrôle devra être effectué sur une partie du corpus pilote.

## Précision géographique

Sept niveaux sont retenus : emprise du site, parcelle, bâtiment, point du site,
point d'adresse, point approximatif et zone documentaire.

La précision ne décrit ni le type de géométrie ni la méthode utilisée. Un point
peut par exemple avoir été placé après contrôle d'une parcelle. La méthode reste
enregistrée séparément.

`centre_commune` et `non_localise` sont retirés du vocabulaire de précision :
ils décrivent l'absence de géométrie de site. Un site connu seulement par sa
commune n'est jamais placé artificiellement au centroïde communal.

### Test des sources

- POP/Mérimée : 10 points fournis et 9 emprises candidates sur 10 notices ;
- CASIAS : 10 entrées avec coordonnées et 10 sans coordonnées dans l'échantillon ;
- géométries automatiquement qualifiées « vérifiées » : 0.

La présence de coordonnées ou d'un contour source ne suffit donc jamais à
attribuer un niveau vérifié sans contrôle spatial adapté.

## Fiabilité

Trois niveaux seulement sont conservés :

- `forte` : preuve directe, cible non ambiguë, aucune contradiction ouverte ;
- `moyenne` : information indirecte mais concordante, ou interprétation simple
  et contrôlée ;
- `faible` : indice unique, ambiguïté, hypothèse ou contradiction ouverte.

La fiabilité s'applique à une information ou une relation, pas à une source dans
son ensemble. `a_verifier` est un statut de travail et non un niveau de
fiabilité. Le nombre de sources ne suffit pas, à lui seul, à augmenter le niveau.

## `autre` et `inconnu`

`autre` signifie qu'une valeur est positivement connue mais absente du
vocabulaire. Il exige le libellé source, une justification et une validation
humaine. À partir de trois occurrences distinctes, le vocabulaire doit être
réexaminé.

`inconnu` signifie que la question est applicable et a été examinée sans qu'une
réponse soit obtenue. Un champ vide dans une source devient `NULL` avec le statut
`non_renseignee_source`, pas `inconnu`. Une question sans objet devient `NULL`
avec `non_applicable`.

## Reproductibilité

Les trois contrôles réussissent :

- secteurs identiques après inversion de l'ordre des notices ;
- situation actuelle identique après inversion des notices POP et MH ;
- grille de qualité identique lors d'une seconde exécution.

Les mesures et empreintes complètes sont conservées dans
`reports/quality/phase4_qualite_classifications.json`.

L'ensemble des 63 tests automatisés du projet réussit après intégration de ces
règles.
