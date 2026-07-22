# Recommandation pour l'application

Version 1.0 — 22 juillet 2026

## Décision recommandée

**Construire une publication web narrative et cartographique, pas un dashboard
et pas encore une application avec serveur.**

La première version doit être une publication statique, rapide et partageable,
alimentée par des exports générés depuis DuckDB. Le développement de l'interface
doit commencer après le premier lot significatif du corpus complet, pas après
l'enrichissement exhaustif des 319 dossiers.

## Forme du produit

La publication doit combiner quatre espaces :

1. **un récit guidé** en cinq ou six chapitres ;
2. **une carte exploratoire** avec filtres par période, secteur et précision ;
3. **des fiches de sites** affichant activités successives, sources et niveau
   d'incertitude ;
4. **une page méthode** expliquant corpus, classifications et limites.

Ce n'est pas un simple inventaire : l'entrée principale reste le récit. La
carte libre vient ensuite pour prolonger l'exploration.

## Architecture technique proposée

```text
Sources brutes
    ↓
Python — extraction, rapprochement, validation
    ↓
DuckDB — référence éditoriale interne
    ↓
Exports web versionnés — JSON / GeoJSON / Parquet
    ↓
Application statique — récit + carte + fiches
```

### Données

- DuckDB reste la base de référence hors ligne ;
- le navigateur ne charge pas directement la base complète ;
- un export par site alimente les fiches ;
- un export allégé alimente la carte ;
- les activités et périodes restent liées pour éviter les filtres trompeurs ;
- les géométries publiques peuvent être simplifiées ou dégradées selon leur
  précision et la sensibilité du site.

### Interface

Une pile cohérente serait :

- [**SvelteKit en export statique**](https://svelte.dev/docs/kit/adapter-static)
  pour les pages et composants narratifs ;
- [**MapLibre GL JS**](https://maplibre.org/maplibre-gl-js/docs/) pour la carte
  interactive ;
- [**Observable Plot**](https://observablehq.com/plot/) ou SVG natif pour les
  graphiques simples ;
- hébergement statique sur [GitHub Pages](https://docs.github.com/en/pages),
  Netlify ou équivalent pendant le MVP.

Ce choix évite une API, un serveur applicatif et une authentification tant que
le projet reste une publication éditoriale mise à jour par lots.

## MVP recommandé

Le MVP public peut contenir :

- le récit en six étapes proposé dans `recits_soutenus_donnees.md` ;
- le corpus complet minimalement cartographié ;
- 30 à 50 fiches plus riches sélectionnées éditorialement ;
- des filtres secteur, période et précision géographique ;
- l'affichage systématique des sources et incertitudes ;
- une page méthodologique ;
- aucune fonction de compte, contribution ou administration publique.

Les autres sites peuvent être présents avec une fiche plus courte. Il n'est pas
nécessaire d'attendre une recherche contemporaine et photographique exhaustive
sur les 319 dossiers pour publier une V1 honnête.

## Évolution vers une véritable application

Une architecture avec API, base en ligne et espace d'administration ne devient
utile que si le projet doit gérer :

- des mises à jour fréquentes par plusieurs personnes ;
- une collecte participative ;
- des parcours touristiques actualisés ;
- des comptes partenaires ;
- des médias volumineux ou des droits différenciés ;
- plusieurs départements ou plusieurs corpus.

L'orientation touristique reste compatible avec le modèle actuel. Elle
nécessitera plus tard des champs récents et vérifiés : visitabilité, horaires,
visibilité depuis l'espace public, propriété, services, accessibilité, durée de
parcours et date de mise à jour. Ces champs ne doivent pas être déduits des
notices historiques.

## Ordre de réalisation

1. généraliser l'extraction et traiter le premier lot de 50 ;
2. produire un prototype de récit avec la carte interne ;
3. terminer le corpus technique des 319 dossiers ;
4. sélectionner 30 à 50 sites éditoriaux ;
5. construire la publication statique ;
6. rechercher des partenaires pour la photographie, l'histoire, le graphisme
   et la future dimension touristique ;
7. décider seulement ensuite si une application avec serveur est nécessaire.

## Recommandation finale

**GO LIMITÉ pour l'application :** commencer le prototypage narratif après le
premier lot de 50 dossiers, tout en poursuivant le corpus complet. Ne pas
construire encore d'infrastructure serveur ni d'application touristique
opérationnelle.
