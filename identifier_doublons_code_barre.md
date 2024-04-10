# Vérification des doublons de code-barres entre les données entrantes et la base de données d'origine

_Nécessite OpenRefine (et potentiellement MarcEdit)_

__Cette vérification se abse sur le principe que tous les code-barres sont préfixés__ : si ce n'est pas le cas, retirer la limite dans l'export des code-barres de la base de données de destination (en évitant de faire planter la base de données).

## Exporter les données

Exporter les données de Koha avec une requête SQL telle que :

``` SQL
SELECT biblionumber, barcode FROM items WHERE barcode IS NOT NULL AND barcode LIKE "%{préfixe}%"
-- Où {préfixe} correspond au préfixe (ex : %ENSP%)
```

Pour les données entrantes, si elles sont déjà une liste d'exemplaires au format CSV, pas besoin de faire une extraction de données.

Au contraire, si elles sont au format MARC :

* Ouvrir MarcEdit
* Depuis l'accueil, exécuter l'outil d'export au format tabulé (_Tools → Export... → Export Tab Delimited Records_)
* Exporter les données séparées par des tabulations avec des `;` en séparateur intra-champ
* Exporter le champ contenant l'identifiant de la notice dans la base de données d'origine et celui contenant le code-barre
* Ouvrir OpenRefine
* Sur la colonne contenant les code-barres, sélectionner la division des cellules à multiples valeurs (_Edit cells → Split multi-valued cells..._)
* Utiliser `;` comme séparateur
* Valider
* Sur la colonne _All_, remplir les données vers le bas (_Edit columns → Fill down_)

## Comparer les données

* Créer un projet pour chaque fichier
* Dans le projet __des données entrantes__, créer une colonne basée sur la colonne contenant les code-barres avec l'expression GREL suivante :

``` GREL
cell.cross("{Nom Projet BDD destination}", "barcode").cells["biblionumber"].value[0]

// Commentaire :
// {Nom Projet BDD destination} est le nom du projet contenant les données de Koha
// "barcode" & "biblionumber" sont à adapter en fonction des noms des colonnes
```

* Afficher les facettes textuelles sur cette nouvelle colonne (_Facet → Text Facet_) :
  * Si aucune cellule n'est remplie, __aucun doublon n'est présent__
  * Si certaines cellules ont des valeurs, __les code-barres de la ligne sont déjà présents dans la base de données de destination__