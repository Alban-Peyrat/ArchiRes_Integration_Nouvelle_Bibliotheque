# Utiliser les scripts de ce dossier

## `edit_records`

* __Ancien script__
* _[Fichier : `edit_records.py`](./edit_records.py)_
* Nécessite de configurer les variables d'environnement :
  * `EDIT_RECORDS_ORIGIN_ID_NAME` : le nom donné de l'identifiant de la base de données d'origine. __Ne doit pas être `bibnb`__ qui est utilisé pour celui du Koha ArchiRès
  * `EDIT_RECORDS_FILE_IN` : le chemin d'accès complet au fichier contenant les notices au format ISO 2709
  * `EDIT_RECORDS_IDS_MAPPING_FILE` : le chemin d'accès complet au fichier contenant la liste des correspondances entre la base de données d'origine et Koha ArchiRès
* À propos du fichier contenant la liste des correspondances entre la base de données d'origine et Koha ArchiRès :
  * Séparateur : `;`
  * Seules deux colonnes sont lues : celle contenant la valeur assignée à la variable d'environnement `EDIT_RECORDS_ORIGIN_ID_NAME` et celle nommée `bibnb`, qui doit contenir les biblionumbers du Koha ArchiRès
  * Il peut y avoir plusieurs biblionumbers du Koha ArchiRès associés, séparés par une virgule, mais cela entraînera une erreur
* À propos du fichier contenant les notices :
  * Elles doivent être au format ISO 2709
* À propos du fichier de sortie :
  * S'appelle `RECORDS_FOR_KOHA.mrc` et est créé dans le même dossier que le fichier contenant les notices d'origine
  * Est au format ISO 2709
* À propos du fichier d'erreur :
  * S'appelle `edit_records_errors.csv`
  * Contient 3 colonnes :
    * `record_nb` : index de la notice dans le fichier original cotnenant les notices
    * valeur assignée à la variable d'environnement `EDIT_RECORDS_ORIGIN_ID_NAME` : contient l'identifiant de la notice qui se trouvait dans la notice
    * `error` : contient le message d'erreur, parfois suivi de `:` et d'une information compélmentaire

## `PPN_in_Koha`

_[Fichier : `PPN_in_Koha.py`](./PPN_in_Koha.py)_


Nécessite de configurer les variables d'environnement :

* `KOHA_SRU` : l'URL du SRU de Koha
* `PPN_IN_KOHA_FILE_IN` : le chemin d'accès complet au fichier contenant la liste des PPNs
* `PPN_IN_KOHA_OUTPUT_FILE` : le chemin d'accès complet au fichier de sortie (`.csv`)

À propos du fichier contenant la liste des PPNs :

* Doit contenir un PPN par ligne
* Peut contenir la valeur `NULL` si une notice n'a pas de PPN (mais puisqu'il n'y a pas l'identifiant de la base d'origine, cela est peu utile)

Le fichier de sortie est composé de 3 colonnes :

* Le PPN normalisé (suppression de tout caractère qui n'est ni un chiffre, ni `X` et ajout de `0` en tête de PPN si nécessaire)
* Le nombre de notices renvoyées
* La liste des biblionumbers renvoyés, séparés par une virgule
  * Si elle contient `SKIPPED_PPN`, le PPN était égal à `NULL`
  * Si elle contient `EMPTY_PPN`, le PPN est devenu vide lors de la préparation de la requête au SRU
  * Si elle contient `SRU_ERROR`, le SRU a rencontré une erreur lors de l'exécution de la requête

## `extract_matching_ids_from_analyzed_FCR_files`

_[Fichier `extract_matching_ids_from_analyzed_FCR_files.py`](./extract_matching_ids_from_analyzed_FCR_files.py)_

Nécessite de configurer les variables d'environnement :

* `EXTRACT_ID_FCR_FILES_FOLDER` : dossier contenant tous les fichiers FCR analysés __au format `.xlsx`__ (et uniquement cela)
* `EXTRACT_ID_FCR_OUTPUT_FILE` : le chemin d'accès complet au fichier de sortie (`.csv`)
* `EXTRACT_ID_FCR_COLUMN_NAME_ORIGIN_ID` : le nom de la colonne contenant l'identifiant dans la base de données d'origine
* `EXTRACT_ID_FCR_COLUMN_NAME_TARGET_ID` : le nom de la colonne contenant l'identifiant dans la base de données de destination
* `EXTRACT_ID_FCR_COLUMN_NAME_ACTION` : le nom de la colonne contenant l'action à effectuer sur la notice
* `EXTRACT_ID_FCR_ACTION` : le chaîne de caractère qui doit être __contenue__ dans la colonne des actions à effectuer pour être détectée comme étant une correspondance valide

Le fichier de sortie est composé de 2 colonnes :

* L'identifiant de la notice dans la base de données d'origine
* L'identifiant de la notice dans la base de données de destination (__/!\\ vérifier qu'il n'y a pas de `nan` dans cette colonne__)

Au cours de l'exécution, le script va écrire dans la console les feuilles des fichiers qu'il n'a pas réussi à interpréter, en listant les colonnes qu'il n'a pas trouvé au sein de la feuille _(exemple dans [le fichier `010_terminal_text.txt`](./files/060_terminal_text.txt))_.
__Il est recommandé de vérifier ces informations.__

## `add_bibnb_barcodes_to_records`

_[Fichier `add_bibnb_barcodes_to_records.py`](./add_bibnb_barcodes_to_records.py)_

Nécessite de configurer les variables d'environnement :

* `ADD_BIBNB_RECORDS_FILE` : le chemin d'accès complet au fichier contenant les notices à modifier
* `ADD_BIBNB_ID_MAPPING_FILE` : le chemin d'accès complet au fichier contenant la liste des identifiants mappés (obtenus via [`extract_matching_ids_from_analyzed_FCR_files`](#extract_matching_ids_from_analyzed_fcr_files) par exemple)
* `ADD_BIBNB_DELETE_RECORDS_FILE` : le chemin d'accès complet au fichier contenant la liste des notices à supprimer (doit être un CSV séparé par `;` et doit contenir au moins la colonne `origin_db_id`)
* `ADD_BIBNB_FILE_OUT` : le chemin d'accès complet au fichier de sortie (format UNIMARC)
* `ADD_BIBNB_ERRORS_FILE` : le chemin d'accès complet au fichier contenant les erreurs recontrées (`.csv`)
* `ADD_BIBNB_PREPEND_ORIGIN_DB_ID` : si nécessaire, une chaîne de caractère à rajouter __devant__ les identifiants de la base de données d'origine contenus dans la liste des identifiants mappés
* `ADD_BIBNB_PREPEND_TARGET_DB_ID` : si nécessaire, une chaîne de caractère à rajouter __devant__ les identifiants de la base de données de destination contenus dans la liste des identifiants mappés
* `ADD_BIBNB_BARCORDE_PREFIX` : le préfixe des code-barres pour cette école
* `ADD_BIBNB_BARCORDE_CITY` : si nécessaire, une lettre (ou chaîne de caractère) ajoutant une précision sur le contexte de la génération du code-barre (par exemple, la ville de la bibliothèque si l'établissement à des bibliothèques dans plusieurs villes)
* `ADD_BIBNB_FICTIVE_ITEM_LIBRARY` : code de bibliothèque à attribuer à un exemplaire fictif
* `ADD_BIBNB_FICTIVE_ITEM_STATUS` : code de statut à attribuer à un exemplaire fictif
* `ADD_BIBNB_FICTIVE_ITEM_ITEMTYPE` : code de statut à attribuer à un exemplaire fictif
