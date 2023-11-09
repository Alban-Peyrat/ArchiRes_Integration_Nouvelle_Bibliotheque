# Intégration de nouvelles bibliothèque au sein du réseau ArchiRès

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

Ce dépôt formalise les différentes étapes pour intégrer une nouvelle bibliothèque au sein du réseau ArchiRès et met à disposition des outils, procédures génériques ou liens vers des outils utilisables.

## Règles générales

Penser à toujours garder des traces de ce qui est fait : dans l'idéal, créer un dépôt spécifique pour cette itnégration, dans lequel seront intégrés les fichiers tels que les mappings, les procédures de modification, les logs de modifications, etc.
Par ailleurs, écrire le nombres de documents concernés, modifiés, importés, etc. tout au long des procédures permet d'identifier plus précisément la source des erreurs.

Il est important de vite déterminer les volumes concernés ainsi que les données concernées pour anticiper au mieux les délais.
Une attention particulière est à porter sur les ressources numériques qu'il faudrait intégrer à Omeka-S.

Afin d'être le plus claire possible, ne pas hésiter à doubler des explications textuelles par des diagrammes, parfois en deux versions : une version détaillée complétée par une version simple pour des interlocuteurs qui n'ont pas les compétences techniques ou les connaissances requises pour comprendre la version originale.


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
