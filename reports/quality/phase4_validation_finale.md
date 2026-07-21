# Validation finale de la phase 4

Date : 21 juillet 2026.

Statut : **phase 4 validée**.

## Publication

Le registre `config/classifications.yml` est publié en version 1.0 avec le
statut `phase4_validee`. Toute modification future devra changer sa version et
être inscrite dans le journal des décisions.

Le registre contient 163 codes répartis dans 17 vocabulaires : secteurs,
activités, installations, énergies, périodes, situation actuelle, protections,
localisation et fiabilité. Les 49 entrées principales qui exigent une définition
explicite en possèdent toutes une.

## Contrôles finaux

- aucune incohérence dans les secteurs, activités et installations ;
- aucune incohérence dans les périodes et la situation actuelle ;
- aucune incohérence dans les règles de précision et de fiabilité ;
- tous les vocabulaires publiés possèdent un libellé ;
- les classifications restent identiques lorsque l'ordre des notices change ;
- les sorties canoniques possèdent une empreinte SHA-256 ;
- les 64 tests automatisés du projet réussissent ;
- aucune erreur de validation finale.

Le détail chiffré et les empreintes sont conservés dans
`reports/quality/phase4_validation_finale.json`.

## Limite maintenue

La reproductibilité automatique est établie. L'accord entre deux personnes sur
les cas ambigus sera mesuré pendant la constitution de l'échantillon pilote.

## Décision

Les classifications sont suffisamment cohérentes, explicites et traçables pour
construire l'échantillon pilote de la phase 5. La phase 4 est terminée.
