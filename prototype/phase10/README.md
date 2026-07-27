# Prototype navigable — phase 10, bloc 6

Statut : **version 0.1 validée uniquement comme point de départ, avec réserves
importantes**.

Le récit, l'exploration, les pages `Les lieux` et la direction artistique ne
sont pas validés dans leur forme actuelle. Le prototype sert désormais de base
concrète pour identifier ce qui doit être conservé, repris ou supprimé.

Ce prototype matérialise l'expérience définie pendant les blocs 1 à 5. Il ne
préjuge pas encore de la pile technique du MVP.

## Lancer

Depuis la racine du dépôt :

```powershell
python -m http.server 8765 --bind 127.0.0.1
```

Puis ouvrir :

<http://127.0.0.1:8765/prototype/phase10/>

Le chargement direct du fichier `index.html` n'est pas pris en charge : les
données et la carte sont chargées par requêtes locales.

## Parcours à examiner

1. l'accueil et l'entrée dans le récit ;
2. les six étapes du récit guidé et la carte qui évolue au défilement ;
3. l'exploration libre, ses quatre filtres et la recherche ;
4. l'alternative en liste et le panneau synthétique d'un site ;
5. les trois récits de lieu : Ozé–Moulinex, Abadie et Bohin ;
6. la page méthode ;
7. l'affichage mobile.

## Données

Le prototype charge les 318 sites et les 403 phases du corpus V1. Les fichiers
web sont régénérés ainsi :

```powershell
python tools/generate_phase10_prototype.py
node tools/generate_phase10_context_map.mjs
```

Les photographies sont déjà intégrées comme éléments narratifs. Leurs légendes
et crédits seront finalisés avec les textes éditoriaux.

## Limites volontaires de la version 0.1

- carte de contexte statique, sans moteur cartographique ni zoom ;
- trois récits de lieu seulement ;
- textes de démonstration encore soumis à revue journalistique ;
- aucune optimisation finale du poids de la carte ;
- aucune publication ni hébergement configuré.

Ces limites servent à évaluer la forme et les passages entre les modes de
lecture avant le développement du MVP.
