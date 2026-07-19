# Méthodologie

## Principes de collecte

1. Auditer une source avant de l'extraire massivement.
2. Archiver le fichier ou la réponse d'origine sans modification.
3. Enregistrer la date de récupération et l'URL précise.
4. Ne jamais écraser une correction manuelle par un traitement automatique.
5. Rendre chaque export reproductible par un script.

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
