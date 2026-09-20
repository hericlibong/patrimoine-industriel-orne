# Mode lieu — journal des phases

Branche `codex/mode-lieu-l1`, ouverte le 20 septembre 2026 depuis `main`.
Plan : `roadmap_mode_lieu.md`. Diagnostic : `2026-09-20_analyse_mode_lieu.md`.

---

## L1 — Structure et navigation (20 septembre 2026)

**Objet.** Qu'ouvrir un lieu fasse réellement changer de mode.

### Fait

**Le panneau du lieu ne traîne plus le panneau de l'ensemble derrière lui.**
C'était la cause du panneau interminable : les deux étaient concaténés. Le
lecteur qui ouvrait un lieu recevait la vallée entière par-dessus sa fiche.

**Le retour et le choix d'un autre lieu sont redonnés dans le panneau du lieu.**
Sans cela, supprimer le panneau de l'ensemble aurait enfermé le lecteur dans la
fiche qu'il venait d'ouvrir. C'était le critère de réception de la phase.

**La liste suit le filtre en cours et dit ce qu'elle masque.** Sous Métallurgie,
elle annonce « 24 sur 43 » et ajoute « 19 lieux masqués par le filtre en
cours ». C'est la règle déjà en vigueur dans le panneau de l'ensemble et sur la
carte : rien ne disparaît en silence. **Décision appliquée sur recommandation,
le porteur ne l'ayant pas tranchée ; elle se change en une ligne.**

**Le lieu ouvert est amené à la vue** dès que la liste s'ouvre. Il était déjà
marqué d'un liseré, mais pouvait se trouver n'importe où dans une liste de
quarante-trois entrées à défilement propre : le marquer ne servait à rien si
rien n'y menait.

**Le sélecteur de métier disparaît en mode lieu, le filtre reste.** Le retour à
l'ensemble retrouve exactement la sélection quittée.

**Le titre de page nomme le lieu.** Il annonçait « Vallée de la Risle · 43 lieux
documentés » alors que le lecteur regardait un moulin. Il annonce désormais le
nom du lieu et, en dessous, sa commune et son lieu-dit. Le nom de l'ensemble
reste accessible par le fil de navigation et par le retour du panneau.

**Le libellé du retour a été corrigé avant livraison.** « Retour aux lieux de
Vallée de la Risle » est fautif : les douze ensembles ne prennent pas le même
article — « Flers », « Bassin de Halouze », « La Ferté-Macé ». Un tiret évite la
question : « ← Retour aux lieux — Vallée de la Risle ».

### Contrôles effectués

Six contrôles du générateur vrais, `ruff` propre, syntaxe JavaScript vérifiée
par Node. Dans le navigateur :

- Mode lieu sans filtre : titre « moulin à papier, tréfilerie », sous-titre
  « Aube · Moulin d'Aubette (Le) », sélecteur masqué, **aucun bloc de
  l'ensemble** sous la fiche, liste de 43 lieux, lieu courant marqué une fois.
- Mode lieu sous Métallurgie : liste de 24 lieux, compteur « 24 sur 43 », note
  « 19 lieux masqués », filtre conservé dans l'état.
- Liste ouverte : le lieu courant est bien dans la partie visible de la zone de
  défilement.
- Retour par le bouton : revient à l'ensemble, filtre restauré, sélecteur de
  nouveau visible, titre redevenu « Vallée de la Risle ». La carte retient bien
  24 lieux sur 43 — vérifié sur les données liées à chaque point, les 19 autres
  attendant une disparition que l'onglet de contrôle ne peut pas produire.
- Clavier : 46 éléments atteignables dans le panneau ; le retour prend le focus ;
  l'ordre est notice, retour, liste, lieux.

### Reste ouvert

- **La longueur du panneau.** Il mesure encore 1 223 pixels : l'historique et la
  chronologie sont toujours ouverts. C'est l'objet de L2, qui les repliera.
- **La zone vide à gauche** subsiste tant que la colonne n'est pas collante —
  objet de L3.
- **La validation du porteur.**

---

## L2 — Hiérarchie des contenus (20 septembre 2026)

**Objet.** Que le panneau se lise dans l'ordre où l'on comprend, et qu'il tienne
dans un écran — conséquence directe du choix « panneau court » du porteur.

### Fait

**Le panneau passe de 1 223 à 618 pixels.** Il tient désormais dans un écran
courant, sans rien perdre : tout ce qui était affiché reste atteignable, replié.

**L'ordre de lecture.** Identité ouverte ; historique documenté avec une amorce
visible et la suite dépliable ; chronologie repliée ; localisation et état des
connaissances repliés ; puis le retour et le choix d'un autre lieu.

**Les métiers sortent de la grille de chiffres.** Ils y figuraient en gras sous
l'étiquette « métier », dans une case conçue pour un nombre. Ils sont écrits en
clair sous le nom : « Bois, papier et imprimerie · Métallurgie et travail des
métaux ». La grille de chiffres disparaît entièrement.

**Les compteurs redondants partent.** Le nombre d'activités, que la liste des
activités donne déjà ; le nombre d'événements datés, qui reste seulement sur le
repli de la chronologie, où il sert d'indication de contenu.

**Deux zones de défilement internes supprimées.** La chronologie et le texte de
la notice en avaient chacune une, dans un panneau qui défilait déjà dans une
page qui défilait. Le repli les rend inutiles.

**L'amorce de l'historique coupe à une fin de phrase**, jamais au milieu d'un
mot. Sur le lieu de référence : « Moulin à papier construit en 1761. Exploité en
1824 par Jacques Marais. Consommait en 1826 11500 kg de drilles et produisait
460 rames. » La suite se déplie.

**Les libellés remplacés** : « Ce que dit la notice » devient « Historique
documenté · D'après la fiche d'inventaire, texte non réécrit » ; « Ce qui est
daté » et « Événements extraits du texte de la notice » deviennent
« Chronologie ». « Notice d'origine » devient « Voir la fiche d'inventaire ».

**La distance au cours d'eau descend dans le bloc secondaire**, avec une
formulation qui ferme la porte à la déduction : « 36 m. Une distance mesurée,
qui n'établit pas un usage de l'eau. »

### Deux défauts corrigés au passage

**Un code brut s'affichait au lecteur.** Le bloc de conservation montrait
`partiellement_conserve`. Le vocabulaire contrôlé du projet porte déjà le
libellé « Partiellement conservé », et le générateur le transmettait déjà : il
n'était simplement pas utilisé. Il l'est.

**Le mot « site » subsistait à quatre endroits de l'interface publique**, et non
à un seul comme annoncé dans l'analyse : le texte de précision, la méthode de la
carte du département, et deux phrases du pied de page. Les quatre sont corrigés.

### Décision appliquée sur recommandation

**Le bloc « Localisation et état des connaissances » s'ouvre quand la
conservation est documentée, et reste replié sinon.** Le porteur ne l'avait pas
tranchée. Vérifié sur les deux lieux de la Risle concernés — une affinerie
partiellement conservée, une usine de quincaillerie conservée — et sur un lieu
dont la conservation est inconnue. Elle se change en une ligne.

### Contrôles effectués

Six contrôles du générateur vrais, `ruff` propre, syntaxe JavaScript vérifiée
par Node. Dans le navigateur :

| Cas | Longueur de notice | Hauteur du panneau |
| --- | --- | --- |
| Lieu de référence | 700 caractères | 618 px |
| Notice la plus courte de la Risle | 122 caractères | 566 px |
| Notice la plus longue de la Risle | 1 259 caractères | 662 px |
| Conservation documentée, bloc ouvert | — | 799 px |

Aucune zone de défilement interne ne subsiste dans le panneau, hors la liste des
autres lieux, qui est repliée. Les quatre blocs repliables s'ouvrent au clic et
au clavier. Tous les lieux de la Risle et de Crulai ont un texte et des dates :
les cas « sans texte » et « sans date » n'existent pas dans les deux ensembles
ouverts et n'ont donc pas pu être éprouvés sur données réelles.

### Reste ouvert

- **La zone vide à gauche** — objet de L3.
- **La validation du porteur.**
