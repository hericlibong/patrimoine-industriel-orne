# Licences des données et droits des images

Version 1.0 — 22 juillet 2026

Ce document fixe les règles de travail du projet. Il ne remplace pas un avis
juridique pour un cas complexe ou une exploitation commerciale particulière.

## Situation du socle pilote

Le socle V1 ne contient aucune photographie patrimoniale destinée à la
publication. Les URL de notices sont conservées, mais leurs images ne sont ni
téléchargées ni redistribuées.

Les deux PNG versionnés dans `reports/quality/` sont des visuels techniques
produits par le projet à partir des données du pilote. Ils servent au contrôle
interne et ne constituent pas des illustrations éditoriales prêtes à publier.
Le projet QGIS référence un fond OpenStreetMap pour le contrôle interactif ;
toute carte publiée devra afficher l'attribution correspondante.

## Règle générale

Une donnée ouverte et l'image affichée à côté de cette donnée peuvent relever
de régimes différents. Une notice librement réutilisable ne rend pas
automatiquement sa photographie libre de droits.

Une image n'entre dans une publication que si les éléments suivants sont
renseignés :

- source et URL pérenne ;
- auteur ou photographe, si connu ;
- détenteur des droits ;
- licence ou autorisation écrite ;
- usages autorisés, notamment commercial ou non commercial ;
- crédit obligatoire ;
- date de la vérification ;
- copie ou URL de la preuve.

En l'absence de réponse, le statut est `droits_inconnus` et l'image est exclue
de la publication. Une simple présence sur Internet, un bouton de téléchargement
ou une image ancienne ne constitue pas une autorisation.

## Conditions par famille de sources

### POP — Mérimée et Palissy

Les données descriptives sont réutilisables sous Licence Ouverte 2.0 sauf
mention ou régime spécifique. POP précise cependant que des tiers peuvent
détenir des droits sur les images ; une autorisation de l'auteur ou des ayants
droit peut être nécessaire. La vérification se fait notice par notice, en
conservant le champ de copyright et le service producteur.

Références officielles : [conditions générales de POP](https://pop.culture.gouv.fr/conditions-generales-utilisation),
[données ouvertes de POP](https://pop.culture.gouv.fr/donnees-ouvertes) et
[centre d'aide POP](https://pop.culture.gouv.fr/aide).

### Inventaire du patrimoine de Normandie

Les mentions légales indiquent que la structure, les textes et les images du
site sont protégés et qu'une reproduction nécessite une autorisation expresse,
sauf mention contraire. Pour la V1, les faits et références sont structurés,
mais les photographies du site ne sont pas reprises.

Référence officielle : [mentions légales de l'Inventaire normand](https://inventaire-patrimoine.normandie.fr/mentions-legales).

### Archives départementales de l'Orne

Les droits dépendent du statut du fonds, du document, de l'auteur et des
conditions fixées par un déposant. La cote et la possibilité de consultation ne
suffisent pas à autoriser une reproduction publique. Toute image retenue devra
faire l'objet d'une vérification auprès du service.

Référence officielle : [consultation et réutilisation des archives privées](https://archives.orne.fr/index.php/particuliers-detenteurs-darchives-privees).

### Gallica

Les métadonnées relèvent de la Licence Ouverte. La réutilisation non commerciale
de nombreux documents numérisés du domaine public est libre avec la mention
`Source gallica.bnf.fr / Bibliothèque nationale de France`. Une réutilisation
commerciale ou un document soumis à un régime particulier peut nécessiter une
licence ou une autorisation. La fiche du document reste décisive.

Référence officielle : [conditions d'utilisation de Gallica](https://gallica.bnf.fr/accueil/fr/html/conditions-dutilisation-de-gallica).

### OpenStreetMap

Les données OpenStreetMap sont sous ODbL 1.0. Une carte publique doit présenter
une attribution lisible à OpenStreetMap et donner accès aux informations de
licence. Le projet ne prévoit pas d'utiliser le serveur public de tuiles OSM
comme infrastructure de production soutenue.

Références officielles : [règles d'attribution de l'OSMF](https://osmfoundation.org/wiki/Licence/Attribution_Guidelines)
et [politique du serveur public de tuiles](https://operations.osmfoundation.org/policies/tiles/).

### Données publiques géographiques

La Licence Ouverte 2.0 autorise la reproduction, l'adaptation et la
redistribution, y compris commerciale, sous réserve d'indiquer la source et la
date de mise à jour. Cette règle couvre notamment les jeux explicitement placés
sous cette licence par CASIAS, la BAN et les produits IGN utilisés. Pour le
BRGM, la Licence Ouverte 2.0 s'applique sauf exception annoncée ; la source BRGM
et la date de mise à jour doivent être citées.

Références officielles : [Licence Ouverte 2.0](https://www.etalab.gouv.fr/wp-content/uploads/2017/04/ETALAB-Licence-Ouverte-v2.0.pdf),
[conditions des données InfoTerre](https://infoterre.brgm.fr/page/conditions-dutilisation-donnees),
[contenu et licence de la BAN](https://adresse.data.gouv.fr/contenu-de-la-ban)
et [jeu CASIAS Normandie](https://www.data.gouv.fr/datasets/carte-des-anciens-sites-industriels-et-activites-de-services-casias-normandie).

### Sites institutionnels, touristiques et exploitants

Les pages EDF, Bohin, Département de l'Orne, offices de tourisme et exploitants
peuvent confirmer une information contemporaine. Leurs textes et images ne sont
pas copiés sans licence explicite ou autorisation. Un lien et une courte
reformulation factuelle sourcée sont privilégiés.

## Registre à créer lors de l'enrichissement photographique

| Champ | Rôle |
|---|---|
| `image_id` | identifiant interne stable |
| `site_id` | site illustré |
| `source_id` | producteur ou collection |
| `url_source` | page ou identifiant pérenne |
| `auteur` | auteur ou photographe |
| `detenteur_droits` | personne ou institution à contacter |
| `licence_code` | licence explicite ou `droits_inconnus` |
| `usage_autorise_code` | interne, éditorial, commercial, tous usages |
| `credit_obligatoire` | formulation à afficher |
| `preuve_droits` | URL, courriel ou convention conservée |
| `date_verification` | date du dernier contrôle |
| `decision_publication` | utilisable, autorisation requise ou exclue |

## Validation avant publication

- aucune image `droits_inconnus` dans le paquet public ;
- attribution visible sur chaque image ou dans une légende clairement reliée ;
- attribution cartographique présente dans toute carte statique ou interactive ;
- crédits et licences conservés dans les métadonnées exportées ;
- nouvelle vérification si la publication change de cadre économique ou de
  support.
