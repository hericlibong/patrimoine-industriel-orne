# Phase 4 — test de la chronologie et de la situation actuelle

Date du contrôle : 21 juillet 2026.

## Échantillons contrôlés

- 10 notices POP/Mérimée industrielles du manifeste de phase 2 ;
- 77 candidats issus de la recherche large dans les Monuments historiques.

Les 77 résultats MH ne constituent pas un corpus industriel validé : ils
contiennent des faux positifs. Les nombres ci-dessous servent seulement à tester
les champs et les règles de classement.

## Résultats simples

### Chronologie

Le champ de siècle `SCLE` est présent dans les 10 notices POP. Il aide à situer
les sites, mais ne remplace pas les dates détaillées ni le texte historique. Les
sept périodes définies sont des filtres calculés : une activité qui traverse
deux périodes appartient aux deux.

### Conservation

Dans POP, les 6 valeurs présentes sont toutes « établissement industriel
désaffecté ». Cette expression indique l'arrêt de l'activité, pas l'état matériel
du site. Elle est donc exclue de la classification de conservation.

Dans les 77 notices MH, seules 4 mentions décrivent directement un état matériel
classable : 1 « bon état », 1 « mauvais état » et 2 « vestiges ». Les 14 mentions
« désaffecté » sont également exclues de la conservation.

Conclusion : la conservation actuelle devra surtout être vérifiée par des
sources récentes ou par observation. Elle n'est pas automatisable à partir de
ces deux champs seuls.

### Usages actuels

Le champ de destination actuelle est vide dans les 77 notices MH testées. Le
modèle autorise plusieurs usages simultanés, par exemple `culture_musee` et
`tourisme_visite`, au lieu d'une catégorie imprécise `usage_mixte`.

Conclusion : les usages actuels nécessiteront des sources récentes, datées et
souvent une vérification humaine.

### Accessibilité

Les sources testées ne donnent pas un droit d'entrée fiable. Le vocabulaire
distingue la visite autorisée, la visibilité depuis l'espace public, la propriété
privée et l'inaccessibilité. Un site visible n'est jamais automatiquement déclaré
visitable.

### Protections

Les 77 notices MH portent toutes un libellé de protection analysable. Elles
produisent 86 mesures : 17 classements et 69 inscriptions, car 9 notices cumulent
les deux types. Neuf mesures sont explicitement partielles ; la portée des 77
autres reste `inconnue` tant que l'arrêté ou la précision de protection n'a pas
été interprété.

L'absence d'une mesure dans la table ne signifie pas « non protégé ». Elle
signifie seulement qu'aucune protection n'a encore été identifiée ou vérifiée.

## Effet sur le projet

- la chronologie historique est en grande partie structurante et calculable ;
- la protection MH est extractible mais exige de séparer type, portée et cible ;
- conservation, usage et accessibilité sont des observations contemporaines à
  dater et à rafraîchir ;
- la phase pilote devra prévoir une enquête manuelle pour ces trois dimensions.

Les mesures détaillées sont conservées dans
`reports/quality/phase4_chronologie_situation_sample.json`.
