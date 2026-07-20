# Bilan d'audit des sources — phase 1

Date : 19 juillet 2026
Périmètre : socle de données V1 sur le patrimoine industriel de l'Orne

## Conclusion opérationnelle

Le projet peut passer aux extractions tests. Aucune source ne suffit seule :

1. l'Inventaire normand fournit le **corpus patrimonial initial** de 319 dossiers ;
2. Mérimée, Palissy et les Monuments historiques **enrichissent** ce corpus sans le remplacer ;
3. CASIAS fournit un **réservoir de candidats**, mais pas une liste de patrimoine ;
4. les couches géographiques servent à tester les relations avec l'eau, la forêt,
   la géologie, le parcellaire et le rail ;
5. les archives, Gallica et les sources locales servent à **vérifier et raconter**
   des cas précis.

La principale difficulté est l'accès automatisé aux 319 dossiers de l'Inventaire
normand. Les pages sont riches et les références `IA` sont stables, mais le site
oppose un contrôle JavaScript aux requêtes directes et aucun export global n'a été
identifié. La phase 2 devra comparer une extraction semi-automatique des pages,
la récupération des PDF et un éventuel accès institutionnel.

## Résultats prioritaires

| Source | Résultat du test | Rôle | Statut |
|---|---|---|---|
| Inventaire industriel de l'Orne | 319 dossiers, références `IA`, pages et PDF ; pas d'export global identifié | principale | validée avec réserves |
| Immeubles Monuments historiques | API filtrable : 420 notices dans l'Orne, 341 coordonnées, 18 candidats industriels par mots-clés avant contrôle manuel | enrichissement | validée |
| Palissy MH | CSV national accessible, très volumineux ; liens possibles par édifice, commune et référence Mérimée | enrichissement | validée avec réserves |
| CASIAS Normandie | WFS filtré : 2 052 sites dans l'Orne ; seulement 209 avec coordonnées `x/y` ; 1 853 indiqués « site non géolocalisé » | élargissement | validée avec réserves |
| Géoplateforme / BAN / cadastre | services et fichiers départementaux accessibles | contexte et localisation | validées avec réserves selon la couche |

Les chiffres sont des mesures de l'accès testé le 19 juillet 2026. Ils ne sont pas
des dénombrements définitifs du patrimoine industriel.

## 1. Sources patrimoniales

### Inventaire du patrimoine industriel de l'Orne

- **Producteur :** Région Normandie, Inventaire général du patrimoine culturel.
- **Périmètre annoncé :** repérage conduit de 1986 à 1994 ; environ 2 500 sites
  repérés à partir des sources historiques et cadastrales ; 319 établissements
  créés avant 1950 et conservant tout ou partie de leur bâti ont été étudiés.
- **Unité :** dossier d'établissement ou de site industriel.
- **Contenu utile :** dénomination, localisation, références cadastrales,
  datation, historique, description architecturale, parties constituantes,
  sources et photographies.
- **Identifiant :** référence stable de type `IA61000851`.
- **Accès testé :** corpus paginé et fiches HTML consultables ; présence de PDF
  numérisés sur certaines fiches. Les URL des PDF utilisent un identifiant opaque.
- **Limites :** de nombreuses fiches sont annoncées « non géolocalisées » ; les
  pages refusent les requêtes HTTP simples par un contrôle JavaScript ; aucun API
  ou export global du corpus n'a été confirmé.
- **Droits :** mention Région Normandie — Inventaire général. Les droits précis
  des textes, notices, PDF et images devront être vérifiés séparément avant
  republication ; une photographie consultable n'est pas automatiquement libre.
- **Décision :** `principale`, `P0`, `validee_avec_reserves`.

### POP / Mérimée

- **Producteur :** ministère de la Culture.
- **Distinction nécessaire :** POP agrège des notices de l'Inventaire général et
  des notices de protection. L'export ouvert identifié sous le nom Mérimée porte
  sur les immeubles protégés au titre des Monuments historiques ; il ne représente
  donc pas les 319 dossiers industriels.
- **Unité :** notice d'édifice.
- **Contenu utile :** référence Mérimée, dénomination, localisation, commune,
  datation, historique, protection, cadastre, cours d'eau, énergie, liens Palissy
  et coordonnées lorsqu'elles existent.
- **Accès :** recherche POP ; CSV, GeoJSON et API pour le sous-ensemble des
  Monuments historiques.
- **Droits :** données descriptives publiques réutilisables avec mention de la
  source ; textes et images peuvent rester protégés et doivent être vérifiés notice
  par notice.
- **Décision :** `enrichissement`, `P1`, `validee_avec_reserves`.

### POP / Palissy

- **Producteur :** ministère de la Culture.
- **Périmètre ouvert testé :** objets protégés au titre des Monuments historiques,
  et non l'intégralité des objets techniques recensés par l'Inventaire général.
- **Accès :** CSV national direct, séparateur `|`, d'environ 363 Mo au moment du
  test. Le fichier est trop volumineux pour l'indexation tabulaire de data.gouv.fr.
- **Champs utiles :** référence `PM`, catégorie technique, objet, édifice,
  commune, code INSEE, état, historique et référence à une notice Mérimée MH.
- **Liens avec un site :** référence Mérimée lorsqu'elle existe ; sinon édifice,
  commune et code INSEE. Ces rapprochements ne devront jamais être acceptés sur le
  seul nom de commune.
- **Exemples pertinents repérés :** collections métallurgiques de la forge de
  Varenne (`PM61000916`) et tourillons de roues (`PM61000814`).
- **Droits :** mêmes précautions que POP/Mérimée pour les textes et images.
- **Décision :** `enrichissement`, `P2`, `validee_avec_reserves`.

### Immeubles protégés au titre des Monuments historiques

- **Accès testé :** API data.culture avec filtre
  `departement_en_lettres="Orne"`, plus exports CSV et GeoJSON.
- **Résultat :** 420 notices ; 341 possèdent des coordonnées WGS84, soit 81,2 %.
- **Couverture industrielle indicative :** 18 notices candidates obtenues par
  recherche de mots-clés dans les dénominations et appellations. Ce nombre inclut
  au moins un faux positif et doit être contrôlé manuellement.
- **Exemples :** filatures de la Martinique et de Rochefort, briqueterie des
  Chauffetières, usine Bohin, Forges de Varenne, minoteries, scieries, tuileries et
  moulins à papier.
- **Limite centrale :** cette source mesure la protection juridique, pas
  l'existence de tout le patrimoine industriel. Une absence ne signifie ni
  disparition ni absence d'intérêt patrimonial.
- **Licence :** Licence Ouverte 2.0 ; mise à jour hebdomadaire annoncée.
- **Décision :** `enrichissement`, `P1`, `validee`.

## 2. Source d'élargissement

### CASIAS

- **Producteur :** Géorisques / services de l'État.
- **Unité :** ancien site industriel ou activité de service inventorié ; les
  lignes d'un export CSV national peuvent aussi représenter une relation avec une
  commune.
- **Accès testé :** couche WFS Normandie
  `ms:drealnorm_casias_s_r28`, filtrée sur `code_depar=61` ; service en EPSG:2154.
- **Résultat :** 2 052 identifiants `code_inven` distincts, sans doublon interne
  observé dans cette couche.
- **Qualité spatiale :** 209 lignes seulement ont `x_wgs84/y_wgs84` ; 1 853 sont
  déclarées « Site non gélocalisé ». La géométrie surfacique du WFS peut
  représenter la commune : elle ne doit pas être publiée comme emprise du site.
- **Complétude :** 1 020 lignes sans nom d'établissement ; `activite_p` vide sur
  toute la couche testée ; 1 333 états « Indéterminé » et 719 « En arrêt ».
- **Bruit :** garages, stations-service, blanchisseries et autres activités sans
  intérêt patrimonial direct. Une classification des activités et une validation
  documentaire sont obligatoires.
- **Précaution :** CASIAS ne prouve ni pollution ni valeur patrimoniale et n'est
  pas exhaustif. Le CSV national pourra contenir davantage d'informations
  d'activité que la couche régionale WFS.
- **Décision :** `elargissement`, `P1`, `validee_avec_reserves`.

## 3. Sources géographiques

### IGN / Géoplateforme

- WFS et WMTS testés ; le catalogue WFS contient de nombreuses couches et impose
  de fixer précisément le produit, la couche et le millésime avant extraction.
- Le géocodeur Géoplateforme répond sur les lieux-dits et adresses. Un test sur
  « Forges de Varenne, Champsecret » a renvoyé un lieu-dit plausible, mais ce point
  ne constitue pas une emprise patrimoniale validée.
- **Décision :** `contexte_geographique`, `P1`, `validee_avec_reserves`.

### Cadastre ouvert

- Fichiers par département disponibles en GeoJSON et Shapefile, avec couches
  communes, sections, feuilles, lieux-dits, parcelles, subdivisions et bâtiments.
- Le fichier GeoJSON compressé des parcelles de l'Orne au millésime 1er juin 2026
  a répondu correctement ; taille observée : environ 97 Mo.
- Le cadastre actuel sert à contrôler une localisation ou une emprise actuelle ;
  il ne prouve pas une emprise historique et ne renseigne pas le propriétaire.
- **Décision :** `contexte_geographique`, `P1`, `validee_avec_reserves`.

### Base Adresse Nationale

- Fichier départemental `adresses-61.csv.gz` accessible ; taille observée :
  environ 6,4 Mo ; Licence Ouverte.
- L'ancienne API `api-adresse.data.gouv.fr` est abandonnée : le projet utilisera
  le géocodeur de la Géoplateforme et les fichiers BAN.
- Une adresse ou un lieu-dit géocodé ne doit pas être transformé en localisation
  précise d'un site sans contrôle complémentaire.
- **Décision :** `contexte_geographique`, `P1`, `validee_avec_reserves`.

### Hydrographie

- La BD TOPAGE, produite par l'IGN, l'OFB et le Sandre, est retenue pour les cours
  d'eau, plans d'eau, surfaces et tronçons hydrographiques.
- Licence Ouverte 2.0 ; diffusion documentée sur data.gouv.fr.
- Les distances aux cours d'eau seront des calculs du projet. Elles ne démontrent
  pas à elles seules l'usage de l'énergie hydraulique.
- **Décision :** `contexte_geographique`, `P1`, `validee_avec_reserves`.

### Forêts actuelles et forêts anciennes

- La BD Forêt v2 est retenue pour l'occupation forestière contemporaine ; son
  millésime peut être ancien selon le département et sa précision n'est pas
  cadastrale.
- La BD Forêts anciennes, construite par comparaison des cartes d'état-major vers
  1850 et de la BD Forêt v2, est ajoutée comme couche distincte. Elle est diffusée
  en WMS/WMTS et est plus pertinente pour étudier les anciennes forges au bois.
- La proximité d'une forêt actuelle ou ancienne reste un indice contextuel, jamais
  une preuve causale sans source historique.
- **Décision :** `contexte_geographique`, `P2` pour la BD Forêt actuelle et `P1`
  pour les forêts anciennes ; `validee_avec_reserves`.

### Géologie et ressources minières — BRGM

- Le service WFS Géologie du BRGM a répondu au test `GetCapabilities`.
- Les cartes géologiques harmonisées à 1/50 000 (Charm-50) fournissent des couches
  vectorielles continues ; des téléchargements et services WMS/WFS sont proposés.
- La licence ou les conditions devront être enregistrées produit par produit au
  téléchargement : les métadonnées observées ne sont pas uniformes.
- La géologie aide à formuler des hypothèses sur les matériaux et minerais, mais
  ne remplace pas les archives d'exploitation.
- **Décision :** `contexte_geographique`, `P2`, `validee_avec_reserves`.

### Réseau ferroviaire

- Pour le réseau actuel, les données SNCF et la BD TOPO sont disponibles ; la
  couche doit distinguer lignes exploitées, neutralisées et déposées.
- Aucun jeu national unique et suffisamment documenté n'a été trouvé pour toutes
  les lignes historiques de l'Orne. Leur reconstruction reposera sur les cartes et
  fonds des Archives de l'Orne, complétés au besoin par les cartes d'état-major.
- Le rail historique sera donc une donnée interprétée ou numérisée, avec cote,
  date et niveau de confiance.
- **Décision :** `contexte_geographique`, `P2`, `validee_avec_reserves`.

### OpenStreetMap

- Un test Overpass sur l'aire INSEE 61 a fonctionné sur un miroir public ; la
  requête `man_made=works` a retourné 55 objets au moment du test.
- Ce résultat illustre le caractère d'appoint de la source : couverture et tags
  dépendent des contributions, et `works` ne décrit pas tout le patrimoine.
- Licence ODbL avec attribution « © les contributeurs OpenStreetMap » et
  obligation de partage à l'identique dans les cas prévus par la licence.
- Les instances publiques Overpass sont limitées et ne doivent pas servir de
  service de production intensif.
- **Décision :** `verification`, `P2`, `validee_avec_reserves`.

## 4. Sources éditoriales

### Archives départementales de l'Orne

- Les inventaires et pages thématiques recensent des fonds d'entreprises et de
  sites directement pertinents : laiteries, Fonderie du Perche, forges de
  Saint-Evroult et d'Aube, Société cotonnière de Flers, tissages, minoteries et
  mines de La Ferrière-aux-Étangs et de La Halouze.
- Des ressources portent aussi sur l'industrialisation textile et le développement
  ferroviaire.
- L'accès est principalement documentaire et manuel. Les cotes constituent les
  identifiants à conserver.
- Les droits de reproduction et de diffusion doivent être contrôlés pour chaque
  image ou document.
- **Décision :** `verification`, `P2`, `validee_avec_reserves`.

### Gallica

- L'API SRU a répondu à une recherche combinant « forge » et « Orne » ; les notices
  XML et identifiants ARK peuvent être collectés. OAI, OCR et IIIF complètent
  l'accès selon les documents.
- Les métadonnées sont sous Licence Ouverte avec attribution BnF/Gallica.
- La plupart des reproductions du domaine public sont librement réutilisables à
  titre non commercial avec mention de source ; la réutilisation commerciale et
  les collections partenaires suivent des règles spécifiques.
- La source est adaptée aux cartes, annuaires, presse, livres et iconographie,
  mais rarement à une géolocalisation directe.
- **Décision :** `verification`, `P2`, `validee_avec_reserves`.

### Sources touristiques, institutionnelles et exploitants

- Elles peuvent confirmer l'état actuel, l'ouverture, la visitabilité, l'usage et
  des coordonnées pratiques. Le site de la Visite des ateliers Bohin démontre la
  valeur de ce type de source pour une usine encore active et visitable.
- Ces informations changent vite : elles doivent être datées et revérifiées avant
  publication. Elles ne sont pas une preuve suffisante pour l'histoire du site.
- Les textes et photographies restent protégés sauf mention contraire.
- **Décision :** `verification`, `P3`, `validee_avec_reserves`.

## 5. Droits et images

Règles retenues pour le socle :

- enregistrer séparément la licence des métadonnées et les droits du média ;
- ne jamais recopier une image parce qu'elle est seulement visible en ligne ;
- conserver l'auteur, le détenteur, la source, l'URL, la date de consultation et
  la mention de crédit exigée ;
- utiliser par défaut les images comme références documentaires, sans les intégrer
  aux exports publics ;
- ouvrir un champ `media_reutilisable` uniquement après vérification explicite.

## 6. Sources et accès écartés pour la V1

| Élément écarté | Motif |
|---|---|
| ancienne API Adresse `api-adresse.data.gouv.fr` | service abandonné au profit de la Géoplateforme |
| géométrie communale CASIAS comme position du site | précision artificielle et potentiellement trompeuse |
| tuiles publiques OSM comme fond de production | service public non garanti pour un usage applicatif soutenu |
| sources touristiques comme preuve historique | contenu secondaire, variable et souvent non sourcé |
| photographie en ligne sans autorisation explicite | droits de diffusion non établis |

## 7. Hiérarchie en cas de contradiction

La hiérarchie dépend du type d'information :

1. **existence, activité et chronologie historiques :** dossier d'Inventaire,
   archive primaire, puis publication historique documentée ;
2. **protection juridique :** données Monuments historiques les plus récentes ;
3. **adresse et commune actuelles :** données officielles actuelles, puis source de
   l'exploitant ;
4. **position ou emprise :** observation ou plan vérifié, cadastre, coordonnées de
   notice, géocodage, puis OSM ;
5. **usage, conservation et accès actuels :** observation datée ou exploitant,
   puis institution locale ;
6. **site industriel supplémentaire :** CASIAS crée un candidat à vérifier, jamais
   une inclusion automatique.

Les valeurs contradictoires restent enregistrées avec leurs sources. La hiérarchie
sert à choisir une valeur de publication, pas à supprimer les autres mentions.

## 8. Programme d'extraction test recommandé

Ordre de la phase 2 :

1. dix dossiers de l'Inventaire couvrant plusieurs secteurs et niveaux de
   géolocalisation ;
2. l'ensemble des Monuments historiques de l'Orne, puis contrôle manuel des
   candidats industriels ;
3. les lignes Palissy liées aux références Mérimée sélectionnées ;
4. un échantillon CASIAS stratifié entre sites localisés, non localisés et types
   d'activités ;
5. BAN, cadastre et BD TOPAGE uniquement sur les communes de l'échantillon ;
6. forêts anciennes, géologie et rail sur quelques cas éditorialement justifiés.

Ce séquençage teste d'abord la constitution des sites et les rapprochements, avant
de télécharger des couches géographiques départementales volumineuses.
