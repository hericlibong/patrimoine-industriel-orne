# Roadmap

Dernière mise à jour : **2026-07-19**

## Règles de suivi

- `[ ]` : à faire ;
- `[-]` : en cours ;
- `[x]` : terminé et vérifié ;
- chaque fin de phase doit mettre à jour ce fichier ;
- une phase n'est terminée que lorsque son point de validation est satisfait ;
- toute modification importante est inscrite dans `journal_decisions.md`.

## Initialisation du projet

- [x] Créer l'arborescence de travail
- [x] Ajouter le README principal
- [x] Ajouter la configuration Python
- [x] Créer les espaces de données brutes, intermédiaires et traitées
- [x] Créer les documents de cadrage et de méthode
- [x] Créer le registre provisoire des sources
- [x] Créer les classifications provisoires
- [x] Créer la roadmap
- [x] Préserver les documents de recherche et de discussion existants

---

## Phase 0 — Formaliser le cadrage

**Statut : terminée le 19 juillet 2026.**

### Intention et périmètre

- [x] Formaliser l'intention éditoriale
- [x] Formaliser les quatre questions principales
- [x] Définir le premier livrable
- [x] Définir la forme finale envisagée
- [x] Définir le hors-périmètre de l'initialisation
- [x] Fixer les bornes chronologiques
- [x] Définir opérationnellement un site industriel
- [x] Définir les critères d'inclusion
- [x] Définir les critères d'exclusion
- [x] Décider comment traiter les sites successifs ou composites
- [x] Décider quelles infrastructures liées à l'industrie sont incluses

### Provenance et interprétation

- [x] Distinguer information sourcée, calculée et interprétée
- [x] Définir les règles de citation des sources
- [x] Définir les règles de datation des observations contemporaines
- [x] Définir les règles de gestion des contradictions entre sources

### Validation de phase

- [x] Relire et approuver le cadrage opérationnel complet
- [x] Inscrire les décisions définitives dans le journal
- [x] Marquer la phase 0 comme terminée

**Point de validation :** savoir précisément ce qui entre ou non dans le corpus.

---

## Phase 1 — Auditer les sources

### Préparer l'audit

- [ ] Définir la grille d'audit commune
- [ ] Créer `registre_sources.csv`
- [ ] Définir les statuts d'audit
- [ ] Définir les critères de priorité

### Auditer les sources patrimoniales

- [ ] Auditer l'Inventaire du patrimoine industriel de l'Orne
  - [ ] Vérifier le nombre et le périmètre des dossiers
  - [ ] Identifier les champs disponibles
  - [ ] Identifier les formats et moyens d'accès
  - [ ] Tester les identifiants et liens permanents
  - [ ] Vérifier les conditions de réutilisation
- [ ] Auditer POP / Mérimée
  - [ ] Distinguer inventaire général et Monuments historiques
  - [ ] Tester recherche, export et liens
  - [ ] Identifier les champs utiles au projet
- [ ] Auditer POP / Palissy
  - [ ] Identifier les objets techniques pertinents
  - [ ] Tester les liens entre objets et sites
  - [ ] Vérifier les conditions de réutilisation
- [ ] Auditer les données Monuments historiques
  - [ ] Tester le filtre sur l'Orne
  - [ ] Vérifier les coordonnées
  - [ ] Mesurer la couverture industrielle

### Auditer les sources d'élargissement

- [ ] Auditer CASIAS
  - [ ] Tester le téléchargement pour l'Orne
  - [ ] Identifier les champs et identifiants
  - [ ] Vérifier les doublons liés aux communes
  - [ ] Évaluer le bruit hors patrimoine industriel
  - [ ] Documenter les précautions d'interprétation

### Auditer les sources géographiques

- [ ] Auditer IGN / Géoplateforme
- [ ] Auditer le cadastre ouvert
- [ ] Auditer la Base Adresse Nationale
- [ ] Auditer les données hydrographiques
- [ ] Auditer les données forestières
- [ ] Auditer les données géologiques et minières du BRGM
- [ ] Auditer les données ferroviaires actuelles et historiques disponibles
- [ ] Auditer OpenStreetMap comme source d'appoint

### Auditer les sources de vérification éditoriale

- [ ] Auditer les Archives départementales de l'Orne
- [ ] Auditer Gallica
- [ ] Identifier les sources touristiques et institutionnelles locales
- [ ] Documenter les droits associés aux images

### Classer les sources

- [ ] Attribuer un rôle définitif à chaque source
- [ ] Documenter les sources écartées et la raison
- [ ] Hiérarchiser les sources en cas de contradiction

### Validation de phase

- [ ] Vérifier que chaque source prioritaire possède une fiche complète
- [ ] Produire le bilan d'audit
- [ ] Mettre à jour `sources.yml`
- [ ] Mettre à jour le journal des décisions
- [ ] Marquer la phase 1 comme terminée

**Point de validation :** chaque source possède un rôle, un mode d'accès et des limites documentées.

---

## Phase 2 — Réaliser des extractions tests

### Préparer les extractions

- [ ] Définir la convention de nommage des fichiers bruts
- [ ] Définir les métadonnées de récupération
- [ ] Créer les premiers modules d'extraction
- [ ] Créer les tests techniques minimaux

### Tester chaque source principale

- [ ] Extraire un échantillon de l'Inventaire normand
- [ ] Extraire un échantillon Mérimée
- [ ] Extraire un échantillon Palissy
- [ ] Extraire un échantillon Monuments historiques
- [ ] Extraire un échantillon CASIAS

### Évaluer les résultats

- [ ] Vérifier les encodages et formats
- [ ] Mesurer les champs renseignés et manquants
- [ ] Identifier les identifiants réutilisables
- [ ] Identifier les doublons internes
- [ ] Tester la présence et la qualité des coordonnées
- [ ] Estimer la part automatisable
- [ ] Identifier les traitements manuels nécessaires

### Validation de phase

- [ ] Archiver les données brutes de test
- [ ] Produire un rapport comparatif des extractions
- [ ] Choisir les méthodes d'extraction définitives
- [ ] Mettre à jour le journal des décisions
- [ ] Marquer la phase 2 comme terminée

**Point de validation :** savoir ce qui est automatisable, semi-automatisable ou manuel.

---

## Phase 3 — Construire le modèle de données

### Modéliser les entités principales

- [ ] Valider la table `sites`
- [ ] Valider la table `activites`
- [ ] Valider la table `etats_actuels`
- [ ] Valider la table `sources`
- [ ] Valider la table `mentions_sources`
- [ ] Définir la table `protections`
- [ ] Définir la table `objets_techniques`
- [ ] Définir la gestion des géométries
- [ ] Décider si une table `exploitants` est nécessaire
- [x] Décider si une table `relations_sites` est nécessaire
- [ ] Définir la table `relations_sites`

### Définir les règles

- [ ] Définir les identifiants internes stables
- [ ] Définir les relations entre tables
- [ ] Définir les champs obligatoires
- [ ] Définir les valeurs nulles et inconnues
- [ ] Définir le traitement des dates imprécises
- [ ] Définir le traitement des activités successives
- [ ] Définir le versionnement des observations actuelles

### Implémenter le modèle

- [ ] Créer le schéma DuckDB
- [ ] Créer les contraintes de validation
- [ ] Mettre à jour le dictionnaire des données
- [ ] Créer un petit jeu de données de test

### Validation de phase

- [ ] Tester un site simple
- [ ] Tester un site multi-activités
- [ ] Tester un site reconverti
- [ ] Tester un site disparu
- [ ] Tester un rapprochement incertain
- [ ] Approuver le modèle V1
- [ ] Mettre à jour le journal des décisions
- [ ] Marquer la phase 3 comme terminée

**Point de validation :** le modèle représente correctement les situations réelles du corpus.

---

## Phase 4 — Construire les classifications

### Secteurs et installations

- [ ] Tester les secteurs provisoires sur les données extraites
- [ ] Définir les règles d'affectation à un secteur
- [ ] Construire le vocabulaire des activités détaillées
- [ ] Construire le vocabulaire des types d'installations
- [ ] Distinguer activité, bâtiment et source d'énergie
- [ ] Documenter les sites multi-secteurs

### Chronologie et situation actuelle

- [ ] Définir les périodes historiques utiles
- [ ] Valider la classification de conservation
- [ ] Valider la classification des usages actuels
- [ ] Valider la classification d'accessibilité
- [ ] Valider la classification des protections

### Qualité

- [ ] Valider les niveaux de précision géographique
- [ ] Valider les niveaux de fiabilité
- [ ] Définir les règles d'emploi de `autre`
- [ ] Définir les règles d'emploi de `inconnu`
- [ ] Tester la reproductibilité du classement

### Validation de phase

- [ ] Publier `classifications.yml` en version 1.0
- [ ] Ajouter les définitions au dictionnaire des données
- [ ] Mettre à jour le journal des décisions
- [ ] Marquer la phase 4 comme terminée

**Point de validation :** un site peut être classé de manière cohérente et explicable.

---

## Phase 5 — Construire l'échantillon pilote

### Composer l'échantillon

- [ ] Définir la méthode d'échantillonnage
- [ ] Sélectionner environ 30 sites
- [ ] Vérifier la diversité géographique
- [ ] Vérifier la diversité sectorielle
- [ ] Inclure plusieurs périodes
- [ ] Inclure plusieurs états de conservation
- [ ] Inclure des sites protégés et non protégés
- [ ] Inclure des cas faciles et difficiles à localiser

### Enrichir les sites

- [ ] Attribuer un identifiant interne
- [ ] Rapprocher les notices entre sources
- [ ] Structurer les activités successives
- [ ] Documenter la situation actuelle
- [ ] Enregistrer les sources et niveaux de confiance
- [ ] Recenser les objets techniques associés
- [ ] Documenter les anomalies et contradictions

### Validation de phase

- [ ] Contrôler manuellement chaque fiche pilote
- [ ] Vérifier qu'aucune information importante n'est sans source
- [ ] Produire le corpus pilote V1
- [ ] Mettre à jour le journal des décisions
- [ ] Marquer la phase 5 comme terminée

**Point de validation :** chaque site pilote possède des sources, une localisation et un niveau de certitude explicites.

---

## Phase 6 — Tester les données géographiques

### Localisation

- [ ] Vérifier les coordonnées existantes
- [ ] Géocoder les adresses suffisamment précises
- [ ] Rapprocher les sites des parcelles cadastrales
- [ ] Identifier les emprises disponibles
- [ ] Signaler les localisations approximatives
- [ ] Conserver les sites non localisés sans leur inventer de coordonnées

### Contexte territorial

- [ ] Tester la proximité aux cours d'eau
- [ ] Tester les relations avec les forêts
- [ ] Tester les relations avec la géologie ou les minerais
- [ ] Tester les relations avec le réseau ferroviaire
- [ ] Vérifier les systèmes de coordonnées utilisés

### Contrôle cartographique

- [ ] Créer une carte de contrôle QGIS
- [ ] Repérer les points aberrants
- [ ] Contrôler manuellement les emprises sensibles
- [ ] Documenter les erreurs et limites

### Validation de phase

- [ ] Valider les règles de précision géographique
- [ ] Produire un bilan de qualité spatiale
- [ ] Mettre à jour le journal des décisions
- [ ] Marquer la phase 6 comme terminée

**Point de validation :** la carte ne présente aucune précision géographique artificielle.

---

## Phase 7 — Produire le socle V1

### Consolider les données

- [ ] Nettoyer le corpus pilote
- [ ] Exécuter les validations finales
- [ ] Produire la base DuckDB
- [ ] Produire l'export CSV
- [ ] Produire l'export Parquet
- [ ] Produire l'export GeoJSON

### Consolider la documentation

- [ ] Finaliser le dictionnaire des données
- [ ] Finaliser le registre des sources
- [ ] Finaliser les classifications
- [ ] Produire le rapport de qualité
- [ ] Produire la liste des anomalies restantes
- [ ] Documenter les limites éditoriales
- [ ] Documenter les licences et droits des images

### Préparer la suite

- [ ] Produire une première carte de contrôle publiable en interne
- [ ] Évaluer l'extraction complète des 319 dossiers
- [ ] Estimer la charge de constitution du corpus complet
- [ ] Identifier les récits réellement soutenus par les données
- [ ] Formuler une recommandation pour l'application

### Décision de fin de socle

- [ ] Choisir `GO`, `GO LIMITE` ou `STOP`
- [ ] Documenter la décision
- [ ] Approuver le socle V1
- [ ] Marquer la phase 7 comme terminée

**Point de validation :** le socle est suffisamment fiable pour décider de la construction de l'application.

---

## Phase ultérieure — Publication interactive

Cette phase reste volontairement non détaillée avant validation du socle V1.

- [ ] Valider le format éditorial définitif
- [ ] Concevoir le parcours narratif
- [ ] Concevoir la carte exploratoire
- [ ] Définir les filtres publics
- [ ] Concevoir les fiches de sites
- [ ] Prototyper l'interface
- [ ] Tester les performances et l'accessibilité
- [ ] Préparer la publication et la maintenance
