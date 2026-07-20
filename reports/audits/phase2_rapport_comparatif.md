# Phase 2 — Rapport comparatif et choix des méthodes

Date de clôture : 20 juillet 2026

## Décision

La phase 2 est validée. Les cinq sources peuvent être intégrées à la chaîne de
travail, avec des rôles et des niveaux d'automatisation différents. La phase 3
peut commencer sur le modèle de données.

Cette décision ne signifie pas que les données sont prêtes à publier ni que le
nombre final de sites est connu. Elle signifie que le projet sait désormais
comment acquérir, contrôler et orienter chaque source.

## Comparaison des sources

| Source | Rôle retenu | Forces constatées | Limites déterminantes | Méthode définitive | Automatisation |
|---|---|---|---|---|---|
| Inventaire normand | corpus principal | 319 dossiers spécialisés ; références `IA` ; profondeur historique | export régional global indisponible ; dossiers détaillés numérisés | extraire les notices structurées via POP, compléter par scans et OCR ciblé | semi-automatique |
| POP / Mérimée | canal structuré du corpus | notice embarquée de 159 champs ; identifiants, historique et coordonnées complets sur l'échantillon | structure Next.js susceptible d'évoluer ; état actuel non fiable | extraction par référence `IA`, validation du `REF`, conservation du HTML brut | automatique avec validation |
| Palissy | objets et machines | références `PM`, protection et édifice bien renseignés | lien Mérimée et coordonnées absents dans l'échantillon | API ciblée après constitution des sites ; rattachement exact ou contrôle humain | automatique avec rattachement contrôlé |
| Monuments historiques | protection juridique | références `PA`, commune, protection et historique très complets | faux positifs ; destination actuelle absente ; 27/77 sans point | API de toutes les notices de l'Orne, mots-clés pour prioriser seulement | automatique avec sélection contrôlée |
| CASIAS | élargissement des candidats | identifiants `SSP` et `BNO`, commune et accès WFS | activité absente de la couche ; nombreux sites non géolocalisés ; fort bruit | WFS départemental, enrichissement fiche/CSV, stockage séparé des candidats | semi-automatique |

## Comparaison quantitative des échantillons

| Source | Notices ou entités | Identifiant principal complet | Coordonnées explicites | Doublons d'identifiant principal |
|---|---:|---:|---:|---:|
| Inventaire, index statiques | 10 dossiers | 10/10 | 0/10 dans les index | 0 |
| POP / Mérimée | 10 | 10/10 | 10/10 | 0 |
| Palissy | 2 | 2/2 | 0/2 | 0 |
| Monuments historiques | 77 | 77/77 | 50/77 | 0 |
| CASIAS, échantillon stratifié | 20 | 20/20 | 10/20 par construction | 0 |

Les taux des petits échantillons ne sont pas extrapolés aux sources complètes.
Le lot CASIAS comporte volontairement dix fiches localisées et dix non
géolocalisées.

## Répartition automatique, semi-automatique et manuelle

### Automatique

- téléchargement et conservation des réponses brutes ;
- métadonnées, empreintes, encodages et validation des formats ;
- parsing JSON, GML et notice structurée POP ;
- mesure de complétude et détection des références dupliquées ;
- validation syntaxique des coordonnées WGS84 ;
- jointure sur une référence externe strictement identique.

### Semi-automatique

- extraction des scans de l'Inventaire et OCR ciblé ;
- rapprochement par nom, commune, édifice, adresse ou proximité ;
- enrichissement des fiches CASIAS depuis d'autres ressources ;
- localisation à partir d'une adresse ou d'un lieu-dit ;
- classement des activités successives et des sites composites.

### Manuel

- validation des rapprochements incertains ;
- exclusion des faux positifs ;
- qualification de l'intérêt patrimonial ;
- vérification de l'emprise et de la précision géographique ;
- état actuel, usage, conservation, visibilité et accessibilité ;
- contrôle éditorial des contradictions et des droits des images.

## Méthodes retenues

Les règles exécutables et les décisions source par source sont fixées dans
`config/extraction.yml`. Les principes communs sont :

1. conserver les données brutes sans modification et avec leur encodage
   original ;
2. produire les données dérivées en UTF-8 ;
3. conserver les notices sources séparées jusqu'au rapprochement ;
4. autoriser une jointure automatique uniquement sur un identifiant externe
   exact ;
5. ne jamais transformer une commune en localisation artificielle de site ;
6. qualifier séparément la présence, la validité et la précision d'un point ;
7. imposer une validation humaine avant publication.

## Archive de validation

L'archive locale `data/archive/phase2_extractions_tests_2026-07-20.zip` contient
uniquement le corpus défini par le manifeste :

- 34 fichiers bruts ;
- 34 fichiers de métadonnées ;
- le manifeste d'extraction versionné ;
- un manifeste interne d'archive.

Elle contient 70 entrées, pèse 374 655 octets et possède l'empreinte SHA-256 :

```text
9e2ac0a1df1290966e4b36b9196f23e3320c37a40d7926c2c22850d39c83f24e
```

L'archive et son fichier `.sha256` restent hors Git. Leur descripteur est
versionné dans `reports/audits/phase2_archive_descriptor.json`.

## Point de validation

Le projet sait ce qui est automatisable, semi-automatisable ou manuel. Les
méthodes d'extraction sont suffisamment définies pour construire, en phase 3,
un modèle qui conserve les notices, les identifiants externes, les
rapprochements et les niveaux de confiance sans perdre la provenance.
