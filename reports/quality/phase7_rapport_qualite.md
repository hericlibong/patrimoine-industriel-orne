# Phase 7 — Rapport de qualité du socle pilote V1

Date : 22 juillet 2026

## Conclusion

Le socle pilote est techniquement cohérent et reproductible. Il peut servir à
une démonstration interne, à une première carte de contrôle et à la conception
d'un prototype narratif.

Il ne constitue pas encore un inventaire public exhaustif : il porte sur 30
sites pilotes, plusieurs données contemporaines restent inconnues et aucune
géométrie n'est qualifiée de vérifiée.

## Périmètre contrôlé

| Élément | Résultat |
|---|---:|
| Sites | 30 |
| Phases d'activité | 47 |
| Relations activité-période | 101 |
| Protections MH confirmées | 6 |
| Objets Palissy recensés | 31 |
| Géométries | 59 : 30 points et 29 zones documentaires |
| Mentions de sources | 148 |
| Sources enregistrées | 21 |
| Tests automatisés | 109 réussis |

Les identifiants des 30 sites concordent entre DuckDB, CSV, Parquet et
GeoJSON. Les 47 phases concordent entre leurs exports CSV et Parquet.

## Évaluation par dimension

| Dimension | Niveau actuel | Motif |
|---|---|---|
| Identité et provenance | solide pour le pilote | 30 références `IA`, identifiants stables et source principale conservée |
| Activités et secteurs | solide pour le pilote | 47 phases structurées et vocabulaire contrôlé |
| Chronologie | mixte et explicite | 30 phases datées par une chronologie ; 17 repérées seulement par `SCLE` |
| Localisation | exploitable avec prudence | 30 points approximatifs, 29 zones documentaires, aucune géométrie vérifiée |
| Situation actuelle | très incomplète | 4 sites documentés récemment, 26 laissés inconnus |
| Protections | partielle par nature | 6 protections confirmées ; l'absence de rapprochement ne prouve pas l'absence de protection |
| Objets techniques | exploratoire | 31 notices Palissy liées comme candidates à un même complexe |
| Droits des images | sans risque immédiat dans les exports | aucune photographie tierce intégrée ; registre de droits à constituer avant enrichissement visuel |

## Contrôles réussis

- champs obligatoires, identifiants et relations conformes au modèle ;
- vocabulaires publiés dans `classifications.yml` version 1.2 ;
- périodes filtrables pour les 30 sites et les 47 phases ;
- provenance distincte pour les quatre observations contemporaines ;
- fichiers de sortie reproductibles et empreintes enregistrées ;
- licences de données et règles relatives aux médias renseignées pour les 21
  sources opérationnelles.

## Points restant à traiter

Huit familles d'anomalies ou de limites restent ouvertes. Elles sont décrites
dans `phase7_anomalies_restantes.md`. Les principales sont :

- 26 situations actuelles inconnues ;
- 9 localisations nécessitant une vérification complémentaire ;
- 17 phases dont la période repose sur le siècle du bâti (`SCLE`) ;
- 31 liens Palissy encore candidats ;
- aucun rapprochement CASIAS réalisé sur le pilote ;
- aucun registre d'autorisations photographiques, puisqu'aucune photographie
  tierce n'est encore intégrée.

Ces limites n'empêchent pas de poursuivre le travail méthodologique. Elles
empêchent en revanche de présenter le pilote comme complet, représentatif ou
prêt à être publié sans relecture éditoriale.

## Décision du bloc

Le bloc « Consolider la documentation » est validé. La documentation indique
désormais ce que contiennent les données, leur provenance, leur qualité, les
anomalies restantes et les conditions de réutilisation.

Cette décision ne clôt pas la phase 7. Il reste à préparer la suite puis à
prendre la décision finale `GO`, `GO LIMITÉ` ou `STOP` sur le socle V1.
