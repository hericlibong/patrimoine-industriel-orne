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
