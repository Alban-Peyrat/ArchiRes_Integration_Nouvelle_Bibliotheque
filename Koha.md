# Opérations liées à Koha

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