# Phase 8 — Constitution du corpus

Statut : **phase terminée ; corpus complet V1 validé le 24 juillet 2026**.

## Adaptation du bloc initial

Le travail a d'abord été calibré sur le pilote puis sur 50 nouveaux dossiers.
Les références restantes ont ensuite été récupérées par une extraction
reprenable, avec un point de contrôle après chaque notice. Le découpage
technique n'affecte pas le résultat : tous les dossiers sont projetés dans le
même format commun.

Répartition prévue :

| Ensemble | Dossiers | Rôle |
|---|---:|---|
| pilotes appartenant au corpus officiel | 29 | méthode déjà validée |
| pilote conservé hors corpus officiel | 1 | `IA00061060` |
| lot 1 | 50 | calibration de la chaîne complète |
| références officielles restantes | 240 | extraction reprenable et harmonisation |
| total officiel | 319 | dossiers sources, pas nombre final de sites |

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

## Correction du calcul 239 → 240

Le corpus commun de 80 contenait bien 30 pilotes et 50 nouveaux dossiers, mais
seulement 79 de ces références appartenaient aux 319 références officielles.
Le pilote `IA00061060` est une ancienne référence valide et enrichie, mais il
n'apparaît plus dans le cadre d'étude officiel actuel. Il reste conservé hors
du corpus principal. Pour compléter exactement les 319 références officielles,
il fallait donc traiter **240 références**, et non 239.

## Corpus commun de 80 dossiers — 23 juillet 2026

Les 30 pilotes et les 50 dossiers du lot 1 ont été réunis dans
`data/interim/phase8_corpus_80.json`. Le format commun conserve les informations
riches des pilotes et utilise des valeurs nulles explicites pour les
enrichissements encore absents du lot 1.

Le contrôle donne 80 références et 80 URLs uniques, 109 activités classées et
aucun candidat au rapprochement selon les références, adresses, lieux-dits ou
points sources disponibles. Les 30 pilotes conservent leur `site_id`. Les 50
nouveaux dossiers restent sans identifiant canonique afin de ne pas figer leur
statut avant le traitement du corpus complet.

## Corpus commun des 319 dossiers — 23 juillet 2026

Les 240 références officielles restantes ont été récupérées avec contrôle du
champ `REF`, archivage brut, empreinte et manifeste de reprise. Les 319 dossiers
officiels sont maintenant harmonisés dans
`data/interim/phase8_corpus_319.json`.

Résultats :

- 319 références officielles uniques ;
- 400 activités structurées ;
- 73 dossiers multi-activités et 34 dossiers multi-secteurs ;
- 407 dénominations sources résolues à 100 % ;
- 8 occurrences reconnues comme composants non productifs et non comme
  activités ;
- 7 paires de dossiers proposées à la revue de rapprochement ;
- 1 dossier collectif proposé à la revue de séparation ;
- 4 dossiers de cités ouvrières à relier à un site industriel sans fusion ;
- 2 dénominations génériques `moulin` dont la production doit être précisée.

Le registre des classifications passe en version 1.4. Les nouveaux termes sont
classés par correspondance exacte. `cité ouvrière`, `collège`, `édifice
sportif`, `ferme` et `haras` sont explicitement séparés des activités
productives.

Les sorties de contrôle sont :

- `reports/quality/phase8_corpus_319_resume.json` ;
- `reports/quality/phase8_corpus_319.csv` ;
- `reports/quality/phase8_corpus_319_rapprochements.csv` ;
- `reports/quality/phase8_corpus_319_separations.csv` ;
- `reports/quality/phase8_corpus_319_anomalies.csv`.

## Revue canonique — 23 juillet 2026

Les sept rapprochements proposés ont été relus à partir des historiques,
adresses, exploitants et points sources. Ils sont tous rejetés comme sites
distincts. La proximité ou le même lieu-dit ne suffisent donc pas à fusionner
deux emprises.

`IA61001399` est une synthèse départementale sans commune, code INSEE, adresse
ou historique de site. Ses quinze fromageries individuelles sont déjà présentes
dans le corpus. La synthèse est conservée comme source mais exclue du décompte.

Le résultat est de **318 sites canoniques pour 319 dossiers sources** :

- 314 sites avec au moins une activité productive ;
- 4 cités ouvrières conservées comme sites non productifs ;
- 403 activités structurées ;
- 5 relations entre sites validées ;
- 318 UUID v4 stables.

Les décisions détaillées sont dans
`config/phase8_decisions_canoniques.yml`. Le rapport de résultat est
`reports/quality/phase8_corpus_canonique.md`.

## Enrichissement et localisation — 23 juillet 2026

Le corpus canonique a été rapproché des extractions départementales POP et
CASIAS. La règle reste conservatrice : une même commune ou une proximité ne
suffisent pas à créer un lien.

- 16 protections MH sont confirmées par une référence `IA` explicite ;
- 31 objets Palissy déjà repérés sont conservés avec un lien encore à vérifier ;
- 131 rapprochements CASIAS recoupent 123 sites ;
- 170 entrées CASIAS restent une file d'élargissement, sans intégration ;
- 318 sites ont un point source, dont 290 qualifiés d'approximatifs ;
- 8 rapprochements CASIAS restent ambigus après revue.

Le contexte territorial est calculé pour les 318 sites à partir de couches IGN
et BRGM archivées par tuiles. Les distances sont des indices de lecture et non
des preuves de causalité historique. Le compte rendu détaillé est
`reports/quality/phase8_enrichissement_localisation.md`.

## Validation du corpus complet V1 — 24 juillet 2026

Les répartitions éditoriales et les indicateurs territoriaux ont été recalculés
sur les 318 sites. Les exports JSON, DuckDB, CSV, Parquet et GeoJSON concordent
sur 318 sites et 403 activités.

Le corpus est validé pour une publication historique, narrative et
cartographique. Cette validation ne signifie pas que toutes les dimensions sont
complètes :

- 315 états de conservation restent inconnus ;
- 316 accessibilités restent inconnues ;
- 290 localisations restent approximatives ;
- seules 42 activités possèdent une période directement calculée depuis une
  chronologie d'activité ;
- 31 liens Palissy et 8 rapprochements CASIAS restent à traiter avec prudence.

Ces limites sont non bloquantes parce qu'elles sont conservées comme telles et
ne sont pas remplacées par des déductions. Le rapport final est
`reports/quality/phase8_validation_corpus_complet.md`.
