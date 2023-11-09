# Complément au fichier de mapping

## Priorité des opérations

* La modification du type de document doit avoir lieu avant de traiter la règle pour l'export Omeka-S

## Informations sur des champs locaux à ArchiRès

* La 099 est unique, toutes les informations déplacées en 099 ne doivent former qu'un seul champ
* La 972 est un champ permettant de conserver le champs le résumé disponible dans la base d'origine
* La 971 est un champ permettant de conserver le type de document dans la base d'origine
* Création du 029$w et existence de 029 :
  * Si aucune 029 n'existe lors de la création du 029$w, en créer une
  * Si une seule 029 existe, ajouter le $w dans celle-ci
  * Si plusieurs 029 existent, ne rajouter le $w qu'à la première 029

## Transformation de la collection (358$a)

Dans la base de données d'origine, l'information de collection et le numéro dans la collection sont fusionnés dans la 358 $a.
Pour essayer de séparer les deux informations, suivre ce protocole :

* Si le premier caractère est `(` et le dernier `)`, les supprimer
* Après cette modification :
  * Si le dernier caractère est un chiffre, remonter vers le premier caractère jusqu'à ce qu'il y ait un autre caractère qu'un chiffre (expression régulière : `\d*$`)
  * une fois ce non-digit caractère atteint, si c'est un espace, atteindre le prochain caractère qui n'est pas un espace (expression régulière `\s*`)
  * si c'est o ou °, regarder si le caractère précédent est un n (expression régulière : `n[o|°]`)
  * si oui, créé un $i à la 225 / 410 avec comme valeur le chiffre / nombre détecté (expression régulière : `n[o|°]\s*(\d*)$`, mettre en $i le contenu du groupe capturé)
  * remonter jusqu'au prochain caractère qui n'est pas un espace (expression régulière : `\s*`)
  * vérifier si ce caractère est une virgule (expression régulière : `[,]?`) :
    * si non, supprimer du 225$a / 410$t toute la partie que l'on vient de remonter
    * si oui, même chose mais en supprimant également cette virgule
  * Doit fonctionner avec l'expression régulière `^(.+?)[,]?\s*n[o|°]\s*(\d*)$` :
    * En cas de match, placer en 225$a le 1er groupe et en 225$i le 2nd groupe
  * Le but est de traiter les numéros qui se trouvent en fin de collections et qui prennent la forme :
    * [titre], no 12
    * [titre] n° 12
    * [titre] n°12
    * etc.

![Illustration](./img/Exemple_Flowchart_Complementaire.svg)