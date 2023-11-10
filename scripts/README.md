# Utiliser les scripts de ce dossier

## `edit_records`

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

* _[Fichier : `PPN_in_Koha.py`](./PPN_in_Koha.py)_
* _Note : utilise l'ancienne version du conencteur SRU Koha, et de manière général pourrait être légèrement amélioré_
* Nécessite de configurer les variables d'environnement :
  * `KOHA_ARCHIRES_SRU` : l'URL du SRU de Koha ArchiRès
  * `PPN_IN_KOHA_FILE_IN` : le chemin d'accès complet au fichier contenant la liste des PPNs
* À propos du fichier contenant la liste des PPNs :
  * Doit contenir un PPN par ligne
  * Peut contenir la valeur `NULL` si une notice n'a pas de PPN (mais puisqu'il n'y a pas l'identifiant de la base d'origine, cela est peu utile)
* Fichier de sortie :
  * Nommé `PPN_in_ArchiRes.csv`, se situe dans le même dossier que le fichier contenant la liste des PPNs
  * Composé de 3 colonnes :
    * Le PPN normalisé (suppression de tout caractère qui n'est ni un chiffre, ni `X` et ajout de `0` en tête de PPN si nécessaire)
    * Le nombre de notices renvoyées
    * La liste des biblionumbers renvoyés, entre `'`, séparés par une virgule