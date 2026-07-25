# Phase 8 — Enrichissement et localisation du corpus complet

Date : 23 juillet 2026  
Statut : **bloc terminé**

## Résultat simple

Le corpus principal reste fixé à **318 sites**. Les sources complémentaires
enrichissent ou recoupent ce corpus ; elles ne créent pas automatiquement de
nouveaux sites.

### Mérimée et Monuments historiques

- 2 346 notices Mérimée de l'Orne examinées, dont 410 références `PA` ;
- 16 protections rattachées à 16 sites ;
- chaque rattachement repose sur une référence `IA` explicitement présente
  dans la notice `PA` ;
- 11 protections possèdent aussi un point MH : les 11 sont à moins de 250 m du
  point de l'Inventaire.

### Palissy

- 5 066 notices Palissy de l'Orne examinées, dont 3 343 références `PM` ;
- les 31 objets techniques déjà recensés aux forges de Varenne sont conservés ;
- leur association reste indiquée `à vérifier`, car POP ne fournit pas de lien
  direct vers le site industriel ;
- aucun autre objet n'est rattaché sur la seule commune ou une simple
  ressemblance de nom.

### CASIAS

- 2 052 entrées examinées ;
- 131 recoupements retenus pour 123 sites du corpus ;
- 87 ont satisfait les règles conservatrices ; 44 autres ont été confirmés
  après lecture du nom, du lieu, de l'adresse et de l'activité ;
- 10 candidats ont été rejetés et 8 restent explicitement ambigus ;
- 170 entrées constituent une file d'élargissement possible. Ce ne sont **ni
  170 sites patrimoniaux confirmés, ni des ajouts au corpus**.

CASIAS sert donc à confirmer ou suggérer. Ses coordonnées ne remplacent jamais
la localisation patrimoniale et la proximité seule ne prouve pas l'identité.

### Localisation

- 318 sites sur 318 possèdent un point source valide dans l'Orne ;
- 28 points sont associés à une zone documentaire déjà qualifiée ;
- 290 restent des `points_approximatifs` ;
- aucun point n'a été inventé, aucun doublon exact de coordonnées n'a été
  détecté ;
- les géométries de travail sont en Lambert-93 et les échanges web en WGS84.

### Contexte territorial

Les distances ont été calculées pour les 318 sites :

- cours d'eau : 103 sites à moins de 25 m, 213 à moins de 100 m, 297 à moins
  de 500 m ;
- forêt : 12 sites dans une formation forestière, 151 autres à moins de 100 m,
  293 sites au total à moins de 500 m ou dans une formation ;
- minerais : 13 sites à moins de 1 km d'un indice BRGM, 215 à moins de 10 km ;
- rail : 10 sites à moins de 100 m, 72 à moins de 500 m, 149 sans tronçon
  répertorié dans un rayon de 5 km.

Ces valeurs sont des **indices spatiaux**. Elles ne démontrent pas à elles
seules que l'eau, la forêt, le minerai ou le rail expliquent l'implantation.

## Traces et fichiers de contrôle

- décisions CASIAS : `config/phase8_decisions_enrichissement.yml` ;
- résumé machine : `reports/quality/phase8_enrichissement_resume.json` ;
- protections MH : `reports/quality/phase8_protections_mh.csv` ;
- objets Palissy : `reports/quality/phase8_objets_palissy.csv` ;
- recoupements CASIAS : `reports/quality/phase8_recoupements_casias.csv` ;
- élargissement CASIAS : `reports/quality/phase8_casias_elargissement.csv` ;
- ambiguïtés : `reports/quality/phase8_ambiguities_enrichissement.csv` ;
- bilan territorial : `reports/quality/phase8_contexte_territorial.json`.
