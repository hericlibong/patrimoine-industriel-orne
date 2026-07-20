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
