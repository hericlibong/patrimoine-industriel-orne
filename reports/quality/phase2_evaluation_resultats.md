# Phase 2 — Évaluation des résultats d'extraction

Date : 20 juillet 2026  
Mesures détaillées : `phase2_evaluation_samples.json`

## Conclusion opérationnelle

La récupération et le contrôle technique des cinq sources peuvent être
automatisés. La constitution du corpus ne peut pas l'être entièrement : le
rapprochement entre sources, la qualification patrimoniale, la précision de la
localisation et surtout l'état actuel exigent une validation humaine.

POP / Mérimée est confirmé comme point d'entrée principal pour les 319 dossiers
de l'Inventaire. Les scans de l'Inventaire serviront de complément. Palissy,
Monuments historiques et CASIAS restent des sources d'enrichissement ou de
candidats, et non des listes directement publiables.

## Encodages et formats

Les 34 fichiers du manifeste ont un format valide et ont été décodés sans
remplacement de caractères.

| Source | Fichiers | Format | Encodage constaté | Décision |
|---|---:|---|---|---|
| Inventaire normand | 20 | HTML | ISO-8859-1 | conserver le brut, convertir les textes dérivés en UTF-8 |
| POP / Mérimée | 10 | HTML contenant une notice structurée | UTF-8 | extraire l'objet structuré embarqué |
| Palissy | 1 | JSON, 2 notices | UTF-8 | parser directement l'API |
| Monuments historiques | 1 | JSON, 77 notices | UTF-8 | parser directement l'API |
| CASIAS | 2 | GML, 20 entités | UTF-8 | parser le XML et ignorer la géométrie non qualifiée |

## Complétude des champs utiles

### POP / Mérimée — 10 notices

La notice structurée embarquée contient 159 champs distincts. Les dix notices
ont toutes une référence `IA`, un titre, une dénomination, une commune, un code
INSEE, un lieu-dit, un historique, une période, une URL de dossier et des
coordonnées.

| Champ utile | Renseigné |
|---|---:|
| Référence, titre, activité, commune, historique, période | 10/10 |
| Coordonnées WGS84 | 10/10 |
| Description | 9/10 |
| Énergie | 8/10 |
| Cours d'eau | 7/10 |
| État indiqué dans la notice patrimoniale | 6/10 |
| Adresse | 0/10 |

L'état renseigné dans une notice ancienne ne sera pas assimilé à l'état actuel.

### Palissy — 2 notices

L'échantillon est trop petit pour estimer la base entière, mais il permet de
tester les difficultés de liaison.

| Champ utile | Renseigné |
|---|---:|
| Référence `PM`, titre, commune, code INSEE, édifice, protection | 2/2 |
| Dénomination, description, historique | 1/2 |
| Référence Mérimée directe | 0/2 |
| Coordonnées | 0/2 |

### Monuments historiques — 77 notices candidates

Les notices contiennent 76 champs distincts. L'identité et la protection sont
bien renseignées, mais la situation actuelle et la description matérielle le
sont peu.

| Champ utile | Renseigné |
|---|---:|
| Référence, titre, dénomination, commune, code INSEE, protection | 77/77 |
| Historique | 75/77 |
| Coordonnées WGS84 | 50/77 |
| État de conservation | 18/77 |
| Cours d'eau | 16/77 |
| Lien Palissy | 7/77 |
| Source d'énergie | 4/77 |
| Description de l'édifice | 1/77 |
| Destination actuelle | 0/77 |

### CASIAS — 20 entrées stratifiées

Le prélèvement contient volontairement dix fiches avec coordonnées et dix
fiches déclarées non géolocalisées. Le taux de 50 % n'est donc pas une
estimation de l'ensemble CASIAS.

| Champ utile | Renseigné |
|---|---:|
| Identifiants `SSP` et `BNO`, commune, code INSEE, état, URL | 20/20 |
| Adresse | 17/20 |
| Code postal | 15/20 |
| Nom d'établissement | 9/20 |
| Activité principale | 0/20 |
| Coordonnées WGS84 | 10/20, par construction de l'échantillon |

## Identifiants et doublons

| Source | Identifiant à conserver | Résultat du test |
|---|---|---|
| Inventaire / POP | `REF` de forme `IA...` | 10 valeurs présentes, uniques et identiques entre les deux représentations |
| Palissy | `reference` de forme `PM...` | 2 valeurs présentes et uniques |
| Monuments historiques | `reference` de forme `PA...` | 77 valeurs présentes et uniques |
| CASIAS | `code_metie` de forme `SSP...` | 20 valeurs présentes et uniques ; clé source principale |
| CASIAS historique | `code_inven` de forme `BNO...` | 20 valeurs présentes et uniques ; alias BASIAS à conserver |

Aucun doublon de référence principale n'a été détecté dans les échantillons.
Les répétitions de codes INSEE indiquent seulement que plusieurs notices se
trouvent dans une même commune : le code commune ne doit jamais servir
d'identifiant de site. Les dix références communes à l'Inventaire et à POP sont
deux représentations des mêmes notices, pas vingt sites.

## Coordonnées

| Source | Présentes | Syntaxe WGS84 valide | Dans l'enveloppe large de l'Orne | Limite |
|---|---:|---:|---:|---|
| Inventaire, index statiques | 0/10 | — | — | utiliser la notice POP correspondante |
| POP / Mérimée | 10/10 | 10/10 | 10/10 | précision exacte du site encore à qualifier |
| Palissy | 0/2 | — | — | rattacher l'objet à un site vérifié |
| Monuments historiques | 50/77 | 50/50 | 50/50 | 27 notices sans point |
| CASIAS stratifié | 10/20 | 10/10 | 10/10 | dix fiches volontairement non géolocalisées |

Le contrôle d'enveloppe détecte seulement les aberrations grossières. Il ne
prouve ni que le point correspond au bon bâtiment, ni qu'il possède la
précision nécessaire à la carte. Pour CASIAS, toute géométrie WFS sera ignorée
si `x_wgs84` et `y_wgs84` sont absents.

## Part automatisable

| Source | Automatisation réaliste | Contrôle humain indispensable |
|---|---|---|
| Inventaire normand | récupération des index, références et listes de scans | OCR ciblé et contrôle des informations absentes de POP |
| POP / Mérimée | extraction des champs, identifiants et coordonnées | activités successives, état actuel et précision du point |
| Palissy | extraction des objets et de leurs références | rattachement objet-site lorsqu'aucune référence Mérimée n'existe |
| Monuments historiques | extraction, filtres départementaux et contrôles de champs | élimination des faux positifs et portée industrielle de la protection |
| CASIAS | extraction WFS, identifiants, communes et coordonnées explicites | activité manquante, intérêt patrimonial, localisation et dédoublonnage |

## Traitements manuels à prévoir

- relire les rapprochements sans identifiant commun ;
- distinguer les activités successives d'un même site ;
- écarter les faux positifs Monuments historiques et CASIAS ;
- vérifier la précision réelle des coordonnées avant publication ;
- rechercher les sites non géolocalisés sans leur attribuer le centroïde communal ;
- OCRiser uniquement les pages de l'Inventaire nécessaires ;
- documenter l'usage, la conservation, la visibilité et l'accessibilité actuels
  avec des sources récentes ;
- contrôler les droits des images indépendamment des notices.

## Décisions pour la suite

1. Normaliser les données dérivées en UTF-8 tout en conservant les fichiers
   bruts dans leur encodage d'origine.
2. Construire le corpus initial à partir des références `IA` de POP / Mérimée.
3. Conserver chaque notice source séparément avant rapprochement dans le modèle.
4. Autoriser les jointures automatiques seulement sur un identifiant externe
   exact ; toute jointure par commune, nom ou proximité doit être contrôlée.
5. Stocker séparément présence, validité et précision des coordonnées.
6. Charger CASIAS dans une table de candidats, sans publication automatique.
7. Ne jamais déduire l'état actuel d'un site d'une notice patrimoniale ancienne.
