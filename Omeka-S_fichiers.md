# Associer des fichiers à des contenus dans Omeka-S

_Note : cette procédure se base sur l'utilisation du webdav avec le module_ [Omeka-S File Sideload](https://omeka.org/s/modules/FileSideload/) _&_ [CSV Import](https://omeka.org/s/modules/CSVImport/).

Cette procédure nécessitent 2 préparations en amont :

1. Créer les notices bibliographiques dans Koha (et attendre un jour pour qu'elles soient exportées dans Omeka-S)
1. Avoir ajouté au webdav les fichiers

La procédure assument que les documents sont importés en accès restreints à une certain catgéorie d'utilsiateurs.

## Alignement des données

Cette étape peut être plus ou moins longue, mais le but final est d'avoir un fichier CSV contenant 2 colonnes : l'identifiant Omeka-S du contenu et le chemin d'accès relatif dans le webdav.

Par exemple, à partir d'un fichier contenant les chemins d'accès dans le webdav et les numéros de notices dans le système d'origine :

1. Rajouter le numéro de notice ArchiRès en se basant sur le numéro de notices du système d'origine
1. Rajouter l'identifiant Omeka-S en se basanr sur le numéro de notice ArchiRès
1. [Optionnel mais recommandé] Vérifier s'il y a déjà des médias rattachés et retirer les contenus ou non en fonction de ce qui est déjà présent
1. Supprimer les identifiants de notices du système d'origine & ArchiRès

__Quelques spécifications sur le fichier de sortie finale__ :

* __L'import réécrira les émdias déjà existants s'ils y en avaient__ (il ne rajoutera pas les nouveau, il écrasera l'existant)
* L'export CSV doit utiliser `;` comme séparateur, et toutes les données doivent être comprises entre `"`
* Il est possible d'importer plusieurs fichiers : utiliser `,` comme séparateur interne au chemin des chemins d'accès
* S'il y a des espaces dans les chemins d'accès au webdav, __ne pas les rempalcer__ par `%20` _(le plus simple étant évidemment de ne juste pas en mettre de base)_
* Les colonnes doivent être nommées :
  * `item` : identifiant du contenu dans Omeka-S
  * `path` : chemin d'accès dans le webdav

Exemple de fichier :

```
"item";"path"
"87604";"admin/PAYV/ALGEDIM 2/RTGJZK 2/D59/D5984.pdf"
"88152";"admin/PAYV/ALGEDIM 2/RTGJZK 2/D60/D6007.pdf,admin/PAYV/ALGEDIM 2/RTGJZK 2/D60/D6008.pdf"
```

## Import des médias

_Si nécessaire, créer une collection sur le modèle `ENSA` en ouvrant aux ajouts (cadenas en haut à droite)_

* __Désactiver la suppression des fichiers dans la configuration de *File Sideload* avant de faire l'import__
* Dans le module _Import CSV_
  * Tableur : le fichier de matching des ID
  * Séparateur de colonne CSV : _point-virgule_
  * Délimiteur de colonne CSV : _guillemet droit_
  * Type d'import : _Contenus_
  * Commentaire : `{Texte indiquant ce qu'est cet import}`
* Après avoir cliqué sur _Suivant_ :
  * Mapper vers les données Omeka S :
    * Colonne avec l'item ID : ne rien faire
    * Colonne avec le chemin relatif sur le sideload :
      * _+ → Source du média → Chargement serveur → Appliquer les changements_
      * _Clef à molette : cocher_ Utiliser un séparateur multivalué _→ Appliquer les changements_
  * Paramètres de base :
    * Propriétaire : `{la personne référente de la bibliothèque}`
    * Visibilité : _public_
    * Collections : `{une collection existante / celle créée avant l'import}`
    * Séparateur pour les valeurs multiples : `,`
  * Paramètres avancés :
    * Action : _Corriger les métadonnées d'une ressource_
    * Colonne de l'identifiant de la ressource : colonne de mon fichier avec l'item ID
    * Propriété de l'identifiant de la ressource : _Identifiant interne_
    * Actions sur les ressources non-identifiées : _Ignorer la ligne_
  * Cliquer sur le bouton _Importer_

Une fois l'import achevé :

* __Réactiver la suppression des fichiers dans la configuration de *File Sideload*__
* Lire les logs et rechercher s'il y a eu des erreurs, les lister et les traiter
* _(Faire quelques vérifications évidemment)_

## Ajout des droits

* Exporter la liste des items (ou utiliser le fichier importé) en utilisant __des retours à la ligne__ comme séparateur
* Utiliser [le job 9 de `fix_visibility_issues`](https://github.com/Alban-Peyrat/OmekaS_utils/blob/master/fix_visibility_issues.py)
  * Vérifier le `.env`
  * Rajouter les groupes en les séparant par des `,` (ex :`3835,3556`)
