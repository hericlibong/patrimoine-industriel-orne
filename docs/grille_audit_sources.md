# Grille d'audit des sources

Version : 1.0 — 19 juillet 2026

## Informations relevées

Chaque source est auditée selon les mêmes critères :

1. producteur et responsabilité éditoriale ;
2. périmètre géographique, chronologique et thématique ;
3. unité décrite : site, édifice, objet, activité, parcelle ou couche ;
4. champs et identifiants disponibles ;
5. formats et moyens d'accès ;
6. possibilité d'extraction automatisée ;
7. présence et précision de la géolocalisation ;
8. licence et droits sur les images ;
9. fréquence ou date de mise à jour ;
10. limites, biais et risques de mauvaise interprétation ;
11. test d'accès réel ;
12. rôle retenu dans le projet.

## Statuts d'audit

| Statut | Signification |
|---|---|
| `a_auditer` | Source seulement identifiée |
| `documentation_verifiee` | Documentation officielle contrôlée, accès non testé |
| `acces_teste` | Accès ou export réellement testé |
| `validee` | Source exploitable sans réserve structurante |
| `validee_avec_reserves` | Exploitable avec limites documentées |
| `bloquee` | Accès inutilisable ou dépendant d'une intervention extérieure |
| `ecartee` | Source non pertinente pour le périmètre V1 |

## Priorités

| Priorité | Critère |
|---|---|
| `P0` | Indispensable à la constitution du corpus initial |
| `P1` | Nécessaire à la localisation, au rapprochement ou à une question éditoriale centrale |
| `P2` | Enrichissement important mais non bloquant pour le socle V1 |
| `P3` | Vérification ponctuelle ou enrichissement futur |

## Décisions possibles

- `principale` : constitue directement le corpus ;
- `enrichissement` : complète les sites déjà identifiés ;
- `elargissement` : fait apparaître des candidats hors du corpus principal ;
- `contexte_geographique` : explique les implantations ;
- `verification` : confirme ou documente des cas particuliers ;
- `ecartee` : non retenue pour le socle V1.

## Règle de validation

Une source prioritaire n'est validée que si son producteur, son périmètre, son
mode d'accès, ses identifiants, sa géolocalisation, sa licence et ses limites
sont documentés. Un lien consultable sans test d'export ne suffit pas.
