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
