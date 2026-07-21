# Enrichissement des 30 sites pilotes

Date du contrôle : 21 juillet 2026

## Résultat simple

| Élément | Résultat |
|---|---:|
| Sites dotés d'un UUID interne stable | 30 |
| Phases d'activité structurées | 47 |
| Protections MH confirmées par un lien `PA` → `IA` | 6 |
| Rapprochement MH rejeté | 1 |
| Notices Palissy recensées | 31 |
| Situations actuelles appuyées par une source récente | 4 |
| Situations actuelles encore inconnues | 26 |
| Mentions de sources enregistrées dans le corpus de travail | 71 |
| Anomalies ou limites documentées | 6 |

Le contrôle automatique ne signale aucune erreur structurelle.

## Ce qui a été enrichi

- Chaque dossier `IA` possède maintenant un UUID v4 propre au projet.
- Les activités successives sont séparées : un moulin devenu filature puis usine
  d'électroménager produit trois phases, et non une seule étiquette.
- Les communes historiques sont conservées ; huit communes actuelles issues de
  fusions sont enregistrées séparément.
- Les protections immobilières ne sont retenues que si la notice `PA` renvoie
  directement à la notice `IA`.
- La collection métallurgique de Varenne comprend 31 notices Palissy. Elle est
  recensée, mais son rattachement à `IA00060965` reste à vérifier.
- Les états relevés par l'Inventaire sont conservés comme observations anciennes.
  Ils ne sont pas présentés comme actuels sans preuve récente.

## Situation actuelle : ce que l'on peut affirmer

Quatre sites disposent d'une source récente retenue à ce stade :

| Référence | Site | Information documentée | Confiance |
|---|---|---|---|
| `IA00060938` | centrale de Rabodanges | production hydroélectrique en activité | forte |
| `IA00061155` | établissements Bohin | production, musée et visites en 2026 | forte |
| `IA00061029` | grosse forge d'Aube | présence et accès ponctuel attestés en 2026 | moyenne |
| `IA00061008` | mine de Halouze | projet de sécurisation et valorisation financé en 2026 | moyenne |

Sources récentes retenues : [EDF — barrage de Rabodanges](https://www.edf.fr/barrage-rabodanges),
[Bohin — organiser sa visite](https://www.bohin.com/pages/organiser-sa-visite),
[Archives de l'Orne — programme 2026](https://archives.orne.fr/sites/default/files/2026-05/Prog%20PEL%2026-WEB.pdf)
et [Département de l'Orne — soutiens financiers](https://www.orne.fr/actualite/dimportants-soutiens-financiers?page=2).

Pour les 26 autres sites, la situation actuelle est `inconnu`. Cela ne signifie
pas que le site a disparu : cela signifie qu'aucune preuve récente suffisante n'a
encore été retenue.

## Corrections et anomalies principales

1. `PA00110771` renvoie à `IA00060964`, pas à `IA00060965`. La protection a donc
   été retirée du candidat et conservée comme rapprochement à vérifier.
2. `IA00061166` se situe historiquement à Écouché, et non à Trun. La commune
   actuelle est Écouché-les-Vallées.
3. Pour `IA00060969`, `IA00061153` et `IA00061060`, le champ historique structuré
   contient un marqueur technique `$26`. La chronologie a été reprise du texte
   rendu de la notice POP.
4. CASIAS n'a pas encore été rapproché : le faire par commune seulement serait
   trop imprécis et produirait des faux positifs.

## Portée de ce bloc

Ce bloc produit un corpus de travail enrichi et traçable. Il ne valide pas encore
chaque fiche pour publication : le dernier bloc de la phase 5 prévoit le contrôle
manuel, la double classification d'un sous-échantillon et la production du corpus
pilote V1.
