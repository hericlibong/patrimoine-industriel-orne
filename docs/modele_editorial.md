# Modèle éditorial — textes historiques et médias

Version : 1.3  
Statut : **matière historique, métadonnées médias et droits qualifiés — phase 9, bloc 4**  
Date : 24 juillet 2026

La configuration opérationnelle correspondante est
`config/editorial.yml`. Ce modèle prépare les données nécessaires à la
narration sans produire encore le récit journalistique ni sélectionner
définitivement les images.

## Trois niveaux de texte

### 1. Texte historique source

`historique_source` et `description_source` reproduisent les informations
présentes dans la notice patrimoniale. Ils sont conservés tels quels, avec leur
référence et leur URL.

Ils ne sont jamais corrigés, résumés ou remplacés dans leur propre champ. Une
faute ou une formulation ancienne peut être signalée dans une note séparée,
mais le texte source reste intact.

### 2. Résumé documentaire

Le `resume_documentaire` est une synthèse factuelle des sources. Il sert à
préparer une fiche, une chronologie ou un repérage éditorial. Ce n'est pas
encore un texte de publication.

Chaque résumé conserve ses références, son auteur ou son mode de production,
son statut de relecture et sa date de validation éventuelle. Un résumé
automatique ou assisté commence obligatoirement au statut `brouillon`.

### 3. Note ou texte journalistique

La `note_journalistique` contient un angle, une hypothèse de récit ou un texte
rédigé. Elle est distincte du résumé documentaire parce qu'elle peut mobiliser
une sélection, une écriture et des sources complémentaires : entretiens,
terrain, archives ou photographie contemporaine.

Elle conserve son auteur et son statut éditorial. Elle ne remplace jamais les
deux niveaux précédents.

## Table `recits_sites`

La table possède une ligne par `site_id`. Elle constitue le dossier éditorial
du site, pas nécessairement la future page publique.

| Groupe | Champs principaux | Rôle |
|---|---|---|
| Identité | `site_id`, `reference_ia`, `titre_source` | Relier le récit au corpus |
| Sources immuables | historique, description, hashes, statuts | Conserver les textes patrimoniaux |
| Repères | siècles, périodes documentaires, périodes d'activité et activités successives | Préparer chronologie et filtres |
| Provenance | source principale et liste complète des références | Identifier l'origine |
| Synthèse | résumé, statut, auteur, sources et validation | Préparer une synthèse factuelle |
| Journalisme | note, statut et auteur | Préparer l'angle ou la rédaction |
| Sélection | statut, besoin de recherche et notes | Organiser la revue éditoriale |

Les textes absents utilisent les statuts `absent_source`, `illisible` ou
`a_verifier`. Un champ vide n'est jamais remplacé artificiellement par un
résumé.

## Table `medias`

La table possède une ligne par relation entre un média et un site :

- `media_id` identifie le média source ;
- `media_site_id` identifie son rattachement au site.

| Groupe | Champs principaux | Rôle |
|---|---|---|
| Relation | média, site et référence `IA` | Relier l'image au corpus |
| Source | source, référence, URL de la notice média, chemin brut et notice IA | Retrouver l'original |
| Description | type, légende et marqueur principal | Comprendre le contenu |
| Crédit | auteur, crédit et mention de droits | Conserver les mentions |
| Éditorial | `selection_media_code` | Principal, secondaire, interne ou écarté |
| Droits | droits, autorisation, usage, licence et preuve | Décider d'un usage |
| Métadonnées brutes | `metadonnees_source` | Conserver les informations fournies sans perte |
| Fichier local | chemin, hash et date | Gérer un fichier sans le versionner |

Une même référence source n'est enregistrée qu'une fois comme média. Si elle
concerne plusieurs sites, plusieurs relations sont conservées sans dupliquer
l'identité du média.

L'inventaire V1 ne télécharge aucun fichier. `url_media` mène à la notice POP
du média ; `url_fichier_source` conserve le chemin ou l'URL du fichier affiché
par POP lorsqu'il est présent. Les métadonnées venant d'archives HTML sont
marquées comme telles et ne reçoivent pas de légende, auteur ou crédit inventé.

## Statuts éditoriaux

Pour les textes : `non_evalue`, `a_examiner`, `retenu`, `secondaire`,
`recherche_complementaire` ou `ecarte`.

Pour les médias : `non_evalue`, `candidat_principal`,
`candidat_secondaire`, `retenu_interne`, `retenu_publication` ou `ecarte`.

`retenu_publication` ne suffit pas à autoriser la diffusion. Le statut de droits
doit également le permettre.

## Droits et autorisations

Trois dimensions restent séparées :

1. la situation juridique connue : inconnue, protégée, licence identifiée ou
   domaine public ;
2. l'état de la demande : non demandée, à demander, envoyée, accordée, refusée
   ou expirée ;
3. l'usage autorisé : métadonnées seulement, référence interne, prototype privé,
   publication autorisée ou interdite.

La publication exige `publication_autorisee` et une preuve conservée :
autorisation, autorisation conditionnelle ou justification que l'autorisation
n'est pas requise.

La qualification V1 est volontairement prudente : les 1 783 médias avec un
crédit source sont `protege` et utilisables en aperçu distant crédité dans le
prototype privé ; les 117 sans crédit exploitable sont `inconnus` et restent à
la référence interne. Aucun des 1 900 médias n'est automatiquement publiable.
Le registre `demandes_autorisation_medias` suit les 1 888 médias distincts, sans
envoyer de demande à ce stade.

## Revue éditoriale

La table `revue_editoriale_sites` ne rédige ni ne hiérarchise le récit. Elle
réunit, pour chacun des 318 sites, la couverture historique, les repères de
chronologie, la couverture iconographique et les recherches encore nécessaires.

Un `media_principal_candidat_reference` désigne seulement une image à regarder
en premier : son statut est `a_revoir`, sa sélection éditoriale n'est pas
validée et son droit de publication n'est pas modifié.

## Prototype interne

Le prototype interne peut utiliser les données, les textes sources avec leur
provenance, les résumés marqués comme brouillons, les métadonnées des médias et
des aperçus crédités dans un espace strictement privé.

Il ne permet pas par défaut une diffusion publique, un partage externe, la
publication intégrale des textes sources, le téléchargement massif des
originaux, la suppression d'un crédit ou le versionnement des fichiers images.

## Garantie de non-écrasement

Les champs sources sont reconstruits depuis `corpus_complet_v1`, ne sont pas
éditables manuellement et conservent leur empreinte SHA-256.

La production doit échouer si un texte source présent dans le corpus disparaît
du livrable éditorial. Les résumés et notes restent toujours dans des champs
distincts, avec leurs sources, auteurs et statuts.
