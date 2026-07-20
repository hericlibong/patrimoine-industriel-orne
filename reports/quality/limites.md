# Registre des limites

Document vivant — dernière mise à jour : 20 juillet 2026

| ID | Source ou étape | Limite constatée | Conséquence | Traitement prévu | Statut |
|---|---|---|---|---|---|
| LIM-001 | Comptage général | Une notice n'équivaut pas nécessairement à un site | Le nombre final de lieux est encore inconnu | Compter séparément notices, candidats, sites rapprochés, cartographiables et publiés | ouverte |
| LIM-002 | Inventaire normand | Aucun export global actuel des 319 dossiers n'a été identifié | Extraction complète non garantie automatiquement | Utiliser POP pour les champs, les dossiers statiques pour les scans, puis mesurer la part d'OCR et de contrôle humain | ouverte |
| LIM-003 | Inventaire normand | Plusieurs dossiers ne sont pas géolocalisés | Une partie du corpus peut rester sans point précis | Rechercher adresse, parcelle, plans et sources complémentaires | ouverte |
| LIM-004 | CASIAS | 1 853 entrées sur 2 052 sont déclarées non géolocalisées dans la couche testée | CASIAS seul ne permet pas de placer la majorité des candidats | Ne jamais utiliser la commune comme faux emplacement ; recouper adresses, archives et cartes | ouverte |
| LIM-005 | CASIAS | Le champ d'activité est vide dans la couche WFS régionale testée | Filtrage patrimonial impossible à partir de cette couche seule | Tester le CSV national et les fiches détaillées | ouverte |
| LIM-006 | CASIAS | La base comprend de nombreuses activités de service sans intérêt patrimonial direct | Surestimation possible du corpus industriel | Classifier puis vérifier chaque candidat avant inclusion | ouverte |
| LIM-007 | Monuments historiques | La source ne couvre que les immeubles protégés | Une absence ne signifie pas absence de patrimoine | Employer la source comme enrichissement, jamais comme corpus exhaustif | permanente |
| LIM-008 | Palissy | Les liens entre objets et sites sont parfois indirects | Risque de mauvais rattachement d'une machine ou d'un objet | Exiger une référence Mérimée ou un contrôle édifice-commune | ouverte |
| LIM-009 | Géolocalisation | Adresse, lieu-dit, point géocodé et parcelle n'ont pas la même précision | La carte peut donner une précision artificielle | Enregistrer et afficher le niveau de précision séparément | permanente |
| LIM-010 | Images | Une image consultable n'est pas nécessairement réutilisable | Risque juridique lors de la publication | Vérifier auteur, détenteur, licence et crédit avant diffusion | permanente |
| LIM-011 | État actuel | Usage, conservation et accessibilité peuvent évoluer rapidement | Informations contemporaines rapidement périmées | Dater les observations et appliquer les durées de fraîcheur définies | permanente |
| LIM-012 | Inventaire normand | Les ressources CSV et cartographique liées depuis data.gouv.fr sont obsolètes ou en erreur | Le jeu régional ne peut pas être téléchargé directement par ces liens | Conserver la date du constat et rechercher un export régional actuel avant extraction complète | ouverte |
| LIM-013 | Inventaire normand | Les anciens dossiers détaillés sont principalement des pages numérisées | Le texte complet n'est pas immédiatement structuré | Réserver l'OCR aux informations absentes de POP et prévoir un contrôle humain | ouverte |
| LIM-014 | Monuments historiques | La recherche industrielle par mots-clés retourne 77 résultats larges et des faux positifs | Ce total ne peut pas être présenté comme un nombre de sites industriels | Classifier et relire les résultats avant tout rapprochement ou comptage | ouverte |
| LIM-015 | Palissy | Les deux objets techniques tests n'ont pas de référence Mérimée directe renseignée | Une jointure automatique par identifiant n'est pas toujours possible | Rapprocher par édifice, commune et texte, puis valider manuellement | ouverte |
| LIM-016 | Encodages | Les anciens fichiers HTML de l'Inventaire sont en ISO-8859-1, contrairement aux autres échantillons en UTF-8 | Risque de caractères altérés lors d'une fusion directe | Conserver le brut et normaliser toutes les données dérivées en UTF-8 | ouverte |
| LIM-017 | Échantillonnage | Les échantillons sont petits, ciblés et, pour CASIAS, volontairement stratifiés | Les taux observés ne décrivent pas nécessairement les sources complètes | Présenter les effectifs bruts et mesurer à nouveau lors de l'extraction complète | permanente |
| LIM-018 | Coordonnées POP et MH | Un point WGS84 valide ne garantit pas l'emprise ni la précision du bâtiment industriel | Risque de publier une localisation trop précise ou décalée | Qualifier la méthode et le niveau de précision avant publication | permanente |
| LIM-019 | État actuel | Les champs de destination et de conservation sont absents ou peu renseignés dans les sources testées | L'état contemporain ne peut pas être produit automatiquement | Recourir à des sources récentes, à l'observation et à une date de vérification | permanente |
| LIM-020 | Provenance | La cible générique de `mentions_sources` ne peut pas être protégée par une clé étrangère SQL unique | Une mention pourrait viser une entité ou un champ inexistant | Le validateur transversal contrôle l'existence de la cible et du champ avant chaque export | resolue |
| LIM-021 | Géométries | Un site peut posséder plusieurs points, parcelles ou emprises de précision différente | Le choix silencieux d'une seule géométrie masquerait l'incertitude | Conserver toutes les géométries et désigner explicitement la référence par usage | permanente |
| LIM-022 | Dates historiques | La conversion d'une expression comme « vers 1850 » en intervalle repose sur une convention du projet | L'intervalle calculé pourrait être pris pour une datation fournie par la source | Conserver le texte original, la précision et la nature calculée de l'intervalle | permanente |
| LIM-023 | DuckDB Spatial | Le type `GEOMETRY` dépend d'une extension DuckDB installée séparément | L'initialisation spatiale échoue sur un nouvel environnement sans cette extension | Fournir l'option `--install-spatial` et arrêter explicitement l'initialisation si l'extension manque | permanente |

## Règle de mise à jour

Ce registre est mis à jour pendant chaque phase. Une limite passe à `resolue`
uniquement lorsque la méthode et le résultat du contrôle sont documentés. Les
limites structurelles restent `permanente` et sont reprises dans le rapport de
qualité final.
