# Phase 10 — Cadrage V2 : une visualisation datajournalistique interactive

**Version :** 2.1 — consolidation après les phases 10.B et 10.C

**Statut :** cadrage général de référence

**Date :** 12 août 2026
**Complété par :** `docs/phase10_architecture.md` pour les décisions d'interface
et `docs/phase10_demonstration.md` pour les constats issus des douze systèmes.

Ce document remplace la version 2.0 du 29 juillet 2026. La nature applicative
du projet est maintenue, mais la logique de récit et les amorces obligatoires
sont abandonnées. Le lecteur arrive directement devant la visualisation et
l'aborde par l'angle de son choix.

---

## 1. Ce que nous construisons

**Une application web de visualisation interactive consacrée au patrimoine
industriel de l'Orne.** Son titre de travail est **« Voyage dans l'Orne
industrielle »** ; il reste provisoire.

Au centre, une carte de l'Orne. Autour, des commandes, des chiffres, une liste
synchronisée et des informations sourcées. Le lecteur peut choisir un système,
un métier, une époque, une distance à l'eau ou rechercher un lieu précis. La
carte, la liste et les indicateurs répondent ensemble.

Il n'existe ni parcours obligatoire ni ordre de lecture. On manipule les
données pour observer, comparer et comprendre.

## 2. Ce que ce n'est pas

Le produit n'est pas :

- un article découpé en chapitres ;
- un site à rubriques ;
- un catalogue de trois cent dix-huit fiches ;
- un portail institutionnel ;
- un tableau de bord de gestion ;
- une reconstitution exhaustive de toute l'industrie ornaise.

La première tentative des 26 et 27 juillet 2026 avait produit des pages, un
défilement et des gabarits interchangeables. Elle est conservée comme
contre-exemple, pas comme base à enrichir.

## 3. Le sujet et le périmètre

Le corpus documente **318 sites** et **403 activités** : forges, moulins,
filatures, papeteries, mines, usines d'épingles et d'aiguilles, laiteries,
tuileries et autres lieux de production.

L'application rend visible leur géographie, leurs métiers, leurs périodes
documentées et les relations explicitement établies par les sources. Elle
permet de voir aussi bien les concentrations industrielles que les sites
dispersés.

Le corpus porte sur des **productions associées à une usine**. Ce qui s'est
fabriqué sans bâtiment industriel identifié — par exemple la dentelle
d'Alençon — est absent par construction. Cette limite doit être affichée.

## 4. Les douze systèmes et les autres sites

Les **douze systèmes industriels** constituent le cœur éditorial actuel. Ils
rassemblent **172 sites**, lus notice par notice. Ce sont des vallées, des
bassins miniers, des villes ou des ensembles de communes dont les sites sont
proches et dont la lecture fait apparaître une histoire distincte.

Un système résulte d'abord d'un regroupement de sites distants de moins de
trois kilomètres de proche en proche. Ce calcul ne prouve ni une frontière ni
une emprise historique. Sur la carte, un système est donc représenté par ses
sites et son nom, jamais par un contour fermé.

Les **146 autres sites ne sont pas écartés** :

- 74 appartiennent à 18 petits ensembles de trois à six sites, dont la lecture
  éditoriale est reportée et pourra produire de nouveaux systèmes plus tard ;
- 72 sont seuls ou par paires selon la règle des trois kilomètres. Ils restent
  consultables individuellement. Cette dispersion calculée ne prouve pas
  qu'ils étaient historiquement isolés.

## 5. Ce que voit le lecteur

Le lecteur arrive directement devant la carte départementale :

- les douze systèmes comme objets principaux ;
- les 146 autres sites, présents mais plus discrets ;
- le réseau hydrographique utile à la lecture ;
- les commandes de recherche et de filtrage ;
- une liste textuelle synchronisée avec la carte.

Il n'y a ni écran d'introduction, ni bouton « commencer », ni parcours imposé.
Les éventuelles amorces sont reportées jusqu'à la visualisation réelle. Si
elles sont ajoutées, leurs intitulés décriront exactement ce qu'elles montrent,
sans question rhétorique ni abstraction.

## 6. Les commandes retenues

La visualisation propose trois leviers et une recherche :

- **métier** : les neuf secteurs du corpus ;
- **époque** : une année située dans une période documentée ;
- **proximité de l'eau** : une distance mesurée au cours d'eau le plus proche ;
- **recherche** : nom, commune, activité ou référence.

La forêt, le minerai, le rail, la situation actuelle et la précision
géographique ne deviennent pas des filtres principaux. Ils sont soit trop peu
discriminants, soit trop incomplets, soit mieux présentés comme information de
contexte.

Deux formulations sont interdites :

- une proximité avec l'eau n'est jamais présentée comme une causalité ;
- la réglette temporelle n'affirme jamais qu'une usine était active une année
  donnée. Elle indique seulement que sa période documentée couvre cette année.

## 7. Fonctionnement de la visualisation

La carte s'ouvre à l'échelle du département. Cliquer sur un système y entre ;
cliquer sur un site ouvre ses informations. Quand un filtre modifie la
sélection, la carte se recadre sur le résultat au lieu de seulement atténuer
des points. Un contrôle permet toujours de revenir au département.

Les états importants sont partageables dans le fragment de l'adresse, après
le `#`, afin de fonctionner aussi sur un fichier statique hors ligne.

Tout ce que la carte porte existe également en texte dans une liste
synchronisée : mêmes sites, mêmes chiffres, mêmes libellés et mêmes limites.

## 8. Les informations affichées

Trois niveaux peuvent coexister sans imposer un récit :

| Niveau | Contenu |
| --- | --- |
| Vue générale | systèmes, sites hors systèmes, chiffres et commandes |
| Système | nom, sites, métiers, constats issus de la lecture et relations sourcées |
| Site | notice courte, événements datés, activités, source et précision géographique |

Des annotations contextuelles pourront signaler un fait au moment où la
visualisation le rend visible. Elles ne sont ni systématiques ni nécessaires à
toutes les combinaisons de filtres.

## 9. Forme cartographique et direction artistique

La carte est un **SVG produit depuis les données et les couches géographiques
locales**. Ce choix permet une composition sur mesure, sans serveur de tuiles ni
dépendance extérieure. Il pourra être réexaminé si un besoin de zoom profond
apparaît.

La carte est un objet composé et habillé, avec titre, légende, échelle,
indicateurs et sources. Elle n'est pas un fond d'écran à bord perdu.

La direction artistique intervient après la validation d'une vue fonctionnelle
sur contenu réel. La vue de référence doit déjà être propre et lisible ; la
phase artistique définit ensuite l'identité complète : typographie, palette,
densité, langage cartographique, images, légendes et mouvements.

## 10. État des données utiles à l'application

Le corpus fournit notamment :

- 318 sites localisés avec un niveau de précision explicite ;
- 403 activités structurées ;
- 314 textes historiques exploitables ;
- 2 360 événements datés sur 314 sites, avec leur phrase source ;
- des relations entre sites, conservées seulement lorsqu'une source les
  établit ;
- les distances aux cours d'eau et d'autres informations territoriales ;
- un inventaire des médias et de leurs droits, sans autorisation de publication
  déduite automatiquement.

La situation actuelle demeure très incomplète : la conservation est inconnue
pour 315 sites sur 318. L'application doit le dire plutôt que combler le vide.

## 11. Règles de preuve

- Toute affirmation renvoie à une source vérifiable.
- Ce qui est inconnu reste explicitement inconnu.
- Une proximité spatiale n'est pas une causalité.
- Une relation n'est affichée que si une source l'établit.
- Une date imprécise reste un intervalle ou une borne ouverte.
- Une période documentée n'est pas une preuve d'activité continue.
- Un point localise un site selon un niveau de précision ; il ne représente pas
  son emprise.
- Un système calculé n'est pas un territoire historique délimité.

## 12. État du projet et suite

Les phases 0 à 9 sont terminées. En phase 10 :

- les données complémentaires ont été produites ;
- les douze systèmes ont été lus ;
- l'architecture de l'application est arrêtée ;
- une première vue sur la Risle a permis de valider le principe général.

La prochaine étape est une **vue fonctionnelle de référence** destinée à
valider la compréhension et les interactions. La direction artistique vient
ensuite sur cette base réelle, avant l'écriture complète et la construction de
l'application.
