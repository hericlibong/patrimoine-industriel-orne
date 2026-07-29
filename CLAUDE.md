# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Nature du projet

Projet datajournalistique sur le patrimoine industriel de l'Orne. Ce dépôt n'est
pas une application : c'est un **socle de données vérifiable et reproductible**
(phases 0 à 9 terminées), plus une phase 10 de conception éditoriale et
d'interface en cours.

Toute la documentation, les noms de champs, les codes de vocabulaire contrôlé et
les messages de commit sont **en français**. Les identifiants Python restent en
anglais pour les mots-clés techniques mais les noms de domaine sont français
(`sites`, `activites`, `protections`, `communes`…).

## Commandes

Le paquet n'est **pas installé** dans `.venv` : `PYTHONPATH=src` est obligatoire.

```powershell
$env:PYTHONPATH = "src"
python -m pytest                      # suite complète (~65 s, 162 tests)
python -m pytest tests/test_phase8_corpus_complet_v1.py -k indicators   # un test
ruff check src tests tools
```

`tests/README.md` mentionne `unittest discover` : c'est obsolète, tous les tests
sont en style pytest (fonctions + `assert`).

Le `.venv` local ne contient que `duckdb`, `pyproj`, `pyyaml`, `pytest`, `ruff`.
Les tests passent sans `pandas`/`geopandas`/`requests` parce qu'ils relisent
majoritairement les **rapports de validation versionnés** de `reports/quality/`.
Rejouer un module du pipeline (extraction, enrichissement, export) exige
d'installer les dépendances complètes de `pyproject.toml`.

### Pipeline (ordre logique, chaque étape a aussi un script console)

```powershell
$env:PYTHONPATH = "src"
# corpus complet (phase 8)
python -m patrimoine_orne.export.corpus_complet_v1
# socle narratif et visuel (phase 9)
python -m patrimoine_orne.export.editorial_v1
python -m patrimoine_orne.export.medias_v1
python -m patrimoine_orne.export.qualifier_medias_v1
python -m patrimoine_orne.export.revue_editoriale_v1
python -m patrimoine_orne.export.validate_narratif_visuel_v1
```

Les noms des scripts console (`patrimoine-orne-*` dans `pyproject.toml`) donnent
la séquence complète des phases 3 à 9. Le README liste les commandes de
géolocalisation, de contrôle QGIS et de base de test.

QGIS s'exécute avec son propre interpréteur, pas avec `.venv` :

```powershell
& "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat" tools\generate_qgis_project.py
```

### Prototype phase 10

```powershell
python tools/generate_phase10_prototype.py     # régénère prototype/phase10/data/
node tools/generate_phase10_context_map.mjs    # régénère la carte de contexte
python -m http.server 8765 --bind 127.0.0.1    # puis /prototype/phase10/
```

L'ouverture directe de `index.html` ne fonctionne pas (chargements `fetch`).

## Architecture

### `src/patrimoine_orne/` — un paquet par étape du pipeline

`extract/` (récupération brute + archivage) → `transform/` (harmonisation,
canonisation) → `enrich/` → `geocode/` → `classify/` → `validate/` → `export/`
(livrables). `model/` contient le schéma DuckDB (`schema.sql`) et les
validations transversales impossibles à exprimer en `CHECK` SQL
(`validation.py`). `sample/` compose l'échantillon pilote.

Chaque module suit le même patron : constantes `DEFAULT_*` pointant des chemins
relatifs à la racine du dépôt, fonctions pures de construction, une fonction
`produce()`/`build_*()`, puis `main()` avec `argparse` qui **imprime un rapport
JSON et sort en code 1 si `checks_passed` est faux**. Une production qui ne
valide pas ne doit jamais laisser des livrables partiels passer pour valides.

### Trois niveaux de vérité, jamais confondus

- `data/raw/` : réponses d'origine, **jamais modifiées ni écrasées**, nommées
  et horodatées selon `docs/conventions_extraction.md`, avec un
  `.metadata.json` voisin (SHA-256, URL, statut HTTP, version de l'extracteur).
- `data/interim/`, `data/processed/`, `data/exports/` : reproductibles par
  script, **non versionnés** (voir `.gitignore`).
- `data/manual/` : corrections humaines documentées, jamais écrasées par un
  traitement automatique.

Ce qui est versionné et fait autorité : `config/*.yml` (décisions, registres
d'UUID, vocabulaires), `docs/*.md`, `reports/quality/*` (rapports et
indicateurs). Les données produites ne le sont pas.

### `config/` — les décisions, pas de la configuration technique

`phase8_site_ids.yml` conserve les UUID v4 stables des 318 sites ;
`phase8_decisions_canoniques.yml` les arbitrages de rapprochement ;
`classifications.yml` le vocabulaire contrôlé ; `validation_pilote.yml` les 30
contrôles de relecture. Modifier un de ces fichiers change le corpus : c'est une
décision éditoriale, à inscrire dans `docs/journal_decisions.md`.

### `reports/quality/` — les tests portent dessus

Les tests n'exécutent pas seulement du code : ils vérifient que les rapports de
validation versionnés annoncent toujours les mêmes effectifs et décisions
(`checks_passed is True`, `decision == "corpus_complet_v1_valide"`, 319 dossiers
sources, 318 sites, 403 activités…). Un changement de pipeline qui modifie ces
nombres fait échouer les tests **par conception** — il faut alors régénérer le
rapport et justifier l'écart, pas ajuster l'assertion à la légère.

### DuckDB est le format de référence

Le `.duckdb` conserve les entités séparées (sites, activités, états, protections,
objets, géométries, mentions de sources). CSV, Parquet et GeoJSON en sont des
vues **aplaties**, une ligne par site, valeurs multiples concaténées avec `|`.
Les identifiants dérivés sont générés par `uuid5` sur un namespace fixe pour
qu'une reconstruction produise les mêmes relations. Les exports sont validés par
comparaison croisée des identifiants et effectifs entre tous les formats.

## Invariants du domaine à respecter

Ces règles sont la raison d'être du projet ; les ignorer produit du travail
inutilisable. Détail dans `docs/methodologie.md`.

- **319 ≠ 318.** 319 dossiers sources de l'Inventaire, 318 sites canoniques
  (`IA61001399` est une synthèse sans emprise), 403 activités. Une notice n'est
  pas un site : voir les cinq niveaux `notice_source` → `site_publie`.
- **Provenance obligatoire.** Toute valeur est `sourcee`, `calculee` ou
  `interpretee`. Le libellé source est conservé à côté du code normalisé, jamais
  remplacé.
- **La précision géographique est un champ distinct des coordonnées.** Un
  centroïde de commune n'est pas l'emplacement d'un bâtiment ; un point POP reste
  `point_approximatif` tant qu'une emprise ou adresse n'est pas validée. Aucun
  script ne déplace un point ni ne relève une précision automatiquement.
- **Aucune fusion automatique.** Un score de similarité, même élevé, ne crée
  qu'une proposition à vérifier. Les deux UUID sont conservés.
- **Les observations contemporaines sont datées** et ne sont publiées comme
  actuelles que dans leur fenêtre de fraîcheur ; sinon `inconnu` ou
  `a_verifier`. Une destination relevée en 1985 n'est pas la situation 2026.
- **Les contradictions entre sources sont conservées**, jamais écrasées.
- **Une image en ligne n'est pas une autorisation.** Les médias sont
  inventoriés par métadonnées ; aucune image n'est téléchargée ni publiée. Les
  aperçus crédités sont tolérés en prototype **strictement interne**.
- **`autre` ≠ `inconnu` ≠ `NULL`** : valeur hors vocabulaire, question examinée
  sans réponse, champ absent de la source.

## Discipline de traçabilité — non négociable

Le porteur du projet exige que **toute modification, orientation ou décision soit
justifiée, notée, documentée et répercutée** dans le suivi. Le socle a été
construit ainsi jusqu'à la phase 9 ; ce niveau d'exigence ne baisse pas parce que
l'on passe à l'interface. Une décision non écrite est une décision perdue.

À la fin de toute unité de travail, **avant de la déclarer terminée** :

1. **`docs/journal_decisions.md`** (versionné) — ajouter une entrée datée
   `## AAAA-MM-JJ — <objet>`, avec le raisonnement, les constats vérifiés et les
   options écartées, terminée par une ligne `Décision : **…**`. Une réouverture
   d'un bloc déjà validé s'y inscrit obligatoirement, avec son motif.
2. **`docs/roadmap.md`** (non versionné, présent localement) — mettre à jour les
   cases `[ ]` / `[-]` / `[x]`, le statut du bloc et son point de validation. Une
   tâche n'est cochée que si son résultat est vérifiable.
3. **Le document de phase concerné** (`docs/phase10_*.md`) — faire évoluer sa
   version et son statut plutôt que d'empiler un nouveau fichier.
4. **`CLAUDE.md`** — si la règle de travail elle-même change.

Règles d'écriture qui découlent de la méthode du projet :

- Toute affirmation chiffrée indique sa population de référence et sa source de
  calcul ; un résultat non reproductible n'entre pas dans un document.
- Une orientation prise sans preuve est signalée comme hypothèse, pas comme
  constat.
- Un bloc dont le point de validation n'est pas atteint n'est pas clos : le cas
  du bloc 6, clos « avec réserves », est le précédent à ne pas reproduire.
- Les documents antérieurs ne sont pas réécrits pour masquer un changement de
  cap ; la décision qui les rouvre est datée et motivée.

## Comment rendre compte au porteur du projet — non négociable

Le porteur du projet est journaliste, pas ingénieur. Un rapport technique est
un rapport inutile : s'il ne peut pas se représenter concrètement ce qui a été
fait, il ne peut pas décider, et le travail part dans la mauvaise direction
sans que personne s'en aperçoive.

Règles pour tout compte rendu :

- **Parler comme à un humain.** Phrases courtes, mots ordinaires. Pas de
  vocabulaire de métier là où un mot courant existe.
- **Montrer avant de résumer.** Un exemple réel — une phrase de notice, un nom,
  une date — vaut mieux qu'une description abstraite de ce qu'on a fait.
- **Dire à quoi ça sert.** Toute tâche accomplie se termine par ce qu'elle
  change concrètement dans la publication. « Des traits entre les points sur la
  carte », pas « une table de relations peuplée ».
- **Un tableau est bienvenu quand il est expliqué.** Il donne à voir d'un coup
  d'œil ce qu'un paragraphe rendrait pénible. Ce qui ne va pas, c'est le
  tableau posé *à la place* d'une explication : les chiffres accompagnent le
  sens, ils ne le remplacent pas.
- **Ne pas nommer les fichiers et les tables** dans le corps d'une explication.
  Ils vont dans la documentation, pas dans la conversation.
- **Dire ce qui coince**, en langage clair, et ce que ça demande comme décision.

Les méthodes de chaque phase sont expliquées dans `docs/phase10_methodes.md`,
tenu à jour au fur et à mesure et rédigé dans la même langue simple.

## Conventions de travail

- Messages de commit en français, préfixe conventionnel (`feat:`, `fix:`,
  `docs:`, `chore:`).
- `ruff` : ligne à 100 caractères, cible py311.
- Documentation en français avec accentuation complète.

## État actuel — phase 10, bloc 7

Le prototype `prototype/phase10/` (version 0.1) est explicitement **retenu comme
contre-exemple**, pas comme base à enrichir : direction artistique, récit
cartographique, exploration et pages « Les lieux » sont jugés non publiables
(diagnostic détaillé dans `docs/phase10_bloc7_refondation_mvp.md`).

La décision du 27 juillet 2026 est qu'**aucun nouveau code d'interface ne doit
être produit avant les nouveaux arbitrages** du bloc 7. Les données, sources et
règles de preuve restent acquises ; l'interface et le storyboard ne le sont pas.
Toute proposition visuelle doit être évaluée dans un navigateur à taille réelle,
notamment en 1440 px.
