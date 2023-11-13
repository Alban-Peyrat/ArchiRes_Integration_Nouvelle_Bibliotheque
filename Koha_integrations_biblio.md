# Intégration des notices bibliographiques dans Koha

## Déboulonner les notices dans la base d'origine

* Identification puis traitement

## Établir le mapping UNIMARC

_Voir un exemple de [mapping entre UNIMARC](./mapping_UNM_to_UNM.xlsx) et [avec une base sans UNIMARC](./mapping_other_to_UNM.xlsx)._

Le réseau ArchiRès se base sur la version française de la norme UNIMARC telle qu'elle est publiée sur [le site de la Transition bibliographique](https://www.transition-bibliographique.fr/unimarc/manuel-unimarc-format-bibliographique/#Bloc%200XX), toutefois certains champs sont propres et au réseau (et certains champs sont hérités [du format utilisé par le Sudoc](https://documentation.abes.fr/sudoc/)).
La liste des divergences et spécficités de l'UNIMARC utilisé dans le réseau ainsi que la manière d'identifier les listes de codes utilisés sont spécifiés dans la documentation technique interne du réseau ([Archires_Structure_Technique/Koha/UNM_champs_locaux.md](https://github.com/Alban-Peyrat/Archires_Structure_Technique/blob/main/Koha/UNM_champs_locaux.md)).

Une grande vigilance doit être apportée à correctement transformer les données d'origine vers les codes corrects, avec une vigilance accrue sur les champs __099__ et __995__ (exemplaires) pour lesquels des données erronées peuvent avoir un impact important.

Lorsque l'on mappe des données en les transformant en des codes dans un document à destination de prestataires ou personnes externes au réseau, il est __impératif d'indiquer les codes et non les libellés__.
Ainsi, dans le cas d'un document exporté vers Omeka-S, on veillera à bien indiquer _099$x1_ et non pas une formulation similaire à _099 $x oui_.

Si l'on souhaite faire apparaître les libellés dans le mapping dans un soucis de lisibilité, veiller à ce qu'il soit extrêmement clair que c'est un commentaire interne et non une demande.
Ne pas hésiter à également rajouter une zone de commentaire spécifique et clairement identifiée destinée aux prestataires ou personnes externes au réseau.
Si nécessaire, ajouter dans un second document des précisions sur certains points (par exemple, expliquer que la 099 est unique, indiquer sur quelle norme nous nous basons et lier le document comportant nos spécificités vis-à-vis de cette norme) (voir [mapping_COMPLEMENT.pdf](./mapping_COMPLEMENT.pdf)).

Dans le cas de mapping qui nécessiterait une suite d'actions, une illustration par un diagramme peut parfois être pertinente (voir [img/Exemple_Flowchart_Complementaire, aussi présent dans mapping_COMPLEMENT.pdf](img/Exemple_Flowchart_Complementaire.svg)).

Dans l'idéal, créer dans la base de données d'origine des exemples (à défaut, en trouver) pour chaque cas de figure de chaque règle de mapping, en indiquant la situation initiale et le comportement voulu (voir [mapping_test_plan.pdf](./mapping_test_plan.pdf)).

## Identification des correspondances entre la base d'origine et la Koha ArchiRès

* Si l'on possède la liste des PPNs des documents de la base d'origine, possibilité d'utiliser le script [`PPN_in_Koha`](./scripts/README.md#ppn_in_koha)
* Selon le volume, la correspondance peut être faite manuellement, mais il faut __absolument veiller à indiquer l'identifiant interne de la base d'origine dans le fichier et que celui-ci soit facilement identifiable via ordinateur__
  * Ne pas identifier le numéro interne de la base d'origine signifie qu'il faudra réidentifier les documents concernés dans la base d'origine, donc prendre le risque d'une perte du travail effectué (informations qui ont changé, informations qui sont les mêmes entre différents documents, etc.)
* Sinon, utiliser [FCR (Find and Compare Record)](https://github.com/Alban-Peyrat/Find_and_Compare_Records)

## Transformation des notices pour l'intégration

* Si nécessaire, transformer les notices qui seront intégrées
  * Bien veiller à supprimer les biblionumbers (001) et numéros d'exemplaires (995$9) pour éviter des imports sur les mauvaises notices et / ou exemplaires
  * Renseigner les biblionumbers sur les notices qui doivent uniquement importer des exemplaires
  * __Toujours modifier les notices mêmes si elles doivent seulement importer les exemplaires__, selon les procédés utilisés, une erreur peut entraîner l'import de la notice et pas uniquement de l'exemplaire
* _Exemple du script [`edit_records`](./scripts/edit_records.py)_

## Import des notices dans Koha

* Sur des lots peu importants, peut être effectué via l'interface professionnel de Koha :
  * Le but est de constituer des lots de moins de 1000 exemplaires afin de pouvoir afficher le rapport final de traitement des notices
  * _Pour diviser un lot de notices, MarcEdit a un outil_ MarcSplit _qui permet de signaler la tailles des lots voulus_
  * Dans l'outil Koha _Télécharger des notices dans le réservoir_, paramétrages de l'import :
    * _NB : cet import part du principe qu'il n'y a qu'un seul lot comprenant les notices pour lesquelles nous n'importons que les exemplaires et de nouvelles notices_
    * Type de notices : _bibliographique_
    * Encodage des caractères : _UTF-8_
    * Format : _MARC_ (ou _MARCXML_ si on les en a XML)
    * Modèle de transformation MARC : _ne pas utiliser_ (privilégier les modifications __avant__ l'import dans Koha)
    * Règle de concordance : _BIBNB_ (qui match sur les biblionumbers)
    * Action en cas de correspondance : _Ignorer la notice entrante_
    * Action s'il n'y a pas de concordance : _Ajouter les notices entrantes_
    * Vérifier les données exempalires incluses ? _Oui_
    * Traitement des exemplaires : _Toujours ajouter les exemplaires_
  * Une fois validé, cliquer sur le bouton _Gestion des notices téléchargées_
  * Puis le bouton _Importer ce lot dans le catalogue_
* Pour des lots plus importants, contacter le prestataire pour utiliser [`bulkmarcimport.pl`](https://perldoc.koha-community.org/misc/migration_tools/bulkmarcimport.html)
  * __Attention__, la seule utilisation faite a été pour mettre à jour des notices, pas pour importer de nouveaux exempalires. Donc __vérifier__ comment faire si utilisation de ce processus

## Identifier les problèmes rencontrés

### Notices qui n'ont pas fusionné correctement

* Identifier la liste des biblionumbers de notice possédant un exemplaire dans la bibliothèque mais qui ne proviennent pas de la base de donnée d'origine avec une requête SQL : `SELECT biblionumber FROM items JOIN biblio_metadata bm USING (biblionumber) WHERE homebranch = "{code}" AND NOT ExtractValue(bm.metadata, '//datafield[@tag="801"]/subfield[@code="9"]') = "{code utilisé}" GROUP BY biblionumber`
* Extraire la liste des biblionumbers qui auraient dû fusionner à partir du fichier MARC importé : grâce à l'outil d'export en délimitation tabulé de MarcEdit, exporter les `001`
* Supprimer les en-têtes si elles existent et [comparer les deux listes](http://barc.wi.mit.edu/tools/compare/) :
  * Si tout s'est bien passé, aucun biblionumber ne doit se trouver uniquement dans une des deux listes
  * Si des biblionumbers se trouvent uniquement dans l'export de Koha, cela devrait être des notices dont les exemplaires ont été créés manuellement, pas par l'import
  * Si des biblionumbers se trouvent uniquement dans l'export du fichier importé, il est probable que les notices qui auraient du recevoir les données n'existent plus :
    * La notice existe dans Koha : fusionner la notice qui a été créé avec cette notice (utiliser la requête `other-control-number={préfixe}{identifiant}` pour identifier la notice incorrectement créée)
    * La notice ne semble plus exister dans Koha : utiliser le rapport ID 1464 `DEBUG_find_unknown_status_biblio_by_biblionumber` pour identifier si elle est présente dans la table des notices supprimées :
      * Si la notice est trouvée uniquement dans la table des notices supprimées, ne rien faire : la notice originale n'existe plus, donc il fallait l'importer _(suppose que les 035 ne sont pas supprimés dans des fusions)_
      * Si la notice est trouvée dans la table des notices supprimées et a une seconde entrée avec `Merged biblio` comme _source_, fusionner la nouvelle notice avec la notice dont le biblionumber s'affiche à côté de `Merged biblio`
      * Si la notice n'est pas trouvée, une erreur a probablement eu lieu lors de l'attribution du biblionumber d'ArchiRès, rechercher les notices manuellement dans le Koha ArchiRès et fusionner si nécessaire

### Exemplaires qui n'ont pas été importés

* _Très probablement dû à des doublons de code-barre_
* Identifier la liste des code-barres des exemplaires de la bibliothèque avec leur titre et auteur avec une requête SQL : `SELECT i.barcode, biblionumber, b.title, b.author  FROM items i JOIN biblio b USING (biblionumber) WHERE i.homebranch = "{code}"`
* Extraire une liste contenant les mêmes informations du fichier MARC importé : grâce à l'outil d'export en délimitation tabué de MarcEdit, exporter les `995$f`, `200$a`, `200$f`
* Corriger ensuite la liste de MarcEdit pour que chaque exemplaire possède sa propre ligne dans le fichier : ouvrir le fichier dans Open Refine :
  * Transformer les cellules des colonnes provenant de la `200` avec l'expression GREL `if((value == null).or(value == ""), 'ø', value)` (permet d'éviter des problèmes dans deux étapes)
  * Transformer les cellules de la colonne contenant les données du `995$f` avec l'option _Split multi-valued cells_ utilisant le séparateur `;`
  * Pour toutes les autres colonnes provenant du fichier MARC, transformer les cellules avec l'option _Fill down_
* Importer le fichier provenant de Koha dans un nouveau projet dans Open Refine
* Dans le projet original (basé sur le fichier MARC), importer les colonnes provenant du fichier de Koha en créant de nouvelles colonnes basées sur celle contenant les données du `995$f` à l'aide de l'expression GREL : `cell.cross("{Nom du Projet du Fichier Koha}", "barcode").cells["{Nom de la Colonne}"].value[0]`
* Réorganiser les colonnes pour mettre cote-à-cote les données
* Filtrer sur la colonne du biblionumber les lignes vides
* Regarder si des lignes ont un biblionumber vide :
  * Si oui, alors ces exemplaires n'ont pas été importés
* Ouvrir une _Text Facet_ sur la colonne des code-barre, puis sélectionner _Facet by choice count_ → augmenter le curseur au-delà de 1.00
* _Sort_ par texte la colonne des code-barres
* Exporter le projet
* Rechercher dans le fichier MARC original, pour chaque code-barre, si les exemplaires sont bien différents ou si ce sont des doublons :
  * Si ce sont les mêmes, ne rien faire
  * S'ils sont différents, importer / créer ceux qui n'ont pas été importés avec un autre code-barre _(nécessite de changer le code-barre physique s'il existe)_