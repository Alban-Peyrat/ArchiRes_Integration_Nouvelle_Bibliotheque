
_texte à rédiger_

## Générer un fichier `.csv` à partir des fichiers analysés de FCR

Pour générer ce fichier, utiliser le script [`extract_matching_ids_from_analyzed_FCR_files.py`](./scripts/extract_matching_ids_from_analyzed_FCR_files.py).

La première chose à faire est de regrouper tous les fichiers analysés (doivent être des fichiers Excel) dans un dossier commun __et uniquement ces fichiers__.
Veiller ensuite à ce que, sur toutes les feuilles de tous les fichiers, les colonnes possédant l'identifiant de la base de données d'origine, de la base de données de destination et la colonne des actions à effectuer portent __strictement__ le même nom.
Définir ensuite les variables d'environnement suivantes :

* `EXTRACT_ID_FCR_FILES_FOLDER` : chemin d'accès complet au dossier contenant les fichiers analysés
* `EXTRACT_ID_FCR_OUTPUT_FILE` : chemin d'accès complet du fichier `.csv` de sortie
* `EXTRACT_ID_FCR_COLUMN_NAME_ORIGIN_ID` : nom de la colonne contenant les identifiants de la base de données d'origine
* `EXTRACT_ID_FCR_COLUMN_NAME_TARGET_ID` : nom de la colonne contenant les identifiants de la base de données de destination
* `EXTRACT_ID_FCR_COLUMN_NAME_ACTION` : nom de la colonne contenant les actions à effectuer
* `EXTRACT_ID_FCR_ACTION` : chaîne de texte __contenue__ dans la colonne d'action permettant de déterminer si le couple d'identifiant doit être extrait dans le fichier (__non sensible à la casse__)

Et exécuter le script.

Si certaines feuilles des fichiers Excel ne contenaient pas toutes les colonnes, le terminal affchera le fichier et la feuille concernée, ainsi que les colonnes non trouvées.
si certaines feuilles auraient dû être analysées, corriger les fichiers Excel et relancezrle script.