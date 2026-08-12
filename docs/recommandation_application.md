# Recommandation pour l'application

**Version :** 2.0

**Date :** 12 août 2026

**Statut :** recommandation actualisée après validation de l'architecture

## Décision recommandée

Construire une **visualisation web interactive de datajournalisme**, statique,
rapide et partageable, consacrée aux 318 sites industriels documentés dans
l'Orne.

Le produit s'ouvre directement sur une carte manipulable. Il ne prend la forme
ni d'un article à chapitres, ni d'un catalogue de fiches, ni d'un tableau de
bord. Le lecteur choisit librement un système, un métier, une époque ou un lieu.

Le titre de travail est **« Voyage dans l'Orne industrielle »**. Il est
provisoire.

## Forme recommandée

La visualisation combine dans un même espace :

1. une carte départementale montrant les douze systèmes comme objets
   principaux et les 146 autres sites plus discrètement ;
2. des commandes limitées au métier, à l'époque et à la proximité de l'eau ;
3. une recherche par nom, commune, activité ou référence ;
4. une liste textuelle synchronisée avec la carte ;
5. des vues de système et de site portant les textes, dates, relations, sources
   et limites disponibles.

Aucun parcours n'est imposé. Les amorces éventuelles seront décidées devant la
visualisation réelle et devront décrire concrètement ce qu'elles affichent.

## Périmètre éditorial

Les douze systèmes déjà lus constituent le cœur éditorial. Ils couvrent 172
sites.

Les 146 autres sites restent tous visibles et consultables :

- 74 sites forment 18 petits ensembles de trois à six sites. Leur lecture est
  reportée et pourra enrichir ultérieurement l'application ;
- 72 sites sont seuls ou par paires selon la règle de proximité retenue. Ils ne
  font pas l'objet d'un chapitre particulier.

Aucun site n'est supprimé. Le seuil de trois kilomètres sert à organiser la
lecture ; il ne définit pas une frontière historique.

## Architecture technique recommandée

```text
Sources brutes et corrections documentées
    ↓
Python — extraction, rapprochement et validation
    ↓
DuckDB — référence éditoriale interne
    ↓
Exports web légers et versionnés
    ↓
Application statique — carte SVG + liste + panneaux d'information
```

Principes techniques :

- DuckDB reste la base de référence hors ligne ;
- le navigateur reçoit seulement des exports adaptés au web ;
- la carte est un SVG généré depuis les données et les couches locales ;
- l'application ne dépend ni d'une API ni d'un serveur de tuiles ;
- l'état partageable est conservé après le `#` dans l'adresse ;
- chaque information cartographique possède un équivalent textuel ;
- le choix d'un framework JavaScript n'est pas nécessaire avant qu'un besoin
  concret le justifie.

Le SVG est retenu pour la simplicité et la composition sur mesure. Ce choix
pourra être réexaminé si l'application exige plus tard un zoom profond ou des
volumes de données sensiblement supérieurs.

## Règles fonctionnelles

- La carte s'ouvre sur le département puis permet d'entrer dans un système.
- Elle se recadre sur le résultat d'un filtre au lieu de seulement atténuer les
  autres points.
- Un système apparaît comme un groupe de sites nommé, jamais comme une zone aux
  frontières supposées.
- Le filtre temporel indique une **période documentée**, pas une activité
  certaine et continue.
- La distance à l'eau reste une mesure, pas une explication causale.
- Les sources, incertitudes et niveaux de précision restent visibles.

## Première réalisation recommandée

Construire une seule vue fonctionnelle complète avec des données réelles pour
valider :

- l'arrivée sur le département ;
- la sélection d'un système ;
- un filtre et le recadrage de la carte ;
- l'ouverture d'un site ;
- la liste synchronisée ;
- la navigation au clavier ;
- le retour à la vue départementale.

Cette vue doit être propre et lisible, mais ne porte pas encore l'identité
visuelle définitive. Son rôle est de vérifier la structure et les interactions.

## Direction artistique

Une fois la vue fonctionnelle comprise et validée, la direction artistique est
appliquée sur ce contenu réel. Elle doit traiter au minimum :

- la typographie et les niveaux de titre ;
- la palette et le contraste ;
- la représentation des systèmes, des sites, des relations et des
  incertitudes ;
- la densité de l'interface ;
- les annotations, images, légendes et crédits ;
- les comportements sur grand écran, ordinateur portable et mobile.

Cette étape ne doit pas être repoussée jusqu'à la fin de l'application : elle
vient immédiatement après la validation de la vue de référence.

## Ordre de réalisation

1. construire et valider la vue fonctionnelle de référence ;
2. définir et appliquer la direction artistique à cette vue ;
3. écrire les contenus nécessaires pour les systèmes et les sites ;
4. étendre la vue validée à l'ensemble du corpus ;
5. contrôler accessibilité, exactitude, performances et droits ;
6. publier une version statique documentée et reproductible.

## Évolutions possibles

Après stabilisation de la première version, le projet pourra accueillir :

- la lecture éditoriale de certains des 18 petits ensembles ;
- des vues par exploitant ou propriétaire lorsque les données seront validées ;
- de nouvelles commandes réellement justifiées par les données ;
- des informations contemporaines vérifiées ;
- une architecture avec API seulement si des mises à jour fréquentes, plusieurs
  contributeurs ou une collecte participative le nécessitent.

Ces possibilités ne doivent pas retarder la construction de la première
version.

## Recommandation finale

**GO pour une application statique de visualisation interactive**, construite
par étapes à partir d'une vue fonctionnelle puis d'une direction artistique
validée. Aucun serveur applicatif, compte utilisateur ou administration en
ligne n'est nécessaire pour la première version.
