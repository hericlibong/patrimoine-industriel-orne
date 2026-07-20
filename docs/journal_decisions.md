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
