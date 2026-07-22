# Phase 7 — Préparation de la suite

Date de validation : 22 juillet 2026

## Résultat du bloc

| Tâche | Livrable | Conclusion |
|---|---|---|
| carte interne | `reports/maps/carte_pilote_interne.png` | 30 sites, 8 catégories et 9 alertes ; carte autonome et explicitement non exhaustive |
| extraction des 319 dossiers | `phase7_evaluation_extraction_complete.md` | faisable de manière semi-automatique, à lancer par lots de 50 |
| estimation de charge | `docs/estimation_charge_corpus_complet.md` | 180–300 h pour le corpus technique ; 260–420 h avec le lot éditorial recommandé |
| récits soutenus | `docs/recits_soutenus_donnees.md` | géographie révélée, activités successives, périodes et eau sont prototypables avec précautions |
| recommandation d'application | `docs/recommandation_application.md` | publication statique narrative et cartographique ; pas de serveur pour le MVP |

## Décisions

1. **GO pour la phase 8**, en commençant par l'énumération contrôlée des 319
   références et un lot de 50 dossiers.
2. **GO LIMITÉ pour l'application** : le prototype narratif peut commencer
   après ce premier lot, sans attendre l'enrichissement complet.
3. L'état actuel et les images seront approfondis sur 30 à 50 sites
   éditoriaux, pas imposés immédiatement aux 319 dossiers.
4. La première application restera statique. DuckDB demeure la référence
   interne et produit les exports web.
5. Les temps de revue seront mesurés pendant le lot de 50 afin de remplacer
   l'estimation actuelle par une charge observée.

## Point d'attention

Le nombre final de sites ne peut toujours pas être annoncé. Les 319 sont des
dossiers sources ; les rapprochements, séparations d'emprises et exclusions
détermineront le nombre de sites canoniques.

Le bloc « Préparer la suite » est terminé. La décision finale a ensuite été
formalisée dans `phase7_decision_socle_v1.md` : `GO` pour la phase 8, par lots.
