# Classifications des secteurs et installations

Statut : **étendu dans le registre 1.4 du corpus complet le 23 juillet 2026**

Le registre exécutable est `config/classifications.yml`. Ce document en fixe les
règles de lecture.

## Principe

Le secteur qualifie une phase d'activité. Il ne qualifie pas définitivement un
site, car une même emprise peut accueillir plusieurs productions simultanées ou
successives.

Ordre de travail :

1. conserver le libellé original de la source ;
2. identifier l'activité réellement exercée ;
3. associer cette activité à un code détaillé ;
4. déduire le secteur depuis ce code ;
5. enregistrer séparément l'installation et l'énergie lorsqu'elles sont connues.

Une correspondance par terme exact peut être automatisée. Une simple présence
de mot-clé ne suffit pas à valider silencieusement une activité.

Une dénomination patrimoniale peut aussi décrire un composant non productif,
par exemple une cité ouvrière. Elle est alors conservée dans
`composants_non_productifs_source` et n'est pas transformée en activité.

## Dimensions séparées

| Dimension | Question | Exemple |
|---|---|---|
| activité | que produit ou transforme-t-on ? | mouture de céréales |
| secteur | à quelle grande famille appartient l'activité ? | agroalimentaire |
| installation | dans quel dispositif fonctionnel travaille-t-on ? | moulin ou minoterie |
| bâtiment | quel élément physique est décrit ? | atelier, cheminée, logement ou hangar |
| énergie | quelle force ou quel combustible est utilisé ? | hydraulique ou charbon |
| rôle énergétique | comment l'énergie intervient-elle ? | force motrice, produite sur place ou achetée |

Ainsi, « moulin à farine » produit l'activité `mouture_cereales`, le secteur
`agroalimentaire` et l'installation `moulin`. « Roue hydraulique verticale »
est un équipement : ce n'est ni une activité ni une énergie.

## Affectation à un secteur

- Une ligne `activites` possède au plus un `secteur_code`.
- Le code est déterminé par `activite_code`, pas par le nom du bâtiment.
- `DENO` et `TICO` fournissent des candidats structurés ; `HIST` peut révéler
  des phases absentes de ces champs.
- Une destination actuelle n'est jamais reclassée comme activité historique.
- `autres_industries` suppose que le caractère industriel est confirmé.
- `inconnu` signifie que l'activité industrielle est attestée mais non classée.
- Les règles détaillées d'emploi de `autres_industries` et `inconnu` sont
  arrêtées dans `docs/classifications_qualite.md`.

## Sites multi-secteurs

Un site est multi-secteurs lorsqu'au moins deux de ses activités appartiennent
à des secteurs différents. Aucun code `activite_mixte` n'est créé.

Conséquences :

- chaque activité conserve sa période et son secteur ;
- le site apparaît dans chaque filtre sectoriel documenté ;
- un comptage tous secteurs confondus déduplique les lignes par `site_id` ;
- la somme des effectifs sectoriels peut dépasser le nombre total de sites ;
- il n'existe pas de secteur principal permanent du site ;
- pour un récit limité à une période, l'activité principale de cette période
  peut être utilisée sans écraser les autres phases.

## Portée du vocabulaire

Le vocabulaire publié en version 1.0 couvre tous les termes `DENO` des 10 notices POP testées et ajoute
les activités attendues dans le cadrage : forges, aiguilles, papier, textile,
bois, matériaux et transformations agroalimentaires. Cette couverture reste à
retester lors de l'extraction complète et du corpus pilote.
