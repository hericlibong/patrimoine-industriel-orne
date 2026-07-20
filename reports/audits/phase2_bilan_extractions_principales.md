# Phase 2 — Bilan des extractions des sources principales

Date du test : 20 juillet 2026  
Manifeste technique : `phase2_extraction_samples_manifest.json`

## Objectif

Vérifier sur de petits échantillons que les cinq sources prioritaires peuvent
être récupérées de façon reproductible, sans encore évaluer complètement leurs
champs, leurs doublons ou leur qualité géographique. Cette évaluation détaillée
constitue le bloc suivant de la phase 2.

## Résultats

| Source | Échantillon | Accès testé | Résultat immédiat | Première conclusion |
|---|---:|---|---|---|
| Inventaire normand | 10 dossiers, 20 fichiers d'index et de sommaire | anciens dossiers statiques officiels | 10 dossiers accessibles, référençant 186 pages numérisées | indexation automatisable, téléchargement des scans encore à tester |
| Mérimée / POP | 10 notices IA correspondant aux mêmes sites | pages de notices POP | 10 notices accessibles ; les 10 relient le portail régional et le dossier statique | récupération automatisable ; extraction des champs HTML à construire |
| Palissy | 2 objets techniques ciblés | API data.culture.gouv.fr | 2 notices, 82 champs sur la première ; aucune référence Mérimée directe renseignée | récupération automatisable ; rattachement au site à contrôler autrement |
| Monuments historiques | 77 résultats larges dans l'Orne | API data.culture.gouv.fr | 77 notices, 76 champs sur la première, 50 avec coordonnées | récupération automatisable ; la sélection par mots-clés contient des faux positifs |
| CASIAS | 10 entrées localisées et 10 déclarées non géolocalisées | service WFS officiel | 10/10 coordonnées dans le premier lot, 0/10 dans le second ; 11 noms d'établissement manquants sur 20 | récupération automatisable ; localisation et qualification très inégales |

## Lecture par source

### Inventaire normand

Le jeu annoncé sur data.gouv.fr ne fournit plus, au moment du test, un export
global exploitable : l'ancienne ressource CSV redirige vers le portail régional
et l'ancien service cartographique renvoie une erreur. Le portail régional
oppose par ailleurs un contrôle JavaScript aux requêtes directes.

Une voie officielle reste disponible : les notices POP renvoient vers les
anciens dossiers statiques du ministère de la Culture. Les index et sommaires de
pages des dix dossiers tests ont tous été récupérés. Les dossiers détaillés sont
principalement des images numérisées : leurs URL peuvent être inventoriées
automatiquement, mais le téléchargement des scans reste à tester. L'extraction
du texte demandera ensuite de l'OCR et une vérification humaine.

### Mérimée / POP

Les dix références `IA` choisies dans l'Inventaire sont accessibles sur POP. Ce
canal est plus adapté à l'extraction structurée des informations descriptives
que les scans des anciens dossiers. Le prochain bloc devra mesurer précisément
les champs récupérables et choisir entre parsing des pages et autre export POP.

### Palissy

L'API permet de cibler exactement des références. Les deux objets techniques
tests sont bien récupérés. Leur champ de référence directe vers une notice
Mérimée n'est toutefois pas renseigné : la liaison objet-site ne pourra donc pas
reposer systématiquement sur une clé commune et devra parfois être vérifiée par
l'édifice, la commune et les textes descriptifs.

### Monuments historiques

La recherche plein texte volontairement large retourne 77 notices. Ce chiffre
n'est ni un nombre de sites industriels ni un corpus à publier : les termes
comme « moulin » peuvent apparaître dans des notices sans que le monument soit
un site industriel pertinent. Les 27 notices sans coordonnées devront aussi
être localisées autrement si elles sont retenues après qualification.

### CASIAS

Le service WFS accepte les filtres sur le département et la nature de la
localisation. Les deux lots tests prouvent que les coordonnées absentes ne sont
pas un incident d'extraction : certaines fiches sont bien déclarées « site non
géolocalisé ». CASIAS reste donc une liste de candidats à recouper, pas une carte
directement publiable. L'absence fréquente du nom d'établissement et du champ
d'activité dans la couche régionale renforce ce besoin de recoupement.

## Traçabilité

- 34 fichiers bruts ont été récupérés ;
- chaque fichier possède un fichier voisin de métadonnées ;
- les 34 couples ont été contrôlés par nom, taille et empreinte SHA-256 ;
- les données brutes sont conservées dans `data/raw/` et exclues de Git ;
- le manifeste versionné contient les chemins, empreintes et observations ;
- le code d'extraction et ses validateurs sont couverts par 17 tests locaux.

## Décision à ce stade

Les cinq sources peuvent entrer dans la chaîne technique. Aucun téléchargement
massif n'est encore lancé. Le bloc suivant doit évaluer les champs, valeurs
manquantes, identifiants, doublons et coordonnées avant de retenir les méthodes
d'extraction définitives.
