# Règles du modèle de données

Statut : **modèle V1 approuvé — règles version 1.2**

Date : 21 juillet 2026

## 1. Identifiants internes stables

### Règle générale

Les entités métier utilisent un UUID version 4 généré une seule fois lors de la
création de la ligne. Cet identifiant :

- ne contient aucune signification éditoriale ;
- ne dépend ni du nom, ni de la commune, ni d'une source ;
- n'est jamais recalculé lors d'une nouvelle extraction ;
- n'est jamais réutilisé pour une autre entité ;
- reste identique dans DuckDB, les exports et l'application.

Exemple :

```text
site_id = 1c2a3a8f-8cb0-4ec2-8b87-72c0a410ca78
```

Les références `IA`, `PM`, `PA`, `SSP`, `BNO`, ARK, SIREN et codes OSM restent
des identifiants externes. Elles sont enregistrées dans
`identifiants_externes`, avec la source et le type de référence.

`sources.source_id` fait exception : il reste un code lisible, stable et
versionné, par exemple `pop_merimee` ou `casias`.

### Réextraction et rapprochement

Une nouvelle extraction recherche d'abord un identifiant externe déjà connu.
Elle met à jour ou complète l'entité existante au lieu de créer un nouvel UUID.

Une ressemblance de nom, de commune ou de coordonnées ne suffit jamais pour
réutiliser automatiquement un UUID.

Une ressemblance crée au maximum une ligne dans
`propositions_rapprochement`. Les deux candidats restent séparés jusqu'à une
décision humaine documentée.

### Fusion de doublons

Si deux sites internes sont ensuite reconnus comme un seul lieu :

1. un `site_id` canonique est choisi ;
2. l'autre ligne passe au statut `fusionne` ;
3. `site_id_canonique` indique la destination ;
4. les anciennes références restent consultables ;
5. aucun identifiant n'est supprimé ou réattribué.

`relations_sites` ne sert pas à représenter cette fusion technique.

## 2. Relations entre les tables

| Parent | Enfant ou association | Cardinalité | Règle |
|---|---|---|---|
| `sites` | `activites` | 1 à plusieurs | une activité appartient à un seul site |
| `sites` | `etats_actuels` | 1 à plusieurs | chaque contrôle contemporain ajoute une observation |
| `sites` | `geometries` | 0 à plusieurs | un site peut rester non localisé |
| `sites` | `noms_sites` | 1 à plusieurs | les noms alternatifs ne sont pas concaténés |
| `activites` | `energies_activites` | 0 à plusieurs | une activité peut utiliser plusieurs énergies |
| `sites` et `exploitants` | `exploitations` | plusieurs à plusieurs | la relation peut préciser une activité et une période |
| `sites` et `objets_techniques` | `liens_objets_sites` | plusieurs à plusieurs | un objet peut changer de lieu |
| `sites` ou `objets_techniques` | `protections` | 0 à plusieurs | une protection vise exactement un type de cible |
| `sites` | `relations_sites` | plusieurs à plusieurs | les sites source et cible restent distincts |
| deux `sites` | `propositions_rapprochement` | plusieurs à plusieurs | une hypothèse de doublon ne fusionne rien |
| `sources` | `mentions_sources` | 1 à plusieurs | toute mention appartient à une source cataloguée |
| toute entité | `mentions_sources` | 0 à plusieurs | ciblage par type, identifiant et éventuellement champ |
| toute entité | `identifiants_externes` | 0 à plusieurs | une référence externe ne désigne qu'une entité active |

Les tables du corpus utilisent des suppressions logiques. Une ligne déjà citée
ou publiée n'est pas supprimée physiquement et aucune suppression en cascade
n'est autorisée dans les tables métier.

Les clés étrangères exactes sont créées dans le schéma DuckDB. Les cibles
génériques de `mentions_sources` et `identifiants_externes` sont contrôlées par
un validateur transversal.

## 3. Champs obligatoires

### Champs techniques communs

Toute entité métier possède :

- son identifiant interne ;
- `statut_enregistrement_code` ;
- `cree_le` ;
- `cree_par` ;
- `modifie_le`.

### Obligations par table

| Table | Champs toujours obligatoires |
|---|---|
| `sites` | `site_id`, statut du corpus, décision d'inclusion, fiabilité |
| `activites` | `activite_id`, `site_id`, libellé source ou code normalisé, fiabilité |
| `etats_actuels` | `etat_actuel_id`, `site_id`, date et méthode de vérification, fiabilité, au moins une dimension renseignée |
| `sources` | `source_id`, titre, producteur, rôle, statut d'audit |
| `mentions_sources` | `mention_id`, `source_id`, cible, nature, statut de valeur, date de consultation |
| `protections` | `protection_id`, une seule cible, type, référence, date de vérification |
| `objets_techniques` | `objet_technique_id`, nom ou dénomination, fiabilité |
| `geometries` | `geometrie_id`, `site_id`, géométrie, type, précision, méthode, fiabilité |
| `exploitants` | `exploitant_id`, nom principal, type |
| `exploitations` | `exploitation_id`, site, exploitant, rôle, fiabilité |
| `relations_sites` | identifiant, deux sites différents, type, statut, fiabilité |
| `propositions_rapprochement` | identifiant, deux candidats différents, méthode, statut, fiabilité |
| `identifiants_externes` | identifiant interne, source, type, valeur, entité cible |

### Obligations conditionnelles

- Un site `inclus` doit avoir une commune de l'Orne, une activité admissible et
  au moins une mention de source.
- Un site `cartographiable` doit avoir une géométrie de référence dont la
  précision est qualifiée.
- Un site `publie` doit avoir un nom éditorial, une décision validée et des
  sources affichables.
- Une activité permettant l'inclusion avant 1950 doit posséder une période
  compatible avec cette borne et une preuve.
- Une protection immobilière renseigne `site_id` ; une protection mobilière
  renseigne `objet_technique_id`, jamais les deux.
- Une relation symétrique impose un ordre canonique des deux UUID pour éviter
  deux lignes inversées.

## 4. Valeurs nulles et inconnues

### Signification de `NULL`

`NULL` signifie uniquement qu'aucune valeur normalisée n'est stockée dans ce
champ. Il ne signifie ni zéro, ni faux, ni « disparu », ni « aucune protection ».

La raison est conservée dans `mentions_sources.statut_valeur_code` :

- `renseignee` : une valeur est connue ;
- `inconnue` : la question a été examinée mais la réponse reste inconnue ;
- `non_renseignee_source` : la source ne fournit pas la valeur ;
- `non_applicable` : le champ n'a pas de sens pour cette entité ;
- `contradictoire` : plusieurs valeurs incompatibles sont conservées ;
- `a_verifier` : une valeur existe mais ne peut pas encore être validée.

### Valeurs interdites

Les données normalisées ne doivent jamais utiliser comme substitut de `NULL` :

- chaîne vide ou espaces ;
- `N/A`, `NC`, `?`, `-` ;
- date `0000-00-00`, année `9999` ;
- coordonnées `0,0` ;
- code numérique arbitraire.

Une chaîne vide présente dans une source peut rester dans `valeur_originale`,
mais devient `NULL` dans la table métier avec le statut
`non_renseignee_source`.

Les codes `inconnu`, `aucune_protection_connue` et similaires appartiennent aux
vocabulaires contrôlés. Les secteurs et activités sont définis ; l'emploi
détaillé des valeurs de qualité et de situation actuelle reste à vérifier dans
les blocs suivants de la phase 4.

## 5. Dates imprécises

Une date historique n'est jamais transformée en date exacte artificielle.
Chaque date structurée comporte :

```text
<nom>_min
<nom>_max
<nom>_precision_code
<nom>_texte_source
```

`min` et `max` décrivent l'intervalle possible. Le texte original est toujours
conservé.

| Texte source | Minimum | Maximum | Précision |
|---|---|---|---|
| `12 mars 1850` | 1850-03-12 | 1850-03-12 | `jour` |
| `mars 1850` | 1850-03-01 | 1850-03-31 | `mois` |
| `1850` | 1850-01-01 | 1850-12-31 | `annee` |
| `années 1850` | 1850-01-01 | 1859-12-31 | `decennie` |
| `vers 1850` | 1845-01-01 | 1855-12-31 | `vers_annee` |
| `avant 1850` | `NULL` | 1849-12-31 | `avant` |
| `après 1850` | 1851-01-01 | `NULL` | `apres` |
| `19e siècle` | 1801-01-01 | 1900-12-31 | `siecle` |
| `1er quart 19e siècle` | 1801-01-01 | 1825-12-31 | `quart_siecle` |
| `2e moitié 19e siècle` | 1851-01-01 | 1900-12-31 | `moitie_siecle` |

La marge de cinq ans pour `vers une année` est une convention calculée du
projet. Elle doit être identifiée comme telle dans la provenance.

Un intervalle ouvert utilise `NULL` pour la borne absente et un code de
précision `avant` ou `apres`, ce qui le distingue d'une date non renseignée.

Les analyses utilisent les intervalles. Aucun milieu d'intervalle n'est publié
comme date réelle.

## 6. Activités successives

Une nouvelle ligne `activites` est créée lorsque l'activité productive change
ou lorsqu'une interruption documentée sépare deux périodes.

Règles :

- forge puis moulin sur la même emprise : un site, deux activités ;
- deux productions simultanées : deux activités dont les périodes se
  chevauchent ;
- changement d'exploitant sans changement de production : même activité,
  nouvelle ligne `exploitations` ;
- changement d'énergie sans changement de production : même activité, nouvelle
  période dans `energies_activites` ;
- arrêt puis reprise documentée : deux phases d'activité ;
- transfert vers une autre emprise : nouveau site et `relations_sites` ;
- incertitude sur la transition : intervalles éventuellement chevauchants,
  jamais de date de rupture inventée ;
- une phase possède au plus un secteur principal ; les productions réellement
  distinctes sont séparées plutôt que classées arbitrairement `activite_mixte` ;
- le site entre dans le corpus principal si au moins une phase admissible se
  termine ou commence au plus tard en 1950.

L'usage contemporain d'un ancien bâtiment n'est pas une activité industrielle
historique : il appartient à `etats_actuels`.

## 7. Versionnement des observations actuelles

`etats_actuels` est un journal d'observations ajouté ligne par ligne.

Chaque nouvelle observation possède :

- un nouvel UUID ;
- un numéro de version croissant par site ;
- une date exacte de vérification ;
- un horodatage d'enregistrement ;
- les dimensions réellement vérifiées ;
- éventuellement `remplace_etat_actuel_id` ;
- un motif : nouvelle observation, correction ou annulation.

Une observation n'écrase et ne supprime jamais une ancienne ligne.

La vue `etats_actuels_courants` sélectionne, pour chaque site et pour chaque
dimension, la dernière valeur non annulée. Ainsi, une nouvelle vérification de
l'accessibilité ne remplace pas automatiquement une observation de conservation
encore valable.

Les usages sont des lignes de `usages_actuels` rattachées à une observation.
Plusieurs usages simultanés sont autorisés, mais un seul peut être principal.
`sans_usage` et `inconnu` ne peuvent pas coexister avec un usage connu.

Les durées de fraîcheur sont calculées séparément :

- accessibilité : 3 mois ;
- usage actuel : 12 mois ;
- conservation : 12 mois.

Une valeur périmée reste dans l'historique mais passe à `a_verifier` pour la
publication. Une observation sans date exacte ne peut pas être présentée comme
un état actuel ; elle reste une mention historique.

## Validation du bloc

Ces règles sont matérialisées par le schéma DuckDB, ses contraintes, le
validateur transversal et les tests automatisés. Les vocabulaires sectoriels
sont validés dans le premier bloc de la phase 4. Les classifications
chronologiques et contemporaines sont validées dans le deuxième bloc ; les
classifications de qualité restent provisoires.
