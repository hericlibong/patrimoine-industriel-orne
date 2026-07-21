# Composition de l'échantillon pilote

Version 0.1 — 21 juillet 2026

## Résultat

Le pilote contient **30 dossiers IA candidats**, choisis dans le corpus officiel
de **319 dossiers** de l'Inventaire du patrimoine industriel de l'Orne.

Ce ne sont pas encore 30 sites canoniques : les rapprochements entre notices et
les contrôles de terrain documentaire seront réalisés dans le bloc
« Enrichir les sites ».

| Contrôle | Résultat |
|---|---:|
| Macro-zones | 6, avec 5 candidats chacune |
| Secteurs représentés | 8 |
| Périodes représentées | 5 |
| Profils de conservation issus des sources | 6 |
| Protections MH déjà identifiées | 7 |
| Sans protection MH identifiée à ce stade | 23 |
| Localisations faciles | 14 |
| Localisations intermédiaires | 10 |
| Localisations difficiles | 6 |
| Sites à plusieurs secteurs présélectionnés | 5 |

## Méthode

L'échantillon est **raisonné par quotas**. Il n'est ni aléatoire ni destiné à
représenter statistiquement les 319 dossiers. Son rôle est de faire rencontrer
au modèle des situations variées avant l'extraction complète.

Les critères sont appliqués ensemble :

- six macro-zones analytiques couvrant l'ouest, les vallées du Noireau et de la
  Vère, l'Alençonnais, les plaines d'Argentan et le pays d'Auge, le pays d'Ouche
  et de la Risle, et le Perche ;
- au moins sept secteurs industriels ;
- plusieurs périodes, de l'Ancien Régime à l'après-guerre ;
- des profils conservés, partiels, dégradés, à l'état de vestiges, disparus et
  inconnus ;
- des dossiers protégés et des dossiers sans protection identifiée ;
- au moins cinq localisations volontairement difficiles.

Les cas rares ou difficiles sont donc volontairement surreprésentés. Un dossier
peut compter dans plusieurs secteurs ou plusieurs périodes.

## Liste des 30 candidats

| Zone de contrôle | Référence | Commune | Désignation courte |
|---|---|---|---|
| Bocage et Andaines | `IA00061008` | Saint-Clair-de-Halouze | Mine de Halouze |
| Bocage et Andaines | `IA00060965` | Champsecret | Affinerie et moulin à blé |
| Bocage et Andaines | `IA00060938` | Rabodanges | Centrale hydroélectrique |
| Bocage et Andaines | `IA00061003` | Les Rotours | Four à chaux |
| Bocage et Andaines | `IA00060901` | Rânes | Affinerie de fer |
| Vallées Noireau-Vère | `IA00061119` | Athis-de-l'Orne | Filature de la Martinique |
| Vallées Noireau-Vère | `IA00060915` | Saint-Georges-des-Groseillers | Filature de la Planchette |
| Vallées Noireau-Vère | `IA00061035` | Saint-Pierre-du-Regard | Filature des Roches |
| Vallées Noireau-Vère | `IA00060902` | Berjou | Filature puis fromagerie |
| Vallées Noireau-Vère | `IA00060896` | Cahan | Filature puis usine de chaussures |
| Alençonnais et Écouves | `IA00061002` | Alençon | Imprimerie Alençonnaise |
| Alençonnais et Écouves | `IA00061073` | Alençon | Scierie Prout |
| Alençonnais et Écouves | `IA00060969` | Alençon | Moulin, filature puis appareils ménagers |
| Alençonnais et Écouves | `IA00060959` | Saint-Denis-sur-Sarthon | Usine de fabrication des métaux |
| Alençonnais et Écouves | `IA00060997` | Saint-Denis-sur-Sarthon | Faïencerie |
| Plaines d'Argentan et pays d'Auge | `IA00061117` | Argentan | Briqueterie Saint-Martin |
| Plaines d'Argentan et pays d'Auge | `IA00061133` | Le Bourg-Saint-Léonard | Laiterie-fromagerie Lavalou |
| Plaines d'Argentan et pays d'Auge | `IA00060909` | Gacé | Distillerie, cidrerie et laiterie |
| Plaines d'Argentan et pays d'Auge | `IA00061166` | Trun | Cidrerie-distillerie Pépin |
| Plaines d'Argentan et pays d'Auge | `IA00061091` | Goulet | Moulin à farine |
| Pays d'Ouche et Risle | `IA00061029` | Aube | Affinerie |
| Pays d'Ouche et Risle | `IA00061155` | Saint-Sulpice-sur-Risle | Établissements Bohin |
| Pays d'Ouche et Risle | `IA00061113` | Saint-Sulpice-sur-Risle | Usine de la Batterie |
| Pays d'Ouche et Risle | `IA00061052` | L'Aigle | Tannerie puis construction mécanique |
| Pays d'Ouche et Risle | `IA00061054` | L'Aigle | Usine d'habillement |
| Perche | `IA00061153` | Longny-au-Perche | Forge de Beaumont |
| Perche | `IA00061060` | Longny-au-Perche | Moulin à papier puis grosse forge |
| Perche | `IA00061147` | Saint-Langis-lès-Mortagne | Cartonnerie |
| Perche | `IA00061135` | Irai | Fonderies du Perche |
| Perche | `IA00061095` | L'Hôme-Chamondot | Briqueterie des Chauffetières |

## Ce qui est provisoire

Les secteurs, périodes, états matériels et difficultés de localisation servent
uniquement à composer l'échantillon. Ils devront être recalculés ou vérifiés à
partir des notices complètes.

En particulier :

- un état de conservation relevé lors d'une enquête des années 1980 n'est pas
  traité comme un état actuel ;
- « sans protection MH identifiée » ne signifie pas juridiquement « non
  protégé » tant que la vérification nominative n'est pas terminée ;
- une référence `IA` n'est pas encore un identifiant de site du projet ;
- aucune coordonnée de présélection ne sera publiée sans contrôle spatial.

## Fichiers de contrôle

- sélection structurée : `config/echantillon_pilote.yml` ;
- bilan automatique : `reports/quality/phase5_composition_echantillon.json` ;
- contrôle reproductible : `python -m patrimoine_orne.sample.pilot`.

Sources de départ :

- [corpus officiel des 319 dossiers](https://inventaire-patrimoine.normandie.fr/dossier/IA61000851/corpus) ;
- [notice de présentation de l'étude](https://pop.culture.gouv.fr/notice/merimee/IA61000851) ;
- export Monuments historiques audité en phase 2 pour repérer les protections.
