# Dictionnaire des données — brouillon V0

Ce dictionnaire sera validé après les premières extractions tests.

## Table `sites`

| Champ | Type prévu | Description |
|---|---|---|
| `site_id` | texte | Identifiant interne stable |
| `nom_principal` | texte | Nom éditorial retenu |
| `autres_noms` | liste | Appellations historiques ou alternatives |
| `commune` | texte | Commune actuelle |
| `code_insee` | texte | Code INSEE actuel |
| `lieu_dit` | texte | Lieu-dit ou adresse historique |
| `longitude` | nombre | Longitude WGS84 |
| `latitude` | nombre | Latitude WGS84 |
| `precision_geographique` | catégorie | Qualité de la localisation |
| `statut_validation` | catégorie | État du contrôle éditorial |

## Table `activites`

| Champ | Type prévu | Description |
|---|---|---|
| `activite_id` | texte | Identifiant de la phase d'activité |
| `site_id` | texte | Site concerné |
| `secteur` | catégorie | Grande famille industrielle |
| `activite_detaillee` | texte | Forge, filature, papeterie, etc. |
| `type_installation` | texte | Moulin, usine, atelier, mine, etc. |
| `date_debut` | date ou intervalle | Début connu ou estimé |
| `date_fin` | date ou intervalle | Fin connue ou estimée |
| `energie` | liste | Eau, bois, vapeur, électricité, etc. |

## Table `etats_actuels`

| Champ | Type prévu | Description |
|---|---|---|
| `site_id` | texte | Site concerné |
| `conservation` | catégorie | État matériel |
| `usage_actuel` | catégorie | Fonction contemporaine |
| `accessibilite` | catégorie | Conditions d'accès ou de visibilité |
| `date_verification` | date | Date de validité de l'observation |
| `methode_verification` | texte | Observation, source officielle, opérateur, etc. |
| `fiabilite` | catégorie | Niveau de confiance de l'état contemporain |

## Table `sources`

| Champ | Type prévu | Description |
|---|---|---|
| `source_id` | texte | Identifiant de la source |
| `producteur` | texte | Organisme responsable |
| `titre` | texte | Titre du jeu ou document |
| `url` | texte | Adresse précise |
| `date_consultation` | date | Date de récupération |
| `licence` | texte | Licence ou conditions connues |

## Table `mentions_sources`

| Champ | Type prévu | Description |
|---|---|---|
| `mention_id` | texte | Identifiant de la mention |
| `site_id` | texte | Site concerné |
| `source_id` | texte | Source concernée |
| `reference_source` | texte | Identifiant de notice ou cote |
| `information` | texte | Information apportée |
| `nature_information` | catégorie | Sourcée, calculée ou interprétée |
| `fiabilite` | catégorie | Niveau de confiance |

## Tables à préciser après audit

- `protections` ;
- `objets_techniques` ;
- `geometries` ;
- `exploitants` ;
- `relations_sites`, requise pour les transferts, successions et complexes.
