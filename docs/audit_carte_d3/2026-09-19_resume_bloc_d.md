# Bloc D — Harmoniser la carte du département — résumé

Branche `codex/carte-departement-d3`. Six enregistrements. Aucune coordonnée,
aucune donnée source modifiée.

## Le point de départ

Deux moteurs de dessin coexistaient. La carte des ensembles tournait sur
l'architecture D3 depuis la séance du jour ; la carte du département — celle sur
laquelle le lecteur clique pour entrer — était restée en SVG écrit à la main,
effacée et reconstruite à chaque geste. Elle n'avait ni survol, ni zoom, ni
cartouche, et ses 146 lieux hors ensembles ne disaient rien du tout.

## Les quatre temps

**D1 — Le dessin tenu par D3.** La carte du département a ses couches posées une
fois et mises à jour par jointure. Les couches sont devenues paramétrables :
chaque niveau déclare les siennes. Les noms d'ensembles passent dans la couche
de surface, ancrés à leur bulle par un décalage constant. Aucun effet visible
attendu, et aucun constaté — sauf deux corrections.

**D2 — Ce que l'ensemble avait déjà.** Une source unique déclare ce que le
lecteur peut désigner à chaque niveau. Les douze bulles et les cent quarante-six
points gris parlent enfin. Le pointage du plus proche, le zoom et ses commandes,
le cartouche avec sa légende et son échelle sont posés.

**D3 — La descente d'échelle.** La carte du département s'approche de la bulle
visée, puis celle de l'ensemble arrive de plus près et se pose. Le retour remonte
symétriquement. Trois garanties empêchent une animation de retenir un lecteur.

**D4 — Vérification.** Six vues, le clavier, le tactile simulé, trois largeurs
d'écran. Neuf règles consignées comme communes aux trois niveaux.

## Ce qui a changé pour le lecteur

| | Avant | Après |
| --- | --- | --- |
| Survol d'une bulle | rien | nom, effectif, disponibilité |
| Survol d'un lieu hors ensemble | rien | nom, commune, activités |
| Zoom au département | absent | présent, retour exact |
| Noms des lieux hors ensembles | jamais | à partir du seuil de zoom |
| Légende | bande au-dessus du cadre | cartouche dans le coin le plus vide |
| Échelle | absente | 20 km, adaptée au zoom et à la largeur |
| Changement de métier | reconstruction | mise à jour, en mouvement |
| Ouvrir un ensemble | substitution d'écran | descente d'échelle |

## Les six défauts trouvés et corrigés

Aucun n'était prévu. Quatre étaient antérieurs au bloc, deux ont été introduits
en cours de route et rattrapés.

1. **« Bassin de Halouze · 13 » affichait « · 1 »** — son chiffre recouvert par
   le nom voisin. Les noms étaient servis du plus gros ensemble au plus petit,
   donc le plus long arrivait sans place. Ils le sont du plus long au plus court.
2. **Deux noms tombaient sur une bulle** et deux paires se chevauchaient. Quatre
   positions candidates ne suffisaient pas ; il y en a vingt-quatre.
3. **Les 146 points gris disparaissaient sur écran étroit**, à 2,6 unités de
   rayon. Ils gardent une taille d'écran constante.
4. **Le cartouche était posé avant le dessin**, donc avant que l'échelle de
   projection soit connue : au premier affichage, la barre manquait ou reprenait
   celle de la vue précédente. Crulai annonçait 500 mètres au lieu d'un
   kilomètre. Ce défaut touchait aussi les ensembles depuis le bloc A.
5. **La descente d'échelle se jouait deux fois** — signalé par le porteur. La
   bulle gardait son gestionnaire de clic alors que D2 avait fait passer le clic
   par la carte : deux appels, deux descentes. Un verrou de navigation a été
   ajouté en second filet.
6. **Un lieu masqué par le filtre restait désignable**, et **le clavier perdait
   l'étiquette au département**. Les deux venaient de D2 ; trouvés par D4, en
   comparant les deux niveaux.

## Les neuf règles communes aux trois niveaux

Elles ne décrivent plus une vue, elles décrivent la carte. Détail dans
`journal_phases_carte.md`.

1. Un seul chemin de dessin ; les couches sont posées une fois et mises à jour.
2. Le cadre prend la proportion de ce qu'il montre.
3. Les signes gardent leur taille d'écran, au zoom comme au redimensionnement.
4. Ce qui ne doit pas grossir vit dans la couche non transformée ; un nom y est
   ancré à son signe et se masque avec lui.
5. Une source unique déclare ce qui se désigne, filtre compris ; le survol et le
   clic passent par elle, jamais par le signe dessiné en dernier. Aucun point
   n'est déplacé pour faciliter le pointage.
6. Le clavier obtient ce que la souris obtient.
7. Légende et échelle vivent dans un cartouche posé dans le coin le plus vide ;
   la légende ne montre que des signes présents.
8. Sous 480 pixels de carte, le cartouche se réduit à l'échelle ; légende et
   précisions descendent sous la carte, repliées.
9. Toute animation cesse si le lecteur a demandé moins de mouvement, et aucune
   animation ne peut le retenir : navigation et retour au cadrage sont garantis
   indépendamment des images produites.

## Ce qui reste ouvert

**Jugement.** Les quatre sous-blocs attendent la validation du porteur. Aucune
case de validation n'est cochée.

**Un écart avec une décision d'architecture.** L'état partageable après le `#`
n'existe pas : le prototype ne lit ni n'écrit aucune adresse, on ne peut pas
partager un lien vers un ensemble, et recharger ramène au département. Rien n'a
été cassé par le bloc D — il n'y avait rien à préserver. Travail à part entière.

**Non vérifié.** Le tactile sur un appareil réel. L'onglet de contrôle est resté
en arrière-plan toute la séance et ne produisait pas d'images : transitions et
redimensionnements ont été éprouvés par leurs états, pas par leur mouvement.

**Limite acceptée.** « Vallée du Noireau » et « Flers » se touchent au
département sans filtre, à toutes les largeurs. Les deux restent lisibles. Le
remède est un trait de rappel entre un nom écarté et sa bulle ; il relève de la
présentation.

**Hors du bloc D**, et déjà consignés : le poids de la page à douze ensembles
— environ trois mégaoctets — et les trois communes d'archive sans contour
actuel, qui bloquent l'ouverture du Noireau et d'Argentan.

## Incident de méthode

Une tentative a supprimé, en retirant l'ancienne fonction de dessin, les
déclarations partagées qui la suivaient dans le fichier : bornes de découpe mal
choisies. Le fichier a été restitué depuis la version enregistrée et le travail
refait en plaçant la fonction après ses dépendances. Rien n'a été perdu. C'est
la deuxième fois dans la journée qu'un découpage par repères textuels se révèle
dangereux — la première avait emporté soixante-dix lignes de CSS.
