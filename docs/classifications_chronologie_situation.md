# Classifications — chronologie et situation actuelle

Statut : **bloc 2 de la phase 4 validé le 21 juillet 2026**.

La source exécutable des vocabulaires est `config/classifications.yml`.

## Périodes historiques

| Code | Période | Usage analytique |
|---|---|---|
| `avant_1789` | avant 1789 | productions d'Ancien Régime et proto-industrie |
| `revolution_premiere_industrialisation` | 1789–1849 | transformations révolutionnaires et première industrialisation |
| `industrialisation_rail_vapeur` | 1850–1913 | essor industriel, rail et vapeur |
| `guerres_entre_deux_guerres` | 1914–1945 | guerres et entre-deux-guerres |
| `modernisation_apres_guerre` | 1946–1975 | modernisation d'après-guerre |
| `mutations_reconversions` | 1976–2000 | fermetures, mutations et reconversions |
| `periode_contemporaine` | depuis 2001 | patrimoine et usages contemporains |

Ces périodes sont des filtres calculés. Elles ne remplacent jamais les dates de
source. Un intervalle qui chevauche une limite appartient à toutes les périodes
concernées.

## Conservation

La classification décrit uniquement ce qui subsiste matériellement : `conserve`,
`degrade`, `partiellement_conserve`, `vestiges`, `ruine`, `disparu` ou `inconnu`.

« Désaffecté » ne décrit pas la conservation. Un bâtiment peut être désaffecté
et très bien conservé, ou encore exploité et dégradé. Ce terme est donc conservé
comme information sur l'activité, jamais converti en état matériel.

Toute valeur contemporaine porte une date de vérification. Sa fraîcheur de
publication est de 12 mois.

## Usages actuels

Un site peut avoir plusieurs usages simultanés. Chaque usage est une ligne de
`usages_actuels`, rattachée à l'observation datée dans `etats_actuels`. Un seul
peut être marqué principal.

La catégorie `usage_mixte` est interdite : les usages réels sont énumérés. Les
codes `sans_usage` et `inconnu` ne peuvent pas coexister avec un usage connu dans
la même observation. La fraîcheur de publication est de 12 mois.

## Accessibilité

La classification sépare :

- visite officiellement autorisée ;
- visite partielle ;
- visibilité depuis l'espace public ;
- propriété privée visible ou non visible ;
- impossibilité ou interdiction d'accès ;
- situation inconnue.

Voir un site depuis la voie publique ne donne aucun droit d'entrée. Le code
`visitable` exige une source récente indiquant les modalités de visite. La
fraîcheur de publication est de 3 mois.

## Protections

Chaque ligne représente une mesure distincte. Le type (`classe_mh`, `inscrit_mh`,
protection locale ou autre), la portée (totale, partielle ou inconnue), la cible
réellement protégée et le statut juridique sont séparés.

Être recensé dans l'Inventaire général n'est pas une protection juridique. Une
absence de mesure enregistrée n'autorise pas à publier « non protégé » : ce
statut exige une vérification officielle datée.

## Limites observées

Le test montre que POP/Mérimée et les notices MH fournissent bien mieux la
chronologie et les protections que la situation contemporaine. La conservation,
l'usage et l'accessibilité nécessiteront une enquête récente pendant le corpus
pilote. Le détail figure dans
`reports/quality/phase4_chronologie_situation.md`.
