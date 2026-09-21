Nous avons identifié une fonctionnalité importante absente du prototype actuel : le filtrage temporel des lieux industriels.

Avant toute implémentation, je veux une analyse critique et une contre-proposition documentée. Ne modifie pas le prototype, le générateur, les données ou la roadmap. Ne crée pas de branche et ne lance aucun développement.

CONTEXTE

Le prototype possède actuellement un filtre par métier, mais aucun filtre temporel. Pourtant, les lieux et leurs activités ne relèvent pas tous des mêmes périodes. Certains traversent plusieurs siècles ou plusieurs phases historiques.

Le filtre temporel avait déjà été envisagé dans la documentation du projet, mais il n’a pas été réintégré pendant la reconstruction de la phase 10D.

Consulte notamment :

- docs/roadmap.md
- docs/phase10_carte_exploratoire_filtres.md
- docs/classifications_chronologie_situation.md
- docs/dictionnaire_donnees.md
- docs/methodologie.md
- docs/regles_modele.md
- docs/phase10_cadrage_v2_application.md
- docs/F10_site/roadmap_mode_lieu.md
- config/classifications.yml
- data/exports/sites_corpus_complet_v1.csv
- data/exports/activites_corpus_complet_v1.csv
- tools/generer_vue_reference.py
- tools/vue_reference_gabarit.html

Vérifie toi-même les données et les effectifs. Les constats actuels sont les suivants :

- 318 lieux dans le corpus ;
- 403 phases d’activité ;
- 29 lieux et 42 phases seulement possèdent actuellement une période d’activité suffisamment structurée ;
- les 318 lieux possèdent des périodes issues des siècles documentaires de la source, mais celles-ci datent principalement des constructions ou transformations et ne prouvent pas une activité continue.

Cette distinction est impérative :

1. période d’activité calculée depuis une phase datée ;
2. siècle ou période documentaire issu de la notice ;
3. événement ponctuel extrait de la chronologie.

Ces trois informations ne doivent pas être mélangées silencieusement.

PROPOSITION À ÉVALUER

Ajouter avant la direction artistique un complément fonctionnel à 10D :

### Intitulé envisagé

« Période d’activité documentée »

### Périodes existantes

- Avant 1789
- 1789–1849 — Révolution et première industrialisation
- 1850–1913 — Industrialisation, rail et vapeur
- 1914–1945 — Guerres et entre-deux-guerres
- 1946–1975 — Modernisation d’après-guerre
- 1976–2000 — Mutations et reconversions
- Depuis 2001 — Patrimoine et usages contemporains

Ces périodes existent déjà dans `config/classifications.yml`.

### Fonctionnement envisagé

- « Toutes les périodes » par défaut.
- Une seule période sélectionnée à la fois dans la première version.
- Un lieu apparaît si au moins une de ses phases d’activité documentées chevauche la période choisie.
- Une phase qui chevauche plusieurs périodes appartient à chacune d’elles.
- Un lieu peut donc apparaître dans plusieurs périodes.
- Les lieux insuffisamment datés restent visibles lorsque le filtre est vide.
- Lorsqu’une période est sélectionnée, les lieux insuffisamment datés sont retirés des résultats.
- L’interface doit expliquer clairement la couverture limitée, par exemple : « 29 lieux suffisamment datés pour ce filtre ».
- Le filtre s’applique aux trois niveaux : département, ensemble et lieu.
- Son état doit être conservé pendant la navigation et restauré au retour.
- Les ensembles ne contenant aucun lieu correspondant disparaissent de la liste, comme avec le filtre métier.
- Le filtre métier et le filtre temporel doivent porter sur la même phase d’activité. Exemple : un lieu ne doit pas apparaître sous « Métallurgie + 1850–1913 » si sa métallurgie appartient à une autre période et si seule une activité textile correspond à 1850–1913.
- Les résultats doivent toujours être dédupliqués par lieu.
- Le filtre doit rester utilisable au clavier et sur écran étroit.
- Aucun style définitif n’est demandé avant 10E.

### Séquence envisagée

1. transmettre au prototype les périodes de chaque phase d’activité ;
2. ajouter la commande et les compteurs ;
3. combiner correctement métier et période ;
4. vérifier les trois niveaux de navigation ;
5. vérifier ordinateur, mobile et clavier ;
6. clore définitivement 10D ;
7. engager ensuite 10E, direction artistique.

TRAVAIL DEMANDÉ

Produis dans un seul document :

`docs/phase10_filtre_temporel.md`

Ce document devra contenir les sections suivantes.

## 1. Analyse de l’idée

Évalue l’intérêt éditorial et fonctionnel du filtre :

- ce qu’il permet réellement de comprendre ;
- ce qu’il ne permet pas d’affirmer ;
- les risques de confusion entre activité, construction, transformation et événement ;
- l’intérêt de le réaliser avant ou après la direction artistique ;
- l’impact sur les trois niveaux département, ensemble et lieu.

## 2. Analyse de la proposition

Examine chaque règle proposée :

- exactitude par rapport au modèle de données ;
- couverture réelle ;
- faisabilité technique ;
- combinaison avec le métier ;
- traitement des lieux insuffisamment datés ;
- cas des activités qui traversent plusieurs périodes ;
- pertinence des sept périodes ;
- intérêt ou non d’utiliser des siècles ou des demi-siècles ;
- pertinence de la période « Depuis 2001 » dans ce filtre ;
- effet sur les compteurs, la carte, les ensembles et les listes ;
- accessibilité, mobile et conservation de l’état.

Indique précisément ce qui est valide, ce qui doit être corrigé et ce qui demande un arbitrage.

## 3. Comparaison des trois sources temporelles

Présente clairement, sous forme de tableau si utile :

- périodes d’activité structurées ;
- périodes documentaires issues de `SCLE` ou des notices ;
- événements datés de la chronologie.

Pour chacune, indique :

- sa couverture ;
- ce qu’elle prouve ;
- ce qu’elle ne prouve pas ;
- si elle peut alimenter un filtre public ;
- le libellé honnête à employer.

Évalue notamment s’il faut proposer :

- un seul filtre strict sur les phases d’activité ;
- un filtre documentaire plus large mais formulé autrement ;
- deux modes distincts ;
- ou aucune combinaison dans la première version.

## 4. Contre-proposition ou enrichissement

Propose ta solution recommandée.

Elle doit préciser :

- le nom exact du filtre ;
- les périodes proposées ;
- sélection simple ou multiple ;
- la règle de correspondance ;
- la combinaison avec le métier ;
- le message de couverture ;
- le traitement des lieux non datés ;
- le comportement aux trois niveaux ;
- les libellés destinés au lecteur ;
- les éventuelles explications méthodologiques ;
- ce qui appartient à 10D et ce qui peut attendre 10E.

Si tu estimes que la proposition initiale est déjà la meilleure, enrichis-la sans créer artificiellement une alternative.

## 5. Mini-roadmap proposée

Présente une mini-roadmap courte et vérifiable comprenant :

- phases ;
- tâches ;
- livrable de chaque phase ;
- contrôles ;
- validation du porteur entre les phases.

Ne lance aucune de ces tâches.

## 6. Arbitrages attendus du porteur

Termine par une liste courte des décisions que je dois prendre avant le développement.

CONTRAINTES

- Aucun code.
- Aucun changement dans les exports.
- Aucune modification de la roadmap principale.
- Aucune création de branche.
- Aucun lancement de 10E.
- Ne présente jamais une période de construction comme une durée d’activité.
- Ne transforme jamais une absence de datation en absence historique.
- Ne suppose pas qu’un lieu a été actif sans interruption entre deux dates.
- Reste concis et concret.

À la fin, fournis seulement un rapport bref indiquant le document créé et les principaux arbitrages proposés. Attends ensuite ma validation.