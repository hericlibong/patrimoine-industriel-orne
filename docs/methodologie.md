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
