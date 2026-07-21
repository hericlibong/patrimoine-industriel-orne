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
