# Carte de contrôle QGIS — phase 6

Ouvrir `controle_phase6.qgs` dans QGIS 3.x. Le projet utilise des chemins
relatifs et peut donc être déplacé avec tout le dépôt.

## Couches

- **Sites sensibles** : les neuf cas ayant demandé une décision explicite ;
- **Sites pilotes** : les trente points POP de travail ;
- **Adresses BAN** : les quatre résultats testés, y compris le résultat rejeté ;
- **Emprises documentaires POP** : vingt-neuf contours, jamais présentés comme
  des emprises vérifiées ;
- **Parcelles actuelles candidates** : parcelles rencontrées par le point POP ;
- **Fond OpenStreetMap** : simple fond de repérage, non utilisé comme preuve.

Le système de travail du projet est **Lambert-93 (EPSG:2154)**. Les couches
GeoJSON sont stockées en WGS84 et reprojetées à la volée par QGIS.

## Reproduire les couches

```powershell
$env:PYTHONPATH = "src"
python -m patrimoine_orne.geocode.cartographic_control
```

Pour reconstruire ensuite le fichier projet avec l'API du QGIS installé :

```powershell
& "C:\Program Files\QGIS 3.44.12\bin\python-qgis-ltr.bat" `
  tools\generate_qgis_project.py
```

Cette seconde commande écrit le projet avec des chemins relatifs, le relit dans
QGIS, vérifie les cinq couches et produit un aperçu de contrôle.

Le contrôle détaillé est enregistré dans
`reports/quality/phase6_controle_cartographique.md`. Cliquer sur un site dans
QGIS permet de lire son motif de contrôle, la décision manuelle et la note.

## Règle d'usage

La carte sert à repérer les incohérences. Elle ne transforme pas une parcelle
actuelle, un contour POP ou un fond OpenStreetMap en preuve de l'emprise
historique du site.
