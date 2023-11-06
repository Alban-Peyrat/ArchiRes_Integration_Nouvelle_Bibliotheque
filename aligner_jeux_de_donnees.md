# Fusionner des jeu de données en se basant sur une clef commune

_En utilisant [Open Refine](https://openrefine.org), source pour la procédure originale : [Merging Datasets with Common Columns in Google Refine / Tony Hisrt, 2011-05-06](https://blog.ouseful.info/2011/05/06/merging-datesets-with-common-columns-in-google-refine/)_

## Règles générales

* Créer un projet pour chaque jeu de donnée en les nommant de manière explicite
* Identifier quel sera le projet qui recevra les données
  * Par exemple, si l'on souhaite relier les identifiants Omeka-S à des chemins d'accès fichiers dans la base de données d'origine, il semble plus pertinent d'utiliser en projet de destination celui contenant les identifiants d'Omeka-S
  * En revanche, si l'on souhaite pouvoir identifier les chemins d'accès qui ne seraient pas associés à des identifiants Omeka-S, il est plus pertinent d'utiliser le projet de la base de données d'origine, puis de filtrer sur les documents possédant un identifiant dans Omeka-S si besoin
* Identifier dans les projets qui seront importés le nom de la colonne qui servira de clef (ou la renommer)
* Dans le jeu de données de destination, ajouter autant que colonnes que nécessaire en sa basant __la colonne contenant la clef__ avec l'espression GREL : `cell.cross("Nom du projet d'origine", "Colonne de la clef dans le projet d'origine").cells["Nom de la colonne du projet d'origine que l'on veut importer"].value[0]`
* Penser à conserver des traces du nombre d'entrées dans les jeux de données d'origine et du nombre d'entrées correctement alignées dans le jeu de données fusionné
* Ne pas hésiter à faire des corrections manuelles si nécessaire
* __Attention aux doublons dans les colonnes servant de clef__

## Utilisation d'une clef qui n'est pas un identifiant

* Si le jeu de données ne possèdent pas d'identifiant unique, mais uniquement des données telles que des titres de documents, il est possible d'utiliser la fonction _fingerprint_ d'Open Refine (exemple : expression GREL `fingerprint(value)`)

## Transformer des nombres en texte

* Si l'on souhaite exporter des identifiants sous forme numérique, les formattages de données peuvent modifier les identifiants, il est donc important de vérifier que ceux-ci conservent leur forme originale
* Selon les scénarios, plusieurs formules peuvent être utilisées en transformant le contenu des cellules :
  * Si l'option _To text_ génère des `.0` : utiliser le Python : `str(int(value))` (et penser à conserver la valeur originale en cas d'erreur)
