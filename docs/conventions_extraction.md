# Conventions d'extraction

Version : 1.0 — 20 juillet 2026

## Organisation des fichiers bruts

Chaque récupération est conservée dans un dossier propre à la source et à la
date de récupération :

```text
data/raw/<source_id>/<AAAA>/<AAAA-MM-JJ>/
```

Nom d'un fichier brut :

```text
<source_id>__<resource_id>__<scope>__<AAAAMMJJThhmmssZ>.<format>
```

Exemple :

```text
data/raw/monuments_historiques_data_culture/2026/2026-07-20/
monuments_historiques_data_culture__immeubles_proteges__orne__20260720T093012Z.json
```

Règles :

- `source_id` reprend l'identifiant défini dans `config/sources.yml` ;
- `resource_id` désigne le jeu, la couche, la notice ou l'export ;
- `scope` indique le périmètre extrait, par exemple `orne`, `france` ou une
  commune ;
- l'heure est enregistrée en UTC et se termine par `Z` ;
- les éléments du nom sont en minuscules, sans accent ni espace ;
- les extensions composées comme `.csv.gz` sont autorisées ;
- un fichier brut existant n'est jamais remplacé.

Une nouvelle récupération d'une même ressource produit donc un nouveau fichier
horodaté.

## Métadonnées de récupération

Chaque fichier brut possède un fichier JSON voisin :

```text
<nom-du-fichier-brut>.metadata.json
```

Champs obligatoires :

| Champ | Signification |
|---|---|
| `schema_version` | Version du format de métadonnées |
| `source_id` | Source déclarée dans `sources.yml` |
| `resource_id` | Ressource ou export récupéré |
| `scope` | Périmètre demandé |
| `retrieved_at` | Date et heure UTC de récupération |
| `source_page_url` | Page officielle décrivant la source |
| `request_url` | URL effectivement appelée |
| `final_url` | URL finale après redirections |
| `http_status` | Code de réponse HTTP |
| `content_type` | Type de contenu annoncé par le serveur |
| `format` | Format logique du fichier |
| `license` | Licence connue au moment de la récupération |
| `file_name` | Nom du fichier brut voisin |
| `file_size_bytes` | Taille exacte du fichier |
| `sha256` | Empreinte du contenu brut |
| `extractor` | Module ou commande responsable |
| `extractor_version` | Version du module d'extraction |
| `git_commit` | Commit du code utilisé, si disponible |
| `query` | Paramètres, filtre ou requête appliquée |
| `notes` | Réserves techniques constatées |

Le hash, la taille et le nom permettent de vérifier que le fichier brut n'a pas
été modifié après sa récupération.

## Séparation des responsabilités

- `extract/naming.py` construit les noms et chemins reproductibles ;
- `extract/metadata.py` produit et vérifie les métadonnées ;
- les modules propres à chaque source seront ajoutés lors des extractions tests ;
- aucun nettoyage métier n'est effectué dans `data/raw/`.

## Échec d'une extraction

Une réponse incomplète ou invalide ne remplace jamais un fichier existant. Le
module de source devra supprimer son éventuel fichier temporaire, conserver le
message d'erreur dans les journaux techniques et retourner un état d'échec.
