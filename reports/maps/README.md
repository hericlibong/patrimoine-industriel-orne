# Carte interne du corpus pilote

## Livrable

`carte_pilote_interne.png` est la première carte de contrôle conçue pour être
partagée en interne. Elle montre :

- les 30 sites pilotes ;
- leur secteur principal ou leur caractère multi-secteurs ;
- les 9 localisations qui demandent encore une vérification ;
- le contour départemental de l'Orne ;
- les limites d'interprétation du pilote.

La carte ne contient pas de fond de tuiles externe. Elle reste donc autonome et
ne dépend pas d'un accès à OpenStreetMap ou à un fournisseur cartographique.

## Usage

La carte peut être utilisée dans une note, une réunion ou une présentation du
projet. Elle ne doit pas être présentée comme une cartographie exhaustive du
patrimoine industriel de l'Orne.

Les points restent approximatifs. Le cercle rouge ne signale ni danger, ni
pollution : il indique uniquement une localisation à vérifier.

## Reproduction

```powershell
& "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat" `
  tools\generate_internal_control_map.py
```

Le script utilise les sites validés de la phase 6 et un contour simplifié créé
à partir des communes de l'Orne diffusées par l'API Découpage administratif.
Le résultat du contrôle et son empreinte sont enregistrés dans
`carte_pilote_interne_validation.json`.
