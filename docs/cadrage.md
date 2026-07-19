# Cadrage du projet

Statut : **validé — version 1.0 du 19 juillet 2026**

## Définition

Construire un socle de données vérifiable permettant de raconter comment
l'industrie a façonné le territoire de l'Orne et ce qu'il en reste aujourd'hui.

## Intention éditoriale

Le projet doit permettre de lire autrement les paysages actuels de l'Orne :
vallées, forêts, bourgs, bâtiments conservés, lieux reconvertis et sites
disparus gardent les traces d'une ancienne géographie industrielle.

Le projet ne doit pas opposer une Orne industrielle passée à une Orne rurale
actuelle. Il doit montrer leurs relations : eau, bois, minerai, agriculture,
bourgs, rail et ressources locales.

## Questions éditoriales

1. Où étaient les sites industriels dans l'Orne ?
2. Quelles activités dominaient ?
3. Pourquoi ces sites étaient-ils implantés là ?
4. Que reste-t-il aujourd'hui ?

## Premier livrable

Le premier livrable n'est pas l'application. C'est un socle comprenant :

- un registre des sources vérifiées ;
- des extractions tests ;
- un modèle et un dictionnaire des données ;
- des classifications contrôlées ;
- un échantillon pilote géolocalisé ;
- une méthode de rapprochement des sources ;
- une documentation des limites et incertitudes.

## Forme finale envisagée

Une publication web narrative et cartographique combinant :

- un récit guidé ;
- une carte exploratoire ;
- des filtres ;
- des fiches de sites ;
- une méthodologie et des sources visibles.

## Hors périmètre de l'initialisation

- développement de l'interface publique ;
- cartographie immédiate des quelque 2 500 sites historiques ;
- plateforme participative ;
- application mobile native ;
- numérisation exhaustive des archives ;
- vérification photographique de tous les sites.

## Périmètre géographique

- Le corpus principal couvre les limites actuelles du département de l'Orne.
- La commune actuelle et, lorsqu'elle diffère, la commune historique sont
  conservées séparément.
- Un site non localisé précisément peut entrer dans le corpus si sa présence
  dans une commune de l'Orne est documentée. Il reste classé `non_localise` et
  n'est pas placé artificiellement au centre de la commune.

## Périmètre chronologique

- Aucune borne ancienne arbitraire : le projet part de la première activité
  industrielle ou proto-industrielle documentée dans les sources.
- Pour entrer dans le corpus principal V1, un site doit avoir connu au moins
  une activité industrielle avant ou pendant l'année 1950.
- L'histoire du site est suivie jusqu'à sa situation contemporaine.
- Un établissement créé uniquement après 1950 n'entre pas dans le corpus
  principal. Il peut être enregistré comme site lié s'il constitue le
  successeur direct, le transfert ou la continuité d'un établissement ancien.

## Définition opérationnelle d'un site industriel

Un site industriel est une emprise géographique distincte, située dans l'Orne
et attestée par une source traçable, où s'est déroulée une activité organisée
d'extraction, de transformation, de fabrication ou de production d'énergie à
destination productive.

La disparition du bâti n'exclut pas le site. Le site peut être conservé,
transformé, ruiné ou disparu.

Une activité artisanale ou un petit atelier n'est retenu que si une source
patrimoniale le classe dans le corpus industriel ou si la documentation établit
une production organisée, mécanisée ou en série dépassant l'usage domestique.

## Critères d'inclusion

Un site entre dans le corpus principal s'il respecte les critères suivants :

1. il est situé dans les limites actuelles de l'Orne ;
2. son existence est attestée par au moins une source identifiable ;
3. il répond à la définition opérationnelle ci-dessus ;
4. il possède au moins une activité documentée au plus tard en 1950 ;
5. sa localisation communale est connue, même si son emplacement exact ne
   l'est pas.

Sont notamment admissibles :

- mines, carrières et autres sites extractifs documentés ;
- forges, affineries, fonderies et travail des métaux ;
- moulins lorsqu'une production est identifiée ;
- manufactures, usines et ateliers répondant aux critères ;
- filatures, papeteries, scieries, verreries, tuileries et briqueteries ;
- laiteries, cidreries, minoteries et autres transformations agroalimentaires ;
- installations de production d'énergie directement associées à l'industrie ;
- sites disparus dont l'existence et la commune sont documentées.

## Critères d'exclusion

Sont exclus du corpus principal :

- exploitations ou bâtiments agricoles sans activité de transformation
  documentée ;
- artisanat domestique ou atelier isolé sans preuve d'organisation productive ;
- commerces, stations-service, garages et dépôts connus uniquement par CASIAS,
  sans intérêt industriel ou patrimonial établi ;
- sièges administratifs sans activité productive sur place ;
- infrastructures générales sans relation fonctionnelle directe avec un site ;
- lieux supposés sans source traçable ;
- établissements créés uniquement après 1950, sauf comme sites liés ;
- inscription dans CASIAS considérée, à elle seule, comme preuve patrimoniale ou
  comme preuve de pollution.

Les cas limites sont conservés dans une file `a_verifier` et ne sont pas
intégrés silencieusement au corpus principal.

## Sites successifs, composites et déplacés

- Une emprise continue conserve un seul `site_id`, même si ses activités, ses
  exploitants ou ses usages changent. Chaque phase est enregistrée séparément.
- Deux emprises physiquement distinctes constituent deux sites, même si elles
  portent le même nom ou appartiennent à la même entreprise.
- Un transfert d'activité crée deux sites reliés par une relation
  `transfert_vers` ou `successeur_de`.
- Un grand ensemble peut comporter un site parent et des composants localisés.
- Les composants ne doivent pas être comptés une seconde fois comme sites
  indépendants dans les statistiques portant sur les établissements.
- En cas de doute, les notices restent séparées et une proposition de
  rapprochement est enregistrée pour vérification.

La table `relations_sites` est donc nécessaire dans le modèle V1.

## Traitement des infrastructures

Les infrastructures sont réparties en trois niveaux :

1. **Site principal** : installation ayant sa propre fonction productive,
   extractive ou énergétique et une identité documentaire autonome.
2. **Composant** : barrage, canal, bief, cheminée, logement ouvrier,
   embranchement ferroviaire ou autre élément directement rattaché à un site.
3. **Contexte cartographique** : cours d'eau, forêt, réseau ferroviaire général,
   géologie, routes et ressources territoriales. Ces éléments expliquent les
   implantations mais ne sont pas comptés comme sites industriels.

## Validation de la phase 0

Ces règles constituent le périmètre opérationnel de départ. Elles pourront être
révisées après les extractions tests, mais toute modification devra être
versionnée et inscrite dans le journal des décisions.
