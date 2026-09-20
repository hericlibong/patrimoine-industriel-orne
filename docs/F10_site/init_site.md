Mission d’analyse — préparer le travail sur ce que le lecteur voit lorsqu’il ouvre un lieu.

Nous venons de terminer le travail principal sur la carte D3 des ensembles. Le socle de référence est maintenant sur main.

Aucune modification de code n’est demandée dans cette mission. Il faut d’abord examiner l’existant, évaluer les propositions ci-dessous et produire une roadmap précise avant toute implémentation.

## 1. Contexte observé

Lorsqu’un lecteur clique sur un point de la carte d’un ensemble, une fiche du lieu apparaît dans la colonne droite.

Les captures de l’état actuel sont ici :

C:/Users/heric/PatrimoineIndustrielOrne/docs/captures_temp/site_01.png
C:/Users/heric/PatrimoineIndustrielOrne/docs/captures_temp/site_02.png
C:/Users/heric/PatrimoineIndustrielOrne/docs/captures_temp/site_03.png

Examine réellement les trois captures.

Dans l’état actuel, le panneau affiche successivement :

- l’identité du lieu ;
- des compteurs d’activités et d’événements ;
- la distance au cours d’eau ;
- les métiers ;
- une longue information sur la précision géographique et la conservation ;
- le lien vers la notice source ;
- « Ce qui est daté » ;
- « Ce que dit la notice » ;
- puis de nouveau les repères généraux de l’ensemble ;
- la liste complète des lieux ;
- les relations générales entre les lieux.

Cela produit un panneau très long. La page entière défile, la carte finit par disparaître et laisse une grande zone vide à gauche. Le lecteur reste entouré d’informations sur l’ensemble alors qu’il a changé de niveau et souhaite comprendre un lieu précis.

Le lieu actif est également difficile à retrouver dans la liste complète : il peut se trouver loin dans la zone déroulante.

## 2. Intention générale

Cliquer sur un lieu doit faire passer l’interface dans un véritable mode « lieu ».

Dans ce mode, le panneau doit servir principalement à :

1. identifier le lieu ;
2. comprendre rapidement son histoire ;
3. consulter sa chronologie si nécessaire ;
4. connaître les limites des informations disponibles ;
5. ouvrir la fiche d’inventaire source ;
6. revenir aux lieux de l’ensemble ou en choisir un autre.

Tout élément qui ne sert ni à comprendre ce lieu ni à poursuivre la navigation doit quitter le panneau principal.

Employer « lieu » dans l’interface publique. Le terme « site » peut rester dans les noms techniques internes.

## 3. Proposition à évaluer

### Organisation générale

Sur ordinateur :

- conserver la carte à gauche comme contexte spatial ;
- éviter que son emplacement devienne une grande zone vide pendant la lecture ;
- étudier une carte ou une colonne gauche fixe/collante et un panneau droit disposant de son propre défilement ;
- conserver une adaptation verticale correcte sur mobile.

Quand un lieu est ouvert :

- masquer le sélecteur de métier ;
- préserver en mémoire le métier éventuellement sélectionné ;
- proposer une action explicite du type « Retour aux lieux de la Vallée de la Risle » ;
- ce retour doit restaurer l’ensemble et son filtre antérieur.

### Contenu proposé du panneau

1. Identité du lieu
   - nom ;
   - commune et lieu-dit ;
   - activités écrites directement ;
   - lien « Voir la fiche d’inventaire ».

2. Média
   - emplacement seulement lorsqu’un média a été sélectionné et que son usage est permis ;
   - légende et crédit obligatoires ;
   - aucune image choisie uniquement parce qu’une URL existe ;
   - dans l’interface finale, ne pas afficher de faux cadre « image indisponible » si aucun média n’est retenu.

3. Historique documenté
   - avant la chronologie ;
   - remplacer « Ce que dit la notice » ;
   - tant que le texte n’est pas éditorialement réécrit, conserver une provenance discrète et honnête telle que « D’après la fiche d’inventaire ».

4. Chronologie
   - après l’historique ;
   - repliable ;
   - remplacer « Ce qui est daté » et « Événements extraits du texte de la notice » ;
   - présenter clairement les constructions, exploitations, productions, transformations et cessations ;
   - ne pas afficher le compteur « 11 événements datés » dans l’entrée de la fiche.

5. Localisation et état des connaissances
   - bloc secondaire et repliable ;
   - conserver la précision géographique sous une formulation courte : un point approximatif ne doit pas être pris pour l’emprise exacte du lieu ;
   - conserver honnêtement les informations connues ou inconnues sur la conservation, sans leur donner la place principale ;
   - déplacer éventuellement la distance au cours d’eau dans ce bloc ;
   - ne jamais présenter cette distance comme une preuve d’utilisation de l’eau.

6. Choisir un autre lieu
   - bloc replié en fin de panneau ;
   - le lieu actuellement ouvert doit être immédiatement repérable si la liste est dépliée ;
   - préciser si cette liste doit respecter le filtre métier mémorisé ou proposer une autre règle.

### Éléments à retirer du mode lieu

- « L’ensemble en quelques repères » ;
- les statistiques générales de la vallée ;
- la liste générale des activités de l’ensemble ;
- le bloc général des relations entre les lieux ;
- les compteurs redondants d’activités et d’événements.

Les liens du lieu ouvert restent mis en évidence sur la carte grâce au comportement déjà réalisé. L’accès aux preuves existantes ne doit pas être refait inutilement.

## 4. Médias et textes : limites à respecter

Le projet possède déjà un inventaire de 1 900 relations média–lieu couvrant 316 des 318 lieux :

C:/Users/heric/PatrimoineIndustrielOrne/data/exports/medias_sites_v1.csv

Les règles sont documentées ici :

C:/Users/heric/PatrimoineIndustrielOrne/docs/licences_droits_images.md
C:/Users/heric/PatrimoineIndustrielOrne/docs/phase10_fiches_sites_methode.md

Cette mission ne doit ni télécharger des images ni intégrer automatiquement un média.

La réécriture éditoriale des historiques sera également une mission distincte. Ne pas transformer automatiquement les 318 notices. Il faudra définir et valider un modèle sur quelques cas différents.

Les recherches complémentaires sur des personnes ou entreprises, par exemple Jacques Marais, constituent un enrichissement ultérieur. Elles ne doivent pas être mélangées à la restructuration de l’interface.

## 5. Travail demandé maintenant

1. Examiner les trois captures.
2. Lire uniquement les portions pertinentes :
   - outils et gabarit responsables du panneau du lieu ;
   - générateur des données nécessaires ;
   - documents méthodologiques cités ;
   - inventaire des médias uniquement pour comprendre ce qui est déjà disponible.
3. Vérifier comment le mode lieu est actuellement assemblé, notamment pourquoi le panneau du lieu est suivi du panneau de l’ensemble.
4. Évaluer notre proposition :
   - points justes ;
   - problèmes ou contradictions ;
   - éléments techniquement réalisables ;
   - décisions qui doivent encore être prises par le porteur.
5. Proposer une architecture cible concise du mode lieu sur ordinateur et mobile.
6. Produire une roadmap complète, méthodologique et matérialisable.

## 6. Forme attendue de la roadmap

Créer un nouveau document de préparation consacré au mode lieu, sans modifier le suivi de la carte des ensembles.

Chaque phase doit comporter :

- un objectif compréhensible ;
- des tâches et sous-tâches à cocher ;
- les fichiers ou données concernés ;
- un livrable visible et précis ;
- des critères de réception ;
- les contrôles nécessaires ;
- une validation explicite du porteur avant la phase suivante.

Le plan doit au minimum distinguer :

- structure et navigation du mode lieu ;
- hiérarchie des contenus ;
- comportement ordinateur/mobile ;
- intégration conditionnelle des médias ;
- définition du modèle de transformation des historiques ;
- essai sur quelques lieux représentatifs ;
- validation et généralisation éventuelle.

La première future mission d’implémentation devrait rester limitée à la structure et à la navigation :

- panneau réellement centré sur le lieu ;
- carte maintenue à gauche ;
- retour à l’ensemble ;
- suppression des répétitions ;
- historique placé avant la chronologie ;
- blocs secondaires repliables ;
- choix d’un autre lieu en dernier.

Mais évalue d’abord si ce périmètre est cohérent avec le code existant.

## 7. Limites de cette mission

- Aucun changement du prototype.
- Aucune création de branche nécessaire pour cette analyse.
- Aucun téléchargement ou intégration d’image.
- Aucune réécriture de notice.
- Aucun changement des données.
- Aucun travail de direction artistique.
- Aucun audit général du dépôt.
- Ne pas relancer ce qui fonctionne déjà sur la carte.

Travail ciblé et proportionné. Le rapport doit être clair, concret et compréhensible par le porteur.

## 8. Rapport attendu

Répondre brièvement avec :

1. diagnostic de l’état actuel ;
2. appréciation de la proposition ;
3. décisions encore nécessaires ;
4. chemin du document de roadmap créé ;
5. première mission recommandée, sans l’exécuter.