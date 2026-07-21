# Validation finale de la phase 5

Contrôle effectué le 22 juillet 2026.

## État de la phase

La structure du corpus pilote est valide, mais la phase 5 n'est pas encore
formellement terminée. Le double classement humain doit être réalisé par deux
personnes différentes avant la clôture.

| Contrôle | Résultat |
|---|---:|
| Fiches contrôlées individuellement | 30 / 30 |
| Activités structurées et sourcées | 47 / 47 |
| Communes actuelles sourcées | 30 / 30 |
| Protections confirmées et sourcées | 6 / 6 |
| Objets Palissy sourcés | 31 / 31 |
| Situations actuelles renseignées avec une source récente | 4 / 4 |
| Cas préparés pour le double classement | 6 |
| Classements humains reçus | 0 / 2 |

Le validateur ne signale aucune information importante renseignée sans source.
Une situation actuelle explicitement `inconnu` est acceptée si cette absence de
preuve récente est justifiée.

## Corrections issues du contrôle manuel

- La laiterie et la fromagerie de `IA00061133` sont traitées comme deux
  productions simultanées entre 1893 et 1980.
- La quincaillerie et la tréfilerie de `IA00061155` sont traitées comme deux
  fonctions complémentaires, sans imposer une succession non documentée.
- La correction d'Écouché pour `IA00061166` est confirmée.
- Les trois recours au texte rendu POP à cause du marqueur `$26` restent
  signalés et sourcés.
- Les réserves concernant la protection et les objets de Varenne sont maintenues.

## Corpus produit

Le fichier `data/pilot/corpus_pilote_v1.json` contient le corpus V1 candidat :

- 30 sites ;
- 47 phases d'activité ;
- 31 notices d'objets techniques ;
- 6 anomalies ou limites documentées ;
- les sources et niveaux de confiance associés.

Son statut reste `v1_candidate_double_classement_en_attente`. Il passera à
`phase5_validee` après réception et comparaison des deux classements humains.

## Double classement à réaliser

Le classeur `data/review/phase5/double_classement_phase5.xlsx` contient :

- trois cas simples : `IA00060938`, `IA00060915`, `IA00061147` ;
- trois cas ambigus : `IA00060965`, `IA00061155`, `IA00061060` ;
- une feuille pour la personne A ;
- une feuille pour la personne B ;
- les sources communes aux deux personnes ;
- le vocabulaire autorisé ;
- une feuille calculant les accords et désaccords.

Les deux personnes doivent travailler séparément. La feuille de comparaison ne
doit être consultée qu'après le remplissage des deux classements.

## Condition de clôture

La phase 5 pourra être terminée lorsque :

1. les deux feuilles auront été remplies par deux personnes différentes ;
2. les désaccords auront été mesurés et commentés ;
3. les règles ambiguës auront été précisées si nécessaire ;
4. le corpus V1 aura été régénéré avec le statut validé.
