# Tests

Les tests peuvent être exécutés sans accès réseau :

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

Les premiers tests couvrent les conventions de nommage, l'horodatage UTC, les
extensions, la structure des métadonnées et la détection d'une modification d'un
fichier brut.
