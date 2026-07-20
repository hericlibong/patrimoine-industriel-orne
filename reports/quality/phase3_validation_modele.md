# Validation du modèle de données — phase 3

Date : 20 juillet 2026

Décision : **modèle V1 approuvé**

## Méthode

Le schéma DuckDB et son validateur transversal ont été confrontés à cinq cas
synthétiques représentatifs du corpus. Ces données ne décrivent aucun site réel.
Chaque test crée une base neuve, charge le même jeu SQL et vérifie le résultat
par requête, sans correction manuelle.

## Résultats

| Cas | Représentation attendue | Résultat | Statut |
|---|---|---|---|
| site simple | un site, une activité, un état, une géométrie et une source | les cinq éléments restent reliés au même UUID | validé |
| site multi-activités | une emprise et deux phases successives | forge puis moulin, sans duplication du site | validé |
| site reconverti | activité historique séparée de l'usage contemporain | filature historique et équipement culturel dans `etats_actuels` | validé |
| site disparu | site conservé dans le corpus sans faux point | état `disparu` et aucune géométrie | validé |
| rapprochement incertain | deux candidats distincts jusqu'à décision humaine | deux UUID, une proposition `a_verifier`, aucune fusion | validé après adaptation |

## Adaptation issue des tests

Le modèle initial ne possédait pas de structure pour enregistrer une hypothèse
de doublon avant décision. La table `propositions_rapprochement` a été ajoutée.
Elle conserve les deux candidats, la méthode, les critères, un score éventuel et
la décision. Elle ne remplace pas `relations_sites`, réservé aux relations
historiques ou fonctionnelles entre emprises réellement distinctes.

Une similarité de nom, commune, lieu-dit ou distance ne fusionne jamais les
sites automatiquement. La fusion technique n'intervient qu'après confirmation,
avec conservation des deux UUID et désignation du site canonique.

## Approbation

Le modèle V1 est approuvé pour structurer le corpus pilote. Il sait représenter
les cinq cas demandés, les activités successives, les états contemporains, les
sites sans géométrie et les incertitudes de rapprochement.

Cette approbation porte sur la structure, pas sur la qualité du futur corpus ni
sur les vocabulaires. Les classifications sont le chantier de la phase 4. Les
cas synthétiques devront aussi être confirmés sur l'échantillon réel lors de la
constitution du corpus pilote.

## Vérifications techniques

- schéma DuckDB `1.0.0` créé et rechargé avec DuckDB Spatial ;
- jeu de base et cinq cas de validation acceptés sans anomalie ;
- cohérence d'une fusion confirmée contrôlée par le validateur transversal ;
- 40 tests automatisés réussis sur l'ensemble du projet ;
- compilation Python réussie.
