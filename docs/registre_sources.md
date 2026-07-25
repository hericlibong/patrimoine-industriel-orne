# Registre consolidé des sources — phases 8 et 9

Version : 1.4 — 24 juillet 2026

La source canonique lisible par les traitements est `config/sources.yml`. Le
fichier `reports/audits/registre_sources.csv` conserve l'état de l'audit initial
de phase 1 ; il ne doit plus être utilisé comme registre opérationnel, car les
produits géographiques réellement testés ont été précisés pendant la phase 6.
La version 1.2 ajoute l'API JSON publique de POP comme accès principal aux
notices Mérimée de l'Inventaire. La version 1.3 consigne les extractions et
rapprochements du corpus complet.

## Sources effectivement mobilisées dans le pilote

| Source | Usage dans le socle | Résultat | Réutilisation des données | Médias |
|---|---|---|---|---|
| Inventaire industriel de l'Orne | définition du corpus de 319 dossiers | corpus principal à traiter en phase 8 | licence globale non identifiée | autorisation requise sauf mention contraire |
| POP — Mérimée | notice principale des 30 sites | 30 références `IA` | Licence Ouverte 2.0 sauf mention contraire | vérifier chaque image |
| POP — Palissy | objets techniques | 31 notices, liens candidats | Licence Ouverte 2.0 | vérifier chaque image |
| Monuments historiques | protections | 6 protections confirmées | Licence Ouverte 2.0 | hors du jeu tabulaire utilisé |
| API Découpage administratif | communes actuelles | 30 codes INSEE | Licence Ouverte 2.0 | aucun média utilisé |
| Cadastre / API Carto | contrôle parcellaire | 30 parcelles candidates | Licence Ouverte 2.0 | aucun média utilisé |
| BAN | contrôle d'adresses | 4 résultats, dont 3 conservés comme contrôles secondaires | Licence Ouverte 2.0 | aucun média utilisé |
| BD TOPO — hydrographie | distances aux cours d'eau | 30 sites calculés | Licence Ouverte 2.0 | aucun média utilisé |
| BD Forêt v2 | contexte forestier | 30 sites calculés | Licence Ouverte 2.0 | aucun média utilisé |
| BRGM / InfoTerre | lithologie et indices miniers | 30 sites calculés | Licence Ouverte 2.0 sauf exception signalée | contenus illustrés du site non réutilisés |
| BD TOPO — rail | distances au réseau répertorié | 30 sites calculés | Licence Ouverte 2.0 | aucun média utilisé |
| OpenStreetMap | fond de contrôle QGIS | usage interne uniquement | ODbL 1.0 | attribution visible requise pour une carte publiée |
| EDF Hydro | activité récente de Rabodanges | 1 situation actuelle | licence non identifiée | textes et images non repris |
| Bohin France | production et visite actuelles | 1 situation actuelle | licence non identifiée | textes et images non repris |
| Archives de l'Orne | programmation institutionnelle 2026 | 1 situation actuelle | selon document et fonds | reproduction à vérifier document par document |
| Département de l'Orne | opération récente sur la mine de Halouze | 1 situation actuelle | licence non identifiée | textes et images non repris |

## Sources conservées pour la suite

| Source | Rôle prévu | État |
|---|---|---|
| CASIAS | recoupement et élargissement raisonné | 2 052 entrées ; 131 recoupements sur 123 sites ; 170 candidats d'élargissement hors corpus |
| IGN — catalogue générique | accès aux produits géographiques | produit, couche, millésime et licence à enregistrer à chaque extraction |
| BD Forêts anciennes | contexte historique vers 1850 | non intégrée au socle pilote |
| Gallica | cartes, presse et documents numérisés | recherche manuelle future ; droits à vérifier par document |
| Sources touristiques locales génériques | accessibilité et information pratique | source volatile, à dater systématiquement |

## Résultats sur le corpus complet

| Source | Extraction | Résultat retenu |
|---|---:|---:|
| POP — Mérimée | 2 346 notices de l'Orne, dont 410 `PA` | 16 protections reliées par référence `IA` explicite |
| POP — Palissy | 5 066 notices, dont 3 343 `PM` | 31 objets documentaires conservés, encore à vérifier |
| CASIAS | 2 052 entrées | 131 recoupements sur 123 sites ; 8 ambiguïtés restantes |
| IGN — hydrographie, forêt, rail | 129 tuiles archivées | contexte calculé pour 318 sites |
| BRGM — lithologie, mines, gîtes | 3 extractions couvrant le corpus | contexte calculé pour 318 sites |

## Règles opérationnelles

1. Une source n'est jamais qualifiée globalement de fiable pour tous ses
   champs. La confiance est attachée à chaque information ou relation.
2. Chaque récupération conserve la source, l'URL ou l'identifiant, la date et
   le millésime disponible.
3. Une proximité géographique est un indice, pas une preuve de causalité
   historique.
4. Une absence dans une base spécialisée ne prouve pas l'absence d'un site,
   d'une protection ou d'un objet.
5. Les images suivent un contrôle de droits distinct des notices et données
   descriptives.
6. Les sources contemporaines sont enregistrées sous leur producteur réel ;
   l'étiquette générique `tourisme_local` n'est utilisée qu'en dernier recours.

## Attributions minimales prévues

- données publiques sous Licence Ouverte : producteur, nom du jeu et millésime
  ou date de mise à jour ;
- OpenStreetMap : `© OpenStreetMap contributors`, avec un lien vers les
  informations de licence ;
- BRGM : BRGM et date de dernière mise à jour du produit ;
- Gallica : `Source gallica.bnf.fr / Bibliothèque nationale de France` ;
- archives : service, cote, auteur ou fonds lorsque ces informations existent.

Le détail des droits et les liens vers les conditions officielles sont repris
dans `docs/licences_droits_images.md`.

## Ajout phase 9 — POP Mémoire

POP Mémoire est désormais une source explicite du projet. L'inventaire couvre
les métadonnées `MEMOIRE` liées aux 318 notices `IA` : 1 900 relations
média-site pour 316 sites. Deux notices ne proposent aucun média exploitable.

Les relations conservent la référence Mémoire, la notice POP correspondante, le
chemin ou l'URL du fichier source, la légende, le crédit, la mention de droits
et le marqueur d'image principale lorsqu'ils sont présents. Les droits de
publication restent à vérifier média par média ; aucun fichier image n'est
téléchargé ou versionné.
