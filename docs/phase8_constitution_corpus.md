# Phase 8 — Constitution du corpus

Statut : **en cours par lots depuis le 22 juillet 2026**.

## Adaptation du bloc initial

Le bloc ne peut pas être exécuté comme une opération unique sur 319 dossiers.
Il est découpé en un lot d'énumération, le pilote déjà traité, un premier lot
de 50 nouveaux dossiers, puis cinq lots supplémentaires. Les cases portant sur
le corpus entier resteront ouvertes jusqu'au traitement du dernier lot.

Répartition prévue :

| Ensemble | Dossiers | Rôle |
|---|---:|---|
| pilote existant | 30 | méthode déjà validée |
| lot 1 | 50 | calibration de la chaîne complète |
| lots 2 à 5 | 50 chacun | généralisation contrôlée |
| lot 6 | 39 | solde du corpus |
| total | 319 | dossiers sources, pas nombre final de sites |

## Énumération définitive

Le portail régional annonce 319 dossiers sur 16 pages mais oppose un contrôle
anti-robot aux requêtes directes. La première hypothèse d'une plage continue de
références a été rejetée : elle omettait des dossiers récents et conservait des
références anciennes absentes du corpus actuel.

La méthode retenue utilise la recherche avancée de l'API publique POP sur le
cadre d'étude exact `patrimoine industriel (patrimoine industriel de l’Orne)`.
Elle renvoie 320 notices :

- la notice de présentation `IA61000851`, exclue parce qu'elle ne décrit pas un
  site ;
- 319 dossiers sources uniques, soit le total annoncé par le portail régional.

La liste contient deux références hors de l'ancienne plage principale :
`IA00062725` et le dossier collectif `IA61001399`. Un dossier collectif n'est
pas exclu : il doit être décomposé en emprises pendant la revue.

Les preuves sont conservées dans
`reports/audits/phase8_enumeration_corpus.json` et
`reports/audits/phase8_references_ia.csv`.

## Changement de méthode POP

L'API actuelle de POP fournit désormais :

- une recherche structurée pour énumérer le corpus ;
- une notice JSON par référence avec contrôle du champ `REF`.

Le JSON de l'API devient donc l'accès principal. L'ancien parseur du HTML
Next.js reste un repli testé, mais n'est plus utilisé pour les nouveaux lots.
Chaque réponse brute est archivée avec son empreinte, ses métadonnées et son
manifeste.

## Règles dossier–site

- une référence `IA` représente un dossier source, pas encore un site ;
- un dossier est d'abord enregistré comme `un_site_presume_a_verifier` ;
- une adresse, une commune ou un titre communs ne déclenchent jamais une
  fusion automatique ;
- plusieurs communes, adresses ou emprises dans un dossier déclenchent une
  vérification de séparation ;
- des activités successives sur une même emprise restent attachées au même
  site ;
- toute fusion, séparation, exclusion ou incertitude doit avoir une décision
  et une justification ;
- le nombre départemental de sites canoniques reste inconnu jusqu'à la revue
  des 319 dossiers.

## Résultat du lot 1

Le lot 1 comprend 50 dossiers non pilotes répartis de manière systématique sur
la liste triée des références. Il sert à rencontrer des variantes de notices ;
il ne constitue pas un échantillon statistique.

Résultats :

- 50 notices JSON archivées et 50 champs `REF` concordants ;
- 62 dénominations sources, toutes classées après passage du registre en
  version 1.3 ;
- 11 dossiers multi-activités ;
- 4 dossiers multi-secteurs relus ;
- ces 4 cas décrivent des conversions successives sur une même emprise ;
- aucun rapprochement automatique ni aucune séparation automatique ;
- 50 sites provisoires pour le seul lot 1 ;
- nombre canonique du corpus complet toujours inconnu.

Les décisions manuelles sont dans `config/phase8_lot1_decisions.yml`. Les
sorties de travail sont dans `reports/quality/phase8_lot1_*`.

## Évolution des classifications

Le lot a révélé onze termes absents des correspondances exactes. Ils ont été
ajoutés sans classement par mot-clé : fenderie, haut fourneau, moulin à foulon,
tissage, confection, ferblanterie, matériel d'équipement industriel,
passementerie, pâte à papier, serrurerie et travail du bois.

Quatre activités et une installation ont été ajoutées au vocabulaire :
`production_fonte`, `foulage_textile`, `passementerie`, `travail_bois` et
`haut_fourneau`. Le registre passe de la version 1.2 à la version 1.3 et de 177
à 182 codes publiés.

## Ce qui reste à faire

- réintégrer formellement les 30 pilotes dans le corpus commun ;
- traiter les 239 dossiers non pilotes restants ;
- revoir le dossier collectif et tous les indices d'emprises multiples ;
- documenter les rapprochements entre dossiers ;
- établir le nombre final de sites seulement après ces décisions.
