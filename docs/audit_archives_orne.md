# Contrôle complémentaire des Archives de l'Orne

Mission ouverte le 10 novembre 2026 à la demande du porteur.
Première passe réalisée le même jour, puis remplacée par l'exécution ci-dessous
à la demande du porteur. L'état courant est donné dans cette première section.

## Exécution et décisions du 10 novembre 2026

Le porteur demande de compléter, enrichir et corriger directement le corpus.

- [x] Ajouter Briante à Colombiers, ferme-distillerie attestée vers 1860.
- [x] Ajouter la Normanderie à Ménil-Erreux depuis la notice PA61000039,
  construction en 1863, coordonnées de la notice, historique et protection.
- [x] Rattacher les fonds d'entreprises à onze fiches de lieux existants dans
  `data/manual/enrichissements_archives.yml` et transmettre ces sources à la vue.
- [x] Indexer l'intégralité du répertoire S, soit 1 169 dossiers numérotés et
  cinq rubriques du supplément, dans `docs/archives_orne_serie_s.csv`.
- [x] Appliquer les critères de périmètre déjà validés aux cas discutés.
- [x] Régénérer le prototype avec 321 lieux, 172 dans les douze ensembles et
  149 hors ensembles.

Les deux nouvelles fiches sont enregistrées dans
`data/manual/lieux_complementaires.yml`. Briante est située par un repère IGN
de lieu-dit, identifiant `PAIHABIT0000000019097745`, coordonnées
`0.055398, 48.482094`. La Normanderie reprend le point Mérimée
`0.197048502306956, 48.4956556867074`, corroboré par le lieu-dit IGN voisin.
La précision de chaque point est exposée dans la fiche.

### Cas tranchés selon le périmètre existant

| Cas | Traitement |
| --- | --- |
| Briante et la Normanderie | Ajoutées. Transformation agro-industrielle attestée avant 1950. |
| Key-Plastics | Maintenue dans les compléments de recherche. Les sources consultées attestent le site après 1950. Une activité antérieure reste nécessaire pour l'admission au corpus principal. |
| Maignan, ASTER et Piron | Écartés de cette intégration, leurs fonctions documentées relèvent du commerce ou des services. |
| Exploitation Collet | Maintenue en recherche agricole. L'activité industrielle de transformation reste à établir. |
| Moulin de Gibout | Source complémentaire possible pour Avoise, propriétaire Houel en 1859. Le rattachement exige le plan de S1039 dossier 5. |
| Moulin de Sarthe et Guéramé | Rapprochement automatique refusé. Une date de règlement commune ne suffit pas. Le point IGN de Guéramé et l'adresse du lieu IA00060972 ne coïncident pas. |
| Manufacture de Sées | Activité textile ancienne établie à l'Hôtel-Dieu dans HDEPOT10 G19–25, p. 56 et suivantes de S5. L'identité avec le fonds 393 J et le lieu précis de production restent à résoudre avant cartographie. |
| Fonderie du Perche | Conserver la distinction avec la SFAR. Le fonds 33 J 211 et la fiche CASIAS BNO6102061 doivent résoudre la localisation Randonnai–Irai. |
| Fromagerie d'Athis, forges de Saint-Evroult, moulin à tan de Radon | Sources et communes connues. Obtenir adresse ou plan des établissements pour les placer et écarter les réemplois d'une emprise déjà recensée. |

Le critère chronologique vient de `config/perimetre.yml`, activité industrielle
attestée au plus tard en 1950. Les cas relevant des services sont traités selon
les exclusions déjà définies dans ce même fichier.

### Répertoire S complet

Le script `tools/repertorier_archives_orne.py` reprend tout le texte extrait des
135 pages, conserve cotes, numéros, pages, intitulés et descriptions. Les cinq
rubriques du supplément figurent aussi dans le CSV. Les références du corpus
dans la même commune et les correspondances de lieux-dits sont proposées pour
retrouver les dossiers.

Ce répertoire contient des demandes de barrages, des lavoirs et plusieurs
dossiers pour un même moulin. Ses 1 174 entrées sont des unités archivistiques.
Le rapprochement des emprises et l'identification de la production déterminent
les lieux supplémentaires admissibles. Les cas identifiés ci-dessus ont reçu
un traitement individuel.

La couverture du document est complète pour l'indexation. La résolution
historique des 1 174 entrées reste partielle. La précédente lecture de huit
lieux est conservée ci-dessous comme historique du travail.

Sources supplémentaires utilisées pour exécuter les ajouts.

- [Mérimée PA61000039, ferme de la Normanderie](https://pop.culture.gouv.fr/notice/merimee/PA61000039).
- [Repère IGN de Briante](https://data.geopf.fr/geocodage/search?q=Briante&index=poi&citycode=61111&limit=5).
- [Repère IGN de la Normanderie](https://data.geopf.fr/geocodage/search?q=Normanderie&index=poi&citycode=61263&limit=5).
- [Repère IGN de Guéramé](https://data.geopf.fr/geocodage/search?q=Guerame&index=poi&citycode=61001&limit=5).

## Historique de la première passe

## Objectif et livrable

Repérer des lieux industriels absents des 319 lieux affichés, puis produire un
tableau de rapprochement avec commune, source, référence existante éventuelle,
statut et vérification suivante.

Le contrôle porte sur trois entrées publiques des Archives de l'Orne.

- [x] Fermes agro-industrielles citées avec Avoise, Briante et la Normanderie.
- [x] Liste publique des fonds d'entreprises, comparaison des noms et communes.
- [x] Inventaire de la série S consacré aux moulins et usines, disponibilité
  du document et première lecture de repérage.
- [x] Bilan chiffré et limites du contrôle consignés.
- [x] Candidats soumis au porteur pour choix de la suite.
- [ ] Choix des candidats à instruire ou à intégrer validé par le porteur.

## Méthode

Comparer les sources avec les noms, communes, lieux-dits et historiques des
318 lieux de l'Inventaire et avec le complément Avoise. Un fonds d'entreprise
peut concerner plusieurs établissements. Un nom absent peut désigner un lieu
déjà recensé sous un autre exploitant. Ces cas restent à rapprocher.

Chaque résultat reçoit l'un des statuts suivants.

- Déjà présent, avec référence.
- Rapprochement à vérifier, avec candidat existant.
- Candidat complémentaire, avec intérêt industriel et source.
- Périmètre à arbitrer, lorsque l'activité relève des services ou de l'agriculture.

## Résultats

30 entrées examinées, dont deux fermes, vingt établissements cités par la page
des entreprises et huit lieux dans un échantillon de la série S.

| Statut | Nombre |
| --- | ---: |
| Déjà présent | 11 |
| Rapprochement à vérifier | 4 |
| Candidat complémentaire | 11 |
| Périmètre à arbitrer | 4 |
| Total | 30 |

Les onze candidats sont des pistes à instruire. Leur identité, leur emprise et
leur éventuel lien avec un lieu existant demandent encore des vérifications.

### Tableau de rapprochement

Les codes de source renvoient aux liens de la section suivante. Les références
IA correspondent aux lieux du socle de l'Inventaire.

| ID | Lieu ou fonds | Commune de la source | Source | Statut | Référence ou vérification suivante |
| --- | --- | --- | --- | --- | --- |
| A01 | Briante | Colombiers | S1, S3 p. 26, S1005 dossier 6 | Candidat complémentaire | Aucun nom ni commune dans le socle. Identifier bâtiments et distillerie. |
| A02 | La Normanderie | Ménil-Erreux | S1, document 45, cote M1405 | Candidat complémentaire | Aucun nom ni commune dans le socle. Examiner le plan de 1862 et les activités. |
| E01 | Lavalou | Le Bourg-Saint-Léonard | S2 | Déjà présent | IA00061133, nom de l'entreprise explicite. |
| E02 | Fonderie du Perche | Randonnai | S2, S4 section 1.7, 33 J 211 | Candidat complémentaire | Distinguer de la SFAR IA00061106, arrêtée en 1983. S4 décrit une petite fonderie familiale. Une piste CASIAS existe aussi à Irai sous BNO6102061, localisation à résoudre. |
| E03 | Forges de Saint-Evroult | Saint-Evroult | S2, S4 section 2 | Candidat complémentaire | Le socle recense scierie, verrerie et fromagerie dans cette commune. Localiser la forge et vérifier les réemplois. |
| E04 | Forge d'Aube | Aube | S2 | Déjà présent | IA00061029, affinerie. D'autres installations d'Aube ont des fiches distinctes. |
| E05 | Société du Caoutchouc Manufacturé | Flers | S2 | Déjà présent | IA00061181, société nommée dans l'historique. |
| E06 | Tissages Salles | La Ferté-Macé | S2 | Déjà présent | IA00060985, Beaudouet, fondation par François Salles dans l'historique. Périmètre du fonds à préciser. |
| E07 | Minoterie Goude et Croissant | Couterne | S2 | Déjà présent | IA00061010, exploitant Croissant. Vérifier si le fonds Goude concerne aussi cette même emprise. |
| E08 | Mine de La Ferrière | La Ferrière-aux-Étangs | S2 | Déjà présent | IA00060912 et IA00061202. Fonds à rattacher au complexe minier. |
| E09 | Magasin Maignan | Argentan | S2 | Périmètre à arbitrer | Commerce, place éventuelle dans le projet à décider. |
| E10 | MIC | Argentan | S2 | Déjà présent | IA00061128, nom et fonds d'archives mentionnés. |
| E11 | Manufacture de Sées | Sées | S2, S5 p. 24, 393 J 1–27 | Candidat complémentaire | Fonds daté de 1769–1830. Les deux fiches actuelles IA00060952 et IA00060953 décrivent d'autres établissements. La p. 25 signale un plan de machines de filature de coton, 25FI464/1, et les dossiers E dépôt 76/232. Identifier précisément le site. |
| E12 | Société fromagère d'Athis | Athis | S2 | Candidat complémentaire | Les six lieux d'Athis-de-l'Orne du socle sont textiles. Vérifier siège, usine et adresse du fonds. |
| E13 | Mine de Halouze | Saint-Clair-de-Halouze | S2 | Déjà présent | IA00060961. |
| E14 | Key-Plastics | Bellême | S2, S6 avis 2414 et 2416 | Candidat complémentaire | Plasturgie route du Mans. Aucun rapprochement trouvé. Distinguer sociétés juridiques et établissement physique. |
| E15 | Maisons France Confort | Alençon | S2 | Déjà présent | IA00061073, ancien site Prout. Vérifier les emprises couvertes par le fonds. |
| E16 | Laiterie Mallet | Condé-sur-Sarthe | S2 | Rapprochement à vérifier | Candidat IA00060970, fromagerie sans nom d'exploitant. IA00061178, autre moulin devenu beurrerie, mentionne aussi Mallet. Contrôler adresse et chronologie. |
| E17 | Imprimerie de Montligeon | La Chapelle-Montligeon | S2 | Déjà présent | IA00061149, historique explicite et déménagement ultérieur. |
| E18 | Exploitation Collet, Val-Heureux | Montmerrei | S2 | Périmètre à arbitrer | Vérifier l'existence d'une transformation agro-industrielle. |
| E19 | Garage Piron | La Chapelle-d'Andaine | S2 | Périmètre à arbitrer | Réparation automobile, intérêt patrimonial à définir. |
| E20 | Bureau d'études ASTER | Alençon | S2 | Périmètre à arbitrer | Ingénierie, identifier le lieu et le lien avec une activité de production. |
| M01 | Moulin du Guichet | Alençon | S3 p. 3, S981 dossier 1 | Candidat complémentaire | Nom absent. Vérifier adresse, plans et suppression en 1863. |
| M02 | Moulin des Filles Sainte-Claire | Alençon | S3 p. 3, S981 dossier 1 | Candidat complémentaire | Nom absent. Distinguer du Guichet et de tout établissement ayant changé d'usage. |
| M03 | Moulin de Sarthe | Alençon | S3 p. 3, S981 dossier 2 | Rapprochement à vérifier | Comparer au moulin générique IA00060972. |
| M04 | Moulin de Guéramé | Alençon | S3 p. 3–4, S981 dossiers 3–4 | Rapprochement à vérifier | IA00060972 cite précisément le règlement du 20 mars 1848 présent dans S3. Comparer les plans avant rapprochement définitif. |
| M05 | Usine d'Ozé | Alençon | S3 p. 4, S981 dossier 5 | Déjà présent | IA00060969. |
| M06 | Moulin des Prés | Colombiers | S3 p. 26, S1005 dossier 1 | Candidat complémentaire | Aucun lieu de cette commune dans le socle. Vérifier destination du moulin et plans. |
| M07 | Moulin à tan de Chaplain | Radon | S3 p. 81–82, S1039 dossier 4 | Candidat complémentaire | Également repéré hors corpus sous CASIAS BNO6101280. Localiser et comparer à Avoise. |
| M08 | Moulin de Gibout | Radon | S3 p. 82, S1039 dossier 5 | Rapprochement à vérifier | Propriétaire Houel cité en 1859. Lien possible avec Avoise, à établir sur plans et actes. |

### Ordre de travail proposé

1. Instruire Briante, la Normanderie et la manufacture de Sées, avec les plans
   et cotes déjà identifiés.
2. Résoudre la Fonderie du Perche, notamment la commune de l'emprise.
3. Compléter Key-Plastics, la fromagerie d'Athis et les forges de Saint-Evroult.
4. Résoudre les quatre rapprochements avant de compter des lieux supplémentaires.
5. Soumettre les moulins restants et les quatre activités de périmètre au porteur.

### Portée de la première passe

La page S2 donne des exemples de fonds. Les vingt établissements ont été
examinés, en séparant les deux forges citées ensemble. Cette liste ne couvre
pas tous les fonds conservés aux Archives.

Le PDF de la série S compte 135 pages. La lecture détaillée a porté sur son
introduction et les notices d'Alençon, Colombiers et Radon. Des repérages ont
également été faits pour Randonnai et Saint-Evroult. Huit lieux sont retenus
dans l'échantillon. Le dépouillement intégral des autres communes reste à faire.
L'introduction du répertoire annonce principalement 1800–1904. Son en-tête
courant indique 1800–1940. Le versement complémentaire 1812 W est signalé comme
consultable en salle de lecture.

Les contrôles locaux ont utilisé les noms, communes et lieux-dits de
`data/exports/sites_corpus_complet_v1.csv`, les historiques de
`data/exports/recits_sites_v1.csv`, la liste complémentaire manuelle et les
candidats CASIAS déjà présents dans `reports/quality/phase8_casias_elargissement.csv`.
Toutes les références IA du tableau ont été vérifiées dans ces fichiers.

## Sources et accès

- **S1** [Catalogue agricole des Archives de l'Orne](https://archives.orne.fr/sites/default/files/2020-09/CAT77.pdf), passage sur les trois fermes et document 45. Le lecteur web refuse l'ouverture intégrale de ce PDF de 90 Mo. Le passage est accessible par son indexation textuelle.
- **S2** [Fonds d'entreprises](https://archives.orne.fr/entreprises).
- **S3** [Inventaire des moulins et usines, série S](https://archives.orne.fr/sites/default/files/2020-09/FRAD061_INV_S_S_MOULINS_USINES.pdf), avril 2015, 135 pages. Lien retrouvé dans la notice publique `https://archives.orne.fr/inventaire/get/101`.
- **S4** [Dossier pédagogique sur l'industrie](https://archives.orne.fr/sites/default/files/2020-09/EDUC22.pdf), sections 1.7 et 2.
- **S5** [Inventaire de l'Hôtel-Dieu de Sées](https://archives.orne.fr/sites/default/files/2020-09/FRAD061_INV_HDEPOT_HDEPOT10_1.pdf), p. 24–25, sources complémentaires, manufacture de Sées.
- **S6** [BODACC A des 25 et 26 juillet 2009](https://www.bodacc.fr/telechargements/COMMERCIALES/PDF/A/BODACC-A_20090141_0001_p000.pdf), avis 2414 et 2416, activité de plasturgie à Bellême.

Le moteur GAIA est annoncé temporairement indisponible. Les pages publiques
et inventaires PDF accessibles servent à cette première passe.

Les pages S2 et du catalogue des inventaires, la notice JSON de S3, son PDF et
son texte extrait sont archivés localement sous
`data/raw/archives_orne/2026-11-10/`. Empreinte SHA-256 du PDF S3
`c16f461ce6ea300ca56c69dadbad033260f52e9f0d2d480bede2d4fc7860134e`.
S5 et S6 ont aussi été ouverts en texte dans le lecteur web pour contrôler
la pagination et la date de publication. S1 et S4 ont été consultés par leurs
passages indexés, cette différence d'accès est conservée pour la reprise.
