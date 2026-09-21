# T1 — Les époques de chaque lieu

**21 septembre 2026.** Première tâche du filtre temporel, décidée dans
`docs/phase10_filtre_temporel.md` version 3. **Aucune donnée du corpus n'a été
modifiée** : l'outil lit les exports et produit un fichier reproductible, non
versionné, dans les données intermédiaires.

Reproduction :

```powershell
python tools/epoques_lieux.py
```

Il imprime un rapport JSON et **sort en code 1 si un contrôle échoue**. Tous les
chiffres de ce relevé en sortent directement.

---

## La règle appliquée

Un lieu appartient à une époque lorsqu'au moins un événement daté de sa
chronologie a **son propre intervalle** qui chevauche cette époque. L'intervalle
est celui que la source donne : « 1949 » vaut 1949–1949, « vers 1920 » vaut
1915–1925, « 19e siècle » vaut 1801–1900, « années 1950 » vaut 1950–1959.

**Rien ne relie deux événements.** Un lieu documenté en 1700 puis en 1900
n'appartient pas aux époques intermédiaires.

**Aucune année n'est inventée.** Les 117 événements dont une borne est ouverte —
103 « après », 14 « avant » — sont écartés du calcul. Ils restent entiers dans
la chronologie du lieu, dans leurs mots d'origine, et le lecteur les y lira
normalement. Le filtre travaille sur les 2 243 événements dont les deux bornes
sont connues.

---

## Ce que ça donne

**314 lieux sur 318** reçoivent au moins une époque. Quatre n'en reçoivent
aucune, et ils sont nommés plus bas.

| Époque | Lieux |
| --- | ---: |
| Av. 1789 | 67 |
| 1789‑1849 | 176 |
| 1850‑1913 | 258 |
| 1914‑1945 | 168 |
| 1946‑1975 | 154 |
| 1976‑2000 | 103 |

Les six effectifs sont **exactement ceux arrêtés avec le porteur** dans la
version 3 du document de décision. C'est le premier des six contrôles.

### Par ensemble

| Ensemble | Lieux | Av. 1789 | 1789‑1849 | 1850‑1913 | 1914‑1945 | 1946‑1975 | 1976‑2000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Vallée de la Risle | 43 | 9 | 33 | 39 | 27 | 14 | 10 |
| Vallée du Noireau | 23 | — | 16 | 18 | 11 | 12 | 3 |
| Flers | 21 | — | 3 | 15 | 13 | 17 | 11 |
| Bassin de Halouze | 13 | 5 | 5 | 12 | 5 | 6 | 6 |
| Alençon | 13 | — | 3 | 6 | 9 | 10 | 5 |
| La Ferté-Macé | 12 | — | 1 | 11 | 8 | 5 | 5 |
| Tinchebray | 9 | — | 3 | 5 | 5 | 8 | 8 |
| Randonnai | 9 | 5 | 6 | 8 | 2 | 1 | 3 |
| Malétable | 8 | 5 | 8 | 7 | 4 | 3 | 2 |
| La Ferrière-aux-Étangs | 7 | 1 | 1 | 5 | 3 | 4 | — |
| Argentan | 7 | 1 | 3 | 5 | 3 | 4 | 3 |
| Crulai et Chandai | 7 | — | 6 | 7 | — | 1 | — |
| **Total** | **172** | **26** | **88** | **138** | **90** | **85** | **56** |

**Les ensembles ne se ressemblent pas, et c'est le propos.** La Risle est le
seul ensemble présent dans les six époques avec du volume partout. Flers et
Tinchebray montent au contraire vers la fin : Flers compte trois lieux
documentés entre 1789 et 1849 et dix-sept entre 1946 et 1975. Randonnai et
Malétable font l'inverse. Aucun autre levier de l'application ne rend cet écart
visible.

### Par métier

| Métier | Lieux | Av. 1789 | 1789‑1849 | 1850‑1913 | 1914‑1945 | 1946‑1975 | 1976‑2000 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Agroalimentaire | 113 | 23 | 81 | 92 | 61 | 57 | 38 |
| Métallurgie et travail des métaux | 79 | 42 | 61 | 70 | 31 | 23 | 18 |
| Textile, habillement et cuir | 76 | 5 | 36 | 65 | 43 | 43 | 23 |
| Bois, papier et imprimerie | 32 | 7 | 12 | 24 | 22 | 22 | 16 |
| Verre, céramique et matériaux de construction | 27 | 6 | 16 | 20 | 12 | 5 | 6 |
| Construction mécanique et électrique | 10 | — | 2 | 5 | 3 | 10 | 7 |
| Extraction | 9 | — | — | 8 | 8 | 6 | 4 |
| Production d'énergie | 6 | 1 | 2 | 3 | 4 | 5 | 1 |
| Chimie, caoutchouc et plastiques | 3 | 1 | — | 3 | 1 | 1 | 2 |

**La métallurgie et la construction mécanique sont deux histoires opposées.**
La métallurgie a 42 lieux documentés avant 1789 et 18 après 1976 : elle décline.
La construction mécanique et électrique n'a aucun lieu avant 1789 et compte dix
de ses dix lieux entre 1946 et 1975 : elle apparaît. L'extraction n'existe pas
avant 1850.

### Les trajectoires

1 époque : 26 lieux · 2 époques : 89 lieux · 3 époques : 104 lieux ·
4 époques : 70 lieux · 5 époques : 20 lieux · 6 époques : 5 lieux

**Soixante et un lieux sautent au moins une époque** entre deux qu'ils occupent.
Ce chiffre est la preuve que le calcul ne comble pas les silences de la source ;
il sert de contrôle, et la section suivante explique pourquoi.

### Les neuf couples sans résultat

| Ensemble | Époque |
| --- | --- |
| Vallée du Noireau | Av. 1789 |
| Flers | Av. 1789 |
| Alençon | Av. 1789 |
| La Ferté-Macé | Av. 1789 |
| Tinchebray | Av. 1789 |
| La Ferrière-aux-Étangs | 1976‑2000 |
| Crulai et Chandai | Av. 1789 |
| Crulai et Chandai | 1914‑1945 |
| Crulai et Chandai | 1976‑2000 |

**Six sur « Avant 1789 »**, deux sur « 1976‑2000 », un sur « 1914‑1945 ». Ce
sont des résultats, pas des pannes : l'interface les affichera « Aucun lieu pour
cette époque ». Crulai est absent de trois époques sur six et sera le cas à
regarder de près en T4.

### Les quatre lieux sans aucune date

| Référence | Nom | Commune | En ensemble |
| --- | --- | --- | --- |
| IA00060920 | scierie | Saint-Germain-de-Clairefeuille | non |
| IA00060934 | tannerie | Vimoutiers | non |
| IA00060971 | tannerie | Alençon | oui |
| IA00060974 | imprimerie | Alençon | oui |

Ils seront retirés de la carte dès qu'une époque est choisie, et comptés à
l'écran : « 4 lieux sans date ». Leur absence documentaire ne devient jamais une
absence historique.

---

## Les six contrôles

Tous passent. L'outil refuse d'écrire son fichier et sort en erreur si un seul
échoue.

| Contrôle | Ce qu'il vérifie |
| --- | --- |
| `effectifs_conformes` | Les 318 lieux, les 314 datés, les 2 243 événements retenus, les 117 écartés et les six effectifs par époque sont ceux arrêtés avec le porteur |
| `epoques_justifiees` | Chaque époque attribuée s'appuie sur au moins un événement nommable |
| `aucun_pont_entre_deux_faits` | Voir ci-dessous |
| `aucune_annee_inventee` | Tout événement écarté l'est pour borne ouverte, et pour aucun autre motif |
| `evenements_ecartes_toujours_lisibles` | Les 117 événements écartés gardent leur texte source et restent affichables |
| `toutes_les_epoques_servent` | Aucune des six époques ne rend zéro lieu |

### Le contrôle qui compte, et comment il peut échouer

Vérifier que le calcul ne comble pas les silences en le comparant à lui-même ne
prouverait rien. Le contrôle le compare donc **au résultat qu'aurait donné la
règle refusée** — celle de l'intervalle entre la première et la dernière date.

Cette règle produit toujours un ensemble d'époques contigu. La nôtre laisse des
trous partout où la source se tait. Si plus aucun lieu ne présentait de trou,
c'est que nous aurions reconstitué la continuité que nous refusons, et le
contrôle échouerait.

Le test a été fait dans les deux sens :

| Règle | Lieux à trou | Contrôle |
| --- | ---: | --- |
| Celle qui est retenue | 61 | **passe** |
| Celle qui a été refusée | 0 | **échoue** |

La règle refusée aurait gonflé 61 lieux et inventé **72 appartenances lieu ×
époque** qu'aucun fait ne documente.

---

## Ce qui est produit

Un fichier de données intermédiaires, reproductible et non versionné, portant
pour chaque lieu la liste de ses époques et pour chaque ensemble les époques
qu'il couvre. C'est cette seconde liste qui permettra à la liste des ensembles
de réagir au filtre, en T4.

Rien n'est encore transmis au prototype ni affiché : c'est l'objet de T2.

**T1 est fait. Validation du porteur attendue avant T2.**
