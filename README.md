# Patrimoine industriel de l'Orne

Projet datajournalistique consacré à **318 sites industriels documentés dans
l'Orne**. Le corpus validé alimente une application web de visualisation
interactive : une carte, des filtres, une recherche et des vues d'ensembles et
de sites que le lecteur explore librement.

La publication s'intitule **« Le patrimoine oublié de l'Orne »**, sous-titrée
*Voyage dans l'Orne industrielle*. Le sujet est le **patrimoine** : l'histoire
industrielle en est le moyen, pas l'objet. Le mot engage une limite qui reste
affichée partout — l'état de conservation est inconnu pour 315 des 318 sites, si
bien que la publication établit un patrimoine **documenté**, non un état des
lieux physique.

## État du projet

**Phases 0 à 9 terminées. Phase 10.D en cours : la vue de référence est
construite et corrigée, son jugement n'est pas rendu.**

Les 319 références officielles récupérées correspondent à **318 sites
canoniques** et **403 activités structurées**. Les sites sont cartographiables
avec un niveau de précision explicite et disposent d'identifiants stables. Le
corpus complet est disponible en JSON, DuckDB, CSV, Parquet et GeoJSON.

La matière éditoriale comprend notamment 314 textes historiques, 2 360
événements datés sur 314 sites, les relations sourcées entre sites et
l'inventaire de 1 888 médias distincts avec leurs statuts de droits. Une
information inconnue n'est jamais complétée par déduction.

Les **douze ensembles industriels** déjà lus forment le cœur éditorial et
rassemblent 172 sites. Les 146 autres sites restent tous visibles et
consultables. Parmi eux, 74 pourront faire l'objet de lectures complémentaires
ultérieures au sein de 18 petits ensembles. Le mot « ensemble » a remplacé
« système » le 14 août 2026 partout où le lecteur le lit ; le registre
`config/phase10_systemes.yml` et les identifiants techniques gardent leur nom.

Un lien entre deux sites n'existe que si une phrase de source l'établit. La
proximité géographique ne prouve rien et ne crée aucun lien : un regroupement
est un calcul, jamais un contour historique.

L'application ne s'ouvre plus sur la carte nue. Le jugement du 13 août 2026 a
montré qu'on ne comprenait pas ce qu'on regardait en arrivant : un titre, un
texte d'arrivée et un mode d'emploi sont désormais posés sur la page elle-même,
sans écran bloquant ni séquence obligatoire. Le refus du parcours imposé reste
entier. Les décisions d'architecture sont arrêtées ; la direction artistique
interviendra après validation de la vue sur contenu réel.

Le suivi détaillé est maintenu localement dans `docs/roadmap.md`, qui n'est pas
versionné.

**Images et droits.** Aucune image n'est téléchargée ni publiée : les médias sont
inventoriés par métadonnées. Les photographies de tiers servant à la conception
interne ne sont pas versionnées — le dépôt étant public, les y placer vaudrait
publication. Six maquettes de la phase 10 s'affichent donc avec un vide à
l'emplacement de leur photographie ; c'est voulu, et documenté dans
`docs/design/phase10/README.md`.

## Documents de référence

- [Cadrage de référence de l'application](docs/phase10_cadrage_v2_application.md)
- [Architecture validée de l'application](docs/phase10_architecture.md)
- [Ce que les douze ensembles permettent d'établir](docs/phase10_demonstration.md)
- [Jugement de la vue de référence](docs/phase10_jugement_vue_reference.md)
- [Méthodes de la phase 10, en langue simple](docs/phase10_methodes.md)
- [Recommandation actualisée pour l'application](docs/recommandation_application.md)
- [Cadrage](docs/cadrage.md)
- [Pistes éditoriales et datavisualisation](docs/pistes_editoriales.md)
- [Méthodologie](docs/methodologie.md)
- [Conventions d'extraction](docs/conventions_extraction.md)
- [Dictionnaire des données](docs/dictionnaire_donnees.md)
- [Modèle éditorial des textes et médias](docs/modele_editorial.md)
- [Registre consolidé des sources](docs/registre_sources.md)
- [Revue de presse et ressources éditoriales externes](docs/revue_de_presse.md)
- [Limites éditoriales](docs/limites_editoriales.md)
- [Licences des données et droits des images](docs/licences_droits_images.md)
- [Estimation de charge du corpus complet](docs/estimation_charge_corpus_complet.md)
- [Constitution du corpus en phase 8](docs/phase8_constitution_corpus.md)
- [Récits soutenus par les données](docs/recits_soutenus_donnees.md)
- [Modèle des entités principales](docs/modele_donnees.md)
- [Règles du modèle](docs/regles_modele.md)
- [Journal des décisions](docs/journal_decisions.md)
- [Sources à auditer](config/sources.yml)
- [Classifications contrôlées](config/classifications.yml)
- [Règles des secteurs et installations](docs/classifications_secteurs.md)
- [Chronologie et situation actuelle](docs/classifications_chronologie_situation.md)
- [Qualité des classifications](docs/classifications_qualite.md)
- [Règles de précision géographique](docs/regles_precision_geographique.md)
- [Périmètre opérationnel](config/perimetre.yml)
- [Méthodes d'extraction validées](config/extraction.yml)
- [Règles structurelles du modèle](config/regles_modele.yml)
- [Règles éditoriales des textes et médias](config/editorial.yml)
- [Validation du modèle V1](reports/quality/phase3_validation_modele.md)
- [Test des secteurs sur l'échantillon](reports/quality/phase4_test_secteurs.md)
- [Test de la chronologie et de la situation actuelle](reports/quality/phase4_chronologie_situation.md)
- [Test de qualité et de reproductibilité](reports/quality/phase4_qualite_classifications.md)
- [Validation finale de la phase 4](reports/quality/phase4_validation_finale.md)
- [Validation finale du corpus pilote](reports/quality/phase5_validation_finale.md)
- [Contrôle des localisations du pilote](reports/quality/phase6_localisation.md)
- [Test du contexte territorial](reports/quality/phase6_contexte_territorial.md)
- [Contrôle cartographique du pilote](reports/quality/phase6_controle_cartographique.md)
- [Bilan de qualité spatiale](reports/quality/phase6_bilan_qualite_spatiale.md)
- [Consolidation du socle pilote V1](reports/quality/phase7_consolidation.md)
- [Rapport de qualité du socle pilote V1](reports/quality/phase7_rapport_qualite.md)
- [Anomalies restantes du socle pilote V1](reports/quality/phase7_anomalies_restantes.md)
- [Préparation de la suite](reports/quality/phase7_preparation_suite.md)
- [Décision finale sur le socle V1](reports/quality/phase7_decision_socle_v1.md)
- [Évaluation de l'extraction complète](reports/quality/phase7_evaluation_extraction_complete.md)
- [Première carte interne](reports/maps/carte_pilote_interne.png)
- [Projet QGIS de contrôle](qgis/controle_phase6.qgs)
- [Validation du corpus complet V1](reports/quality/phase8_validation_corpus_complet.md)
- [Indicateurs du corpus complet](reports/quality/phase8_indicateurs_corpus_complet.json)
- [Limites restantes du corpus complet](reports/quality/phase8_anomalies_restantes.csv)
- [Couverture de la matière historique](reports/quality/phase9_recits_sites_couverture.md)
- [Inventaire des médias](reports/quality/phase9_medias_sites_inventaire.md)
- [Qualification des droits et usages](reports/quality/phase9_droits_medias.md)
- [Revue éditoriale des sites](reports/quality/phase9_revue_editoriale.md)
- [Validation du socle narratif et visuel](reports/quality/phase9_validation_narratif_visuel.md)

## Produire le corpus complet V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.corpus_complet_v1
```

Cette commande recalcule les indicateurs, produit les exports complets et
interrompt la validation si les effectifs ou identifiants divergent entre
JSON, DuckDB, CSV, Parquet et GeoJSON.

## Produire les récits de sites V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.editorial_v1
```

Cette commande produit les exports éditoriaux CSV et Parquet, ajoute la table
`recits_sites` à la base DuckDB du corpus complet et vérifie la concordance des
318 identifiants.

## Produire l'inventaire des médias V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.medias_v1
```

Cette commande inventorie les métadonnées médias sans télécharger les images,
produit les exports CSV et Parquet, ajoute la table `medias` à DuckDB et liste
les notices sans média exploitable.

## Qualifier les droits des médias V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.qualifier_medias_v1
```

Cette commande met à jour les statuts d'usage sans déduire d'autorisation,
produit le registre `registre_autorisations_medias_v1.csv` et ajoute
`demandes_autorisation_medias` à DuckDB. Elle ne télécharge aucune image et
n'envoie aucune demande.

## Produire la revue éditoriale V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.revue_editoriale_v1
```

Cette commande produit `revue_editoriale_sites_v1.csv`, son Parquet et sa table
DuckDB. Elle propose des médias à examiner sans les sélectionner ni les rendre
publiables.

## Valider le socle narratif et visuel V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.validate_narratif_visuel_v1
```

Cette commande compare corpus, récits, médias et revue éditoriale. Elle échoue
si un texte source est perdu, si un média manque de provenance ou si les
identifiants des 318 sites divergent.

## Produire la chronologie des sites

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.chronologie_v1
```

Cette commande extrait et verse les événements datés dans `chronologie_sites`,
produit les exports CSV et Parquet et conserve la formulation source. Une date
imprécise reste imprécise et une période documentée n'est pas assimilée à une
activité continue.

## Régénérer la vue de référence

```powershell
python tools/generer_vue_reference.py
```

Vue de référence de la phase 10.D : un fichier HTML autonome portant trois
niveaux — département, ensemble, site — avec le filtre par métier, la liste
synchronisée avec la carte et les phrases de source qui prouvent les liens,
atteignables au clavier comme à la souris. Les données de Crulai y sont
embarquées pour le contrôle de robustesse.

La commande **sort en code 1 si un effectif ne correspond plus** au registre
`config/phase10_systemes.yml` : douze ensembles, 172 sites regroupés, 146 hors
ensembles, 43 sites et cinq liens pour la Risle, sept sites et aucun lien pour
Crulai.

Elle lit directement la base du corpus complet et n'importe pas le paquet : pas
de `PYTHONPATH`, mais `data/processed/` doit avoir été produit au préalable. La
vue est volontairement neutre sur le plan graphique — elle éprouve la
compréhension et la structure, jamais l'esthétique.

## Régénérer la première vue de la Risle

```powershell
python tools/generer_ecran_risle.py
```

Cette vue autonome, produite le 5 août 2026, a servi à valider le principe
général de l'application : le cadre habillé, le recadrage de la carte et
l'annotation posée sur la forme. Elle est conservée comme jalon et ne porte
aucune direction artistique définitive.

## Produire le socle pilote V1

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.export.socle_v1
```

Cette commande reconstruit la base DuckDB de référence et les exports CSV,
Parquet et GeoJSON dans `data/processed/` et `data/exports/`. Le fichier
`sites_pilote_v1.csv` présente une ligne par site ; `activites_pilote_v1.csv`
présente une ligne par phase d'activité avec ses dates et périodes. Ces
livrables sont générés localement et ne sont pas versionnés.

## Localisations du pilote

Les contrôles BAN et cadastraux sont reproductibles avec :

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.extract.pilot_geography
python -m patrimoine_orne.geocode.pilot
python -m patrimoine_orne.extract.territorial_context
python -m patrimoine_orne.geocode.territorial_context
python -m patrimoine_orne.geocode.cartographic_control
```

La première commande interroge les services publics IGN et archive les réponses.
La seconde qualifie les résultats sans transformer une géométrie automatique en
localisation vérifiée.
Les deux suivantes extraient puis calculent le contexte territorial. La dernière
reconstruit les cinq couches GeoJSON utilisées par le projet QGIS de contrôle.

Le fichier projet QGIS est ensuite généré et validé avec l'environnement Python
fourni par QGIS :

```powershell
& "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat" `
  tools\generate_qgis_project.py
```

## Base DuckDB de test

Le modèle nécessite Python, DuckDB et l'extension DuckDB Spatial. Le jeu
d'essai est synthétique et ne décrit aucun site réel.

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.model.database `
  --database data/processed/phase3_model_test.duckdb `
  --seed tests/fixtures/model_seed.sql `
  --install-spatial
```

La commande crée le schéma, charge l'échantillon et exécute toutes les
validations transversales.

## Organisation des données

- `data/raw/` : fichiers originaux, jamais modifiés ;
- `data/interim/` : résultats intermédiaires reproductibles ;
- `data/manual/` : corrections humaines documentées ;
- `data/processed/` : corpus nettoyé ;
- `data/exports/` : livrables CSV, Parquet et GeoJSON.
- `data/archive/` : archives locales validées, non versionnées.

## Principes

1. Vérifier les sources avant toute extraction massive.
2. Conserver les données brutes intactes.
3. Distinguer les faits sourcés, les données calculées et les interprétations.
4. Documenter les incertitudes et la précision géographique.
5. Ne construire l'application qu'après validation du socle V1.
