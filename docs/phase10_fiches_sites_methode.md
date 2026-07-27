# Phase 10 — Fiches de sites, pages « Les lieux » et méthode

**Version :** 1.0 — architecture des contenus validée
**Statut :** validée comme point de départ évolutif
**Date :** 27 juillet 2026

## Trois niveaux, trois fonctions

La publication ne possède pas une fiche unique reproduite 318 fois. Elle
distingue :

| Niveau | Population | Fonction |
| --- | ---: | --- |
| Aperçu | tous les résultats visibles | identifier rapidement un site sans ouvrir de panneau |
| Panneau cartographique | 318 sites | donner les faits essentiels dans le contexte de la carte |
| Page `Les lieux` | sélection éditoriale humaine | raconter un cas qui apporte une preuve ou une nuance au récit |

La page méthode est transversale. Elle explique comment les données, les textes,
les images et les incertitudes ont été construits.

Cette séparation évite deux erreurs :

- transformer le corpus en catalogue de 318 pages identiques ;
- forcer des blocs vides ou des récits artificiels pour les sites moins
  documentés.

## Couverture réelle à prendre en charge

| Matière | Couverture |
| --- | ---: |
| Sites avec un historique source | 314 sur 318 |
| Sites avec une description source | 257 sur 318 |
| Sites avec au moins un média inventorié | 316 sur 318 |
| Relations média-site | 1 900 |
| Phases avec période d'activité structurée | 42 phases concernant 29 sites |
| Situations actuelles appuyées par une source récente | 4 sites |
| Points approximatifs | 290 sites |
| Zones documentaires | 28 sites |

`chronologie_disponible` dans la revue éditoriale signifie qu'un repérage
chronologique est possible. Cela ne signifie pas que les activités possèdent
toutes des dates structurées. Le gabarit doit donc proposer plusieurs formes de
chronologie sans inventer de bornes.

## Aperçu court

L'aperçu apparaît au survol, au focus d'un résultat ou après une pression
courte sur un marqueur.

Il contient au maximum :

- nom du site ;
- commune ;
- une ou deux activités, puis `+ n autres` si nécessaire ;
- symbole et libellé de précision ;
- miniature uniquement si elle est déjà chargée et éditorialement retenue.

Il ne contient ni texte historique long, ni chronologie, ni liste de sources.
Son contenu est entièrement disponible dans la liste accessible.

## Panneau de détail dans l'exploration

### Structure

Le panneau doit tenir dans un écran courant et se lire dans cet ordre :

1. **repère** — commune et mention `Site sélectionné` ;
2. **identité** — nom public du site ;
3. **image** — seulement si une image a été retenue et peut être publiée ;
4. **phrase factuelle courte** — par exemple `Un même lieu, trois activités
   documentées` ;
5. **activités** — succession structurée ou liste simple ;
6. **situation actuelle** — conservation, usages et accessibilité séparés ;
7. **localisation** — niveau de précision et explication courte ;
8. **actions** — sources, page `Les lieux` éventuelle et retour aux résultats.

Le panneau n'est pas un mini-article. Il fournit suffisamment d'éléments pour
comprendre le marqueur et décider d'approfondir.

### Alimentation des champs

| Élément public | Source de données | Règle |
| --- | --- | --- |
| Nom | `sites.nom_principal` ou titre éditorial validé | conserver la référence au titre source |
| Commune | `communes_source` | ne pas remplacer par une commune déduite du point |
| Activités | lignes de `activites` ordonnées | aucune activité principale inventée |
| Dates | bornes et textes de date des phases | préférer le texte source public à une précision artificielle |
| Situation | conservation, usages, accessibilité | trois dimensions distinctes |
| Précision | `precision_geographique_code` | libellé constant dans carte, liste et panneau |
| Source | `source_principale_url` et références du récit | ouvrir la notice d'origine |
| Image | média retenu après revue humaine | légende et crédit obligatoires |

### Image absente

Si aucune image n'est retenue, le titre remonte en haut du panneau. Aucun cadre
gris, pictogramme d'usine ou texte `Image indisponible` ne remplace
artificiellement le média.

Les deux sites sans média inventorié restent donc consultables sans dégradation
fonctionnelle.

### Accès à « Les lieux »

Le bouton `Ouvrir ce lieu` apparaît uniquement si une page éditoriale a été
produite. Pour les autres sites, le panneau se termine par `Voir les sources`.
L'absence de page développée n'est pas présentée comme un contenu manquant.

## Page éditoriale « Les lieux »

### Principe

Une page `Les lieux` répond à une question journalistique. Elle n'est pas
déclenchée par un seuil automatique de médias, de longueur historique ou de
nombre d'activités.

Le squelette est stable, mais le corps du récit reste modulaire. Une page sur
Ozé peut être dominée par les transformations d'activité ; Abadie par
l'inscription spatiale et les réseaux ; Bohin par la continuité productive et
la situation actuelle.

### Éléments obligatoires

1. **contexte de navigation**
   - chapitre ou état de carte d'origine ;
   - lien de retour conservant les filtres ;
2. **question et identité**
   - titre ;
   - commune ;
   - activité ou trajectoire utile au récit ;
   - question journalistique explicite ;
3. **média d'ouverture**
   - image ou document choisi ;
   - date ou période ;
   - légende ;
   - crédit ;
   - type : vue actuelle, archive ou document ;
4. **ce que les sources établissent**
   - synthèse factuelle rédigée et relue ;
   - références attachées aux affirmations ;
5. **évolution du lieu**
   - chronologie des activités quand elle est soutenue ;
   - sinon repères documentaires clairement nommés ;
6. **situation actuelle**
   - activité ;
   - conservation matérielle ;
   - usages ;
   - accessibilité ;
   - date et source de vérification lorsqu'elles existent ;
7. **localisation et contexte**
   - carte ;
   - précision géographique ;
   - relations territoriales sourcées ou simple contexte explicitement
     distingué ;
8. **sources et crédits**
   - liste complète des sources mobilisées ;
   - crédits des médias directement sous chaque média ;
   - lien vers la méthode générale.

### Modules facultatifs

Ils n'apparaissent que s'ils répondent à la question de la page :

- photographie actuelle comparée à une archive ;
- document technique ou plan ;
- graphique ou petit multiple ;
- flux d'approvisionnement ou de diffusion ;
- citation courte ;
- chiffres d'emploi ou de production ;
- objets ou protection patrimoniale ;
- encadré de limite ou de recherche encore nécessaire.

Le gabarit ne réserve pas d'espace vide à un module absent.

## Chronologie

### Cas 1 — phase datée

Une phase possède une borne exacte, approximative ou un intervalle. La
chronologie affiche le texte public le plus fidèle :

```text
1809                 vers 1840                 vers 1937
Moulin ━━━━━━━━━━━━━ Filature ━━━━━━━━━━━━━━━ Moulinex ┄┄┄
                                             fin inconnue
```

- `vers`, `attesté`, `entre` et `avant/après` restent visibles ;
- une fin inconnue utilise une ligne ouverte ou discontinue ;
- la ligne ne se prolonge jamais automatiquement jusqu'à aujourd'hui ;
- une interruption n'est pas comblée sans source.

### Cas 2 — activités ordonnées sans dates structurées

Les activités apparaissent sous forme de succession documentaire :

```text
Usine à papier
Activité documentée — dates non structurées dans le corpus
```

Le gabarit ne dessine pas d'axe temporel.

### Cas 3 — siècles de construction ou transformation

Les informations issues du champ source `SCLE` apparaissent dans un bloc
distinct :

> Repères de construction et de transformation documentés par la notice.

Elles ne sont jamais intitulées `Période d'activité`.

### Cas 4 — situation actuelle

La situation actuelle n'est pas le dernier segment de la chronologie
industrielle. Elle possède son propre bloc, car un bâtiment conservé, un usage
muséal ou une accessibilité vérifiée ne prolongent pas nécessairement
l'activité historique.

## Informations absentes, inconnues ou incertaines

Les formulations publiques sont contrôlées :

| Cas | Formulation |
| --- | --- |
| Historique absent de la notice | `La notice source ne fournit pas d'historique.` |
| Description absente | bloc omis ; absence indiquée dans les sources |
| Activité sans date structurée | `Dates d'activité non structurées dans le corpus.` |
| Conservation inconnue | `Conservation non documentée par une source récente.` |
| Usage inconnu | `Usage actuel non documenté.` |
| Accessibilité inconnue | `Conditions d'accès non vérifiées récemment.` |
| Point approximatif | `Le point situe le site approximativement.` |
| Zone documentaire | `Le repère correspond à une zone de source, pas à une emprise vérifiée.` |
| Image sans droit de publication | média non affiché ; métadonnées conservées en interne |

Les termes `disparu`, `sans usage`, `inaccessible` ou `non protégé` ne sont
jamais utilisés pour remplacer une information inconnue.

## Synthèses et textes

Les trois niveaux du modèle éditorial restent visibles dans le processus :

1. historique et description sources, conservés sans réécriture ;
2. résumé documentaire factuel ;
3. texte journalistique publié.

Le public lit le texte journalistique et les synthèses factuelles validées. Il
peut consulter la notice d'origine, mais la publication ne reproduit pas par
défaut l'intégralité des textes sources.

Une note ou un résumé encore `brouillon`, `non_produit` ou `non_evalue` ne peut
pas être publié comme texte achevé.

## Sources, légendes et crédits

- chaque graphique ou affirmation propre à un cas indique sa source à
  proximité ;
- la liste complète apparaît en fin de page ;
- chaque média conserve légende, auteur ou crédit, référence et date ;
- le crédit est directement visible sous le média, pas uniquement dans une
  modale ;
- le lien vers la notice média et l'image complète est disponible ;
- un recadrage éditorial significatif est signalé ;
- le statut de sélection éditoriale et le droit d'usage restent deux décisions
  séparées.

Le cadrage de phase 10 suppose que les autorisations nécessaires seront
obtenues pour les médias retenus. Le gabarit prévoit donc les images finales,
mais l'export public doit toujours vérifier la preuve de droit correspondante.

## Navigation et retours

### Depuis le récit

La page affiche :

```text
← Retour au chapitre « Un lieu, plusieurs vies »
```

Le retour restaure le chapitre et l'étape du scrollytelling.

### Depuis l'exploration

La page affiche par exemple :

```text
← Retour à la carte · Textile · 1789–1849 · 14 résultats
```

Le retour restaure recherche, filtres, centre, zoom et site sélectionné.

### Accès direct

Si la page a été ouverte par une URL partagée, deux sorties restent disponibles :

- `Voir ce site sur la carte` ;
- `Reprendre le récit`.

Le fonctionnement ne dépend jamais uniquement de l'historique du navigateur.

## Page méthode

### Fonction

La méthode doit permettre de comprendre et vérifier la publication sans devenir
la documentation technique interne du dépôt.

Elle forme une page continue avec sommaire ancré :

1. **Périmètre**
   - ce que représentent les 318 sites ;
   - ce que le corpus ne représente pas ;
2. **Des sources au corpus**
   - 319 dossiers sources ;
   - 318 sites canoniques ;
   - règles de rapprochement ;
3. **Activités et secteurs**
   - 403 phases ;
   - classement d'une phase, jamais secteur principal forcé du site ;
4. **Temps**
   - périodes d'activité ;
   - repères documentaires ;
   - couverture réelle des dates ;
5. **Carte et précision**
   - 290 points approximatifs ;
   - 28 zones documentaires ;
   - limites des couches de contexte ;
6. **Situation actuelle**
   - conservation, usage et accessibilité séparés ;
   - quatre situations récentes documentées ;
7. **Textes, images et droits**
   - textes sources, synthèses et écriture journalistique ;
   - sélection humaine ;
   - légendes, crédits et autorisations ;
8. **Sources, version et limites**
   - sources principales ;
   - date de mise à jour ;
   - version des données ;
   - corrections et contact.

### Forme

- résumé lisible en tête de page ;
- schéma simple `sources → rapprochement → sites → phases → publication` ;
- chiffres contextualisés, sans tableau de bord ;
- tableaux accessibles pour les classifications ;
- exemples concrets de précision et d'incertitude ;
- liens vers les sources et, si prévu, les données publiques ;
- date et version visibles.

Les détails de scripts, tables DuckDB, chemins locaux et procédures internes
restent dans la documentation de maintenance.

## Composants nécessaires

Le bloc 5 n'ajoute que les composants absents du système validé :

1. panneau de site ;
2. ligne ou liste d'activités ;
3. chronologie avec dates incertaines et fin ouverte ;
4. bloc de situation actuelle ;
5. bloc de précision ;
6. média avec légende et crédit ;
7. note de limite ;
8. liste de sources ;
9. barre de retour contextuelle ;
10. sommaire ancré de la méthode.

Il n'est pas prévu de générateur de page universel, de carrousel, de galerie
automatique, d'accordéon systématique ou de composant vide.

## Portée de la validation

L'architecture suivante est validée comme référence :

1. conserver trois niveaux : aperçu, panneau pour 318 sites et pages
   `Les lieux` sélectionnées ;
2. ne pas créer automatiquement une page longue pour chaque site ;
3. omettre les blocs sans contenu plutôt que produire des placeholders ;
4. utiliser plusieurs formes de chronologie selon la qualité des dates ;
5. séparer la situation actuelle de la chronologie industrielle ;
6. imposer légende, crédit et source à proximité de chaque média ;
7. conserver le contexte de retour vers le récit ou la carte ;
8. faire de la méthode une page éditoriale lisible, avec les détails techniques
   réservés à la maintenance.

Cette validation ne fige pas les longueurs de texte, le nombre final de pages
`Les lieux`, l'ordre de certains modules facultatifs, leur densité visuelle ou
leur comportement responsive. Le prototype pourra les ajuster lorsqu'un test
d'usage, d'accessibilité ou de performance le justifie, sans remettre en cause
les trois niveaux et les règles de preuve.
