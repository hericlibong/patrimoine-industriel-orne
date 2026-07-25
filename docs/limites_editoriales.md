# Limites éditoriales du corpus complet et du socle narratif V1

Version 1.1 — 25 juillet 2026

Ce document traduit les limites techniques en règles de publication. Il doit
être relu lors de la conception de la première narration et avant toute mise en
ligne publique.

## Ce que le corpus complet permet d'affirmer

- les 318 sites canoniques permettent de décrire les emprises documentées par
  l'Inventaire industriel de l'Orne ;
- plusieurs activités peuvent se succéder ou coexister sur une même emprise ;
- les sources documentent des relations possibles entre les sites et l'eau,
  les forêts, les ressources minérales ou le rail ;
- certaines traces industrielles subsistent, sont reconverties ou restent à
  documenter aujourd'hui ;
- les sources patrimoniales, juridiques, environnementales et géographiques ne
  décrivent pas le même objet et doivent être croisées.

## Ce que le corpus complet ne permet pas d'affirmer

- le nombre total de sites industriels de l'Orne ;
- la proportion départementale de chaque activité, période ou état de
  conservation ;
- qu'une proximité spatiale explique historiquement l'implantation d'un site ;
- qu'un site est pollué parce qu'il figure dans CASIAS ;
- qu'un site n'est pas protégé parce qu'aucune protection n'a été rapprochée ;
- qu'un bâtiment est conservé ou accessible en 2026 à partir d'une enquête des
  années 1980 ;
- qu'un point POP, une parcelle actuelle ou un contour documentaire représente
  exactement l'emprise industrielle historique.

## Règles de comptage

Les termes suivants ne sont jamais interchangeables :

- `dossier source` : une notice ou un dossier `IA` ;
- `site candidat` : une emprise possible avant rapprochement ;
- `site canonique` : une emprise physique distincte retenue après
  rapprochement ;
- `phase d'activité` : une activité exercée pendant une période ;
- `site cartographiable` : site doté d'une géométrie qualifiée ;
- `site publié` : site ayant passé les contrôles éditoriaux et juridiques.

Un site multi-activités est compté une fois dans un décompte de lieux, mais
autant de fois que nécessaire dans un décompte de phases. Un filtre combinant
activité et période doit les chercher sur la même phase afin d'éviter de relier
une activité à une période pendant laquelle une autre production occupait le
site.

## Chronologie

Les dates imprécises restent des intervalles. `Vers 1850` ne devient jamais
`1850`. Les périodes provenant d'une chronologie de phase sont séparées de
celles calculées depuis `SCLE`. Ce dernier champ situe principalement une
campagne de construction ou de transformation et ne prouve pas une activité
continue pendant tout le siècle.

La période contemporaine est ajoutée seulement lorsqu'une source récente
documente le site. Elle ne signifie pas automatiquement que l'activité
industrielle ancienne se poursuit.

## Situation actuelle et accessibilité

Vingt-six sites sur trente n'ont pas de source récente suffisante pour décrire
leur situation actuelle. La valeur publique doit alors être `Situation actuelle
à documenter`, et non une reprise de la destination ancienne.

`Visitable`, `visible depuis l'espace public` et `privé` sont des notions
distinctes. Une carte ne constitue jamais une autorisation d'accès. L'adresse
précise d'un site privé ou fragile peut être simplifiée si sa diffusion crée un
risque pour les personnes, le propriétaire ou le patrimoine.

## Localisation

Les 30 points du pilote sont `point_approximatif` et les 29 contours disponibles
sont `zone_documentaire`. Aucune géométrie n'est qualifiée de vérifiée. Neuf
localisations portent une alerte de contrôle explicite.

La carte publique devra rendre l'incertitude visible : symbole adapté, niveau
de précision dans la fiche et absence de zoom trompeur. Un site non localisé
reste dans le corpus sans recevoir de coordonnées inventées.

## Contexte territorial

Les distances à l'eau, aux forêts, aux indices miniers et au rail constituent
des pistes de récit. Une causalité exige une source historique propre au site.
Les couches forestières et ferroviaires décrivent principalement un état
récent et ne restituent pas automatiquement le paysage de la période étudiée.

Les résultats du pilote peuvent être racontés comme des exemples : `18 des 30
sites pilotes se trouvent à moins de 100 mètres d'un cours d'eau`. Ils ne
doivent pas devenir : `60 % des sites industriels de l'Orne dépendaient de
l'eau`.

## Protections et CASIAS

Une protection MH concerne une mesure juridique et parfois seulement une
partie du site. Son absence dans le rapprochement n'est pas une preuve
d'absence de protection.

CASIAS recense des activités susceptibles d'avoir laissé une pollution, mais
ne prouve ni pollution effective ni valeur patrimoniale. Ses 2 052 entrées de
l'Orne ne sont pas additionnées automatiquement aux sites du corpus.

## Sources, textes et images

Les textes historiques longs servent à comprendre et structurer les faits ; ils
ne sont pas republiés intégralement. La publication privilégie la reformulation,
les citations courtes nécessaires et le lien vers la notice.

Une licence ouverte sur les données descriptives ne couvre pas nécessairement
les photographies. Toute image sans droit ou autorisation explicite est exclue.
Les règles détaillées sont dans `docs/licences_droits_images.md`.

## Formulations recommandées

| À éviter | À employer |
|---|---|
| `emprise exacte` | `zone documentaire issue de la source` |
| `site actuel disparu` sans observation | `situation actuelle inconnue` |
| `absence de protection` | `aucune protection rapprochée à ce stade` |
| `site pollué CASIAS` | `ancienne activité recensée dans CASIAS` |
| `implanté grâce au minerai proche` | `présence d'un indice minier à proximité, relation historique à vérifier` |
| `date de 1850` pour « vers 1850 » | `autour de 1850, selon la source` |

## Niveau de publication actuel

Le corpus complet et son socle narratif sont adaptés à une carte de contrôle,
à une démonstration interne et à la préparation d'un prototype narratif. Ils ne
constituent pas encore un inventaire départemental exhaustif ni un paquet
photographique publiable.

## Limites du socle narratif et visuel V1

Les 314 historiques et 257 descriptions disponibles sont conservés dans leurs
champs sources ; leur présence ne rend pas leurs textes intégralement
republiables. Les 4 historiques et 61 descriptions absents restent signalés
comme tels, sans reconstruction automatique.

Les 1 900 relations média-site sont toutes sourcées, mais aucune image ne peut
être ajoutée par défaut à une publication publique. Parmi elles, 1 783 possèdent
un crédit exploitable pour le prototype privé ; les 117 autres restent des
références internes à compléter. Les candidats d'image principale sont des
repères de revue, non des choix éditoriaux ou juridiques.
