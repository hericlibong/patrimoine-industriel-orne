# Tests

Les tests peuvent être exécutés sans accès réseau :

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Les premiers tests couvrent les conventions de nommage, l'horodatage UTC, les
extensions, la structure des métadonnées et la détection d'une modification d'un
fichier brut.

Les tests du modèle chargent l'extension DuckDB Spatial, créent une base en
mémoire, injectent `fixtures/model_seed.sql`, puis vérifient les contraintes SQL,
les validations entre tables et la vue des états actuels. Si l'extension
spatiale n'est pas installée, ces seuls tests sont ignorés explicitement.
