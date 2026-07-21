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

`fixtures/phase3_validation_cases.sql` ajoute les cinq scénarios qui ont servi à
approuver le modèle V1. Ces lignes sont toutes fictives et ne doivent jamais être
exportées dans le corpus patrimonial.

`test_classify_sectors.py` contrôle le registre YAML, la séparation entre
activité, installation, énergie et équipement, ainsi que la couverture des 13
dénominations du test de phase 4.
