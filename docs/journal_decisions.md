# Journal des décisions

## 2026-07-19 — Initialisation

- Le projet est défini comme une publication datajournalistique, narrative et cartographique.
- Le premier livrable est un socle de données, pas une application.
- L'Inventaire du patrimoine industriel de l'Orne est le candidat au rôle de corpus initial.
- CASIAS est une source d'élargissement et non une source patrimoniale principale.
- La conservation, l'usage actuel et l'accessibilité seront modélisés séparément.
- Les données brutes seront conservées sans modification.
- Une roadmap suivie par cases à cocher est ajoutée au projet.

## 2026-07-19 — Clôture de la phase 0

- Le corpus principal couvre les limites actuelles du département de l'Orne.
- Aucune borne ancienne fixe n'est imposée ; la première activité documentée
  constitue le début possible d'un site.
- L'entrée dans le corpus principal exige une activité au plus tard en 1950.
- Les établissements uniquement postérieurs à 1950 sont exclus du corpus
  principal, mais peuvent apparaître comme successeurs ou sites liés.
- Un site correspond à une emprise distincte, pas à un nom d'entreprise.
- Une même emprise conserve un identifiant unique à travers ses activités
  successives ; un déplacement crée un nouveau site relié au précédent.
- Les infrastructures sont distinguées entre sites, composants et couches de
  contexte.
- La table `relations_sites` est déclarée nécessaire.
- Les règles d'inclusion et d'exclusion sont fixées dans `config/perimetre.yml`.
- Les informations contemporaines disposent d'une durée de fraîcheur avant
  publication : trois mois pour l'accès, douze mois pour l'usage et la
  conservation, trente jours pour la protection juridique.
- Les contradictions sont conservées et documentées, jamais écrasées
  silencieusement.
- La phase 0 est terminée ; la phase 1 peut commencer.

## 2026-07-19 — Clôture de la phase 1

- L'Inventaire du patrimoine industriel de l'Orne est confirmé comme corpus
  principal : 319 dossiers étudiés, avec une extraction à tester en mode
  semi-automatique faute d'export global identifié.
- POP / Mérimée et l'export des Monuments historiques sont distingués : les
  immeubles protégés enrichissent le corpus, mais ne le définissent pas.
- Palissy est retenue pour les objets techniques liés aux sites, avec rapprochement
  par référence Mérimée ou, à défaut, par édifice et commune contrôlés.
- L'API des Monuments historiques retourne 420 notices dans l'Orne, dont 341 avec
  coordonnées ; 18 candidats industriels par mots-clés restent à revoir.
- CASIAS est confirmé comme source d'élargissement uniquement. La couche WFS testée
  contient 2 052 sites dans l'Orne, mais seulement 209 coordonnées explicites et
  un bruit thématique important.
- Une géométrie CASIAS représentant une commune ne sera jamais publiée comme
  position d'un établissement.
- La BD TOPAGE est retenue pour l'hydrographie ; la BD Forêt v2 et la BD Forêts
  anciennes sont conservées comme deux contextes distincts.
- Le réseau ferré actuel sera issu de données SNCF ou IGN. Le réseau historique
  sera reconstruit à partir de cartes et d'archives datées, avec niveau de confiance.
- OpenStreetMap reste une source de vérification et d'appoint sous ODbL.
- L'ancienne API Adresse est écartée au profit des fichiers BAN et du géocodeur de
  la Géoplateforme.
- Les droits des métadonnées et ceux des images seront enregistrés séparément.
  Aucune image visible en ligne ne sera considérée réutilisable par défaut.
- La phase 2 commencera par un petit échantillon multi-secteurs de l'Inventaire,
  avant les téléchargements géographiques départementaux volumineux.
- La phase 1 est terminée ; les extractions tests peuvent commencer.

## 2026-07-20 — Comptage et documentation des limites

- Le projet distingue désormais les notices sources, les sites candidats, les
  sites rapprochés, les sites cartographiables et les sites publiés.
- Aucun nombre de lieux définitif ne sera annoncé avant rapprochement,
  dédoublonnage, application du périmètre et qualification géographique.
- Chaque livraison présentera séparément les effectifs de ces cinq niveaux.
- Les limites méthodologiques et techniques sont centralisées dans le registre
  vivant `reports/quality/limites.md` et seront reprises dans le rapport de
  qualité final.

## 2026-07-20 — Phase 2, préparation des extractions

- La phase 2 est conduite bloc par bloc, avec validation avant de passer au bloc
  suivant.
- Les fichiers bruts sont rangés par source, année et date de récupération.
- Leur nom contient la source, la ressource, le périmètre et l'heure UTC.
- Chaque fichier brut possède un JSON voisin décrivant l'accès, la licence, la
  requête, la taille, le hash SHA-256 et la version du code.
- Un fichier brut ou son fichier de métadonnées ne peut pas être remplacé
  silencieusement.
- Les modules communs de nommage et de métadonnées sont couverts par 11 tests
  techniques sans accès réseau.
- Le bloc « Préparer les extractions » est terminé. Le bloc suivant peut tester
  les cinq sources principales sur des échantillons limités.

## 2026-07-20 — Phase 2, test des cinq sources principales

- Les cinq extractions tests ont abouti et produit 34 fichiers bruts contrôlés
  par métadonnées, taille et empreinte SHA-256.
- L'Inventaire normand est accessible par les anciens dossiers statiques liés
  depuis POP, mais son contenu détaillé est principalement composé de scans.
- Les ressources d'export liées depuis le jeu data.gouv.fr de l'Inventaire
  normand sont obsolètes ou en erreur à la date du test.
- Les dix notices Mérimée `IA` correspondant à l'échantillon sont accessibles
  sur POP et constituent le canal prioritaire pour les champs descriptifs.
- L'API Palissy permet un ciblage exact, mais les deux objets tests n'ont pas de
  référence Mérimée directe renseignée.
- La recherche large dans les Monuments historiques retourne 77 notices, dont
  50 avec coordonnées ; cet effectif inclut des faux positifs et ne constitue
  pas un nombre de sites industriels.
- Les deux lots CASIAS confirment la distinction entre fiches localisées et
  fiches explicitement non géolocalisées ; aucune coordonnée ne sera inventée.
- Le bloc « Tester chaque source principale » est terminé. L'évaluation détaillée
  des formats, champs, identifiants, doublons et coordonnées reste à réaliser.

## 2026-07-20 — Phase 2, évaluation des résultats

- Les 34 fichiers ont un format valide. Les anciens HTML de l'Inventaire sont
  en ISO-8859-1 ; les autres échantillons sont en UTF-8. Les données dérivées
  seront normalisées en UTF-8 sans modifier les fichiers bruts.
- Les pages POP contiennent une notice structurée exploitable. Sur dix notices,
  l'identifiant, l'activité, la commune, l'historique, la période et les
  coordonnées sont présents dans tous les cas.
- POP / Mérimée est confirmé comme point d'entrée du corpus initial. Les scans
  de l'Inventaire seront utilisés seulement pour compléter les informations.
- Les références `IA`, `PM`, `PA`, `SSP` et `BNO` sont conservées comme
  identifiants externes. Un code INSEE ne sera jamais utilisé comme identifiant
  de site.
- Aucun doublon de référence principale n'a été trouvé dans les échantillons.
  Les notices issues de sources différentes resteront séparées jusqu'au
  rapprochement explicite.
- La validité WGS84 est contrôlable automatiquement, mais la précision réelle
  du point doit être qualifiée avant publication.
- Une géométrie CASIAS est ignorée lorsque les coordonnées WGS84 explicites sont
  absentes ou que la fiche est déclarée non géolocalisée.
- L'extraction technique est largement automatisable. La qualification
  patrimoniale, les faux positifs, les rapprochements incertains, l'OCR ciblé et
  la situation actuelle exigent une validation humaine.
- Le bloc « Évaluer les résultats » est terminé. La validation finale de la
  phase 2 doit maintenant arrêter les méthodes d'extraction définitives.

## 2026-07-20 — Clôture de la phase 2

- Les 34 fichiers bruts de test et leurs 34 métadonnées ont été archivés à
  partir du seul manifeste validé. Les fichiers d'essais non référencés ont été
  exclus.
- L'archive est locale, immuable et hors Git. Son descripteur et son empreinte
  SHA-256 sont versionnés pour permettre le contrôle de son intégrité.
- L'Inventaire normand reste le corpus principal, mais son accès structuré se
  fera par les notices POP / Mérimée ; les scans seront un complément ciblé.
- Palissy sera interrogée après constitution des sites afin d'enrichir les
  objets techniques, avec contrôle humain en l'absence de référence Mérimée.
- Les Monuments historiques seront extraits pour tout le département ; les
  mots-clés serviront à prioriser la revue et non à exclure automatiquement.
- CASIAS sera chargé dans une table séparée de candidats. L'activité devra être
  enrichie et aucune géométrie sans coordonnées WGS84 explicites ne sera publiée.
- Les jointures automatiques sont limitées aux identifiants externes exacts. Les
  rapprochements par commune, nom, adresse ou proximité restent à valider.
- Les méthodes définitives sont enregistrées dans `config/extraction.yml` et le
  rapport comparatif de phase dans `reports/audits/phase2_rapport_comparatif.md`.
- Le point de validation est atteint : le projet distingue désormais les
  opérations automatiques, semi-automatiques et manuelles.
- La phase 2 est terminée ; la phase 3 peut commencer.

## 2026-07-20 — Phase 3, entités principales

- `sites` représente une emprise distincte et stable. Les activités, états
  contemporains et géométries sont sortis de cette table pour conserver leur
  pluralité et leur historique.
- `activites` contient une ligne par phase industrielle. Les énergies multiples
  seront normalisées dans `energies_activites`.
- `etats_actuels` conserve des observations datées sans écraser les contrôles
  antérieurs. Conservation, usage et accessibilité restent distincts.
- `sources` décrit les fonds et jeux de données ; `mentions_sources` conserve
  la référence individuelle et cible une entité ou un champ précis.
- `protections` peut viser soit un site, soit un objet technique. La partie
  réellement protégée doit être décrite explicitement.
- Les objets techniques sont reliés aux sites par `liens_objets_sites`, afin de
  représenter une origine et un emplacement actuel différents.
- Les géométries sont stockées séparément en Lambert-93 et exportées en WGS84.
  Plusieurs géométries et niveaux de précision peuvent coexister pour un site.
- La table `exploitants` est déclarée nécessaire. `exploitations` porte la
  relation datée entre exploitant, site et éventuellement phase d'activité.
- `relations_sites` relie deux emprises sans les fusionner. Les premiers types
  sont composant, transfert, succession, dépendance et infrastructure partagée.
- Le modèle conceptuel est documenté dans `docs/modele_donnees.md` et le
  dictionnaire passe en version conceptuelle 0.2.
- Le bloc « Modéliser les entités principales » est terminé. Les identifiants,
  contraintes, valeurs nulles et dates imprécises restent à définir.

## 2026-07-20 — Phase 3, règles du modèle

- Les entités métier utilisent des UUID version 4, générés une seule fois et
  indépendants des noms, communes et références des sources.
- Les références `IA`, `PM`, `PA`, `SSP`, `BNO` et autres sont conservées dans
  `identifiants_externes`. Une réextraction réutilise l'UUID seulement après
  correspondance exacte d'un identifiant externe.
- Une fusion de doublons conserve les deux UUID : l'un devient canonique et
  l'autre est redirigé sans suppression.
- Les suppressions physiques et les cascades sont interdites dans le corpus.
  Les corrections utilisent des statuts et des lignes de remplacement.
- Les obligations minimales sont définies table par table, avec des conditions
  supplémentaires pour les sites inclus, cartographiables et publiés.
- `NULL` signifie qu'aucune valeur normalisée n'est stockée. La cause est
  qualifiée séparément : inconnue, absente de la source, non applicable,
  contradictoire ou à vérifier.
- Les dates imprécises sont stockées sous forme d'intervalle minimum-maximum,
  avec un code de précision et le texte original. Aucun milieu d'intervalle
  n'est publié comme date réelle.
- Un changement de production ou une interruption documentée crée une nouvelle
  phase d'activité. Un changement d'exploitant ou d'énergie seul ne crée pas
  automatiquement une nouvelle activité.
- `etats_actuels` fonctionne en ajout seulement. Une nouvelle observation reçoit
  un UUID et une version ; l'ancienne ligne reste dans l'historique.
- La vue courante sélectionnera la dernière valeur valide séparément pour la
  conservation, l'usage et l'accessibilité, avec leurs durées de fraîcheur.
- Les règles sont documentées dans `docs/regles_modele.md` et leur version
  opérationnelle dans `config/regles_modele.yml`.
- Le bloc « Définir les règles » est terminé. Le schéma DuckDB peut maintenant
  être implémenté.

## 2026-07-20 — Phase 3, implémentation du modèle

- Le modèle est matérialisé dans DuckDB par un schéma versionné `0.1.0` : les
  tables métier, leurs clés étrangères, contrôles locaux et trois vues de
  lecture sont créés par un seul fichier SQL reproductible.
- Les géométries utilisent le vrai type `GEOMETRY` de DuckDB Spatial. Le système
  de travail est imposé à `EPSG:2154` ; l'extension est donc une dépendance
  explicite de l'initialisation.
- Les contraintes SQL bloquent notamment les intervalles de dates inversés,
  les auto-relations, les protections à zéro ou deux cibles, les doublons
  d'identifiants externes et les observations contemporaines vides.
- Un validateur Python complète DuckDB pour les règles entre tables : existence
  des cibles et champs de provenance, obligations des sites inclus ou
  cartographiables, géométrie de référence, cohérence des exploitations et des
  versions d'état, ordre des relations symétriques.
- La vue `etats_actuels_courants` recompose chaque dimension séparément. Une
  nouvelle observation d'accessibilité ne remplace donc pas une conservation
  plus ancienne encore pertinente.
- Le jeu `tests/fixtures/model_seed.sql` est entièrement synthétique. Il teste
  trois sites fictifs, des activités successives, un transfert, une machine
  déplacée, un site disparu sans géométrie et un état contemporain révisé.
- Le dictionnaire passe en version 0.4 et distingue maintenant les types
  conceptuels de leurs types DuckDB effectifs.
- Le bloc « Implémenter le modèle » est terminé. La validation de phase doit
  maintenant confronter ce modèle à plusieurs cas représentatifs du corpus.

## 2026-07-20 — Clôture de la phase 3

- Cinq scénarios synthétiques reproductibles ont été testés : site simple,
  multi-activités, reconverti, disparu et rapprochement incertain.
- Le site simple conserve sous un même UUID une activité, une observation
  actuelle, une géométrie de référence et sa provenance.
- Une forge devenue moulin reste un seul site avec deux phases successives.
- La reconversion est stockée dans `etats_actuels` et ne devient jamais une
  activité industrielle historique.
- Un site disparu reste dans le corpus sans géométrie artificielle lorsque son
  emplacement précis est inconnu.
- Le dernier cas a révélé un manque du modèle initial : aucune structure ne
  permettait d'enregistrer une hypothèse de doublon avant décision.
- `propositions_rapprochement` est donc ajoutée. Elle conserve deux sites
  candidats, les critères et le score éventuel, sans aucune fusion automatique.
- `relations_sites` reste réservée aux relations historiques ou fonctionnelles
  entre emprises distinctes ; elle ne sert pas à la déduplication.
- Le schéma DuckDB passe en version `1.0.0`, le dictionnaire en version 1.0 et
  les règles opérationnelles en version 1.1.
- Les 40 tests du projet réussissent. Le rapport détaillé est conservé dans
  `reports/quality/phase3_validation_modele.md`.
- Le modèle V1 est approuvé pour le corpus pilote. Cette validation porte sur
  sa structure ; les vocabulaires seront construits en phase 4 et les scénarios
  devront être rejoués sur les données réelles du pilote.
- La phase 3 est terminée. La phase 4 peut commencer.

## 2026-07-21 — Phase 4, secteurs et installations

- Les secteurs provisoires ont été testés sur les 10 notices POP du manifeste
  de phase 2 : les 13 dénominations `DENO` sont couvertes par le vocabulaire.
- Cette couverture de 100 % décrit uniquement l'échantillon et ne peut pas être
  extrapolée au corpus complet.
- L'unité classée est désormais la phase d'activité. Le secteur du site est
  dérivé de ses activités et n'est pas stocké directement dans `sites`.
- Le code `activite_mixte` est supprimé. Un site qui traverse plusieurs secteurs
  conserve plusieurs activités datées et apparaît dans chaque filtre concerné.
- Les comptages globaux dédupliquent par `site_id`; additionner les secteurs
  peut compter plusieurs fois un même lieu.
- Activité, installation, bâtiment, énergie et rôle énergétique sont séparés.
  Une roue hydraulique est un équipement, tandis que « produite sur place » est
  un rôle ou une provenance, pas une énergie.
- `DENO` et `TICO` servent de point d'entrée, mais `HIST` doit être relu : une
  filature de l'échantillon a été convertie en minoterie sans que cette seconde
  activité apparaisse dans la dénomination structurée.
- Le registre `config/classifications.yml` passe en version 0.2. Les secteurs,
  activités détaillées, installations et énergies sont validés pour ce bloc ;
  les autres classifications de phase 4 restent provisoires.
- Le rapport est enregistré dans
  `reports/quality/phase4_test_secteurs.md` et ses mesures dans
  `reports/quality/phase4_secteurs_sample.json`.
- Les 45 tests du projet réussissent après ajout des contrôles sectoriels.
- Le bloc « Secteurs et installations » est terminé. Le bloc suivant porte sur
  la chronologie et la situation actuelle.

## 2026-07-21 — Phase 4, chronologie et situation actuelle

- Sept périodes historiques contiguës sont définies comme filtres analytiques.
  Elles ne remplacent pas les dates sources et un intervalle peut relever de
  plusieurs périodes.
- La conservation décrit uniquement l'état matériel. « Désaffecté » est exclu,
  car il qualifie l'arrêt de l'activité.
- Les usages actuels deviennent une table liée aux observations datées. Plusieurs
  usages peuvent coexister ; `usage_mixte` est interdit et un seul usage peut être
  principal.
- L'accessibilité sépare droit de visite et visibilité. Un site visible depuis
  l'espace public n'est pas automatiquement visitable.
- Une protection est stockée mesure par mesure. Type, portée et élément protégé
  sont distincts ; l'Inventaire général n'est pas une protection juridique.
- Sur 10 notices POP, `SCLE` est toujours renseigné, mais les 6 valeurs d'état
  sont toutes des mentions de désaffectation, inutilisables pour la conservation.
- Sur 77 candidats MH, la destination actuelle est toujours vide. Seules quatre
  mentions décrivent directement la conservation ; 14 indiquent seulement une
  désaffectation.
- Les 77 notices MH produisent 86 mesures de protection : 17 classements et 69
  inscriptions. Neuf sont explicitement partielles ; les autres gardent une
  portée inconnue jusqu'à vérification.
- Le schéma DuckDB passe en version `1.1.0`, le dictionnaire en version 1.1 et
  les règles du modèle en version 1.2.
- Les 54 tests du projet réussissent après ajout des contrôles de chronologie,
  d'usages multiples et de protections multiples.
- Le registre des classifications passe en version 0.3. Le deuxième bloc de la
  phase 4 est terminé ; le bloc suivant porte sur la qualité.

## 2026-07-21 — Phase 4, qualité

- Sept niveaux de précision géographique sont validés : emprise du site,
  parcelle, bâtiment, point du site, point d'adresse, point approximatif et zone
  documentaire.
- Le type de géométrie, la méthode de localisation, la précision et la fiabilité
  sont quatre dimensions distinctes.
- `centre_commune` et `non_localise` deviennent des statuts sans géométrie de
  site. Aucun centroïde communal ne peut être publié comme emplacement.
- La présence d'une coordonnée ou d'un contour dans une source ne suffit pas à
  attribuer un niveau vérifié. Sur les échantillons POP et CASIAS, aucune
  précision n'est validée automatiquement.
- La fiabilité utilise uniquement `forte`, `moyenne` et `faible` et s'applique à
  une information ou une relation. `a_verifier` reste un statut de travail.
- `autre` exige une valeur documentée absente du vocabulaire, le libellé source,
  une justification et une validation humaine. Trois occurrences distinctes
  déclenchent une revue du vocabulaire.
- `inconnu` exige qu'une question applicable ait été examinée sans réponse. Une
  source vide et une question non applicable restent `NULL` avec des statuts
  différents.
- Les classements des secteurs et de la situation actuelle restent identiques
  lorsque l'ordre des notices est inversé. La grille de qualité produit aussi
  une sortie identique lors d'une seconde exécution.
- Le test établit la reproductibilité technique. L'accord entre personnes devra
  être testé par double classement pendant le corpus pilote.
- Les 63 tests automatisés du projet réussissent après ajout des contrôles de
  qualité et de reproductibilité.
- Le schéma DuckDB passe en version `1.2.0`, le dictionnaire et le modèle en
  version 1.2, les règles du modèle en version 1.3 et le registre des
  classifications en version 0.4.
- Le troisième bloc de la phase 4 est terminé. Il reste à exécuter le bloc de
  validation finale avant de publier `classifications.yml` en version 1.0.

## 2026-07-21 — Clôture de la phase 4

- `config/classifications.yml` est publié en version `1.0` avec le statut
  `phase4_validee`.
- Le registre contient 163 codes répartis dans 17 vocabulaires contrôlés.
- Les 49 entrées principales qui exigent une définition explicite en possèdent
  toutes une. Le dictionnaire des données passe en version 1.3 et rassemble les
  définitions nécessaires à la lecture du registre.
- Les trois validateurs de secteurs, de situation actuelle et de qualité ne
  signalent aucune incohérence.
- Les tests de reproductibilité restent positifs : l'ordre des notices ne
  modifie ni les secteurs ni la situation actuelle, et la grille de qualité est
  stable lors d'une nouvelle exécution.
- Les empreintes SHA-256 du registre et des sorties de contrôle sont archivées
  dans `reports/quality/phase4_validation_finale.json`.
- Les 64 tests automatisés du projet réussissent après ajout du contrôle de
  publication V1.
- La reproductibilité humaine reste à mesurer par double classement pendant la
  phase 5 ; cette limite n'empêche pas l'utilisation du registre pour le pilote.
- La phase 4 est terminée. La phase 5 peut construire l'échantillon pilote avec
  les classifications V1.

## 2026-07-21 — Phase 5, composition de l'échantillon pilote

- Le pilote est un échantillon raisonné par quotas et non un tirage aléatoire.
  Il teste la variété des situations ; il ne mesure pas statistiquement le corpus.
- L'univers de départ est le corpus officiel de 319 dossiers de l'Inventaire du
  patrimoine industriel de l'Orne. CASIAS n'intervient pas dans la composition
  initiale et servira seulement à l'élargissement et au recoupement.
- L'unité de sélection est le dossier `IA` candidat. Les 30 références ne valent
  pas encore 30 sites canoniques avant rapprochement.
- Trente candidats sont retenus, avec cinq dossiers dans chacune des six
  macro-zones de contrôle.
- L'échantillon couvre huit secteurs, cinq périodes, six profils de conservation
  issus des sources, sept protections MH déjà identifiées et six localisations
  difficiles.
- Les états matériels anciens, l'absence apparente de protection et la difficulté
  de localisation restent des signaux provisoires à vérifier pendant
  l'enrichissement.
- La sélection structurée est enregistrée dans
  `config/echantillon_pilote.yml` et son contrôle dans
  `reports/quality/phase5_composition_echantillon.json`.
- Le bloc « Composer l'échantillon » est terminé. Le bloc suivant porte sur
  l'enrichissement et le rapprochement des 30 candidats.

## 2026-07-21 — Phase 5, enrichissement des sites pilotes

- Les 30 candidats reçoivent chacun un UUID v4 stable, distinct de leur
  référence `IA`.
- Les 43 dénominations `DENO` sont toutes classées après extension du registre ;
  la relecture des historiques porte le total à 47 phases d'activité.
- Le registre des classifications passe en version `1.1` avec 174 codes. Les
  ajouts couvrent notamment distillerie, faïencerie, fromagerie, tréfilage,
  habillement, chaussures et préparation du tan.
- Six rapprochements entre protection `PA` et dossier `IA` sont confirmés par un
  renvoi direct. Le cas `PA00110771` est rejeté pour `IA00060965`, car la source
  renvoie à `IA00060964`.
- La collection métallurgique de Varenne comprend 31 notices Palissy archivées.
  Son lien avec `IA00060965` reste candidat, avec une confiance faible.
- Quatre situations actuelles sont appuyées par des sources récentes. Pour les
  26 autres sites, `inconnu` est enregistré afin de ne pas actualiser
  artificiellement des observations anciennes.
- Trois notices POP contiennent le marqueur `$26` dans leur champ historique
  structuré ; leur chronologie est reprise du texte rendu et l'anomalie reste
  documentée.
- Le rapprochement CASIAS est différé à une extraction dédiée, car un appariement
  communal ne serait pas assez précis.
- Le bloc « Enrichir les sites » est terminé. La validation manuelle des fiches
  reste à réaliser dans le dernier bloc de la phase 5.

## 2026-07-22 — Phase 5, validation du corpus pilote

- Les 30 fiches sont contrôlées individuellement selon une grille commune.
- Les chronologies de `IA00061133` et `IA00061155` sont précisées : activités
  simultanées pour la laiterie-fromagerie, activités complémentaires pour la
  quincaillerie-tréfilerie.
- Le référentiel officiel des 381 communes actuelles de l'Orne est archivé. Les
  six communes nouvelles utilisées dans le pilote sont confirmées.
- L'audit de provenance couvre les 30 notices principales, les 30 communes
  actuelles, les 47 activités, les 6 protections, les 31 objets Palissy et les
  4 situations contemporaines renseignées.
- Le corpus pilote V1 candidat est produit dans
  `data/pilot/corpus_pilote_v1.json`. Sa structure passe tous les contrôles.
- Un classeur de double classement est préparé pour trois cas simples et trois
  cas ambigus. Il sépare les réponses des personnes A et B et calcule les accords.
- La phase 5 n'est pas marquée comme terminée : deux classements réellement
  indépendants et la documentation de leurs désaccords restent nécessaires.

## 2026-07-22 — Clôture de la phase 5

- La décision précédente faisant du double classement humain une condition de
  clôture est annulée. Ce contrôle est disproportionné au stade du pilote et ne
  vérifie pas l'exactitude historique des informations.
- Le protocole et les grilles déjà préparés sont conservés comme outils
  facultatifs. Aucun classement humain indépendant n'est déclaré comme réalisé.
- La conséquence acceptée est limitée : quelques catégories interprétatives
  pourraient être comprises différemment par un autre lecteur et être révisées.
  Les sources, les faits documentés, les identifiants et le modèle de données ne
  sont pas affectés.
- Un contrôle extérieur ne sera réexaminé que si des ambiguïtés récurrentes
  apparaissent ou si un partenaire demande une validation formelle.
- Les contrôles requis sont satisfaits : 30 fiches relues, provenance vérifiée,
  corpus pilote V1 produit et limites documentées. La phase 5 est terminée.

## 2026-07-22 — Phase 6, localisation

- Les 30 notices pilotes possèdent un point POP valide en Lambert-93 et WGS84 ;
  29 possèdent aussi une emprise documentaire exploitable.
- Ces géométries sont toutes qualifiées d'approximatives. Une coordonnée source
  valide n'est pas assimilée à un bâtiment ou à une emprise vérifiée.
- Sur sept adresses renseignées, quatre seulement ont un numéro unique. Trois
  géocodages BAN concordent avec le point POP ; le résultat de `IA00060969`,
  distant d'environ 1,2 kilomètre, est rejeté.
- L'intersection des points POP avec le Parcellaire Express renvoie une parcelle
  actuelle candidate pour les 30 sites. Seules six références concordent encore
  directement avec le cadastre cité dans la notice.
- Une parcelle actuelle candidate ne prouve ni l'emprise historique, ni la
  propriété, ni la conservation du site.
- Aucun centroïde communal ni aucune coordonnée de remplacement n'est créé. Le
  bloc « Localisation » de la phase 6 est terminé ; la phase reste en cours.

## 2026-07-22 — Phase 6, contexte territorial

- Les distances sont calculées pour les 30 sites à partir du point POP de
  travail. Elles restent des indices spatiaux sans valeur causale automatique.
- Dix-huit sites sont à moins de 100 mètres d'un tronçon hydrographique et 27 à
  moins de 500 mètres.
- Deux sites sont inclus dans une formation de la BD Forêt v2, 13 autres sont à
  moins de 100 mètres et 14 entre 100 et 500 mètres. Le millésime 2006-2019 est
  conservé avec chaque résultat.
- La lithologie simplifiée BRGM est renseignée pour les 30 sites. Vingt-trois
  ont un indice minier ou un gîte à moins de 10 km, sans que cela établisse un
  approvisionnement historique.
- Dix sites sont à moins de 500 mètres d'un tronçon ferroviaire de la BD TOPO ;
  14 n'en ont aucun dans le rayon testé de 5 km. La couche n'est pas présentée
  comme exhaustive pour les lignes disparues.
- La transformation des 30 points entre Lambert-93 et WGS84 est cohérente. Le
  Lambert-93 reste le système de calcul et le WGS84 celui de l'export web.
- Le bloc « Contexte territorial » est terminé. Le contrôle cartographique reste
  le prochain bloc de la phase 6.

## 2026-07-22 — Pistes éditoriales et passage au corpus complet

- Les résultats de contexte territorial du pilote sont conservés comme pistes
  de récit et de datavisualisation, pas comme conclusions sur tout le département.
- Les 30 sites constituent uniquement un pilote méthodologique non représentatif.
  Leurs proportions ne doivent pas être extrapolées.
- Après validation du socle V1, la méthode sera appliquée aux 319 dossiers du
  corpus source de l'Inventaire du patrimoine industriel de l'Orne.
- Le nombre final de sites pourra différer de 319 après rapprochement des
  notices, séparation des emprises, exclusions et traitement des cas ambigus.
- Les 2 052 entrées CASIAS ne sont pas ajoutées automatiquement au corpus :
  elles restent une source de recoupement et d'élargissement raisonné.
- Une phase dédiée au passage au corpus complet est ajoutée à la roadmap avant
  la construction de la publication interactive.
- Les interprétations liées à l'eau, la forêt, aux minerais et au rail devront
  être recalculées sur ce corpus complet et vérifiées historiquement.

## 2026-07-22 — Phase 6, contrôle cartographique

- Une carte QGIS à chemins relatifs superpose les 30 points POP, 29 emprises
  documentaires, 30 parcelles actuelles candidates et quatre résultats BAN.
- Aucun point grossièrement aberrant n'est détecté : tous restent dans
  l'enveloppe de l'Orne, les transformations de coordonnées sont cohérentes,
  les communes concordent avec les parcelles et aucun quasi-doublon à moins de
  50 mètres n'apparaît.
- Neuf cas sensibles ont été relus et disposent d'une décision explicite : une
  emprise absente, une très petite, deux très grandes, un point situé à 11,7
  mètres de son contour, trois adresses non uniques et un résultat BAN rejeté.
- Les seuils de surface et de distance déclenchent une relecture ; ils ne
  définissent pas une emprise industrielle correcte.
- Aucun point n'est déplacé. Les 30 localisations restent approximatives et les
  parcelles actuelles restent de simples candidates.
- Le premier fichier QGIS écrit manuellement ne résolvait pas les couches dans
  QGIS et a été remplacé. Le projet est désormais généré puis relu avec l'API de
  QGIS 3.44.12 : les cinq couches, leurs effectifs, le CRS Lambert-93 et le fond
  OpenStreetMap sont validés par QGIS lui-même.
- Un aperçu de contrôle et un rapport JSON de validation sont conservés avec le
  projet afin d'éviter qu'une validation seulement syntaxique soit répétée.
- Le bloc « Contrôle cartographique » est terminé. Le dernier bloc de validation
  de la phase 6 peut commencer.

## 2026-07-22 — Validation finale de la phase 6

- Les règles de précision géographique passent en version 1.0. La présence de
  coordonnées, d'un contour ou d'une parcelle candidate ne suffit jamais à
  qualifier une géométrie de vérifiée.
- Les 30 points POP restent `point_approximatif` et les 29 contours restent
  `zone_documentaire`. Les trois points BAN acceptés et les 30 parcelles
  candidates restent des géométries secondaires de contrôle.
- Aucune géométrie n'est qualifiée de vérifiée et aucune coordonnée n'a été
  inventée ou déplacée.
- Les 30 points sont valides et cohérents entre Lambert-93 et WGS84. Aucun point
  grossièrement aberrant n'a été détecté.
- L'intitulé cartographique « Sites sensibles », trop ambigu, est remplacé par
  « Localisations à vérifier ». Il décrit une incertitude de localisation, pas
  un danger, une pollution ou une fragilité patrimoniale.
- Le bilan de qualité spatiale autorise le passage à la phase 7. Cette décision
  valide la méthode sur le pilote, pas la précision complète des 319 dossiers.
- La phase 6 est terminée.

## 2026-07-22 — Phase 7, consolidation du socle pilote V1

- Le corpus de phase 5 et les résultats géographiques validés en phase 6 sont
  réunis dans un corpus pilote consolidé reproductible.
- DuckDB devient le format de référence du socle. Il conserve les relations
  détaillées entre les 30 sites, 47 activités, 59 géométries, 31 objets
  techniques et 148 mentions de sources.
- CSV, Parquet et GeoJSON sont des vues aplaties à raison d'une ligne ou d'une
  entité par site. Ils ne remplacent pas le modèle relationnel pour l'édition.
- Les quatre formats contiennent les mêmes 30 identifiants de sites. Les
  validations de la base et les 99 tests automatisés réussissent.
- Les localisations restent prudentes : 30 points approximatifs, 29 emprises
  documentaires et aucune géométrie déclarée vérifiée.
- Les 30 fiches passent au statut technique `cartographiable`, mais aucune
  décision de publication n'est prise à ce stade.
- Les fichiers de données produits restent locaux et non versionnés ; leur
  construction, leur rapport de contrôle et leurs empreintes sont
  reproductibles.
- Le bloc « Consolider les données » de la phase 7 est terminé. La phase 7
  reste en cours jusqu'à la consolidation documentaire et à l'approbation du
  socle V1.

## 2026-07-22 — Correctif chronologique du socle V1

- Le bloc de consolidation est rouvert après constat que les périodes définies
  en phase 4 n'étaient pas présentes dans les exports de phase 7.
- L'écart provient d'un critère de validation incomplet : les formats,
  identifiants et effectifs étaient contrôlés, mais pas la possibilité de
  filtrer effectivement le livrable par période.
- Les identifiants, la géographie et les traitements antérieurs restent
  inchangés. La correction est additive et utilise les traitements existants.
- Trente phases d'activité disposent maintenant de bornes normalisées depuis
  une chronologie explicite. Dix-sept phases sans bornes utilisent le champ POP
  `SCLE` comme repérage, avec une méthode distincte et visible.
- Les 30 sites et les 47 phases d'activité possèdent au moins une période
  filtrable. Aucune date exacte n'est créée à partir d'une expression
  imprécise.
- Le CSV des sites sépare les périodes d'activité et les périodes issues de
  `SCLE`. Un CSV distinct fournit une ligne par phase d'activité.
- DuckDB contient une relation normalisée `activites_periodes_v1` destinée aux
  croisements entre périodes, secteurs et productions.
- La période contemporaine est ajoutée au niveau du site pour les quatre
  situations actuelles appuyées par une source récente. Elle n'est pas
  attribuée automatiquement à une activité précise lorsque plusieurs
  productions historiques coexistent.
- Le code d'usage provisoire `industrie_actuelle` est corrigé en
  `activite_industrielle`, qui est la valeur du vocabulaire contrôlé.
- Un contrôle fonctionnel du filtrage par période est ajouté aux validations
  finales pour empêcher la réapparition de cet écart.

## 2026-07-22 — Phase 7, consolidation de la documentation

- Le dictionnaire passe en version 1.5 et décrit le socle relationnel ainsi que
  les exports complémentaires des sites et des phases d'activité.
- `config/sources.yml` version 1.1 devient le registre opérationnel canonique.
  Il contient 21 sources avec licence des données, statut des médias,
  attribution et lien vers les conditions ; le CSV de phase 1 reste une trace
  historique de l'audit.
- Les quatre observations contemporaines sont désormais rattachées à leur
  producteur réel : EDF, Bohin, Archives de l'Orne et Département de l'Orne.
- Le registre des classifications passe en version 1.2 avec 177 codes. Les
  trois méthodes de calcul des périodes sont publiées sans modifier le
  découpage chronologique validé en phase 4.
- Le rapport de qualité conclut que le pilote est cohérent pour une
  démonstration interne et la conception d'un prototype, mais ni exhaustif ni
  publiable sans relecture éditoriale.
- Huit familles d'anomalies ou de limites restent visibles. Elles ne bloquent
  pas la poursuite méthodologique, mais interdisent certains énoncés trop
  affirmatifs sur l'état actuel, la localisation, CASIAS et les objets Palissy.
- Aucune photographie tierce n'est intégrée au socle. Toute future image devra
  disposer d'un auteur, d'un détenteur de droits, d'une licence ou autorisation,
  d'un crédit et d'une preuve avant publication.
- Les 106 tests automatisés réussissent. Le bloc « Consolider la
  documentation » est terminé ; la phase 7 reste en cours.

## 2026-07-22 — Phase 7, préparation de la suite

- Une première carte autonome de contrôle interne présente les 30 sites par
  secteur et rend visibles les 9 localisations à vérifier. Elle ne dépend pas
  d'un serveur de tuiles et affiche ses limites directement dans le visuel.
- Le portail officiel confirme 319 dossiers sur 16 pages. La récupération POP
  est validée sur 30 notices, mais l'énumération complète, la reprise par lots
  et la file de revue humaine doivent encore être généralisées.
- La phase 8 commencera par la liste contrôlée des 319 références puis un lot
  de 50 dossiers. Les autres dossiers seront traités par paquets comparables.
- La charge du corpus technique est estimée entre 180 et 300 heures. Un lot
  éditorial récent et iconographique de 30 à 50 sites porte le scénario de
  première publication entre 260 et 420 heures. Ces fourchettes seront
  recalculées à partir du temps observé sur le premier lot.
- Les récits immédiatement prototypables portent sur la révélation de la
  géographie industrielle, les vies successives des sites, la chronologie et
  l'eau comme indice. Les statistiques départementales, l'état actuel global
  et les causalités environnementales restent reportés.
- La recommandation est une publication statique narrative et cartographique,
  alimentée par DuckDB et des exports web. Une infrastructure serveur n'est pas
  justifiée pour le MVP.
- Décisions : `GO` pour la phase 8 par lots et `GO LIMITÉ` pour un prototype
  applicatif après le premier lot de 50. Le bloc « Préparer la suite » est
  terminé ; la phase 7 reste ouverte jusqu'à la décision finale de socle.

## 2026-07-22 — Approbation du socle V1 et clôture de la phase 7

- Décision formelle : **`GO` pour la phase 8, par lots**.
- Le socle V1 est approuvé comme base méthodologique, documentaire et
  technique. Cette approbation porte sur la chaîne et ses règles, pas sur
  l'exhaustivité des 30 sites pilotes.
- La phase 8 commencera par l'énumération contrôlée des 319 références `IA`,
  puis par un premier lot de 50 dossiers non pilotes.
- Les temps de revue, erreurs, variantes et cas bloqués de ce lot serviront à
  recalibrer la charge et à corriger la chaîne avant les lots suivants.
- Le nombre final de sites reste inconnu jusqu'aux rapprochements, séparations
  d'emprises et exclusions documentées.
- Les limites relatives aux situations actuelles, localisations, objets
  Palissy, CASIAS et droits des images restent en vigueur.
- Le socle pilote V1 est approuvé et la phase 7 est terminée.

## 2026-07-22 — Phase 8, énumération et premier lot

- Le bloc « Constituer le corpus » est exécuté par lots : les cases globales
  restent ouvertes jusqu'au traitement des 319 dossiers.
- La déduction par plage numérique est abandonnée parce qu'elle ne reproduit
  pas le corpus actuel. L'énumération utilise la recherche avancée de l'API POP
  sur le cadre d'étude exact.
- La recherche renvoie 320 notices. `IA61000851` est exclue comme notice de
  présentation ; les 319 autres références concordent avec le total officiel.
- Le dossier collectif `IA61001399` est maintenu. Il sera décomposé en emprises
  pendant la revue et ne doit pas être interprété comme un site unique.
- L'API JSON de POP devient l'accès principal pour les nouveaux lots. Le HTML
  Next.js reste le repli testé.
- Le registre des sources passe en version 1.2 et les règles d'extraction en
  version 1.1 pour consigner ce changement d'accès.
- Le lot 1 contient 50 dossiers non pilotes répartis sur la liste des
  références. Les 50 JSON bruts sont archivés et les 50 `REF` concordent.
- Onze termes sources complètent les correspondances exactes. Quatre activités
  et une installation sont ajoutées ; les classifications passent en version
  1.3 avec 182 codes publiés.
- Les 62 dénominations du lot sont classées. Quatre dossiers multi-secteurs ont
  été relus et conservés comme quatre sites à activités successives.
- Le lot 1 contient donc 50 sites provisoires. Le nombre canonique du corpus
  principal reste inconnu jusqu'à la revue de tous les lots.

## 2026-07-23 — Réunion des 30 pilotes et des 50 dossiers du lot 1

- Les deux ensembles sont projetés dans un corpus intermédiaire commun de 80
  dossiers. Le dossier `IA` est l'unité de cette étape, pas le site canonique.
- La structure commune conserve les enrichissements des 30 pilotes. Les champs
  encore absents des 50 nouveaux dossiers restent nuls ou explicitement
  inconnus ; aucune information n'est inventée pour uniformiser artificiellement
  les deux ensembles.
- Les 30 `site_id` existants sont conservés. Aucun `site_id` n'est attribué aux
  50 nouveaux dossiers avant le traitement des 319 dossiers.
- Les 80 références et les 80 URLs sont uniques. Les 109 activités possèdent
  toutes une activité et un secteur contrôlés.
- Le contrôle par référence, URL, commune-adresse, commune-lieu-dit et proximité
  des points ne propose aucun rapprochement parmi les 80 dossiers.
- Le résultat reste intermédiaire : 80 sites provisoires de travail, sans total
  canonique départemental.

## 2026-07-23 — Intégration des références officielles restantes

- Le calcul initial de 239 dossiers restants est corrigé : `IA00061060`, bien
  que présent dans les 30 pilotes, n'appartient pas à l'énumération officielle
  actuelle. Le corpus de 80 ne couvrait donc que 79 des 319 références.
- `IA00061060` reste conservé dans le pilote enrichi mais hors du corpus
  principal. Les 240 références officielles réellement restantes ont été
  récupérées pour obtenir exactement 319 dossiers officiels.
- L'extraction est reprenable : le manifeste est réécrit après chaque notice
  réussie. Une interruption ne force plus à recommencer les téléchargements.
- Les 319 dossiers sont harmonisés dans un format commun. Ils représentent des
  dossiers sources, pas encore le nombre définitif de sites.
- Le registre des classifications passe en version 1.4. Les 407 dénominations
  du corpus sont toutes résolues ; 8 occurrences non productives sont
  conservées comme composants et non transformées en activités.
- Le contrôle signale 7 paires à examiner pour un rapprochement, le dossier
  collectif `IA61001399` à décomposer, 4 cités ouvrières à relier sans fusion
  et 2 moulins dont la production doit être précisée.
- Aucune fusion, séparation ou relation n'est décidée automatiquement. Le
  nombre de sites canoniques reste inconnu jusqu'à cette revue.

## 2026-07-23 — Revue canonique et décompte des sites

- Les sept paires proposées automatiquement ont été relues depuis les
  historiques, adresses, exploitants et emprises. Elles correspondent toutes à
  des sites distincts ; aucune fusion n'est appliquée.
- `IA61001399` est requalifié comme dossier de synthèse sans emprise. Ses
  quinze dossiers individuels de fromageries sont déjà présents. La synthèse
  reste une source mais sort du décompte des sites.
- Le corpus principal passe donc de 319 dossiers sources à **318 sites
  canoniques**.
- Les quatre cités ouvrières restent quatre sites distincts. Deux sont reliées
  comme composants de la mine de Halouze et deux comme dépendances de la mine
  de La Ferrière-aux-Étangs.
- La fenderie de Larchamp reste distincte de l'affinerie-moulin, avec une
  relation de dépendance documentée.
- Les deux activités génériques `moulin` sont remplacées par les productions
  décrites dans les historiques : mouture, scierie, foulage, préparation du
  tan et production hydroélectrique.
- Les 318 sites reçoivent un UUID v4 stable. Les 29 identifiants déjà attribués
  aux pilotes officiels sont conservés sans modification.
- Ce total de 318 porte sur le corpus principal de l'Inventaire. De nouveaux
  sites pourront encore être ajoutés par d'autres sources, notamment CASIAS ou
  les archives, après vérification.

## 2026-07-23 — Enrichissement et localisation des 318 sites

- L'ancienne API data.culture testée en phase 2 n'est plus utilisable à son
  ancienne adresse. L'extraction départementale passe par la recherche avancée
  actuelle de POP ; les réponses brutes restent archivées.
- Une protection MH est confirmée uniquement quand la notice `PA` cite la
  référence `IA`. Cette règle confirme 16 protections sur 16 sites.
- Les 31 objets Palissy des forges de Varenne sont conservés comme associations
  documentaires à vérifier. Aucun nouvel objet n'est attaché par commune.
- CASIAS ne modifie pas le total canonique. Sur 2 052 entrées, 131 recoupements
  sont retenus pour 123 sites. Après revue de 62 cas limites, 44 sont
  confirmés, 10 rejetés et 8 restent ambigus.
- Les 170 candidats d'élargissement CASIAS restent hors corpus jusqu'à une
  vérification patrimoniale.
- Les 318 sites possèdent un point source valide ; 290 restent des points
  approximatifs et 28 disposent d'une zone documentaire qualifiée.
- Le contexte territorial est calculé par tuiles IGN et par enveloppe BRGM. Les
  proximités sont publiables comme indices, jamais comme causes historiques
  prouvées.

## 2026-07-24 — Validation du corpus complet V1 et clôture de la phase 8

- Le corpus complet V1 est validé avec 318 sites canoniques et 403 activités.
- Les exports JSON, DuckDB, CSV, Parquet et GeoJSON possèdent des effectifs et
  identifiants concordants.
- Les répartitions sectorielles sont multi-appartenances : elles ne doivent pas
  être additionnées pour retrouver le total du corpus.
- Les 318 sites possèdent une période documentaire, mais seules 42 activités
  sur 403 disposent d'une période calculée depuis une chronologie d'activité.
  Les deux mesures restent séparées dans les exports.
- La situation actuelle est insuffisamment couverte : 315 conservations et 316
  accessibilités restent inconnues. Le corpus n'est donc pas présenté comme un
  guide de visite départemental.
- Les 290 points approximatifs restent publiables à l'échelle départementale
  avec un niveau de précision visible et un zoom adapté.
- Les 31 liens Palissy, 8 rapprochements CASIAS ambigus et 170 candidats CASIAS
  d'élargissement restent documentés sans être transformés en certitudes.
- Les limites restantes sont jugées non bloquantes pour une première
  publication historique et cartographique.
- Décision : **phase 8 terminée ; passage possible à la phase 9**.

## 2026-07-24 — Cadrage des données éditoriales

- Les textes sont séparés en trois niveaux : source patrimoniale immuable,
  résumé documentaire dérivé et texte journalistique.
- Les résumés conservent leurs sources et passent par une validation humaine ;
  les textes journalistiques conservent leur auteur et leur statut éditorial.
- La table `recits_sites` portera une ligne par site et conservera ensemble les
  textes sources, les repères documentaires et les champs de travail éditorial.
- La table `medias` portera les métadonnées, crédits, décisions de sélection,
  statuts de droits, demandes d'autorisation et usages permis.
- La sélection d'un média et son droit de publication restent deux décisions
  distinctes.
- Le prototype interne pourra utiliser les données et les textes sourcés ainsi
  que les métadonnées et aperçus distants crédités, dans un espace privé. Cette
  possibilité n'autorise aucune diffusion publique.
- Les textes sources ne seront pas saisis manuellement dans les tables
  éditoriales. Ils seront reconstruits depuis le corpus et contrôlés par
  empreinte SHA-256 ; un texte dérivé ne pourra jamais les remplacer.
- Décision : **bloc 1 de la phase 9 validé ; aucune extraction de média ni
  régénération des exports n'est encore engagée**.

## 2026-07-24 — Réintégration de la matière historique

- La matière historique est placée dans une table dédiée `recits_sites`, sans
  alourdir la table cartographique `sites`.
- Les 318 sites possèdent chacun une ligne éditoriale et les identifiants
  concordent exactement avec le corpus complet.
- 314 historiques sont renseignés et 4 sont explicitement absents de la
  source.
- 257 descriptions sont renseignées et 61 sont explicitement absentes de la
  source.
- 256 sites possèdent les deux textes ; 3 ne possèdent ni historique ni
  description.
- Les textes sont copiés sans réécriture et contrôlés par empreinte SHA-256.
- Les siècles, périodes documentaires, périodes d'activité, activités
  successives et références de sources sont conservés.
- Les champs de résumé documentaire et de texte journalistique restent vides
  et portent leurs statuts initiaux ; aucun texte n'a été généré à ce stade.
- Décision : **bloc 2 de la phase 9 validé**.

## 2026-07-24 — Inventaire des médias

- 1 900 relations média-site sont inventoriées pour 316 sites sur 318.
- Deux notices ne présentent aucun média exploitable : `IA00061048` et
  `IA00061085`.
- 1 888 références médias distinctes sont conservées. Huit références sont
  reliées à plusieurs sites ; ces relations ne sont pas supprimées.
- Aucun doublon technique strictement identique n'a été trouvé.
- 1 783 médias possèdent une légende, un crédit et une mention de droits dans
  les métadonnées JSON archivées ; aucun auteur individuel n'y est renseigné.
- 117 médias proviennent d'archives HTML de POP : référence et URL sont
  conservées, mais aucun crédit, auteur ou légende n'est inventé.
- Les 282 marqueurs d'image principale sont conservés lorsqu'ils existent.
- Les droits restent `inconnus` et les usages `metadonnees_seulement` jusqu'au
  bloc de qualification dédié.
- Décision : **bloc 3 de la phase 9 validé ; aucun fichier image n'est
  téléchargé ou versionné**.

## 2026-07-24 — Qualification des droits et usages des médias

- Les usages sont séparés en trois niveaux : consultation interne,
  prototype privé et publication publique.
- Les 1 900 relations média-site reçoivent toutes le statut d'autorisation
  `a_demander` : aucun droit de publication n'est déduit des métadonnées POP.
- 1 783 médias avec crédit source sont classés `protege` et
  `prototype_prive` ; 117 sans crédit exploitable sont classés `inconnus` et
  `reference_interne`.
- Aucun média n'est classé `publication_autorisee`.
- Le registre contient 1 888 lignes, une par média distinct ; il prépare la
  trace des demandes et réponses mais n'envoie aucun courriel.
- Les crédits bruts sont conservés ; les 117 crédits manquants sont marqués à
  compléter. Aucun fichier image n'est téléchargé ou versionné.
- Décision : **bloc 4 de la phase 9 validé ; publication publique bloquée tant
  qu'une licence ou autorisation documentée n'est pas renseignée**.

## 2026-07-24 — Préparation de la sélection éditoriale

- La revue éditoriale mesure la couverture documentaire disponible et ne
  mesure pas la valeur patrimoniale ou journalistique des sites.
- Les 318 sites possèdent un repère chronologique ; 268 ont une couverture
  historique forte, 47 moyenne et 3 faible selon les textes et repères sources.
- La couverture iconographique est forte pour 286 sites, moyenne pour 1,
  faible pour 29 et absente pour 2.
- 284 sites combinent une matière historique au moins moyenne, une chronologie
  et un média avec crédit à examiner ; 287 candidats d'image principale sont
  proposés au statut `a_revoir`.
- 4 sites demandent une recherche historique, 31 une recherche visuelle et 35
  une recherche complémentaire au total.
- Tous les sites restent au statut `a_examiner` ; aucun récit ni média n'est
  sélectionné automatiquement.
- Décision : **bloc 5 de la phase 9 validé**.

## 2026-07-25 — Validation du socle narratif et visuel V1

- Les 318 sites concordent entre le corpus, `recits_sites`, `medias` et la
  revue éditoriale.
- Les 314 historiques et 257 descriptions présents dans le corpus sont tous
  conservés dans l'export éditorial, avec leur empreinte de contrôle.
- Les 1 900 relations média-site possèdent une provenance et un statut de
  droits ; aucune n'est publiable automatiquement.
- Les 318 sites restent `a_examiner` : aucun récit ou média n'est retenu par
  le calcul.
- Le socle narratif et visuel V1 est approuvé comme base de conception de la
  publication interactive.
- Décision : **phase 9 terminée ; passage possible à la phase 10**.

## 2026-07-26 — Phase 10, cadrage éditorial et produit

- La première publication est définie comme une expérience statique de
  datajournalisme associant un récit visuel et une exploration libre du même
  corpus.
- L'accueil recommande le data storytelling, mais donne immédiatement accès à
  la carte exploratoire et à la recherche. Le récit ne constitue pas un
  parcours obligatoire.
- Le récit est prévu sur une page continue composée de chapitres identifiables
  et partageables. L'exploration, les fiches et la méthode disposent de leurs
  propres espaces.
- Le public principal est un lecteur curieux sans connaissance préalable. Les
  habitants et passionnés locaux ainsi que les lecteurs experts sont servis par
  des niveaux de détail progressifs, sans créer plusieurs produits.
- La promesse est de faire apparaître la géographie industrielle documentée de
  l'Orne, de montrer les transformations de certains lieux et de permettre
  l'exploration des sites, des sources et des incertitudes.
- La datavisualisation doit révéler la géographie du corpus, comparer les
  activités documentées, suivre des trajectoires multi-activités et représenter
  les incertitudes. Elle ne doit produire ni classement départemental
  exhaustif, ni causalité automatique, ni bilan artificiel de l'état actuel.
- Les proximités à l'eau, à la forêt, aux minerais et au rail restent des
  indices spatiaux et des supports d'études de cas.
- La chronologie distingue les périodes documentaires disponibles pour les 318
  sites des périodes d'activité datées, disponibles pour seulement 29 sites et
  42 activités.
- Le MVP comprend quatre espaces : accueil-récit, exploration, fiches de sites
  et méthode. Il reste statique et ne comporte ni serveur, ni CMS, ni comptes,
  ni administration en ligne.
- Les 318 sites disposent d'une fiche documentaire structurée ; 30 à 50 fiches
  sont enrichies après revue éditoriale humaine et peuvent alimenter le récit.
- Les quatre filtres initiaux sont l'activité ou le secteur, la période, la
  commune ou recherche textuelle et la précision géographique.
- La diffusion est progressive : prototype privé, version candidate relue,
  puis première version publique. L'interface fonctionne sans photographie et
  aucun média n'est publié sans sélection, crédit et droit documentés.
- Le cadrage consolidé est conservé dans
  `docs/phase10_cadrage_editorial_ux.md`.
- Décision : **bloc 1 de la phase 10 terminé ; le parcours narratif et le data
  storytelling peuvent être conçus dans le bloc 2**.

## 2026-07-26 — Rectification du cadrage éditorial de la phase 10

- L'adresse éditoriale n'est plus formulée à partir d'un public principal ou de
  personas. Le projet est un sujet documentaire, datajournalistique,
  interactif et publié en ligne, destiné aux personnes intéressées par le sujet
  et par sa forme.
- L'intention première est journalistique : exactitude des informations,
  intérêt de l'enquête, articulation entre données, sources, images, cartes et
  récit.
- Les quatre usages déjà définis sont conservés, mais ils décrivent les
  possibilités offertes par le sujet et non des segments de public.
- La phase 10 vise directement une forme complète avec photographies, documents
  visuels et datavisualisations. Elle ne planifie pas une version éditoriale
  appauvrie sans images.
- Le cadrage part de l'hypothèse de travail que les autorisations nécessaires
  seront obtenues pour les images retenues. Les crédits et preuves restent
  suivis conformément au modèle éditorial de phase 9.
- Il n'existe pas de catalogue autonome des 318 sites. Tous les sites sont
  sélectionnables dans l'exploration et apparaissent dans un panneau de détail
  lié à la carte, à la recherche ou à une visualisation.
- Trente à cinquante cas peuvent recevoir un portrait éditorial plus ample,
  articulant récit journalistique, images, chronologie, carte, données et
  sources.
- Les éventuels prototypes intermédiaires sont des outils de conception de la
  forme finale et non des niveaux de publication distincts.
- Cette rectification remplace les décisions du cadrage initial concernant le
  public principal, la diffusion progressive sans images et les 318 fiches
  documentaires conçues comme pages autonomes.

## 2026-07-27 — Phase 10, parcours narratif et data storytelling

- Le parcours narratif comprend un prologue, cinq chapitres et une conclusion
  méthodologique : révélation de la géographie, diversité des productions, eau,
  transformations successives, réseaux extérieurs, traces actuelles et
  construction de l'enquête.
- La démonstration repose sur sept familles de visualisations : carte de
  révélation, secteurs, eau, trajectoires multi-activités, flux documentés,
  connaissances contemporaines et constitution du corpus.
- Les vues globales décrivent uniquement les 318 sites du corpus de
  l'Inventaire. Les relations historiques et causalités éventuelles sont
  racontées par des études de cas sourcées.
- Une chronologie animée des 403 activités est écartée : seules 42 activités
  et 29 sites disposent d'une période d'activité suffisamment datée. Les
  chronologies restent attachées aux cas documentés.
- Douze études de cas principales sont retenues après lecture humaine :
  Putanges-Pont-Écrepin, Brochard, Bohin, Rabodanges, Ozé-Moulinex,
  Sainte-Gauburge, Sées, l'usine à papier Abadie, la chocolaterie de Tinchebray,
  l'usine de flaconnage de Saint-Evroult, la Grosse Forge d'Aube et la mine de
  Halouze.
- Six cas complémentaires sont conservés en réserve pour la cohérence
  iconographique, géographique ou sectorielle.
- Le chapitre sur l'eau distingue les distances calculées sur tout le corpus
  des relations fonctionnelles établies dans les historiques de sites.
- Le chapitre sur les réseaux extérieurs utilise uniquement des flux
  documentés : papier, chocolat, flaconnage, appareils de levage et imprimés.
- Le chapitre sur la situation actuelle montre d'abord la lacune documentaire :
  quatre situations récentes seulement, sans produire de bilan départemental.
- Le récit reste non linéaire : chaque chapitre peut rejoindre l'exploration,
  un panneau de site, un portrait ou la méthode, puis revenir à son état
  précédent.
- Chaque visualisation dispose d'une alternative textuelle ou tabulaire et
  aucune information n'est accessible uniquement au survol.
- Le storyboard détaillé est conservé dans
  `docs/phase10_parcours_narratif_datastorytelling.md`.
- Décision : **bloc 2 de la phase 10 terminé ; la direction artistique et le
  modèle visuel peuvent être conçus dans le bloc 3**.

## 2026-07-27 — Phase 10, proposition de direction artistique

- Le benchmark est limité à cinq références et à des mécanismes précis :
  essai visuel, récit cartographique, scrollytelling accessible, relation
  lieu-image-récit et exploration d'un patrimoine industriel. Aucun gabarit
  existant n'est repris comme modèle complet.
- Trois directions ont été comparées : `Atlas industriel vivant`, `Dossier
  d'atelier` et `Paysage productif`.
- `Atlas industriel vivant` est la direction recommandée. Elle associe un fond
  papier chaud, une encre sombre, un accent oxyde, une grille contemporaine et
  une hiérarchie donnant une place équivalente aux données, aux cartes, aux
  textes et aux images.
- Le trio typographique proposé est Newsreader pour les titres, IBM Plex Sans
  pour le texte et l'interface, et IBM Plex Mono pour les données, sources et
  identifiants.
- La carte générale ne doit pas attribuer un secteur principal artificiel à
  chaque site. Les correspondances sectorielles apparaissent au moment du
  filtrage ; les sites multi-secteurs restent sélectionnables par chacune de
  leurs activités.
- La précision et l'incertitude combinent forme, motif et libellé. La couleur
  seule ne porte jamais l'information.
- Les images ne reçoivent ni sépia automatique ni colorisation. Les crédits et
  légendes restent visibles sous les médias ; les maquettes utilisent des
  emplacements de travail et ne constituent pas une sélection de publication.
- Trois écrans ont été matérialisés : accueil, exploration en trois zones et
  portrait enrichi de l'usine à papier Abadie. Ils sont conservés dans
  `docs/design/phase10/`.
- Le système visuel est volontairement limité aux quinze éléments nécessaires
  à ces écrans et au storyboard ; aucun composant générique spéculatif n'est
  ajouté.
- La proposition complète est conservée dans
  `docs/phase10_direction_artistique.md`.
- Décision provisoire : **le bloc 3 reste en cours jusqu'à l'arbitrage de la
  direction recommandée et des trois écrans ; aucun développement d'interface
  n'est engagé**.

## 2026-07-27 — Phase 10, rejet de l'atlas et retour à l'angle initial

- La direction `Atlas industriel vivant` est rejetée. Elle est jugée froide,
  stéréotypée, trop proche d'un dossier institutionnel ou d'un catalogue et
  insuffisamment datajournalistique.
- Les silhouettes d'usines, le fond papier, l'oxyde et la grille technique
  traduisaient le mot « industriel » au lieu de traduire l'enquête.
- Le titre de travail « L'Orne industrielle » est abandonné. Il déplaçait le
  sujet vers une présentation générale du département industriel et effaçait
  l'idée d'un patrimoine oublié derrière l'image rurale actuelle.
- Le cadrage initial contenait déjà la bonne tension : partir des paysages
  ruraux, puis révéler la couche industrielle. La dérive se situait dans le
  titre, l'ouverture du storyboard et leur traduction visuelle.
- Le récit est rectifié sans opposer artificiellement ruralité et industrie :
  l'image rurale est réelle mais incomplète ; les activités industrielles,
  agricoles, les ressources, les bourgs et les paysages se superposaient.
- En l'absence de comparaison avec d'autres départements, la publication ne
  qualifiera pas encore l'Orne de territoire à concentration industrielle
  supérieure. Elle montrera le nombre, la diversité et la répartition des
  sites du corpus.
- La version 0.5 du cadrage remplace l'accroche « Faire apparaître l'Orne
  industrielle » par « Révéler l'autre Orne ». La version 1.1 du parcours
  déplace le passage technique de 319 dossiers à 318 sites vers la conclusion
  méthodologique.
- Une nouvelle direction `Paysage révélé` est proposée. Elle organise
  l'ouverture selon la séquence paysage actuel → question → données → carte
  réelle → étude de cas.
- `L'autre Orne — sur les traces d'un patrimoine industriel oublié` est un
  titre de travail destiné aux maquettes, pas une décision définitive.
- Les nouvelles cartes utilisent le contour réel de l'Orne et les 318
  localisations du corpus. L'exploration place la carte avant l'interface et
  n'affiche un panneau de site qu'après sélection.
- Les maquettes utilisent une photographie réelle des méandres de l'Orne et la
  vue aérienne Abadie `IVR25_19886100649X`, avec crédits visibles. Elles ne
  valent pas sélection définitive pour publication.
- La première proposition est archivée et reste exclue de toute base de
  développement.
- Décision provisoire : **le bloc 3 reste en cours ; la direction `Paysage
  révélé`, son titre de travail et ses trois écrans doivent être arbitrés avant
  toute conception technique de l'interface**.

## 2026-07-27 — Phase 10, seconde revue de la direction visuelle

- La direction `Paysage révélé` n'est pas validée. L'accueil est jugé plus
  engageant dans sa composition, mais l'ensemble reste trop abstrait et
  s'éloigne encore de la vision du projet.
- Le titre `L'autre Orne` est rejeté. Il n'a jamais été formulé par l'auteur du
  projet. Le travail de titre devra repartir de l'idée initiale de
  **patrimoine industriel oublié**.
- La silhouette départementale avec points est rejetée comme modèle de carte,
  sur l'accueil comme dans l'exploration. Elle porte les 318 coordonnées du
  corpus, mais ne montre ni rivières, ni végétation, ni bourgs, ni rail et ne
  constitue donc pas la carte vivante attendue.
- Le contrôle contre les 381 contours communaux actuels trouve 317 points dans
  un contour et un point source de la centrale hydroélectrique de
  Saint-Philbert-sur-Orne à environ 1,9 m de la limite communale. Les marqueurs
  larges et le contour simplifié de la maquette amplifient visuellement les
  débordements. La future carte devra rendre la précision approximative
  explicite et conserver ce cas de bord au contrôle.
- Le panneau contextuel de l'exploration est retenu comme base de travail. Il
  pourra réunir activités successives, dates disponibles, explication courte,
  précision, sources et éventuellement une image éditorialement sélectionnée.
- Le libellé et la rubrique `Les lieux` ne sont pas validés. Les portraits ne
  formeront pas une section autonome par défaut : chaque cas long devra répondre
  à une question précise du récit.
- La photographie Abadie peut documenter la coexistence d'une usine, d'un bourg,
  de champs et d'une rivière, mais l'image ne définit pas à elle seule la
  démonstration. Son usage doit être rattaché à une question éditoriale et, si
  une comparaison avec aujourd'hui est envisagée, à une source contemporaine.
- La validation d'un écran d'exploration a été anticipée dans le bloc 3 alors
  que le fond géographique, les couches, les échelles et les interactions
  appartiennent au cadrage du bloc 4. Aucune nouvelle maquette ne sera produite
  avant cet arbitrage fonctionnel.

## 2026-07-27 — Phase 10, troisième proposition visuelle

- Rectification : la demande précédente n'était pas de supprimer `Les lieux`,
  mais d'en expliquer l'utilité. La rubrique est conservée comme base de
  travail et ne vaut toujours pas catalogue des 318 sites.
- Sa fonction proposée associe trois lectures : inscription spatiale sur une
  photographie annotée, évolution historique documentée et situation actuelle.
- Activité, conservation matérielle, usage actuel, accessibilité et précision
  géographique restent des dimensions distinctes. Une cessation d'activité ne
  permet pas de déduire la conservation du bâti ou son usage présent.
- Le cas Abadie matérialise cette règle : la cessation vers 1978 est
  documentée ; conservation, usage actuel et accessibilité sont indiqués comme
  inconnus dans le corpus.
- La carte des nouvelles maquettes utilise les 318 localisations et les couches
  géographiques locales disponibles : limites communales, cours d'eau, forêts,
  rail actuel et principaux bourgs. Elle remplace la silhouette schématique
  rejetée, sans préjuger des choix fonctionnels détaillés du bloc 4.
- Le panneau de l'usine d'Ozé montre une photographie, trois phases d'activité,
  les dates disponibles, la précision `zone documentaire`, les sources et
  l'absence de situation récente documentée.
- Trois écrans sont produits dans `docs/design/phase10/` : accueil `07`,
  exploration `08` et `Les lieux` `09`.
- Décision provisoire : **cette troisième proposition constitue une base
  d'arbitrage, pas une direction artistique implicitement validée**.

## 2026-07-27 — Phase 10, validation de la direction artistique

- La troisième proposition est explicitement validée comme **bon point de
  départ** et devient la direction visuelle de référence pour la suite de la
  phase 10.
- La validation porte sur l'atmosphère générale, l'accueil immersif, la place
  centrale d'une carte géographique réelle, le panneau contextuel, la fonction
  de `Les lieux` et le système visuel minimal.
- Cette validation ne fige pas l'interface au pixel près. Les couches, filtres,
  niveaux de zoom et interactions seront précisés dans le bloc 4 ; le
  comportement du data scrollytelling sera précisé lors du prototypage.
- Les ajustements issus des tests responsive, d'accessibilité ou de
  compréhension pourront être appliqués sans rouvrir toute la direction
  artistique.
- Décision : **bloc 3 de la phase 10 terminé ; le bloc 4 peut commencer**.

## 2026-07-27 — Phase 10, lancement du bloc 4

- Une proposition fonctionnelle de carte exploratoire et de filtres est
  produite dans `docs/phase10_carte_exploratoire_filtres.md`.
- La vue initiale montre les 318 sites sans agrégats, sans filtre et sans
  panneau ouvert. Les couches d'eau, de forêt et de rail actuel restent des
  contextes cartographiques et ne modifient pas les résultats.
- Les quatre filtres proposés sont l'activité, la période d'activité, la
  situation actuelle et la précision géographique. La commune passe par la
  recherche.
- Le filtre temporel utilise seulement les 42 phases réellement datées,
  concernant 29 sites. Les repères documentaires issus des siècles de
  construction ne sont pas présentés comme des durées d'activité.
- Lorsqu'activité et période sont combinées, elles doivent correspondre à une
  même phase. Les résultats sont toujours dédupliqués par `site_id`.
- La situation actuelle sépare conservation, usages et accessibilité. Le
  contraste entre quatre situations récentes documentées et 314 non
  documentées reste explorable.
- `Point approximatif` et `Zone documentaire` reçoivent deux symboles
  distincts. Comme le GeoJSON public actuel contient uniquement des points,
  aucune emprise fictive n'est dessinée pour une zone documentaire.
- La liste et le détail alternent dans un panneau unique afin d'éviter une
  interface permanente en trois colonnes. La liste constitue l'alternative
  accessible aux 318 marqueurs.
- Une planche fonctionnelle est conservée dans
  `docs/design/phase10/10_exploration_etats_fonctionnels.*`.
- Décision provisoire : **bloc 4 en cours ; les interactions restent à
  arbitrer avant validation**.

## 2026-07-27 — Phase 10, validation du bloc 4

- L'architecture de la carte exploratoire et des filtres est validée comme
  **point de départ évolutif**.
- La validation porte sur la vue départementale sans agrégats, les quatre
  filtres initiaux, la séparation entre couches et filtres, le panneau unique
  liste-détail, le volet mobile et la liste accessible.
- Les règles de données sont confirmées : période limitée aux phases réellement
  datées, correspondance activité-période sur une même phase, situation actuelle
  multidimensionnelle et précision toujours visible.
- Les seuils de zoom, la densité cartographique, les libellés, l'ordre des
  contrôles et les dimensions des panneaux restent ajustables pendant le
  prototypage lorsqu'un test concret le justifie.
- Décision : **bloc 4 de la phase 10 terminé ; le bloc 5 peut commencer**.

## 2026-07-27 — Phase 10, lancement du bloc 5

- Une proposition de gabarits est produite dans
  `docs/phase10_fiches_sites_methode.md`.
- Trois niveaux sont distingués : aperçu court, panneau cartographique
  disponible pour les 318 sites et page `Les lieux` réservée à une sélection
  éditoriale humaine.
- Une page longue n'est jamais créée automatiquement à partir d'un score, d'un
  nombre de médias ou d'une longueur d'historique.
- Le panneau reste factuel et compact. L'image est omise si aucun média n'est
  retenu ; aucun placeholder industriel générique ne la remplace.
- Le gabarit `Les lieux` possède des blocs obligatoires de preuve mais autorise
  seulement les modules facultatifs nécessaires à la question du cas.
- La chronologie distingue phase datée, activités ordonnées sans dates,
  repères de construction et situation actuelle. Une fin inconnue ne se
  prolonge jamais artificiellement jusqu'à aujourd'hui.
- Les formulations d'absence, d'inconnu et d'incertitude sont définies. Les
  termes `disparu`, `sans usage`, `inaccessible` ou `non protégé` ne remplacent
  jamais une donnée inconnue.
- Les médias conservent légende, crédit, référence et lien à proximité. Le
  cadrage suppose les autorisations obtenues, mais l'export public doit toujours
  vérifier la preuve correspondante.
- Les retours vers le récit ou la carte restaurent le chapitre, les filtres, le
  cadrage et la sélection antérieurs.
- La page méthode est conçue comme une page éditoriale publique en huit
  sections ; les scripts, tables et chemins locaux restent dans la maintenance.
- Une planche fonctionnelle est conservée dans
  `docs/design/phase10/11_fiches_lieux_methode.*`.
- Décision provisoire : **bloc 5 en cours ; les gabarits restent à arbitrer
  avant validation**.

## 2026-07-27 — Phase 10, validation du bloc 5

- L'architecture des panneaux, des pages `Les lieux` et de la méthode est
  validée comme **point de départ évolutif**.
- Les trois niveaux sont confirmés : aperçu court, panneau disponible pour les
  318 sites et page longue réservée aux cas sélectionnés humainement.
- Les règles de preuve sont confirmées : chronologie adaptée à la qualité des
  dates, situation actuelle séparée, inconnues explicites, sources et crédits à
  proximité.
- La page méthode publique en huit sections est confirmée ; la documentation
  technique détaillée reste dans la maintenance.
- Les longueurs de texte, le nombre final de pages `Les lieux`, l'ordre des
  modules facultatifs, la densité et le responsive restent ajustables pendant
  le prototypage lorsqu'un test concret le justifie.
- Décision : **bloc 5 de la phase 10 terminé ; le bloc 6 peut commencer**.

## 2026-07-27 — Phase 10, lancement du bloc 6

- Un prototype navigable 0.1 est produit dans `prototype/phase10/`.
- Il matérialise l'accueil, un data scrollytelling en six étapes, l'exploration
  libre, la liste accessible, le panneau synthétique, trois récits `Les lieux`
  et la page méthode.
- Le prototype utilise les 318 sites et les 403 phases du corpus. Les pages
  longues restent limitées à trois cas choisis éditorialement : Ozé–Moulinex,
  Abadie et Bohin.
- La carte de contexte est générée à partir des couches géographiques réelles
  déjà préparées. Elle reste volontairement statique dans cette première
  version ; le moteur cartographique, le zoom et les optimisations relèvent du
  MVP après validation de la composition.
- Les filtres respectent les règles du socle : activité et période sur une même
  phase, quatre situations actuelles documentées, distinction entre point
  approximatif et zone documentaire.
- Le contrôle interne a vérifié les deux modes de lecture, les changements
  d'état du récit, la recherche, les filtres, les couches, l'état sans résultat,
  la liste, les panneaux, le clavier et un format mobile.
- Aucun framework, serveur applicatif ou système de composants supplémentaire
  n'est introduit pour cette étape de validation.
- Décision provisoire : **bloc 6 en cours ; le prototype 0.1 doit être examiné
  avant tout développement complet**.

## 2026-07-27 — Phase 10, validation réservée du bloc 6

- Le prototype 0.1 est validé comme **point de départ concret** afin de pouvoir
  poursuivre la phase 10.
- Cette décision valide le résultat du bloc — l'existence d'un prototype
  navigable — mais pas la qualité ni la forme définitive de l'expérience.
- La revue relève trop d'incohérences, d'abstractions artificielles et de
  séquences difficiles à comprendre ou inopérantes.
- Les difficultés concernent tous les niveaux : récit, exploration et pages
  `Les lieux`.
- La direction artistique devra elle aussi être réexaminée ; sa validation
  antérieure comme point de départ ne la rend pas définitive.
- Le bloc 7 ne doit donc pas industrialiser directement le prototype 0.1. Il
  commencera par distinguer, à partir de problèmes concrets, ce qui doit être
  conservé, repris ou supprimé.
- Cette reprise devra rester ciblée et éviter une nouvelle couche de conception
  abstraite, de surcode ou de composants inutiles.
- Décision : **bloc 6 terminé avec réserves importantes ; le bloc 7 peut
  commencer sans considérer l'expérience actuelle comme validée**.

## 2026-07-27 — Phase 10, lancement du bloc 7 comme refondation

- Après examen sur grand écran, le porteur du projet conclut que le prototype
  0.1 n'est pas seulement imparfait : il engage une mauvaise direction
  visuelle, narrative et fonctionnelle.
- Le résultat est jugé illisible et non publiable. Il ressemble à un site web
  à rubriques ou à un catalogue, et non à une publication de
  datajournalisme suffisamment originale et construite.
- Le récit cartographique, l'exploration et les pages `Les lieux` sont tous
  considérés comme incompréhensibles ou inopérants dans leur forme actuelle.
- Les problèmes signalés comprennent notamment les superpositions de points,
  la réaction peu intelligible des filtres, la grossièreté des panneaux, les
  volumes typographiques excessifs et l'absence de démonstration claire pendant
  le défilement.
- La direction artistique validée précédemment comme point de départ n'est plus
  retenue comme référence à développer.
- Le prototype devient un contre-exemple documenté. Les données, les sources et
  les règles de preuve restent acquises ; l'interface et le storyboard ne le
  sont pas.
- Le bloc 7 commence donc par une refondation : reformulation de la
  démonstration journalistique, choix d'une forme éditoriale principale,
  recherche visuelle sur contenu réel et validation d'une tranche verticale
  avant tout développement complet.
- Toute nouvelle direction devra être évaluée dans le navigateur à sa taille
  réelle, notamment sur une fenêtre de 1440 px.
- Le projet ira jusqu'à la fin du bloc 7 puis s'arrêtera pour une nouvelle
  évaluation. Le bloc 8 ne sera pas lancé automatiquement afin de ne pas
  investir dans le contrôle d'une expérience qui resterait insatisfaisante.
- Décision : **bloc 7 lancé comme phase de refondation du MVP ; aucun nouveau
  code d'interface ne doit être produit avant les nouveaux arbitrages**.

## 2026-07-28 — Phase 10, réouverture du bloc 2 et choix de l'unité intermédiaire

### Réponses du porteur du projet aux quatre questions de cadrage

- **Sujet** : mettre en avant le patrimoine industriel oublié de l'Orne et
  montrer comment il a façonné le paysage du département, ou comment il s'est
  adapté à sa géographie et à son hydrographie, contre l'image d'un département
  essentiellement rural.
- **Échelle** : les **318 sites**. Le démonstrateur de vingt à trente lieux
  évoqué au début du projet n'était qu'un échantillon destiné à établir un
  motif de travail ; il n'est pas le livrable.
- **Phrase à emporter** : « Dans l'Orne, les paysages ne se regardent pas
  seulement : ils se lisent comme les traces d'une ancienne géographie
  industrielle. »
- **Rôle de la carte** : instrument de démonstration, jamais sujet du récit.
  Le récit pose la question, la carte apporte la preuve, l'exploration libre
  vient ensuite. Trois fonctions : prouver, comparer, explorer.
- **Nature du sujet** : datajournalistique, à vocation historique et
  culturelle. Le projet n'est pas un relevé topologique, géographique ou
  technique ; ces aspects sont un cadre, pas le contenu.
- **Images** : la conception se fait comme si les autorisations d'utilisation
  étaient acquises. La question des droits reste traitée par le porteur du
  projet et ne conditionne plus les arbitrages de forme.

### Constats vérifiés dans le corpus complet V1

Calculs effectués sur `data/processed/patrimoine_orne_corpus_complet_v1.duckdb`,
tables `sites`, `sites_activites`, `activites` et `recits_sites`.

- **Deux géographies industrielles distinctes.** Médianes de distance au cours
  d'eau par secteur : énergie 29 m, métallurgie 30 m, textile 32 m,
  agroalimentaire 36 m — contre extraction 301 m, verre-céramique-matériaux
  344 m et chimie 430 m. 82 % des sites métallurgiques, 81 % des sites textiles
  et 75 % des sites agroalimentaires sont à moins de 100 m d'un cours d'eau,
  contre 17 % des sites de verre, céramique et matériaux.
- **Les sites d'extraction sont sur la ressource** : 825 m d'un indice minéral
  en médiane, contre 7 709 m pour l'ensemble du corpus.
- **77 % du corpus s'organise en ensembles.** Un regroupement des 318 sites
  localisés par lien de proximité à 3 km produit 88 ensembles ; 246 sites
  appartiennent à un ensemble d'au moins trois sites et 44 sites seulement
  restent isolés.
- **L'unité intermédiaire prend trois formes** : la vallée (Risle 43 sites,
  Noireau 23, Flers 21, La Ferté-Macé 12, Tinchebray 9, Randonnai 9), le bassin
  de ressource (La Ferrière-aux-Étangs à 1 273 m d'un indice minéral,
  Saint-Clair-de-Halouze à 2 531 m) et le pôle urbain (Alençon, Argentan, à
  plus de 250 m de l'eau).
- **Les ensembles ont une spécialité marquée** : La Ferté-Macé 100 % textile,
  Noireau 87 % textile, Randonnai 78 % métallurgie, Risle 56 % métallurgie.
  Deux vallées voisines et hydrauliques produisent des industries différentes :
  l'eau fournit la force, l'histoire décide de la production.
- **La progression chronologique n'est pas démontrable.** Seules 25 activités
  possèdent une date de début exploitable. Les périodes issues de `SCLE` vont
  dans le sens d'un éloignement de l'eau et d'un rapprochement du rail au fil
  du temps, mais ce champ date des campagnes de construction, il est multivalué
  et un site compte dans plusieurs périodes. Cet indice ne peut pas porter la
  structure du récit.
- **Le signal forestier est peu discriminant** : médiane du corpus à 94 m d'une
  formation forestière. Seule la métallurgie s'en détache (56 m) et le cas
  demande un examen site par site.

### Anomalie éditoriale relevée

- Les champs `historique_source` des sites `IA00060969` (moulin d'Ozé, puis
  filature, puis Moulinex) et `IA00061153` (affinerie dite forge de Beaumont)
  valent `$26`. Les notices sources contiennent des textes complets. Les deux
  sites appartiennent à l'échantillon pilote de la phase 5 et ont donc été
  enrichis par le parseur HTML plutôt que par l'API JSON.
- La validation de la phase 9 n'a pas pu le détecter : elle contrôle
  l'intégrité SHA-256 des textes, c'est-à-dire leur conservation, et non leur
  plausibilité. Une valeur corrompue a donc été conservée fidèlement.
- `IA00060969` est l'une des douze études de cas du bloc 2 et l'une des trois
  pages `Les lieux` du prototype 0.1.
- Correction à programmer dans le bloc 7, avec un contrôle de plausibilité des
  textes sources ajouté à la validation.

### Conséquences retenues

- Le bloc 2 est **rouvert**. Sa structure en prologue, cinq chapitres et
  conclusion reposait sur une progression temporelle que les données ne
  soutiennent pas.
- La structure de remplacement est une **descente d'échelle** : département,
  puis ensemble cohérent, puis lieu. Elle oppose des géographies au lieu de
  suivre une chronologie.
- Les 318 sites ne doivent jamais être présentés comme 318 objets individuels
  sur une vue d'ensemble. C'est ce traitement, et non leur nombre, qui a produit
  l'effet de catalogue du prototype 0.1.
- La **vallée de la Risle** est retenue comme premier cas travaillé : ensemble
  le plus dense, spécialité lisible du fil métallique et de la quincaillerie,
  et présence de trois des études de cas déjà sélectionnées.
- Les blocs 4 et 5 ne sont pas rouverts. Leurs architectures fonctionnelles
  restent valides ; c'est leur exécution dans le prototype et la direction
  artistique qui sont en cause.
- Décision : **bloc 2 rouvert sur une structure de descente d'échelle ;
  la vallée de la Risle sert de première tranche verticale ; les blocs 4 et 5
  restent acquis**.

## 2026-07-28 — Ouverture d'un registre de revue de presse

- Le porteur du projet signale un reportage paru le jour même dans l'édition
  Normandie d'`actu.fr` sur un lieu de Saint-Clair-de-Halouze, commune du
  corpus, et demande qu'un fichier soit créé pour référencer ce type de
  ressource.
- Le registre est créé dans `docs/revue_de_presse.md`. Il est distinct du
  registre des sources du corpus : un article de presse est une source
  secondaire et n'entre dans le modèle de données que par le circuit normal des
  mentions de sources, avec une date d'observation, une méthode de vérification
  et un niveau de fiabilité.
- Ces ressources répondent à un manque identifié : 315 des 318 sites ont une
  conservation inconnue et 316 une accessibilité inconnue. La presse locale et
  les associations sont l'une des rares voies permettant de documenter une
  situation actuelle sans enquête de terrain systématique. Un article ne prouve
  toutefois ni une autorisation d'accès, ni une protection, ni une relation
  historique.
- Le contenu de l'article n'a pas pu être lu : le domaine `actu.fr` refuse la
  récupération automatique. La référence est donc enregistrée avec son titre
  reconstitué depuis l'adresse de la page, sans résumé ni exploitation.
- Le site pressenti est `IA00060960`, *affinerie, filature*, lieu-dit
  « Forge (La) », situé à 27 mètres d'une formation forestière actuelle. La
  désignation employée par le porteur du projet, le lieu-dit et la position en
  forêt concordent. L'ensemble extractif `IA00060961`, situé à l'intérieur d'une
  formation forestière, reste une possibilité à écarter ou confirmer.
- Le rattachement reste `a_confirmer` et aucune valeur du corpus n'a été
  modifiée.
- Ce site présente par ailleurs un intérêt éditorial propre, indépendant de
  l'article : affinerie de 1530 fondée par le comte de Flers, convertie en
  filature vers 1840, consommant en 1841 de 120 000 à 130 000 kg de coton de
  Louisiane et de Géorgie, détruite par un incendie en 1897. Il illustre à la
  fois le motif de réemploi d'un site hydraulique et l'ouverture de l'industrie
  ornaise sur des marchés lointains.
- Décision : **`docs/revue_de_presse.md` créé comme registre des ressources
  éditoriales externes, avec des règles d'emploi qui les maintiennent hors du
  corpus tant qu'une vérification n'a pas eu lieu ; une place leur sera prévue
  dans la publication**.

## 2026-07-28 — Lecture de `PR-2026-001` : une chaîne du fer documentée et vivante

- Le texte de l'article a été communiqué par le porteur du projet. Il décrit le
  **chevalement de la mine de fer de Saint-Clair-de-Halouze**, en fonctionnement
  de 1907 à 1976, importé d'Allemagne en 1953, avec des galeries à plus de
  360 mètres et 42 nationalités employées sur le site.
- Le premier rattachement supposé, `IA00060960` — *affinerie, filature* au
  lieu-dit « Forge (La) » — est **écarté** : il reposait sur le mot « forge »,
  le lieu-dit et la position en forêt, non sur le contenu. Le sujet est la mine.
  L'épisode confirme la règle : un rattachement est une décision vérifiée, pas
  une déduction.
- Le site pressenti devient `IA00061008`, lieu-dit « Puits 2 (Le) », dont la
  notice mentionne une modernisation entre 1951 et 1954 cohérente avec le
  chevalement de 1953, et qui est le seul site de la commune déjà classé
  `partiellement_conserve`. `IA00061007` reste à départager.
- **L'article documente une situation actuelle pour plusieurs sites.**
  L'association « le Savoir et le Fer », active depuis plus de vingt-cinq ans,
  entretient et ouvre à la visite le carreau de la mine, les fours de la
  Butte-Rouge à Dompierre, les Forges de Varenne à Champsecret, la Maison du Fer
  et la Halle du Fer. Le corpus ne compte que quatre situations actuelles
  documentées ; cet article peut porter le total à six ou sept.
- **Réserve de saisonnalité retenue** : « visitable les mardis et jeudis à 11 h
  pendant l'été » n'est pas « visitable ». Toute valeur d'accessibilité versée
  devra porter sa condition et sa période, sous peine d'envoyer un lecteur
  devant une grille fermée hors saison.
- **Contradictions conservées** : l'article donne 1907–1976, les notices
  `IA00061007` et `IA00061008` donnent 1905 et 1980. Aucune valeur n'est
  corrigée ; l'écart est enregistré et sera arbitré source contre source. La
  profondeur — 360 m dans l'article, 85 m en 1911 dans la notice — relève
  vraisemblablement d'une évolution et non d'une contradiction.
- **Constat éditorial majeur.** Les notices du corpus documentent d'elles-mêmes
  la chaîne que l'association fait visiter : `IA00060894`, à Dompierre,
  « alimentait en gueuses l'affinerie de Varenne à Champsecret » ; `IA00060964`,
  à Varenne, était « alimentée en fonte par le haut fourneau de Dompierre » ;
  `IA00060965` indique que les fers étaient « vendus aux cloutiers de Chanu et
  de Tinchebray ». Il existe donc, du minerai au clou, une **relation historique
  établie par les sources** et non déduite d'une proximité spatiale — le niveau
  de preuve que la méthode exige pour affirmer un lien.
- Le bassin de Halouze–Dompierre–Champsecret réunit ainsi trois qualités que la
  vallée de la Risle n'a pas au même degré : des relations entre sites
  documentées, une protection Monuments historiques sur `IA00060964`, 31 objets
  Palissy rattachés à `IA00060965`, et surtout un **présent vivant** — une
  association, des visites, des témoins — là où le corpus est presque muet sur
  la situation actuelle.
- Le choix de la vallée de la Risle comme première tranche verticale n'est pas
  modifié à ce stade : il appartient au porteur du projet. Le bassin du fer est
  enregistré comme alternative sérieuse et, en tout état de cause, comme second
  cas de la typologie des ensembles.
- **Troisième anomalie de texte source** relevée : l'historique de `IA00060961`
  commence par « 955 ; », visiblement tronqué au début. À traiter avec les
  historiques corrompus `IA00060969` et `IA00061153`.
- Décision : **article `PR-2026-001` qualifié ; versement des situations
  actuelles à programmer par le circuit des mentions de sources, avec condition
  de saisonnalité ; le bassin du fer est retenu comme second cas de la typologie
  et comme alternative possible pour la première tranche verticale**.

## 2026-07-29 — Direction de travail : lire d'abord, dessiner ensuite

- Le porteur du projet constate que la reprise part dans plusieurs directions à
  la fois et demande une ligne unique et clairement écrite. Le constat est
  fondé : trois fils ont été ouverts en deux jours — analyse spatiale par
  secteur, revue de presse, bassin du fer — sans qu'aucun soit refermé.
- **Diagnostic retenu.** Tout ce qui a été produit en phase 10 a été conçu à
  partir de chiffres sur le corpus — 318 sites, 403 phases, 73 lieux à
  plusieurs vies, 9 secteurs — et jamais à partir de son contenu. Les 314 textes
  historiques ont été extraits, contrôlés, empreintés et validés, mais ils
  n'ont pas été lus. On ne produit pas de journalisme avec des effectifs ; on
  produit un catalogue. C'est ce qui explique des gabarits applicables à
  n'importe quel lieu.
- La découverte de deux historiques valant `$26`, dont celui d'une des douze
  études de cas retenues, confirme matériellement que ces textes n'ont jamais
  été ouverts.
- **Direction arrêtée** : la reprise commence par la lecture de la matière sur
  un ensemble cohérent et de taille lisible, les 43 sites de la vallée de la
  Risle. Aucune forme, aucun écran et aucune direction artistique ne sont
  produits avant que cette lecture ait rendu son résultat.
- La lecture cherche les personnes, les entreprises, les productions, les
  effectifs, les ruptures, et surtout les relations que les notices établissent
  entre elles — le type de lien qu'aucune analyse spatiale ne peut trouver,
  comme l'a montré la chaîne Dompierre–Varenne.
- **Un seul fil ouvert à la fois.** Le bassin du fer reste le deuxième cas et
  n'est pas traité maintenant, malgré l'avantage de son présent documenté.
  Correction des historiques, versement des situations actuelles et revue de
  presse sont différés après la lecture.
- Décision : **lire les 43 notices de la vallée de la Risle et en consigner le
  résultat avant toute proposition de forme ; les autres chantiers restent
  fermés jusque-là**.

## 2026-07-29 — Résultat de la lecture de la vallée de la Risle

Lecture complète des 43 notices consignée dans `docs/phase10_lecture_risle.md`,
version 1.0. Principaux résultats.

- **La vallée fabriquait de très petits objets métalliques** : épingles,
  aiguilles, pointes, clous, boucles de sellerie, dés, agrafes, crochets,
  cardes, plumes métalliques, broches à tricoter. Ce fait n'apparaît dans
  aucune statistique du corpus, puisque les neuf secteurs rangent ces
  productions sous « métallurgie et travail des métaux », au même titre qu'un
  haut fourneau. Il a fallu lire pour le voir.
- **Les notices établissent elles-mêmes une chaîne de production complète.**
  `IA00061017`, haut fourneau du Logeard attesté en 1491, « alimentait en fonte
  la forge d'Aube » ; `IA00061029`, affinerie d'Aube, était « affectée jusqu'en
  1850 à l'affinage de la fonte produite au haut fourneau du Logeard » et
  « alimentait en fer la fenderie d'Aube » ; `IA00061129` est « dépendant de la
  forge d'Aube ». La filière fonte–fer–fil–épingle s'étire sur environ
  vingt-cinq kilomètres et chaque maillon est un site distinct du corpus.
- **Seize notices sur quarante-trois** mentionnent une usine établie sur
  l'emplacement d'un moulin, ou la conversion d'un moulin. L'industrie ne
  s'installe pas dans un paysage vierge : elle réutilise une chute d'eau déjà
  équipée. C'est la démonstration la plus directe de la phrase retenue pour le
  lecteur.
- **La concentration industrielle est cartographiable** : six sites du corpus
  portent le nom de Benjamin Bohin, dont cinq rachats, et trois d'entre eux
  voient leur production « transférée à l'usine de Saint-Sulpice-sur-Risle »
  après 1945. Les familles Mouchel et Turquet apparaissent chacune sur deux à
  trois sites.
- **La sortie de l'énergie hydraulique est documentée sans rupture
  géographique** : la fenderie d'Aube devient usine hydroélectrique vers 1909,
  la centrale d'Aube alimente à partir de 1919 Boisthorel, Bohin et des usines
  de L'Aigle. Le réseau électrique dessert exactement les usines que la rivière
  faisait tourner.
- **Trois usines de Rai étaient encore actives à la fin des années 1980**, liées
  entre elles : Eurofac et Rai-Tillières transforment des métaux « produits à
  l'usine voisine de Boisthorel » et livrés par voie ferrée particulière. La
  filière ne s'est pas éteinte, elle s'est resserrée.
- Quatre lieux sont retenus pour un traitement long : `IA00061029` affinerie
  d'Aube, `IA00061155` Bohin, `IA00061053` Boisthorel et `IA00061017` haut
  fourneau du Logeard.

### Correction d'un constat antérieur

- Il a été écrit le 28 juillet que la progression chronologique n'était pas
  démontrable, seules 25 activités du corpus possédant une date de début
  exploitable. Ce constat portait sur les données **structurées** et reste
  exact à ce titre : sur les 65 activités des 43 sites de la Risle, 8
  seulement ont une date de début structurée.
- Mais les textes de ces mêmes 43 notices citent **321 années distinctes**. La
  mention « chronologie détaillée non encore structurée pour ce dossier »
  figure dans la quasi-totalité des activités.
- La chronologie n'est donc pas absente du corpus : elle est présente en texte
  libre et n'a pas été extraite. L'abandon de l'arc chronologique reste valable
  pour l'instant, mais son motif change : ce n'est pas que les dates manquent,
  c'est qu'elles ne sont pas exploitables en l'état. Un chantier d'extraction
  est possible et doit être arbitré.
- Décision : **lecture de la Risle close ; la démonstration retenue est
  spatiale et filière — un paysage déjà équipé, une vallée qui est une chaîne
  de production, une filière encore lisible aujourd'hui ; le chantier
  d'extraction des dates en texte libre est ouvert à l'arbitrage**.

## 2026-07-29 — Changement de nature du produit : une application, pas un site

- Le porteur du projet corrige une erreur de cadrage qui remonte au début de la
  phase 10 : **le produit n'est pas un site web**. C'est une **application web
  interactive de datajournalisme**, créative et originale, qui peut se résumer
  à une carte et un tableau de bord.
- C'est la cause profonde de l'échec du prototype 0.1. Décliné en site, le
  projet a produit des rubriques, des pages, un défilement et des gabarits
  applicables à n'importe quel lieu, c'est-à-dire un catalogue. Le diagnostic
  antérieur attribuait ce résultat au traitement des 318 sites ; la cause
  première est la nature même de l'objet.
- **Le récit n'est pas linéaire.** Le lecteur choisit son entrée, son
  exploration et ses vues. Le récit naît de l'exploration : la carte annote ce
  qu'elle montre, la sélection ouvre une histoire, les liens entre sites se
  dessinent avec la phrase qui les prouve.
- Deux règles d'écriture en découlent : chaque vue doit se suffire à elle-même,
  et la démonstration se construit par répétition depuis des angles différents
  plutôt que par accumulation d'étapes. Des amorces cliquables sont
  obligatoires, faute de quoi une carte ouverte reste un outil et non une
  publication.
- **Trois niveaux d'écriture** sont arrêtés : l'annotation de quelques lignes
  écrite pour une situation précise, le texte d'ensemble de deux cents mots
  écrit par nous, et le texte de lieu d'une centaine de mots tiré de la notice.
  Une entrée complète a été rédigée et validée comme exemple de référence :
  filtre « travail du métal », vallée de la Risle, chaîne du haut fourneau de
  1491 aux épingles, puis tréfilerie de La Fonte et ses 135 ouvriers de 1867
  dont 10 enfants.
- **Réserve du porteur du projet sur la carte** : elle ne doit pas être en
  plein écran. Sur les grands écrans, une carte à bord perdu devient grossière.
  Elle doit être encadrée et habillée — cadre assumé, marge, titre de vue,
  légende, indicateurs, source. Contrainte structurante pour la direction
  artistique, à respecter dès la première proposition visuelle.
- Un **nouveau document de cadrage** est produit,
  `docs/phase10_cadrage_v2_application.md`, version 2.0. Il ne corrige pas
  `docs/phase10_cadrage_editorial_ux.md` : il repart d'une autre définition du
  produit et le remplace. L'ancien document est conservé sans modification.
- Décision : **le produit est une application web interactive de
  datajournalisme, à récit non linéaire, organisée autour d'une douzaine de
  systèmes industriels ; cadrage V2 arrêté ; la carte sera encadrée et habillée,
  jamais en plein écran**.

## 2026-07-29 — Reconstruction de la roadmap de la phase 10

- La section « phase 10 » de `docs/roadmap.md` était devenue illisible : quatre
  couches successives y avaient été empilées en trois jours — réouverture du
  bloc 2, direction de travail, étape de lecture, cadrage V2 — sans que la
  structure d'ensemble soit reprise.
- Le porteur du projet demande une roadmap reconstruite sur le cadrage V2,
  avec des phases résumées, un objectif et un livrable affichés, et des tâches
  cochables tenues à jour au fil de l'avancement.
- L'ancienne organisation en neuf blocs est remplacée par **neuf phases**
  allant de 10.A à 10.I : compléter les données manquantes, constituer et lire
  les systèmes, arbitrer l'architecture, construire une vue de référence,
  direction artistique, écrire la matière éditoriale, construire
  l'application, qualité et accessibilité, publication.
- Chaque phase affiche un résumé en deux phrases, son objectif, son livrable et
  son point de validation. Les tâches sont regroupées en sous-ensembles
  numérotés lorsque la phase le justifie.
- L'ordre retenu place la **vue de référence avant la direction artistique**.
  Cette vue est volontairement neutre sur le plan graphique : elle éprouve la
  compréhension et la structure, pas l'esthétique. La direction artistique
  n'intervient qu'ensuite, sur une forme dont on sait qu'elle fonctionne.
- L'écriture éditoriale complète est également placée **après** la validation de
  la vue, afin de ne pas rédiger les textes de douze systèmes avant de savoir
  si la forme tient.
- Le travail des blocs 1 à 7 de la première tentative est conservé dans une
  section « historique », qui distingue ce qui reste utilisable — architectures
  fonctionnelles des blocs 4 et 5 — de ce qui ne fait plus référence.
- Les règles de suivi en tête de fichier sont renforcées : mise à jour au fil
  de l'eau et non après coup, et interdiction de cocher une tâche dont le
  résultat n'est pas vérifiable par un tiers.
- Rappel : `docs/roadmap.md` figure dans le `.gitignore` et n'existe donc que
  sur la machine du porteur du projet. Le présent journal est la seule trace
  versionnée de cette réorganisation.
- Décision : **roadmap de la phase 10 reconstruite en neuf phases 10.A à 10.I
  sur le cadrage V2 ; la vue de référence précède la direction artistique et
  l'écriture éditoriale complète**.

## 2026-07-29 — Extraction des relations entre sites et extension du modèle

### Rectification d'un constat erroné

- Il a été écrit à plusieurs reprises que la table `relations_sites` était vide.
  **C'est faux.** Elle contenait cinq relations établies en phase 8 : deux cités
  ouvrières rattachées à l'ensemble extractif de Halouze, deux à celui de
  La Ferrière-aux-Étangs, et la fenderie `IA00061188` dépendant de l'affinerie
  `IA00061187` à Larchamp.
- Cette dernière relation avait été présentée le 29 juillet comme un ajout
  manuel de la phase 10, rattrapé après une exclusion à tort du filtre. Elle
  existait depuis la phase 8, avec une justification identique. L'erreur venait
  d'une vérification faite sur le schéma du modèle plutôt que sur le contenu de
  la base.

### Extension du vocabulaire contrôlé

- Les cinq types de relations définis en phase 3 — `composant_de`,
  `transfert_vers`, `successeur_de`, `depend_de`,
  `partage_infrastructure_avec` — décrivent tous des relations de **structure**.
  Aucun ne représente un **flux de production**.
- Or quatorze des vingt liens extraits des textes sont de cette nature : un haut
  fourneau qui envoie sa fonte à une forge. Les ranger sous `depend_de` aurait
  confondu deux réalités distinctes — une cité ouvrière qui dépend de sa mine,
  et une forge qui achète de la fonte à son voisin.
- Le porteur du projet a validé l'ajout d'un sixième type, **`approvisionne`** :
  le site source fournit une matière au site cible.
- **Règle d'orientation fixée** : la relation est toujours enregistrée du
  fournisseur vers le destinataire, quelle que soit la formulation de la source.
  « Alimentait la forge de la Roche » et « alimentée en fer par la forge du
  Champ-de-la-Pierre » produisent des lignes de même sens.
- Modifications : contrainte `CHECK` de `model/schema.sql` et
  `docs/modele_donnees.md`.

### Versement par la chaîne de production

- Les 18 relations nouvelles ont été inscrites dans
  `config/phase8_decisions_canoniques.yml`, avec leurs identifiants stables dans
  `config/phase8_site_ids.yml`, puis la chaîne complète a été rejouée :
  canonisation, enrichissement du corpus, contexte territorial, production du
  corpus complet.
- Une écriture directe dans la base aurait disparu à la première
  reconstruction. Le passage par la configuration garantit la reproductibilité.
- La reconstruction du corpus efface les tables éditoriales de la phase 9. Elles
  ont été refabriquées et la validation du socle narratif et visuel repasse au
  vert.

### Contrôles

- Quatre tests ont échoué en gardant l'ancien effectif de cinq relations. C'est
  leur fonction : empêcher qu'un changement d'effectif passe inaperçu. Ils ont
  été mis à jour avec le motif du changement inscrit en commentaire.
- Les 162 tests passent. Les effectifs du corpus sont inchangés : 319 dossiers
  sources, 318 sites, 403 activités.

### Résultat

- **23 relations en base, reliant 36 sites.**
- La chaîne la plus complète est à Randonnai : le haut fourneau de Gaillon à
  Irai alimente deux affineries à Randonnai, qui alimentent la fenderie de
  Conturbie. Quatre sites, trois niveaux, entièrement sourcés.
- Trois relations de transfert vers les établissements Bohin sont marquées
  comme interprétées : la source dit « l'usine de Saint-Sulpice-sur-Risle » sans
  la nommer, et la commune compte cinq sites.
- Décision : **type `approvisionne` ajouté au modèle ; 18 relations de
  production versées par la chaîne de production ; l'orientation est toujours
  du fournisseur vers le destinataire**.

## 2026-08-05 — Un écran, pour décider si le projet tient

- Le porteur du projet constate que le pilotage a pris la place de la vision :
  phases, mouvements, tables et rapports se sont substitués à ce qu'on cherche
  à raconter, et il est devenu spectateur de son propre projet.
- Décision de méthode : arrêter la préparation et fabriquer un écran réel sur la
  vallée de la Risle, avec les vraies données, pour qu'il juge si ce qu'il voit
  raconte l'histoire qu'il veut porter — ou s'il faut arrêter.
- L'écran est un fichier autonome, `prototype/risle/index.html`, sans serveur ni
  dépendance. Il contient les 43 usines de la vallée, le tracé réel de la Risle
  et de ses affluents, les liens entre sites, et 368 événements datés.
- Trois principes du cadrage V2 y sont éprouvés : la carte est encadrée et
  habillée et non en plein écran ; le récit naît de l'exploration au lieu d'être
  imposé ; l'annotation est posée sur la carte, à côté de la forme qu'elle
  décrit.
- Un ajout non prévu s'est révélé indispensable : **la carte se recadre sur ce
  qu'elle démontre**. Atténuer quelques points sur une vue large ne se remarque
  pas — c'est exactement le défaut relevé sur le prototype 0.1. Une mise en
  évidence n'est une démonstration que si le cadrage suit.
- Décision : **l'écran de la vallée de la Risle est produit et remis au porteur
  du projet ; la suite du projet dépend de son jugement sur cet écran**.

## 2026-08-05 — Un système peut en alimenter un autre

- La lecture de Flers, troisième système, fait apparaître une relation que le
  modèle ne sait pas représenter : **la vallée du Noireau filait le coton que
  la ville de Flers tissait**.
- Cinq notices du Noireau indiquent que leurs fils étaient « vendus à Flers et à
  Condé-sur-Noireau ». Les notices de Flers décrivent des tissages, non des
  filatures. La complémentarité est documentée des deux côtés.
- Un seul de ces liens est exprimable dans `relations_sites`, parce qu'il désigne
  un site précis : la filature de la Planchette alimente le tissage de la
  Planchette, construits par le même homme. Les autres pointent vers une
  **ville**, pas vers un site.
- La table des relations relie des sites. Ici, la relation lie **deux
  systèmes**. C'est une question ouverte pour l'application : faut-il un niveau
  de relation entre ensembles, ou bien la relation reste-t-elle un fait
  éditorial exposé dans le texte sans être modélisé ?
- La décision est reportée jusqu'à la lecture des douze systèmes : si le cas ne
  se reproduit pas, il ne justifie pas une modification du modèle.
- Décision : **relation Noireau–Flers consignée dans les documents de lecture ;
  l'arbitrage sur sa modélisation attend la fin des lectures**.

## 2026-08-10 — La dentelle d'Alençon, ou ce que le corpus ne peut pas contenir

- Le porteur du projet relève l'absence de la dentelle dans le système
  d'Alençon. Vérification faite, elle est absente de tout le corpus : aucun des
  318 sites, aucune des 403 activités, aucun des 314 historiques.
- L'absence ne vient pas de notre extraction. Dans les sources brutes, la
  dentelle n'apparaît que dans des édifices religieux, des manoirs, un lieu-dit
  homonyme et un unique objet inventorié, `PM61002792`.
- Explication retenue, à confirmer auprès de l'Inventaire : le point d'Alençon
  est une dentelle à l'aiguille, faite à la main, sans bâtiment de production ni
  machine. Une enquête sur le patrimoine **industriel** ne la rencontre pas.
- **Portée générale.** Le corpus documente des usines ; tout ce qui s'est
  fabriqué sans usine en est absent par construction. Ce n'est pas une lacune à
  combler mais une définition du périmètre.
- Conséquence éditoriale : l'absence doit être écrite dans la publication. Un
  lecteur qui connaît son territoire la repérera immédiatement — c'est ce qui
  vient de se produire.
- Consigné dans `docs/limites_editoriales.md` et dans la lecture d'Alençon.
- Décision : **le périmètre « productions avec usine » est explicité comme
  limite affichée de la publication, et non traité comme un manque**.

## 2026-08-10 — Deuxième relation entre systèmes, la question se confirme

- La lecture de La Ferté-Macé fait apparaître un second cas de relation entre
  deux systèmes : le tissage des Peupliers `IA00060982` est « acquis en 1904 par
  la Société Générale des Tissages et Filatures de Flers ».
- C'est la société flérienne — née officiellement de la fusion de 1907 — qui
  achète une usine de La Ferté-Macé trois ans plus tôt.
- Après la relation Noireau → Flers relevée le 5 août, le cas n'est donc pas une
  exception. La question posée alors reste ouverte mais gagne en poids : le
  modèle relie des sites, pas des ensembles.
- Aucune décision n'est prise avant la fin des douze lectures. Si un troisième
  cas apparaît, l'arbitrage deviendra nécessaire.

## 2026-08-11 — Les douze systèmes sont lus

- La lecture des douze systèmes industriels est terminée : **172 sites sur 318**,
  soit 54 % du corpus, lus notice par notice.
- Douze formes distinctes, dont aucune ne reproduit la précédente : une chaîne
  de production, une vallée qui change de fibre, une ville qui tisse, deux
  bassins miniers de modèles opposés, une préfecture sans métier, une monoculture
  textile, une ville qui n'a pas fermé, une dynastie de cinq siècles, un pays où
  l'industrie recule, un système qui monte, et une lisière.
- **Cinq relations entre systèmes** ont été relevées au fil des lectures :
  Noireau → Flers, Flers → La Ferté-Macé, Tinchebray → Frênes, Randonnai →
  Pontchardon, Tourouvre → Gaillon et Randonnai. Trois d'entre elles manquent à
  la base et attendent un versement groupé.
- **Une lacune d'extraction est identifiée** : lorsque l'acheteur nommé dans une
  notice est lui-même un site du corpus, le motif le range parmi les exploitants
  et non parmi les relations. Une classe entière de liens échappe ainsi à
  l'extraction automatique.
- Trois décisions restent en attente et doivent être prises avant de poursuivre :
  1. verser les trois relations manquantes, ce qui suppose d'arbitrer le type
     `acquisition_site`, absent du vocabulaire du modèle ;
  2. décider si une relation entre **systèmes** doit être représentée, ou si elle
     reste un fait éditorial exposé par le texte ;
  3. décider du sort des 146 sites hors des douze systèmes — 74 dans des
     ensembles de trois à six sites, 72 isolés ou par paires.
- Décision : **phase 10.B.2 close ; les arbitrages différés sont désormais
  bloquants pour la suite**.

## 2026-08-11 — Périmètre éditorial arrêté : douze systèmes, aucun site écarté

Décision du porteur du projet.

- Les **douze systèmes** lus sont validés comme **cœur éditorial de
  l'application**. Ils rassemblent 172 des 318 sites.
- Les **72 sites seuls ou par paires** restent visibles et consultables
  individuellement sur la carte, avec leur notice et leur chronologie.
- Les **74 sites des 18 petits ensembles** de trois à six sites sont conservés.
  Leur lecture éditoriale est **reportée**, non annulée : ils pourront devenir
  de nouveaux systèmes si leur étude fait apparaître une histoire suffisamment
  forte.
- **Aucun site n'est écarté du projet.**
- Le seuil de regroupement reste à **trois kilomètres**. L'élargir à cinq
  couvrirait 80 % du corpus mais fusionnerait le Noireau, Flers et Tinchebray
  en un seul bloc, ainsi que Halouze et La Ferrière : les deux meilleures
  démonstrations du travail disparaîtraient.

### Nuance retenue sur le mot « isolé »

- « Isolé » ne signifie ici qu'une chose : **aucun autre site du corpus à moins
  de trois kilomètres**. C'est le résultat d'une règle que nous avons choisie.
- Cela ne prouve **ni** que l'usine fonctionnait seule, **ni** qu'elle
  n'appartenait à aucun réseau historique. Les documents de lecture ne doivent
  pas laisser croire le contraire.
- Ces 72 sites sont hétérogènes : beaucoup de moulins et de fromageries, mais
  aussi des tuileries, des papeteries et des usines métallurgiques. Ils ne
  forment pas encore un sujet.
- Une **analyse courte** est validée pour vérifier si leur dispersion raconte
  réellement quelque chose. Si une démonstration solide apparaît, elle pourra
  devenir une entrée éditoriale ; sinon ils resteront des sites individuels
  consultables.

Décision : **douze systèmes comme cœur éditorial ; aucun site écarté ; seuil
maintenu à trois kilomètres ; analyse courte des 72 sites dispersés, sans
présumer qu'ils étaient historiquement isolés**.

## 2026-08-11 — Les 72 sites dispersés : un constat, pas un chapitre

Décision du porteur du projet.

- Les 72 sites seuls ou par paires **ne font pas l'objet d'une entrée
  éditoriale**. Ils restent tous visibles et consultables sur la carte.
- La présentation générale pourra signaler le **constat vérifié** : ces sites
  sont plus souvent agroalimentaires ou liés aux matériaux — 50 % et 14 %,
  contre 27 % et 6 % chez les sites regroupés — quand le métal et le textile
  dominent les systèmes.
- **Aucune explication causale non sourcée ne sera avancée.** La formulation
  proposée dans le compte rendu — « les moulins suivent les ruisseaux, les
  tuileries suivent l'argile » — est une interprétation qui n'est appuyée par
  aucune source du corpus. Elle est écartée.
- Sur tout le reste, ces sites sont identiques aux autres : début médian 1854
  contre 1827, fin médiane 1937 contre 1935, durée médiane 100 ans contre 114,
  et 28 % encore actifs après 1950 contre 30 %.

Décision : **pas de chapitre sur les sites dispersés ; le constat de
répartition par métier est signalé dans la présentation générale, sans
explication causale**.

## 2026-08-11 — Titre de travail, arrivée et amorces : la phase 10.C est close

Décisions du porteur du projet.

- **Titre de travail** : « Voyage dans l'Orne industrielle ». Provisoire.
- **À l'arrivée**, le lecteur voit directement la carte de l'Orne, les douze
  systèmes, les autres sites et les commandes de recherche et de filtrage.
  Aucun parcours ni récit ne lui est imposé.
- **Les amorces cliquables sont reportées.** Elles pourront être ajoutées après
  matérialisation de la visualisation, si elles apportent une aide réelle. Leurs
  intitulés devront décrire exactement ce que la commande affiche, sans
  formulation abstraite.
- L'objection avancée le 29 juillet — une carte ouverte sans amorce reste un
  outil et non une publication — n'est pas écartée mais différée. Elle sera
  tranchée devant l'écran réel plutôt que sur une hypothèse.

Décision : **phase 10.C close ; les neuf décisions d'architecture sont
arrêtées et documentées dans `docs/phase10_architecture.md`**.

## 2026-08-12 — Mise à jour des documents généraux de référence

- Le cadrage V2 du 29 juillet ne reflétait plus plusieurs décisions prises en
  phases 10.B et 10.C : il rendait les amorces obligatoires, conservait les
  anciens effectifs des systèmes et décrivait encore une logique plus
  narrative que la visualisation libre désormais retenue.
- `docs/phase10_cadrage_v2_application.md` passe en version 2.1 et devient la
  présentation générale à jour : 318 sites, douze systèmes couvrant 172 sites,
  146 autres sites tous conservés, arrivée directe sur la carte, filtres
  validés, règles du temps et architecture SVG statique.
- Le `README.md`, qui annonçait encore la phase 9 en cours, est aligné sur
  l'avancement réel et donne accès en premier aux documents de phase 10.
- `docs/recommandation_application.md`, version 1.0 du 22 juillet, décrivait
  l'ancien site narratif et recommandait MapLibre. Sa version 2.0 recommande
  l'application statique de visualisation interactive et reprend l'ordre
  validé : vue fonctionnelle, direction artistique, contenus, extension.

Relecture de cohérence effectuée le même jour. Les effectifs des quatre
documents ont été recoupés un par un avec les rapports de contrôle versionnés :
2 360 événements datés sur 314 sites, 314 textes historiques, 1 888 médias
distincts, neuf secteurs, conservation inconnue pour 315 sites sur 318,
172 sites en systèmes et 146 hors systèmes. Tous concordent. Le passage de
2 320 à 2 360 est la conséquence de la réparation des deux historiques
corrompus en phase 10.A.3, non un recomptage.

Deux écarts relevés à cette occasion et corrigés :

- L'en-tête de `docs/phase10_architecture.md` était resté celui de la première
  rédaction : il annonçait « six décisions » et renvoyait à un traitement
  séparé du titre, des premières secondes et des amorces, alors que le document
  en contient dix et traite ces trois points aux sections 8, 9 et 10. L'entrée
  du 11 août parlait de son côté de neuf décisions. Le décompte exact est
  **dix** ; le document passe en version 1.1. Aucune décision n'est modifiée,
  seul le décompte l'est.
- `CLAUDE.md` décrivait encore l'état du bloc 7 et maintenait l'interdiction du
  27 juillet de produire du code d'interface. Cette interdiction attendait les
  arbitrages désormais rendus : elle est **levée**, la phase 10.D consistant
  précisément à construire une vue fonctionnelle. La section d'état renvoie
  maintenant aux trois documents qui font foi et distingue les deux prototypes,
  le contre-exemple de la première tentative et l'écran de la Risle du 5 août.

Décision : **le cadrage V2 version 2.1, l'architecture version 1.1, le README
et la recommandation version 2.0 sont les documents généraux actualisés avant
l'ouverture de la phase 10.D ; l'interdiction de produire du code d'interface
est levée**.
