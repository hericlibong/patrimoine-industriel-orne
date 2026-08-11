# Phase 10.C — Architecture de l'application

**Version :** 1.0 — six décisions arrêtées
**Statut :** validé par le porteur du projet le 11 août 2026
**Date :** 11 août 2026

Chaque décision porte son motif et l'option écartée. Les points laissés ouverts
— nom de la publication, premières secondes, amorces cliquables — sont traités
séparément.

---

## 1. La carte s'ouvre sur le département, systèmes en objets principaux

**Décision.** À l'arrivée, le lecteur voit les **douze systèmes** comme objets
principaux, les **146 autres sites** en points fins et discrets, et le réseau
hydrographique en fond. Cliquer sur un système y entre.

**Conséquence à l'écran.** Douze ensembles nommés sur l'Orne, avec leur nombre
de sites. Le sujet tient en entier dès la première seconde.

**Motif.** C'est la seule échelle où l'on comprend qu'il y a douze histoires et
non trois cent dix-huit points. Le cadrage V2 l'impose : « les 318 sites ne
doivent jamais apparaître comme 318 objets ».

**Option écartée.** Les 318 points identiques du prototype 0.1, illisibles à
1440 px.

**Contrainte de représentation.** Un système est figuré par **ses sites
regroupés et un nom posé à côté** — jamais par un contour fermé, un polygone ou
une zone colorée. Une forme fermée ferait croire à une frontière ou à une emprise
historique vérifiée, qui n'existe pas : le regroupement résulte d'une règle de
proximité que nous avons choisie.

**Réserve.** Tant que les noms ne sont pas validés, l'étiquette affiche la
commune principale.

---

## 2. Trois leviers de filtrage, et la recherche

### Retenus

| Levier | Ce qu'il fait | Pourquoi il tient |
| --- | --- | --- |
| **Métier** | les neuf secteurs du corpus | c'est lui qui fait apparaître le contraste Risle/Noireau |
| **Époque** | une réglette d'années | 2 320 événements datés le rendent enfin possible |
| **Proximité de l'eau** | distance mesurée au cours d'eau le plus proche | médianes de 21 à 30 m dans les vallées contre 344 m pour les matériaux |
| *Recherche* | nom, commune, activité, référence | seule façon d'atteindre un site précis parmi 318 |

### Exclus

| Levier | Motif de l'exclusion |
| --- | --- |
| **Forêt** | médiane du corpus à 94 m : ne discrimine rien |
| **Minerai** | trompeur — les forges de Randonnai sont à 12 km du premier indice recensé alors qu'un lavoir à mines y est attesté en 1855 |
| **Rail** | 149 sites sur 318 hors du rayon de recherche |
| **Situation actuelle** | 3 sites documentés sur 318 : un filtre qui ne rend presque rien |
| **Précision géographique** | outil de spécialiste ; reste affiché en symbole et dans la fiche |

**Motif d'ensemble.** Ne conserver que les leviers dont il a été **vérifié**
qu'ils font apparaître quelque chose. La liste du bloc 4 datait d'avant les
mesures.

**Option écartée.** Les six filtres prévus en juillet.

### Deux règles de langage, non négociables

**La proximité de l'eau est une mesure, pas une cause.** Le filtre affiche une
distance constatée. Il ne dit ni que la rivière explique l'implantation, ni
qu'elle fournissait l'énergie du site. Le libellé public doit dire « à moins de
100 mètres d'un cours d'eau », jamais « alimenté par la rivière ».

**Le filtre temporel ne déduit jamais qu'une usine était active.** Voir la
décision 3.

---

## 3. Le temps : une période documentée, jamais une activité déduite

**Décision.** La réglette d'années sélectionne les sites dont la **période
documentée** couvre l'année choisie. Elle n'affirme pas qu'ils fonctionnaient
cette année-là.

**Conséquence à l'écran.** Le compteur affiche « *31 sites dont la période
documentée couvre 1900* », et non « 31 usines en activité ». Une mention
permanente accompagne la réglette :

> Une période documentée n'est pas une preuve d'activité continue. La date de
> départ est souvent une **première mention** : un moulin attesté en 1809
> existait avant.

**Motif.** Entre une première attestation et une cessation, le corpus ne dit
rien des interruptions. Plusieurs sites lus ont chômé puis repris — les
affineries de Randonnai sont « inactives en 1804 » et « restaurées vers 1810 ».
Afficher « en activité » serait inventer une continuité que les sources
n'établissent pas.

**Option écartée.** Le compteur « usines en activité », employé dans l'écran de
référence de la Risle. **Il doit y être corrigé.**

---

## 4. La carte recadre au lieu d'atténuer

**Décision.** À chaque changement de levier, la carte se **recadre** sur ce qui
reste. Jamais en dessous de l'échelle d'un système. Un contrôle permanent ramène
au département.

**Conséquence à l'écran.** Choisir « métal » rapproche la carte des vallées
métallurgiques au lieu de laisser le lecteur chercher ce qui a changé.

**Motif.** L'atténuation seule est invisible : le prototype 0.1 mettait en
évidence 213 points sur 318 et le résultat restait « visuellement proche de la
carte précédente ».

**Option écartée.** Atténuer sans bouger le cadrage.

---

## 5. Des adresses partageables, compatibles avec un fichier hors ligne

**Décision.** L'état de l'application vit dans le **fragment de l'adresse**,
après le `#`, et non dans le chemin.

```text
#systeme=la-vallee-du-fil
#site=IA00061155
#metier=metal&annee=1900
#systeme=le-noireau&annee=1935
```

**Conséquence à l'écran.** On peut envoyer à quelqu'un « la Risle en 1900,
filtrée sur le métal », et le lien fonctionne — y compris sur un fichier ouvert
depuis un disque, sans serveur ni connexion.

**Motif.** La publication doit rester une application statique fonctionnant hors
ligne. Un chemin du type `/systeme/la-vallee-du-fil` exigerait un serveur qui
sache le router : cela romprait cette contrainte.

**Option écartée.** Les chemins d'URL, et l'état conservé seulement dans
l'historique du navigateur — qui n'est pas partageable.

---

## 6. Tout ce que la carte montre existe en texte

**Décision.** Une liste synchronisée, toujours atteignable, contenant les mêmes
sites, les mêmes chiffres et les mêmes libellés que la carte. Les annotations
sont du texte réel, jamais des images.

**Conséquence à l'écran.** Qui ne voit pas la carte lit la même chose dans la
liste, sans perte.

**Motif.** Règle d'accessibilité du cadrage V2. Elle rend aussi la publication
citable et indexable.

**Option écartée.** Une version texte séparée, qui diverge toujours de la
version principale.

---

## 7. Pas de moteur cartographique : un SVG produit depuis nos données

**Décision.** La carte est un **SVG généré** à partir du corpus et des couches
géographiques locales, comme dans l'écran de référence de la Risle.

**Conséquence à l'écran.** Une carte entièrement composée par nous : nos
rivières, nos sites, nos systèmes, sans décor imposé, sans serveur de tuiles,
fonctionnant hors ligne.

**Motif.** Simplicité et **besoin de composition sur mesure**. Nous ne
cherchons pas un fond de carte du monde réel mais une figure construite pour une
démonstration précise, où chaque trait a une raison d'être. Aucune dépendance
externe, aucun service tiers, un seul fichier.

**Option écartée.** MapLibre GL JS. Ce n'est pas qu'il imposerait le plein écran
— il s'encadre parfaitement. C'est qu'il apporterait un fond de carte
contemporain, avec ses routes, ses noms et ses couleurs, que nous ne contrôlons
pas et qui parasiterait la lecture.

**Réserve.** À revoir si le besoin d'un zoom profond apparaît : le SVG atteint
ses limites au-delà de l'échelle du site.

---

## 8. Titre de travail

**Décision.** La publication porte le titre de travail **« Voyage dans l'Orne
industrielle »**. Il est provisoire et pourra changer.

---

## 9. Ce que voit le lecteur en arrivant

**Décision.** Le lecteur voit **directement la carte de l'Orne** : les douze
systèmes, les autres sites, et les commandes de recherche et de filtrage.
**Aucun parcours ni récit ne lui est imposé.**

**Conséquence à l'écran.** Pas d'écran d'accueil, pas de séquence introductive,
pas de bouton « commencer ». L'outil est là, immédiatement manipulable.

**Motif.** Le produit est une application, pas un article. Imposer une entrée
narrative reproduirait la logique de site qui a fait échouer la première
tentative.

---

## 10. Les amorces cliquables sont reportées

**Décision.** Les amorces ne sont **pas définies maintenant**. Elles pourront
être ajoutées après matérialisation de la visualisation, **si elles apportent
une aide réelle**.

**Règle de rédaction, si elles sont ajoutées.** Les intitulés resteront
**concrets et décriront exactement ce que la commande affiche**. Pas de
formulation abstraite ni de question rhétorique.

Exemple de ce qui est attendu : « les usines à moins de 100 mètres d'un cours
d'eau ». Exemple de ce qui est écarté : « pourquoi toutes au bord de l'eau ? ».

**Note.** Il avait été avancé qu'une carte ouverte sans amorce resterait un
outil plutôt qu'une publication. L'objection n'est pas écartée mais **différée** :
elle sera tranchée devant la visualisation réelle, ce qui est plus sûr que de la
trancher sur une hypothèse.
