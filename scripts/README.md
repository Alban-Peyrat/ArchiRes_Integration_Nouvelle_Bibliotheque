# Utiliser les scripts de ce dossier

## `PPN_in_Koha`

* _[Fichier : `PPN_in_Koha.py`](./PPN_in_Koha.py)_
* _Note : utilise l'ancienne version du conencteur SRU Koha, et de manière géénral pourrait être légèrement amélioré_
* Nécessite de configurer les variables d'environnement :
  * `KOHA_ARCHIRES_SRU` : l'URL du SRU de Koha ArchiRès (pas de slash final)
  * `PPN_IN_KOHA_FILE_IN` : le chemin d'accès complet au fichier contenant la liste des PPNs
* À propos du fichier contenant la liste des PPNs :
  * Doit contenir un PPN par ligne
  * Peut contenir la valeur `NULL` si une notice n'a pas de PPN (mais puisqu'il n'y a pas l'identifiant de la base d'origine, cela est peu utile)
* Fichier de sortie :
  * Nommé `PPN_in_ArchiRes.csv`, se situe dans le même dossier que le fichier contenant la liste des PPNs
  * Composé de 3 colonnes :
    * Le PPN normalisé (suppression des espaces et de la mention `PPN`)
    * Le nombre de notices renvoyées
    * La liste des biblionumbers renvoyés, entre `'`, séparés par une virgule