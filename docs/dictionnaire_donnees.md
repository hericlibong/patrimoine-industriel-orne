# Dictionnaire des données — version 1.7

Statut : **socle pilote V1 consolidé le 22 juillet 2026**.

Le schéma exécutable de référence est
`src/patrimoine_orne/model/schema.sql`. Les contrôles qui portent sur plusieurs
tables sont dans `src/patrimoine_orne/model/validation.py`.

## Conventions

- `identifiant` désigne un UUID version 4 généré une seule fois ;
- `code` désigne une valeur issue d'un vocabulaire contrôlé ;
- `date structurée` désigne un ensemble de champs capable de représenter une
  date exacte ou imprécise ;
- les références externes `IA`, `PM`, `PA`, `SSP` et `BNO` ne remplacent jamais
  les identifiants internes ;
- les géométries ne sont pas stockées dans `sites`.

Les vocabulaires de précision géographique et de fiabilité sont définis dans
`config/classifications.yml`. La précision, la méthode de production de la
géométrie et la fiabilité de l'information sont trois champs indépendants.

## Référentiel des classifications V1

Le registre `config/classifications.yml` version 1.3 est la source canonique des
182 codes publiés. Le dictionnaire en fixe ici le sens ; les libellés exhaustifs
des 45 activités détaillées et des 33 installations restent dans le registre.

### Secteurs industriels

| Code | Définition |
|---|---|
| `extraction` | extraction des ressources du sous-sol |
| `metallurgie_travail_metaux` | production, transformation et façonnage des métaux |
| `textile_habillement_cuir` | fibres, filature, tissage, confection et cuir |
| `bois_papier_imprimerie` | transformation du bois, papier, carton et impression |
| `verre_ceramique_materiaux_construction` | verre, brique, tuile, céramique, chaux et ciment |
| `agroalimentaire` | transformation productive des aliments et boissons |
| `energie` | production d'énergie destinée à être distribuée |
| `chimie_caoutchouc_plastiques` | produits chimiques, caoutchouc et plastiques |
| `mecanique_electrique` | machines et matériels mécaniques ou électriques |
| `autres_industries` | activité industrielle connue sans secteur adapté |
| `inconnu` | activité attestée dont le secteur reste indéterminé |

Le secteur qualifie une phase d'activité, jamais directement le site. Les
activités, installations, énergies et rôles énergétiques sont quatre
vocabulaires distincts.

### Corpus intermédiaire de phase 8

`phase8_corpus_80.json` utilise le dossier source comme unité temporaire.
`dossier_id` et `dossier_reference` contiennent la référence `IA`. `site_id`
contient l'identifiant interne lorsqu'il a déjà été attribué ; sa valeur nulle
sur les nouveaux dossiers signifie « pas encore attribué » et non « site sans
identité ».

`origine` distingue `pilote_30` et `phase8_lot1_50`.
`statut_traitement` distingue les pilotes enrichis des dossiers seulement
structurés et classés. `nombre_sites_provisoire` vaut un tant qu'aucune fusion
ou séparation n'est décidée. Cette valeur ne doit pas être additionnée comme
un total définitif du département.

### Périodes historiques

| Code | Bornes |
|---|---|
| `avant_1789` | avant 1789 |
| `revolution_premiere_industrialisation` | 1789–1849 |
| `industrialisation_rail_vapeur` | 1850–1913 |
| `guerres_entre_deux_guerres` | 1914–1945 |
| `modernisation_apres_guerre` | 1946–1975 |
| `mutations_reconversions` | 1976–2000 |
| `periode_contemporaine` | depuis 2001 |

Ces périodes sont des filtres calculés et ne remplacent jamais les dates des
sources. Un intervalle peut relever de plusieurs périodes.

La méthode de calcul accompagne toujours la période :

| Code de méthode | Signification |
|---|---|
| `chronologie_phase` | période calculée depuis les dates documentées d'une phase d'activité |
| `siecles_source_site` | période de repérage calculée depuis `SCLE`, sans preuve automatique de continuité de l'activité |
| `situation_actuelle_documentee` | période contemporaine ajoutée au site lorsqu'une observation récente est sourcée |

### Situation actuelle

Conservation :

| Code | Définition |
|---|---|
| `conserve` | ensemble industriel structurant encore présent et lisible |
| `degrade` | ensemble subsistant mais matériellement dégradé |
| `partiellement_conserve` | seule une partie des éléments documentés subsiste |
| `vestiges` | traces matérielles limitées sans ensemble complet |
| `ruine` | structures subsistant principalement à l'état de ruine |
| `disparu` | aucun élément industriel identifié ne subsiste à l'emplacement vérifié |
| `inconnu` | aucune observation récente ne permet de conclure |

Usages actuels : `activite_industrielle`, `artisanat_production`,
`culture_musee`, `tourisme_visite`, `logement`, `commerce_services`, `bureaux`,
`agriculture`, `stockage`, `equipement_public`, `vacant`, `sans_usage`, `autre`
et `inconnu`. Plusieurs usages peuvent coexister dans une même observation.

Accessibilité : `visitable`, `partiellement_visitable`,
`visible_espace_public`, `prive_visible`, `prive_non_visible`, `inaccessible` et
`inconnu`. La visibilité ne constitue jamais une autorisation d'entrée.

Protections : `classe_mh`, `inscrit_mh`, `protection_locale` et
`autre_protection`. La portée est séparée : `totale`, `partielle` ou `inconnue`.
Une mesure possède également un statut : `active`, `modifiee`, `abrogee` ou
`a_verifier`.

### Localisation et qualité

Précision géographique : `emprise_site_verifiee`, `parcelle_verifiee`,
`batiment_verifie`, `point_site_verifie`, `point_adresse`,
`point_approximatif` et `zone_documentaire`.

Fiabilité :

| Code | Définition |
|---|---|
| `forte` | preuve directe, cible non ambiguë et aucune contradiction ouverte |
| `moyenne` | information indirecte concordante ou interprétation simple contrôlée |
| `faible` | indice unique, ambiguïté, hypothèse ou contradiction ouverte |

`autre` désigne une valeur connue absente du vocabulaire. `inconnu` signifie
qu'une question applicable a été examinée sans réponse. Aucun de ces codes ne
remplace un champ source vide, une valeur non applicable ou un statut
`a_verifier`.

## Correspondance avec DuckDB

| Type du dictionnaire | Type DuckDB | Règle d'implémentation |
|---|---|---|
| identifiant interne | `UUID` | valeur v4 créée une seule fois ; `uuid()` par défaut |
| code ou texte | `VARCHAR` | chaîne vide interdite dans les champs identifiants |
| date | `DATE` | dates historiques imprécises stockées par intervalle |
| horodatage | `TIMESTAMPTZ` | date et fuseau conservés |
| booléen | `BOOLEAN` | `true`, `false` ou `NULL` si la règle l'autorise |
| valeur de provenance | `JSON` | valeur originale ou normalisée structurée |
| géométrie | `GEOMETRY` | extension DuckDB Spatial obligatoire, travail en EPSG:2154 |

Les clés étrangères, unicités et contrôles simples sont appliqués directement
par DuckDB. Le validateur transversal contrôle notamment les cibles génériques,
les champs ciblés, les obligations conditionnelles des sites, la géométrie de
référence et la cohérence des versions. Tous les vocabulaires V1 sont définis
dans `config/classifications.yml` et validés à la clôture de la phase 4.

Une `date structurée` est matérialisée par quatre champs : `<nom>_min`,
`<nom>_max`, `<nom>_precision_code` et `<nom>_texte_source`. Les entités métier
possèdent aussi les champs techniques communs `statut_enregistrement_code`,
`cree_le`, `cree_par` et `modifie_le`.

## Table `sites`

Une ligne représente une emprise industrielle distincte.

| Champ | Type conceptuel | Description |
|---|---|---|
| `site_id` | identifiant | Identifiant interne stable du site |
| `site_id_canonique` | identifiant nullable | Site conservé lorsqu'un doublon interne est fusionné |
| `nom_principal` | texte | Nom éditorial actuellement retenu |
| `niveau_structurel_code` | code | Site principal ou composant autonome |
| `commune_actuelle_code_insee` | texte | Code INSEE de la commune actuelle |
| `commune_actuelle_nom` | texte | Nom de la commune actuelle |
| `commune_historique_nom` | texte | Commune citée historiquement lorsqu'elle diffère |
| `lieu_dit_principal` | texte | Lieu-dit éditorial retenu |
| `statut_corpus_code` | code | Candidat, rapproché, cartographiable, publié ou exclu |
| `decision_inclusion_code` | code | Inclus, exclu ou à vérifier |
| `motif_decision` | texte | Justification éditoriale de l'inclusion ou exclusion |
| `fiabilite_code` | code | Niveau de confiance global du rapprochement |
| `notes_internes` | texte | Notes non destinées directement à la publication |
| `cree_le` | horodatage | Création de la ligne dans le projet |
| `modifie_le` | horodatage | Dernière modification de la ligne |

Les autres appellations sont stockées dans `noms_sites`. Les coordonnées et
emprises sont stockées dans `geometries`.

## Table `noms_sites`

| Champ | Type conceptuel | Description |
|---|---|---|
| `nom_site_id` | identifiant | Identifiant de l'appellation |
| `site_id` | identifiant | Site concerné |
| `nom` | texte | Appellation originale ou normalisée |
| `type_nom_code` | code | Principal, historique, entreprise, lieu-dit ou autre |
| `debut` | date structurée | Début d'usage connu |
| `fin` | date structurée | Fin d'usage connue |
| `fiabilite_code` | code | Niveau de confiance |

## Table `activites`

Une ligne représente une phase d'activité sur un site.

| Champ | Type conceptuel | Description |
|---|---|---|
| `activite_id` | identifiant | Identifiant interne de la phase d'activité |
| `site_id` | identifiant | Site concerné |
| `secteur_code` | code | Grande famille industrielle |
| `activite_code` | code | Activité détaillée normalisée |
| `activite_libelle_source` | texte | Libellé conservé depuis la source |
| `type_installation_code` | code | Moulin, usine, atelier, mine, centrale, etc. |
| `debut` | date structurée | Début exact ou estimé de la phase |
| `fin` | date structurée | Fin exacte ou estimée de la phase |
| `principale` | booléen | Activité principale pour la période concernée |
| `fiabilite_code` | code | Niveau de confiance |
| `notes` | texte | Précisions et réserves |

`secteur_code` est déduit de `activite_code`. Il ne décrit jamais directement
le site entier. Les définitions et les cas multi-secteurs sont documentés dans
`docs/classifications_secteurs.md`.

Dans le corpus consolidé et les exports, chaque phase possède également
`periodes_codes`, `periodes_libelles`, `periode_methode_code` et
`siecles_source_site`. Ces champs sont dérivés : les dates et textes sources
restent l'information de référence.

## Tables dérivées d'export V1

`sites_export_v1` contient une ligne par site. Les champs temporels ajoutés
sont :

| Champ | Description |
|---|---|
| `siecles_source` | valeurs originales du champ POP `SCLE` |
| `periodes_activite_codes` | périodes calculées depuis les chronologies des activités |
| `periodes_source_codes` | périodes de repérage calculées depuis `SCLE` |
| `periodes_situation_actuelle_codes` | période contemporaine attestée par une observation récente |
| `periodes_codes` | union des deux listes pour le filtrage des sites |
| `periodes_libelles` | libellés lisibles correspondant aux codes |
| `periode_methode_codes` | méthodes utilisées pour produire les périodes |
| `premiere_annee_documentee` | borne la plus ancienne repérée, sans valeur de date exacte |
| `derniere_annee_documentee` | borne la plus récente repérée, sans preuve de continuité |

`activites_export_v1` contient une ligne par phase d'activité et conserve ses
dates structurées, ses périodes et leur méthode. `activites_periodes_v1`
déplie cette information en une ligne par couple activité-période pour les
analyses et datavisualisations.

## Table `energies_activites`

| Champ | Type conceptuel | Description |
|---|---|---|
| `energie_activite_id` | identifiant | Identifiant interne du lien entre activité et énergie |
| `activite_id` | identifiant | Phase d'activité concernée |
| `energie_code` | code | Eau, bois, charbon, vapeur, électricité, etc. |
| `role_energie_code` | code | Produite sur place, force motrice, combustible ou autre |
| `debut` | date structurée | Début documenté de l'usage de cette énergie |
| `fin` | date structurée | Fin documentée de l'usage de cette énergie |
| `fiabilite_code` | code | Niveau de confiance |

`energie_code` décrit la force ou le combustible. `role_energie_code` indique
son rôle ou sa provenance, par exemple force motrice, produite sur place ou
achetée. Un équipement comme une roue hydraulique n'est pas une énergie.

## Table `etats_actuels`

Une ligne représente une observation contemporaine datée, conservée dans
l'historique.

| Champ | Type conceptuel | Description |
|---|---|---|
| `etat_actuel_id` | identifiant | Identifiant de l'observation |
| `site_id` | identifiant | Site observé |
| `conservation_code` | code | Conservé, dégradé, partiellement conservé, vestiges, ruine, disparu ou inconnu |
| `accessibilite_code` | code | Visitable, visible depuis l'espace public, privé, inaccessible ou inconnu |
| `date_verification` | date | Date de l'observation ou de la consultation |
| `conservation_valide_jusqu_au` | date calculée dans la vue | Échéance de fraîcheur de la conservation |
| `usage_valide_jusqu_au` | date calculée dans la vue | Échéance de fraîcheur de l'usage actuel |
| `accessibilite_valide_jusqu_au` | date calculée dans la vue | Échéance de fraîcheur de l'accessibilité |
| `methode_verification_code` | code | Terrain, source officielle, exploitant, image, etc. |
| `fiabilite_code` | code | Niveau de confiance de l'observation |
| `version_numero` | entier | Numéro croissant des observations du site |
| `remplace_etat_actuel_id` | identifiant nullable | Observation précédente corrigée ou remplacée |
| `motif_version_code` | code | Nouvelle observation, correction ou annulation |
| `enregistre_le` | horodatage | Date d'insertion dans le projet |
| `notes` | texte | Limites de l'observation |

## Table `usages_actuels`

Une observation peut décrire plusieurs usages simultanés. Une ligne représente
un usage précis, jamais une catégorie générique « mixte ».

| Champ | Type conceptuel | Description |
|---|---|---|
| `usage_actuel_id` | identifiant | Identifiant interne de l'usage observé |
| `etat_actuel_id` | identifiant | Observation contemporaine datée |
| `usage_code` | code | Industrie, culture, tourisme, logement, stockage, etc. |
| `principal` | booléen | Usage principal de l'observation ; un seul au maximum |
| `partie_site` | texte | Partie du site concernée, si elle est connue |
| `notes` | texte | Précisions et limites |

## Table `sources`

Une ligne représente un fonds, un jeu de données ou une source éditoriale, pas
une notice individuelle.

| Champ | Type conceptuel | Description |
|---|---|---|
| `source_id` | code stable | Identifiant lisible défini dans le registre des sources |
| `titre` | texte | Nom du fonds ou jeu de données |
| `producteur` | texte | Organisme ou auteur responsable |
| `role_code` | code | Principal, enrichissement, élargissement, contexte ou vérification |
| `url_reference` | texte | Page générale de la source |
| `methode_acces_code` | code | API, WFS, HTML, archive, consultation manuelle, etc. |
| `licence_donnees` | texte | Licence ou conditions des données |
| `droits_medias` | texte | Règles distinctes pour les images et médias |
| `statut_audit_code` | code | État de validation de la source |
| `date_dernier_audit` | date | Dernière vérification de la source |
| `notes` | texte | Réserves permanentes ou techniques |

## Table `identifiants_externes`

Cette table permet de retrouver une entité à partir d'une référence de source
sans faire dépendre son UUID interne de cette référence.

| Champ | Type conceptuel | Description |
|---|---|---|
| `identifiant_externe_id` | identifiant | Identifiant interne de la correspondance |
| `source_id` | identifiant | Source responsable de la référence |
| `type_identifiant_code` | code | IA, PM, PA, SSP, BNO, ARK, SIREN, OSM, etc. |
| `valeur` | texte | Valeur originale de l'identifiant externe |
| `entite_type_code` | code | Type d'entité interne ciblée |
| `entite_id` | identifiant | UUID de l'entité interne |
| `principal_pour_source` | booléen | Référence principale dans cette source |
| `date_verification` | date | Dernier contrôle de la correspondance |
| `fiabilite_code` | code | Niveau de confiance du rattachement |

La combinaison `source_id`, `type_identifiant_code` et `valeur` est unique.

## Table `mentions_sources`

Une ligne représente une information apportée par une source à une entité ou à
un champ précis.

| Champ | Type conceptuel | Description |
|---|---|---|
| `mention_id` | identifiant | Identifiant interne de la preuve |
| `source_id` | identifiant | Source du catalogue |
| `reference_source` | texte | Référence `IA`, `PM`, `PA`, `SSP`, `BNO`, cote, ARK, etc. |
| `url_precise` | texte | URL de la notice ou du document consulté |
| `date_consultation` | date ou horodatage | Date de récupération ou de consultation |
| `localisateur` | texte | Page, image, folio, ligne ou champ source |
| `entite_type_code` | code | Table métier ciblée |
| `entite_id` | identifiant | Ligne métier ciblée |
| `champ_cible` | texte | Champ précis soutenu, si applicable |
| `valeur_originale` | texte ou JSON | Valeur conservée avant normalisation |
| `valeur_normalisee` | texte ou JSON | Valeur transformée utilisée par le projet |
| `statut_valeur_code` | code | Renseignée, inconnue, absente de la source, non applicable, contradictoire ou à vérifier |
| `nature_information_code` | code | Sourcée, calculée ou interprétée |
| `fiabilite_code` | code | Niveau de confiance attribué |
| `extracteur` | texte | Script ou méthode de production |
| `version_extracteur` | texte | Version du traitement automatique |
| `notes` | texte | Réserves, contradictions ou justification |

## Table `protections`

Une ligne représente une protection portant soit sur un site, soit sur un objet
technique.

| Champ | Type conceptuel | Description |
|---|---|---|
| `protection_id` | identifiant | Identifiant interne de la protection |
| `site_id` | identifiant nullable | Site protégé, si la cible est immobilière |
| `objet_technique_id` | identifiant nullable | Objet protégé, si la cible est mobilière |
| `type_protection_code` | code | Classé MH, inscrit MH, protection locale ou autre |
| `reference_protection` | texte | Référence externe `PA`, `PM` ou autre |
| `date_protection` | date structurée | Date de la décision de protection |
| `element_protege` | texte | Partie ou objet réellement concerné |
| `portee_code` | code | Protection totale, partielle ou de portée inconnue |
| `statut_actuel_code` | code | Active, modifiée, abrogée ou à vérifier |
| `date_verification` | date | Dernier contrôle dans la source officielle |

Une seule des colonnes `site_id` et `objet_technique_id` doit être renseignée.
Une même référence `PA` ou `PM` peut porter plusieurs mesures : chaque mesure
garde son propre `protection_id`.

## Table `objets_techniques`

| Champ | Type conceptuel | Description |
|---|---|---|
| `objet_technique_id` | identifiant | Identifiant interne de l'objet |
| `nom_principal` | texte | Titre éditorial retenu |
| `denomination_code` | code | Machine, outil, collection, moteur, turbine, etc. |
| `description` | texte | Description matérielle |
| `fabricant` | texte | Fabricant documenté |
| `date_creation` | date structurée | Date ou période de création |
| `reference_palissy` | texte | Référence `PM` lorsqu'elle existe |
| `etat_conservation_code` | code | État matériel connu de l'objet |
| `date_verification` | date | Dernière observation contemporaine |
| `fiabilite_code` | code | Niveau de confiance |
| `notes` | texte | Réserves et informations complémentaires |

## Table `liens_objets_sites`

| Champ | Type conceptuel | Description |
|---|---|---|
| `lien_objet_site_id` | identifiant | Identifiant du lien |
| `objet_technique_id` | identifiant | Objet concerné |
| `site_id` | identifiant | Site concerné |
| `type_lien_code` | code | Origine, fabrication, usage, emplacement historique ou actuel |
| `debut` | date structurée | Début du lien, si connu |
| `fin` | date structurée | Fin du lien, si connue |
| `fiabilite_code` | code | Niveau de confiance |
| `notes` | texte | Justification du rattachement |

## Table `geometries`

| Champ | Type conceptuel | Description |
|---|---|---|
| `geometrie_id` | identifiant | Identifiant interne de la géométrie |
| `site_id` | identifiant | Site localisé |
| `geom` | géométrie EPSG:2154 | Point, ligne ou polygone normalisé en Lambert-93 |
| `type_geometrie_code` | code | Point, bâtiment, parcelle, emprise ou zone documentaire |
| `precision_geographique_code` | code | Emprise, parcelle, bâtiment, point vérifié, adresse, point approximatif ou zone documentaire |
| `methode_localisation_code` | code | Source directe, géocodage, cadastre, relevé, interprétation, etc. |
| `crs_source` | texte | Système de coordonnées de la donnée d'origine |
| `geometrie_reference` | booléen | Géométrie retenue pour un usage donné |
| `usage_code` | code | Affichage, analyse, emprise historique ou autre |
| `date_geometrie` | date structurée | Période représentée par la géométrie |
| `date_verification` | date | Dernier contrôle spatial |
| `fiabilite_code` | code | Niveau de confiance |
| `notes` | texte | Réserves et méthode détaillée |

Les exports web seront transformés en `EPSG:4326`. Un site peut exister sans
ligne dans cette table.

`commune_seule` et `non_localise` ne sont pas des valeurs de
`precision_geographique_code` : dans ces deux cas, aucune géométrie de site
n'est créée.

## Table `exploitants`

| Champ | Type conceptuel | Description |
|---|---|---|
| `exploitant_id` | identifiant | Identifiant interne de la personne ou organisation |
| `nom_principal` | texte | Raison sociale ou nom retenu |
| `type_exploitant_code` | code | Personne, entreprise, administration, association, inconnu |
| `identifiant_externe` | texte | SIREN ou autre identifiant lorsqu'il existe |
| `notes` | texte | Contexte historique et réserves |

## Table `noms_exploitants`

| Champ | Type conceptuel | Description |
|---|---|---|
| `nom_exploitant_id` | identifiant | Identifiant de l'appellation |
| `exploitant_id` | identifiant | Exploitant concerné |
| `nom` | texte | Raison sociale ou variante historique |
| `debut` | date structurée | Début d'usage connu |
| `fin` | date structurée | Fin d'usage connue |
| `fiabilite_code` | code | Niveau de confiance |

## Table `exploitations`

| Champ | Type conceptuel | Description |
|---|---|---|
| `exploitation_id` | identifiant | Identifiant interne de la relation |
| `site_id` | identifiant | Site concerné |
| `exploitant_id` | identifiant | Personne ou organisation concernée |
| `activite_id` | identifiant nullable | Phase d'activité concernée, si identifiable |
| `role_code` | code | Exploitant principal, coexploitant, concessionnaire ou gestionnaire |
| `debut` | date structurée | Début de la relation |
| `fin` | date structurée | Fin de la relation |
| `fiabilite_code` | code | Niveau de confiance |
| `notes` | texte | Réserves et justification |

## Table `relations_sites`

| Champ | Type conceptuel | Description |
|---|---|---|
| `relation_site_id` | identifiant | Identifiant interne de la relation |
| `site_source_id` | identifiant | Site d'origine de la relation orientée |
| `site_cible_id` | identifiant | Site de destination de la relation orientée |
| `type_relation_code` | code | Composant, transfert, succession, dépendance ou partage |
| `debut` | date structurée | Début de validité de la relation |
| `fin` | date structurée | Fin de validité de la relation |
| `statut_validation_code` | code | Confirmée, probable, hypothèse ou à vérifier |
| `fiabilite_code` | code | Niveau de confiance |
| `notes` | texte | Description et justification |

Un site ne peut pas être relié à lui-même. Les relations incertaines ne
fusionnent jamais automatiquement les sites.

## Table `propositions_rapprochement`

Une ligne représente une hypothèse de doublon entre deux sites candidats. Elle
ne fusionne jamais les sites automatiquement.

| Champ | Type conceptuel | Description |
|---|---|---|
| `proposition_rapprochement_id` | identifiant | Identifiant interne de la proposition |
| `site_a_id` | identifiant | Premier site candidat, UUID le plus petit |
| `site_b_id` | identifiant | Second site candidat, UUID le plus grand |
| `methode_code` | code | Méthode ayant produit la proposition |
| `score_similarite` | décimal nullable | Indice technique compris entre 0 et 1, jamais décision automatique |
| `criteres` | JSON | Nom, commune, adresse, distance et autres indices comparés |
| `statut_decision_code` | code | À vérifier, confirmé même site ou rejeté sites distincts |
| `site_canonique_id` | identifiant nullable | Site conservé uniquement après confirmation |
| `date_decision` | date nullable | Date de la décision humaine |
| `fiabilite_code` | code | Niveau de confiance de la proposition ou décision |
| `notes` | texte | Justification et réserves |

Une proposition ouverte conserve deux sites distincts. Une confirmation désigne
l'un des deux comme canonique ; un rejet conserve définitivement les deux sites.
