# Phase 10.A.1 — Extraction des relations entre sites

**Version :** 1.0
**Statut :** mouvement 1 terminé, liste candidate produite, rien versé au corpus
**Date :** 29 juillet 2026

## Objet

Les textes historiques des notices affirment des liens entre sites — un haut
fourneau qui alimente une forge, une usine rachetée par un industriel, une
production transférée ailleurs.

**Rectification du 29 juillet 2026.** Il a d'abord été écrit dans ce document
que la table `relations_sites` était vide. C'est faux : elle contenait déjà cinq
relations établies en phase 8 — deux cités ouvrières rattachées à la mine de
Halouze, deux à celle de La Ferrière-aux-Étangs, et la fenderie de Larchamp
dépendant de son affinerie. Cette dernière avait même été présentée à tort comme
un ajout manuel de la phase 10 : elle existait depuis la phase 8, avec la même
justification.

Ce qui manquait n'était donc pas la table, mais les relations de production.

Sans elles, la carte de l'application reste un semis de points. Avec elles, elle
peut montrer un réseau.

Le script est `tools/extraire_relations_sites.py`. Il ne modifie rien : il
produit une proposition à relire.

## Choix arrêtés le 29 juillet 2026

### Les cinq types de liens retenus

| Type | Ce qu'il décrit | Exemple relevé |
| --- | --- | --- |
| `approvisionnement` | Un site fournit une matière à un autre | « alimentait en fonte la forge d'Aube » |
| `fourniture` | Un site reçoit une matière ou une énergie d'un autre | « fils de laiton fournis par l'usine voisine de Boisthorel » |
| `dependance` | Un site dépend industriellement d'un autre | « fenderie dépendant de la forge d'Aube » |
| `transfert` | Une production passe d'un site à un autre | « production transférée à l'usine de Saint-Sulpice-sur-Risle » |
| `liaison` | Deux sites sont physiquement reliés | « reliée en 1885 par chemin de fer à voie étroite au moulin de Mâle » |

### Ce qui n'est pas un lien entre sites

Trois cas ont été écartés explicitement, et l'écart est ce qui donne sa valeur
à la liste.

**La succession d'activités sur un même lieu.** Un moulin à farine devenu
tréfilerie n'est pas un lien entre deux sites : c'est un seul site avec deux
activités successives, déjà représenté dans le modèle. Seize sites de la seule
vallée de la Risle sont dans ce cas.

**La dépendance seigneuriale ou institutionnelle.** « Moulin dépendant de
l'abbaye de Saint-Martin de Sées », « dépendant du château de Flers »,
« dépendait de la baronnie de la Ferrière » décrivent une propriété, pas une
relation industrielle. Le script les écarte au moyen d'une liste de termes —
abbaye, château, comte, baron, marquis, seigneur, domaine, prieuré.

**L'infrastructure de transport.** « Relié à la gare du Châtellier », « reliés à
la station de Saint-Bomer-les-Forges » désignent un équipement ferroviaire, non
un autre site du corpus. Ces mentions restent intéressantes pour le récit mais
ne peuplent pas la table des relations.

### Les liens vers l'extérieur, dans un fichier séparé

Beaucoup de mentions pointent hors du corpus : le coton de Louisiane et de
Géorgie, le cacao de Côte d'Ivoire et du Cameroun transformé à Berlin, le
minerai vendu en Allemagne et en Belgique, les bois de Chine, de Hongrie et du
Canada, les colorants d'Inde.

Ce ne sont pas des relations entre sites de l'Orne. Elles sont donc extraites
séparément, dans `mentions_externes.csv`, sans jamais être mélangées aux
relations internes. Elles constituent la matière d'une démonstration précise :
ces usines rurales travaillaient pour des approvisionnements et des marchés
lointains.

### Les liens par exploitant : déduits, donc à part

Soixante-treize mentions nomment un acquéreur ou un exploitant. Elles
permettent de rapprocher des sites — six portent le nom de Benjamin Bohin,
cinq celui du Ferodo.

Mais ce rapprochement n'est **pas affirmé par une source** : il est déduit de
la présence d'un même nom dans deux notices. Il relève donc de l'information
`calculee` et non `sourcee` au sens de `docs/methodologie.md`. Le fichier
`liens_exploitants.csv` reste séparé pour cette raison, et ces liens ne
pourront être versés qu'après une vérification d'identité des personnes ou des
sociétés.

## Méthode de résolution

Une mention comme « l'affinerie de Varenne à Champsecret » doit désigner un
site précis. La résolution croise deux signaux.

**Le nom de lieu.** Un répertoire est construit à partir des communes, des
lieux-dits et des noms de sites du corpus. Seuls les mots d'au moins cinq
lettres et non génériques sont retenus. Les types d'installation en sont
exclus : « affinerie » n'est pas un nom de lieu, sinon la mention se résoudrait
sur n'importe quelle affinerie du département.

**Le nombre de repères concordants.** Un site qui partage deux repères avec la
mention — sa commune et son lieu-dit — prime sur celui qui n'en partage qu'un.
C'est ce qui distingue le bon site de Champsecret des quatre autres.

**Le type d'installation, en dernier recours.** Si plusieurs sites restent à
égalité, ceux dont la notice décrit le type mentionné sont préférés.

Une mention qui ne se résout pas devient une mention externe. Une mention qui
en désigne plusieurs reste `ambigu` et attend un arbitrage humain.

## Résultat du mouvement 1

| Sortie | Volume |
| --- | ---: |
| Relations candidates entre sites | 18 |
| — dont résolues sur un site unique | 12 |
| — dont ambiguës, plusieurs candidats | 6 |
| Mentions vers l'extérieur | 56 |
| Mentions d'exploitants | 73 |
| Notices lues | 314 |

Les fichiers sont dans `data/interim/` : `relations_candidates.csv`,
`mentions_externes.csv` et `liens_exploitants.csv`.

Chaque ligne porte la phrase source qui l'établit. Aucune ligne ne peut être
retenue sans que cette phrase la justifie.

## Contrôle effectué

Un balayage large, volontairement peu précis, avait relevé 81 segments
susceptibles de contenir un lien. Les segments non repris par l'extraction
définitive ont été relus un par un.

Vingt segments ne sont pas repris. Dix-neuf sont des exclusions justes :
dépendances seigneuriales, infrastructure ferroviaire, déplacements internes à
un même site, et un faux positif — « l'indépendant de l'Orne » est le nom d'un
journal, non une dépendance.

**Un seul manque avéré** : la fenderie `IA00061188`, « dépendant de l'affinerie
et du haut fourneau de Larchamp », est écartée parce que la même phrase
contient « propriété du baron de Larchamp », ce qui déclenche le filtre des
dépendances seigneuriales. À arbitrer au mouvement 2.

## Limites connues

- L'extraction ne repose que sur les formulations recensées. Une tournure
  inhabituelle échappe au script.
- Les mentions externes contiennent du bruit : la formule « vendue à » sert
  aussi bien à décrire une vente de marchandise qu'une cession d'entreprise.
- Les liens ambigus ne sont pas tranchés automatiquement, et ne doivent pas
  l'être.
- Le corpus n'est pas modifié à ce stade.

## Reproductibilité

```powershell
$env:PYTHONPATH = "src"
python tools/extraire_relations_sites.py
```

Le script est déterministe. Toute formulation ajoutée après une lecture
manuelle doit être inscrite dans le script lui-même, afin qu'une nouvelle
exécution retrouve le même résultat.

## Suite

Mouvement 2 : contrôler l'échantillon, trancher les six liens ambigus,
arbitrer le cas `IA00061188`, écarter ce qui n'est pas prouvé. Mouvement 3 :
verser dans `relations_sites` et mesurer.
