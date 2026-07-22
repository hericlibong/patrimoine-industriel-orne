# Phase 7 — Décision finale sur le socle V1

Date d'approbation : 22 juillet 2026

## Décision

**GO pour la phase 8, par lots.**

Le socle V1 est approuvé comme base méthodologique, documentaire et technique
pour passer des 30 sites pilotes aux 319 dossiers sources de l'Inventaire du
patrimoine industriel de l'Orne.

Le traitement par lots est une règle d'exécution et de contrôle. Il ne remet
pas en cause l'approbation du socle.

## Ce qui est approuvé

- le périmètre éditorial, géographique et chronologique ;
- la définition d'un site comme emprise physique distincte ;
- le modèle relationnel DuckDB et les exports CSV, Parquet et GeoJSON ;
- les identifiants internes stables et la provenance par information ;
- les classifications en version 1.2 ;
- la représentation des activités successives et des périodes ;
- les règles de précision et d'incertitude géographiques ;
- les méthodes d'extraction testées sur les sources prioritaires ;
- le registre des sources, les limites éditoriales et les règles relatives aux
  images ;
- la méthode de validation appliquée au corpus pilote.

## Ce que cette approbation ne signifie pas

- les 30 sites ne deviennent pas le corpus final ;
- le nombre final de sites n'est pas encore connu ;
- les 319 dossiers ne correspondent pas nécessairement à 319 sites ;
- les 2 052 entrées CASIAS ne sont pas intégrées automatiquement ;
- les points approximatifs ne deviennent pas des emprises vérifiées ;
- les situations actuelles inconnues ne sont pas complétées par hypothèse ;
- aucune publication photographique n'est autorisée sans contrôle des droits.

## Conditions de passage à la phase 8

1. construire et valider la liste des 319 références `IA` uniques ;
2. traiter d'abord un lot de 50 dossiers non pilotes ;
3. mesurer la durée de revue, les erreurs, les variantes et les cas bloqués ;
4. corriger la chaîne avant de poursuivre les lots suivants ;
5. conserver les données brutes, manifestes et preuves de provenance ;
6. ne fusionner ou séparer des emprises qu'avec une décision documentée ;
7. maintenir une file explicite pour les rapprochements et localisations à
   vérifier ;
8. recalculer les récits et statistiques uniquement sur le corpus complet.

## Premier jalon de la phase 8

Le premier jalon n'est pas l'extraction immédiate de toutes les sources
complémentaires. Il comprend :

- l'énumération des 319 références ;
- leur contrôle d'unicité et de disponibilité ;
- l'extraction structurée d'un premier lot de 50 ;
- un rapport de cadence et de qualité ;
- une révision de l'estimation de charge.

## Approbation et clôture

Le socle pilote V1 est **approuvé**. La phase 7 est **terminée**.

Les 110 tests automatisés du projet réussissent au moment de cette approbation.

La phase suivante autorisée est la phase 8 « Passer au corpus complet », selon
la stratégie par lots décrite ci-dessus.
