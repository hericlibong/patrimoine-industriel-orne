# Classifications — qualité

Statut : **bloc 3 de la phase 4 validé le 21 juillet 2026**.

La source exécutable des vocabulaires est `config/classifications.yml`.

## Trois dimensions différentes

| Dimension | Question | Exemple |
|---|---|---|
| type de géométrie | quelle forme est stockée ? | point ou polygone |
| méthode de localisation | comment a-t-elle été produite ? | cadastre ou géocodage |
| précision géographique | que localise-t-elle réellement ? | bâtiment vérifié ou point approximatif |

Ces dimensions ne sont jamais fusionnées. La fiabilité constitue encore une
quatrième dimension : elle indique la solidité de la preuve utilisée.

## Précision géographique

| Code | Signification |
|---|---|
| `emprise_site_verifiee` | limites de l'ensemble industriel contrôlées |
| `parcelle_verifiee` | parcelle rattachée au site et contrôlée |
| `batiment_verifie` | bâtiment industriel identifié |
| `point_site_verifie` | point contrôlé sur le site |
| `point_adresse` | adresse géocodée sans validation du bâtiment |
| `point_approximatif` | emplacement approximatif dans une zone connue |
| `zone_documentaire` | zone historique non encore alignée sur le terrain actuel |

Les quatre premiers codes nécessitent une validation humaine. Une coordonnée
présente dans une source ne devient pas automatiquement une géométrie vérifiée.

`commune_seule` et `non_localise` sont des statuts de localisation sans
géométrie de site. Le centre d'une commune ne peut pas servir de faux emplacement.

## Fiabilité

| Code | Critère minimal |
|---|---|
| `forte` | preuve directe, cible non ambiguë, aucune contradiction ouverte |
| `moyenne` | recoupement indirect concordant ou interprétation simple contrôlée |
| `faible` | indice unique, ambiguïté, hypothèse ou contradiction ouverte |

Le niveau est attribué à l'information concernée. Une source officielle peut
être précise sur une protection et insuffisante sur l'emplacement actuel. Une
valeur `faible` peut être conservée, mais elle ne doit pas être publiée comme un
fait certain.

## Emploi de `autre`

Employer `autre` uniquement lorsqu'une valeur est réellement documentée mais
qu'aucun code du vocabulaire ne convient. Sont obligatoires :

- le libellé original ;
- une justification ;
- une validation humaine.

Ne jamais employer `autre` pour une valeur absente, inconnue, non applicable ou
simplement incertaine. Trois occurrences sur des entités distinctes déclenchent
une revue du vocabulaire, sans création automatique d'un nouveau code.

## Emploi de `inconnu`

Employer `inconnu` seulement si la question est applicable, a été examinée et
reste sans réponse. Distinguer :

- source vide : `NULL` et `non_renseignee_source` ;
- question sans objet : `NULL` et `non_applicable` ;
- valeur candidate incertaine : valeur conservée et `a_verifier` ;
- recherche effectuée sans résultat : `inconnu`.

## Reproductibilité

Une classification reproductible utilise la même version du registre, conserve
les valeurs sources et produit une sortie canonique triée. Chaque rapport reçoit
une empreinte SHA-256. Un changement d'empreinte doit provenir d'une modification
identifiée des entrées, du code ou du registre.

Le test automatique est complété pendant le pilote par un double classement
humain d'un sous-échantillon de cas simples et ambigus.
