# Méthodologie

## Principes de collecte

1. Auditer une source avant de l'extraire massivement.
2. Archiver le fichier ou la réponse d'origine sans modification.
3. Enregistrer la date de récupération et l'URL précise.
4. Ne jamais écraser une correction manuelle par un traitement automatique.
5. Rendre chaque export reproductible par un script.

Les règles de nommage, d'horodatage et de métadonnées techniques sont définies
dans `docs/conventions_extraction.md`.

## Nature des informations

Chaque information doit pouvoir être identifiée comme :

- `sourcee` : présente explicitement dans une source ;
- `calculee` : produite par un traitement reproductible ;
- `interpretee` : issue d'une décision éditoriale documentée.

## Rapprochement des sources

Aucune fusion ne doit reposer sur le seul nom du site. Les rapprochements
utiliseront, selon leur disponibilité :

- identifiant officiel ;
- commune et code INSEE ;
- adresse ou lieu-dit ;
- coordonnées ou parcelle ;
- dénomination et variantes ;
- activité et période.

Les rapprochements ambigus seront conservés comme propositions à vérifier.

## Comptage des sites

Un enregistrement provenant d'une source n'est pas automatiquement un site.
Le projet distingue cinq niveaux :

1. `notice_source` : ligne, notice ou dossier tel que fourni par une source ;
2. `site_candidat` : implantation industrielle possible, encore à vérifier ;
3. `site_rapproche` : plusieurs mentions ont été réunies autour d'une même
   emprise ou d'un même établissement ;
4. `site_cartographiable` : site rapproché disposant d'une localisation dont la
   précision est connue ;
5. `site_publie` : site cartographiable ayant passé le contrôle éditorial.

Le nombre de notices, notamment les 319 dossiers de l'Inventaire ou les entrées
CASIAS, ne doit jamais être présenté comme le nombre définitif de sites.

Le décompte final sera produit après :

- rapprochement des références entre sources ;
- détection des doublons et des sites composites ;
- distinction des déplacements, successions et changements d'activité ;
- application des critères d'inclusion chronologique et thématique ;
- qualification de la précision géographique ;
- contrôle des cas ambigus.

À chaque livraison, les nombres de notices, candidats, sites rapprochés, sites
cartographiables et sites publiés seront indiqués séparément.

## Géolocalisation

La précision doit être enregistrée séparément des coordonnées. Un centroïde de
commune ne doit jamais être présenté comme l'emplacement vérifié d'un bâtiment.

Pour le pilote, les points et contours présents dans POP constituent la première
localisation de travail. Leur validité numérique et leur présence dans
l'enveloppe de l'Orne sont contrôlées automatiquement, mais ils restent
`geometrie_approximative` jusqu'à une vérification cartographique.

Seules les adresses comportant un numéro unique sont géocodées automatiquement
avec le service BAN de la Géoplateforme. Le résultat doit viser la même commune,
avoir un score d'au moins 0,65 et se trouver à moins de 250 mètres du point POP.
Une rue sans numéro, une plage ou plusieurs numéros ne produit aucun point.

La parcelle actuelle est recherchée par intersection du point POP avec le
Parcellaire Express via API Carto. Elle reste une parcelle candidate : cette
intersection ne prouve ni l'emprise historique, ni la propriété, ni la présence
actuelle du site. Une référence cadastrale ancienne différente n'est pas une
erreur automatique, le parcellaire pouvant avoir évolué.

### Contrôle cartographique

La carte QGIS de contrôle superpose les points POP, les contours documentaires,
les parcelles candidates et les résultats BAN. Les points sont testés contre
l'enveloppe de l'Orne, la transformation Lambert-93/WGS84, le code communal de
la parcelle, l'intersection avec cette parcelle et les quasi-doublons à moins de
50 mètres.

Une emprise est soumise à relecture lorsque le point se trouve à plus de cinq
mètres de son contour, lorsqu'elle manque ou lorsque sa surface est inférieure à
100 m² ou supérieure à 100 000 m². Ces seuils sont des détecteurs d'anomalies,
pas une définition de la taille normale d'un site industriel.

Chaque cas signalé reçoit une décision et une note. Le contrôle ne déplace
jamais automatiquement un point et ne relève jamais la précision d'une
géométrie sur la seule base de sa cohérence visuelle.

## Contexte territorial

Les distances aux cours d'eau, formations forestières, indices miniers et voies
ferrées sont calculées depuis le point POP provisoire. Les couches sont demandées
en WGS84, puis les calculs et contrôles de système utilisent le Lambert-93 quand
cela est nécessaire.

Les seuils sont enregistrés avec les résultats et servent uniquement à regrouper
des distances. Aucun seuil ne transforme une proximité en relation historique.
Les couches contemporaines ou récentes ne sont jamais décrites comme une
reconstitution du paysage industriel ancien.

Le contexte géologique utilise une lithologie simplifiée au 1:1 000 000. Les
indices BRGM de mines et de gîtes sont recherchés dans un rayon de 10 km. Ces
deux résultats servent à repérer des pistes de recherche ; ils ne prouvent ni
l'approvisionnement, ni l'exploitation par le site étudié.

## Situation actuelle

La conservation, l'usage et l'accessibilité sont trois informations distinctes.
Elles doivent comporter une source et une date de vérification.

Chaque observation contemporaine comporte au minimum :

- la valeur observée ;
- la date d'observation ou de consultation ;
- la source ;
- la méthode de vérification ;
- le niveau de fiabilité.

Avant publication :

- l'accessibilité et la visitabilité doivent avoir été vérifiées dans les trois
  derniers mois ;
- l'usage actuel et la conservation doivent avoir été vérifiés dans les douze
  derniers mois ;
- les protections juridiques doivent être rafraîchies depuis la source
  officielle dans les trente derniers jours.

Une information plus ancienne n'est pas supprimée : elle est signalée comme
ancienne et passe au statut `a_verifier` pour l'affichage contemporain.

## Citations et provenance

- Toute information retenue doit renvoyer à une entrée de `mentions_sources`.
- La mention conserve l'identifiant de la source, la référence de la notice ou
  la cote, l'URL lorsqu'elle existe et la date de consultation.
- La valeur originale est conservée avant normalisation.
- Une transformation automatique doit être reliée au script et à sa version.
- Une interprétation éditoriale doit être explicitement marquée comme telle.
- La publication affiche au minimum la source principale de chaque fiche et sa
  date de dernière vérification.
- Une source secondaire ne remplace pas une source primaire disponible.

## Contradictions entre sources

Les informations contradictoires sont conservées ; aucune valeur n'est écrasée
silencieusement.

La priorité dépend du type d'information :

- statut juridique : source officielle du ministère de la Culture ;
- faits historiques : archives et dossiers d'Inventaire, selon la précision et
  la date des travaux ;
- localisation : cadastre, plans, orthophotographies et observations spatiales
  vérifiables ;
- usage et accès actuels : observation récente, propriétaire ou exploitant,
  puis source institutionnelle locale.

Lorsqu'une contradiction correspond à deux périodes différentes, elle est
représentée comme une évolution. Lorsqu'elle reste irrésolue, la valeur publiée
est marquée `a_verifier`, les versions concurrentes sont conservées et le choix
éditorial est documenté.

## Images

La présence d'une image en ligne ne vaut pas autorisation de réutilisation. Les
droits, crédits et conditions de diffusion doivent être enregistrés avant toute
publication.

## Documentation des limites

Les limites rencontrées sont consignées dans
`reports/quality/limites.md`. Pour chaque limite, le projet enregistre :

- la source ou l'étape concernée ;
- le problème observé ;
- son effet possible sur les résultats ou le récit ;
- les sites ou données concernés lorsque cela peut être mesuré ;
- la solution appliquée ou la vérification nécessaire ;
- le statut de résolution et la date du constat.

Une limite non résolue n'interdit pas nécessairement la publication, mais elle
doit être visible dans le rapport de qualité et ne doit jamais être compensée par
une précision inventée.

## Évaluation des extractions tests

L'évaluation de la phase 2 est calculée à partir du manifeste versionné des
fichiers bruts. Le fichier `reports/quality/phase2_evaluation_samples.json`
conserve les mesures détaillées et l'empreinte du manifeste utilisé.

Une valeur est considérée comme renseignée lorsqu'elle n'est ni nulle, ni une
chaîne vide, ni une collection vide. La complétude est mesurée champ par champ
sur chaque échantillon ; elle ne doit pas être extrapolée à la source complète
si l'échantillon est ciblé ou stratifié.

Les doublons internes sont recherchés sur les identifiants propres aux sources :
`IA` pour l'Inventaire et Mérimée, `PM` pour Palissy, `PA` pour les Monuments
historiques, `SSP` et `BNO` pour CASIAS. Un code INSEE répété n'est pas un
doublon : plusieurs sites peuvent appartenir à la même commune.

Le contrôle des coordonnées distingue :

- leur présence explicite ;
- leur validité numérique en WGS84 ;
- leur présence dans une enveloppe géographique large de l'Orne ;
- leur précision réelle, qui doit encore être qualifiée séparément.

Le contrôle d'enveloppe ne valide jamais l'emplacement d'un bâtiment. Une
géométrie CASIAS n'est pas utilisée lorsque les champs WGS84 explicites sont
absents ou que la fiche est déclarée non géolocalisée.

L'automatisation est évaluée séparément pour l'acquisition, le parsing et la
publication. Une extraction automatisable peut produire un simple candidat :
l'inclusion patrimoniale, les rapprochements incertains et la situation actuelle
restent soumis à une validation humaine.

## Validation du modèle de données

Le modèle V1 est validé sur cinq scénarios reproductibles : site simple, site
multi-activités, site reconverti, site disparu et rapprochement incertain. Les
cas sont synthétiques et ne sont jamais mélangés au futur corpus réel.

Chaque scénario est chargé dans une base DuckDB neuve, puis contrôlé par des
requêtes automatisées et par le validateur transversal. Une validation réussie
signifie que la structure représente le cas sans duplication, perte d'historique
ou précision géographique inventée. Elle ne prouve pas la qualité des sources.

Un rapprochement incertain conserve deux UUID et crée une proposition à
vérifier. Aucun score de similarité, même élevé, ne déclenche de fusion. La
décision et sa date doivent être enregistrées avant de désigner un site
canonique.

## Classification des activités industrielles

La classification sectorielle s'applique à chaque phase d'activité, pas au site
entier. Le libellé original reste dans `activite_libelle_source`; le code
normalisé est ajouté sans le remplacer.

Les correspondances exactes répertoriées dans `config/classifications.yml`
peuvent être appliquées automatiquement. Un terme absent du registre, une
production multiple dans un même libellé ou une chronologie ambiguë exige une
revue humaine. `HIST` est relu même lorsque `DENO` est classé, car il peut révéler
une conversion ultérieure.

Un site multi-secteurs conserve plusieurs lignes `activites`. Pour les filtres,
il apparaît dans tous ses secteurs documentés. Pour un total global, les lignes
sont dédupliquées par `site_id`; la somme des secteurs peut donc dépasser le
nombre de sites.

Activité, installation, bâtiment, énergie et rôle énergétique sont traités
séparément. Un bâtiment ne permet pas, à lui seul, de déduire une production.

## Chronologie et situation actuelle

Les périodes historiques sont des catégories analytiques calculées à partir des
intervalles conservés dans le modèle. Elles ne remplacent ni les dates ni les
expressions originales des sources. Une activité qui chevauche une frontière
chronologique est rattachée aux deux périodes.

Conservation, usage actuel et accessibilité sont des observations contemporaines
distinctes. Elles doivent être datées et ne sont publiées comme actuelles que
pendant leur durée de fraîcheur. « Désaffecté » qualifie l'arrêt d'une activité,
pas l'état matériel du site.

Plusieurs usages peuvent être enregistrés pour une même observation. Les droits
d'accès ne sont jamais déduits de la simple visibilité depuis l'espace public.
Une visite possible doit être attestée par une information récente.

Les protections sont enregistrées mesure par mesure. Le type juridique, la
portée, l'élément protégé et le statut de la mesure restent séparés. L'Inventaire
général est une source de connaissance et ne constitue pas, à lui seul, une
protection juridique.

## Qualité des classifications

La précision géographique décrit ce que la géométrie localise réellement. Elle
est distincte de la forme stockée, de la méthode de localisation et de la
fiabilité de la preuve. Une coordonnée fournie par une source reste une
coordonnée source tant que son rattachement au site n'a pas été contrôlé.

La fiabilité est attribuée à chaque information ou relation : `forte`, `moyenne`
ou `faible`. Elle ne se déduit ni du prestige d'une source, ni du seul nombre de
sources. `a_verifier` reste un statut de travail distinct.

`autre` sert à conserver une valeur connue absente du vocabulaire ; `inconnu`
signifie qu'une question applicable a été examinée sans réponse. Un champ vide
dans une source reste `NULL` avec son statut de provenance.

La reproductibilité technique est contrôlée en rejouant les classifications
avec les mêmes entrées dans un ordre différent. Les sorties sont triées et
associées à une empreinte SHA-256.

Un double classement humain avait été préparé pour mesurer l'accord entre deux
lecteurs. Il est reporté, car sa charge est disproportionnée au stade du pilote
et il ne contrôle pas l'exactitude historique des données. Cette absence ne
bloque pas le corpus V1 : les sources, les règles et les niveaux de confiance
sont conservés, mais les catégories interprétatives restent révisables. Le test
ne sera réexaminé que si des désaccords récurrents apparaissent ou si un
partenaire demande une validation formelle avant publication.

## Échantillon pilote

Le pilote est composé par échantillonnage raisonné à quotas dans les 319 dossiers
de l'Inventaire normand. L'unité de sélection est un dossier `IA` candidat, et
non encore un site canonique du projet.

La sélection vise la diversité utile au test : six macro-zones, au moins sept
secteurs, plusieurs périodes et états matériels, des protections différentes et
des localisations de difficulté variée. Les cas difficiles sont volontairement
surreprésentés ; les résultats du pilote ne sont donc pas extrapolables au corpus
complet.

Les valeurs utilisées pour composer l'échantillon sont des signaux provisoires.
Elles ne sont versées au modèle comme faits qu'après lecture de la notice,
rapprochement des sources et contrôle. La conservation ancienne n'est jamais
présentée comme actuelle, et l'absence de protection repérée n'est pas traitée
comme une preuve juridique d'absence.

## Enrichissement du pilote

Chaque dossier `IA` reçoit un UUID v4 stable enregistré dans
`config/enrichissement_pilote.yml`. La référence `IA` est conservée comme
identifiant externe et ne sert jamais de clé interne.

Les dénominations `DENO` sont séparées en phases d'activité. Le texte `HIST` est
relu pour ordonner les conversions, ajouter une phase absente de `DENO` et
conserver les expressions de dates telles que « vers 1840 ». Une chronologie
ambiguë reste marquée `ordre_a_verifier`.

Un rapprochement MH n'est confirmé que lorsque la notice `PA` renvoie directement
à la référence `IA`. Une commune, un nom voisin ou le mot « forge » ne suffisent
pas. De même, un objet Palissy sans référence Mérimée directe reste un lien
candidat, avec une confiance faible, même si l'édifice et la commune concordent.

La situation contemporaine est une observation séparée. Une destination relevée
par l'Inventaire dans les années 1980 est conservée comme observation historique,
mais n'est pas recopiée comme situation 2026. En l'absence de source récente,
la valeur actuelle est explicitement `inconnu`.

Le corpus de travail est reconstruit avec
`python -m patrimoine_orne.enrich.pilot`. Les données dérivées sont écrites dans
`data/interim/phase5_pilot_enriched.json` et le contrôle versionné dans
`reports/quality/phase5_enrichissement_pilote.json`.

## Validation du pilote

Chaque fiche est relue avec la même grille : identité, communes, activités,
chronologie, protections, objets, situation actuelle, provenance et décision de
maintien dans le pilote. La liste des trente contrôles est conservée dans
`config/validation_pilote.yml`.

La présence d'une source est contrôlée pour le nom du site, la commune actuelle,
chaque activité, chaque protection, chaque objet et toute valeur contemporaine
qui n'est pas `inconnu`. Une inconnue justifiée n'est pas une information sans
source : elle indique précisément qu'aucune preuve récente suffisante n'a été
retenue.

Le contrôle documentaire manuel des trente fiches, l'audit de provenance et les
tests automatiques constituent la validation requise du pilote. Le protocole de
double classement préparé sur six cas est conservé comme possibilité future,
mais il n'est ni réalisé ni présenté comme une validation acquise.

## Consolidation et exports du socle pilote V1

Le socle pilote est reconstruit par une commande unique à partir du corpus V1
de phase 5 et des résultats géographiques validés en phase 6. Les valeurs vides
sont normalisées en valeurs nulles, les listes sont ordonnées de manière
déterministe et les informations de provenance sont conservées.

DuckDB est le format de référence. Il conserve séparément les sites, activités,
états et usages actuels, protections, objets techniques, géométries,
identifiants externes et mentions de sources. Les identifiants des entités
dérivées sont générés de manière déterministe afin qu'une reconstruction
produise les mêmes relations.

CSV, Parquet et GeoJSON ont pour unité une ligne ou une entité par site. Ils
présentent une vue aplatie de la base : les activités, secteurs, communes et
autres valeurs multiples sont concaténés avec le séparateur `|`. Le GeoJSON
utilise le point WGS84 de référence ; il n'emploie pas le contour documentaire
comme emplacement certifié.

La validation finale compare le nombre de sites et l'ensemble de leurs
identifiants dans le corpus consolidé et dans les trois exports. Elle exécute
également les contrôles transversaux de la base DuckDB. Un écart ou une erreur
interrompt la production.

### Correction chronologique du 22 juillet 2026

La première production du socle ne projetait pas les périodes historiques dans
les exports. Les périodes avaient été définies et testées en phase 4, mais le
contrôle final vérifiait les formats, les identifiants et les effectifs sans
tester un usage éditorial élémentaire : filtrer le CSV par période. Le bloc de
consolidation a donc été rouvert et ce critère est désormais obligatoire.

Les expressions datées des phases d'activité sont normalisées selon les règles
du modèle. Le texte original reste conservé. Par exemple, `vers 1850` devient
un intervalle calculé de 1845 à 1855 et non une date exacte. Les périodes sont
ensuite calculées par chevauchement avec cet intervalle.

Deux provenances temporelles restent distinctes :

- `chronologie_phase` : période calculée depuis le début ou la fin documentée
  d'une activité ;
- `siecles_source_site` : période de repérage calculée depuis le champ `SCLE`
  de POP, qui date des campagnes de construction ou de transformation du site
  et ne prouve pas à lui seul toute la durée de l'activité industrielle.
- `situation_actuelle_documentee` : période contemporaine ajoutée au site
  uniquement lorsqu'une observation récente possède une source.

Le CSV des sites rassemble les périodes documentées pour faciliter le filtrage,
mais conserve séparément `periodes_activite_codes` et
`periodes_source_codes`. L'export `activites_pilote_v1.csv` possède une ligne
par phase d'activité et doit être utilisé pour relier une production à une
période sans mélanger les activités successives d'un même site.

Dans DuckDB, `activites_periodes_v1` fournit une ligne par relation entre une
phase d'activité et une période. Cette table dérivée est adaptée aux comptages
et aux croisements entre secteurs, productions et périodes.

## Passage au corpus complet par lots

La phase 8 n'assimile jamais les 319 dossiers sources à 319 sites. La recherche
avancée de l'API POP sur le cadre d'étude exact renvoie 320 notices. La notice
de présentation `IA61000851` est exclue, ce qui produit 319 références uniques
et concorde avec le total du portail régional.

Les notices des nouveaux lots sont conservées en JSON brut depuis l'API POP.
Le parseur HTML validé pendant les phases 2 et 5 reste une solution de repli.
Les dossiers sont traités par lots : 30 pilotes, 50 nouveaux dossiers dans le
lot de calibration, puis quatre lots de 50 et un dernier lot de 39.

Une référence IA crée seulement un candidat. Les activités successives peuvent
rester rattachées à une même emprise. Une fusion de dossiers ou une séparation
d'emprises exige une décision documentée. Le nombre canonique n'est calculé
qu'après la revue complète.
