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
