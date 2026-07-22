# Phase 7 — Évaluation de l'extraction complète des 319 dossiers

Date : 22 juillet 2026

## Conclusion

L'extraction des 319 dossiers est **faisable**, mais la chaîne actuelle n'est
pas encore une commande prête à lancer sur le corpus complet.

La récupération des notices POP et des champs principaux pourra être largement
automatisée. La constitution des sites, les activités successives, les
rapprochements ambigus, la précision géographique et l'état actuel resteront
semi-automatiques.

## Ce qui est vérifié

- le [corpus officiel de l'Inventaire normand](https://inventaire-patrimoine.normandie.fr/dossier/IA61000851/corpus)
  affiche toujours 319 dossiers et une pagination de 16 pages ;
- les 10 notices du test de phase 2 puis les 30 notices du pilote ont été
  récupérées par référence `IA` ;
- les 30 références demandées concordent avec le champ `REF` de POP ;
- les 30 pages HTML représentent 5,1 Mo, soit environ **52 Mo** pour 319 pages
  si la taille moyenne reste comparable ;
- les champs d'identité, commune, dénomination, historique, période et
  coordonnées sont présents dans les 30 notices pilotes ;
- la chaîne sait déjà produire un corpus structuré, DuckDB, CSV, Parquet et
  GeoJSON.

## Ce qui manque avant le lancement massif

| Élément | Situation actuelle | Travail nécessaire |
|---|---|---|
| liste des 319 références | le portail les affiche par pages | créer un extracteur de pagination et exiger exactement 319 références uniques |
| téléchargement POP | extracteur limité à une liste pilote YAML | accepter un manifeste complet, reprendre après interruption et limiter le rythme des requêtes |
| parsing | validé sur 30 notices | tester un premier lot de 50 puis gérer les variantes et les champs de repli |
| activités | exceptions écrites pour le pilote | produire une file de revue pour les successions et conversions détectées dans `HIST` |
| identifiants internes | attribués aux 30 pilotes | générer puis figer les UUID des nouvelles emprises |
| rapprochement des sites | réalisé sur le pilote | détecter doublons, dossiers liés et dossiers contenant plusieurs emprises |
| géographie | chaîne validée sur 30 points | exécuter par lots et placer les cas ambigus dans une file de contrôle QGIS |
| état actuel | seulement 4 sites récemment sourcés | ne pas en faire un prérequis pour les 319 ; prioriser les sites éditoriaux |
| scans et OCR | 186 pages repérées pour 10 dossiers tests | télécharger et OCRiser uniquement les pages utiles, pas plusieurs milliers de pages par défaut |

## Taille probable du chantier

Les 10 anciens dossiers testés renvoient vers 186 pages numérisées, soit 18,6
pages par dossier en moyenne. Une extrapolation mécanique donnerait environ
5 900 pages pour 319 dossiers. Ce chiffre est seulement un ordre de grandeur :
l'échantillon est petit et la longueur varie selon les dossiers.

Cette volumétrie confirme la stratégie suivante : POP pour la structure et le
texte principal ; scans et OCR seulement lorsqu'une information importante
manque ou doit être vérifiée.

## Risques techniques

1. modification de la structure des pages POP ou du portail régional ;
2. références manquantes, dupliquées ou dossiers liés ;
3. champ `HIST` présent à l'écran mais remplacé par un marqueur dans l'objet
   structuré ;
4. limites de débit, erreurs temporaires et reprise après interruption ;
5. variations de dénomination entraînant un classement manuel ;
6. coordonnées valides mais insuffisamment précises pour une publication.

Ces risques sont gérables avec un manifeste, des fichiers bruts immuables, des
reprises par lot et une file de revue humaine. Aucun ne justifie un arrêt du
projet.

## Stratégie recommandée

1. extraire et figer les 319 références ;
2. traiter un lot de validation de 50 dossiers non pilotes ;
3. mesurer les erreurs, variantes et temps de revue ;
4. corriger la chaîne avant les 239 dossiers restants ;
5. traiter les dossiers par lots de 50 avec rapport à chaque lot ;
6. lancer les enrichissements coûteux seulement après stabilisation du corpus
   principal.

## Décision

**GO pour la phase 8, par lots.**

Il ne faut pas lancer immédiatement tous les enrichissements et OCR. Le premier
jalon de la phase 8 doit être la liste contrôlée des 319 références puis un lot
de 50 dossiers destiné à recalibrer la charge.
