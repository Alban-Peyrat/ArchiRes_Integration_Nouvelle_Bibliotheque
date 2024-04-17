# Tests pour la correction des données

## Tests sur les corrections à apporter au lot

* `Kentika_ENSP75109` :
  * Type de document ArchiRès = `REV` : doit se trouver dans le fichier _SKIPPED_
* `Kentika_ENSP2576` :
  * Type de document ArchiRès = `Chapitre` : doit se trouver dans le fichier _SKIPPED_
* `Kentika_ENSP2675` :
  * Plusieurs 099 : elles doivent être fusionnées en une seule
  * `100$a` au format incorrect : doit être correcte sur toutes les positions __et__ comporter une date 1
  * 101 : indicateurs doivent être 0 et vide
  * Plusieurs 181 : elles doivent être fusionnées
  * Sous champs `6` et `2` manquant en 182 : doivent être rajoutés
  * Plusieurs 183 : elles doivent être fusionnées
  * 615 avec seulement un $a : doit avoir un `$2` ajouté
  * 615 avec seulement un $2 : doit être supprimés
  * 615 avec `$2` → `$a` : `$a` doit être avant le `$2`
  * 700 avec un $4 en début de champ : `$a` doit être devant `$4`
  * 972 avec uniquement un `$9` : doit être supprimé
* `Kentika_ENSP247` :
  * `100$a` : les deux dates doivent être vides
  * `701` avec plusieurs `$a` et `$4` (le même) : 5 `701` attendue, toutes avec un `$4070` et `_1` en indicateur
  * `330` est là : doit être là
  * `972` est là : doit être là
* `Kentika_ENSP75921` :
  * `101$a` pas à la norme (un des deux) : doit comporter deux `$a`,  `cat` et `und`
  * `225` est là : doit être là
  * `410` est là : doit être là
* `Kentika_ENSP6675` :
  * `214$d` égal `0` : plus de `214$d`
  * Plusieurs exemplaires en `995` : 1 `995` par exemplaire
* `Kentika_ENSP61129` :
  * `225$a` uniquement avec des espaces : plus de 225
  * `410$t` uniquement avec des espaces : plus de 410
* `Kentika_ENSP49147` :
  * `029` avec une année en 214$d, le type de document Kentika "Tpfe", un numéro de notice Kentika :
    * Génération des indicateurs vides
    * Génération du $a `FR`
    * Génération du $m avec une année, `TPFE`, 2x ENSP et un numéro
  * `328` avec 214$c et $d et type de document Kentika "Tpfe" :
    * Génération des indicateurs vide puis 0
    * Génération du $b "Tpfe"
    * Génération du $c "Paysage"
    * Génération du $e avec le contenu du 214$c (tout en majuscule)
    * Génération du $d avec une date
    * Les sous-champs sont dans cet ordre
  * `330$a` uniquement avec des espaces : plus de 330
  * 700 : les indicateurs doivent être vide et 1
  * `972$a` uniquement avec des espaces : plus de 972
* `Kentika_ENSP323` :
  * Plusieurs 463 : doivent être fusionnées
  * `463` : le `$t` doit être avant le `$x`
  * 710 : les indicateurs doivent être 0 et 2
* `Kentika_ENSP50` : Pluseierus items fusionnés : 2 items
* `Kentika_ENSP351` : Pluseierus items fusionnés : 5 items
* `Kentika_ENSP76759` : `029` avec _Atelier régional_ : une 029 `TATE`
* `Kentika_ENSP1175` : `029` avec _CESP_ : une 029 `CESP`
* `Kentika_ENSP74521` : `029` avec _Dep_ : une 029 `PFE`
* `Kentika_ENSP426` : `029` avec _Mémoire_ : une 029 `MEMU`
* `Kentika_ENSP72545` : `029` avec _Memoire ENSP_ : une 029 `MES`
* `Kentika_ENSP271` : `029` avec _Mémoire ENSP_ : une 029 `MES`
* `Kentika_ENSP76792` : `029` avec _Thèse_ : une 029 `THES`
* `Kentika_ENSP816` : `029` avec _tpfe_ : une 029 `TPFE`
* `Kentika_ENSP26547` :
  * `029` Pas de date : `029` avec 9999 en date
  * `328` pas de date : `328` avec `[s. d.]` en date
* `Kentika_ENSP20640` : `328` pas de 214$c : `328$e` avec _École nationale supérieure de paysage_
* `Kentika_ENSPFICTIF000` : `029` avec _Travaux d'atelier_ : une 029 `TATE`
* `Kentika_ENSPFICTIF001` : `029` avec une valeur non mappée : une 029 `TATE`
* `Kentika_ENSP72793` :
  * Une `700` et une `710`: la `700` reste en `700`, la `710` devient `711`
  * Plusieurs $a en 711 : 3 `711$4070` attendues à partir de ce champs, donc 4 au total avec la `710` qui passe en `711`
  * Plusieurs $u dans la `856` : deux `856`, chaucne avec son $u
* `Kentika_ENSP42` : une `701` sans `7X0` : une `700` avec 2 `701` (split)
* `Kentika_ENSP9204` :  une `711` sans `7X0` : une `710` abvec une `711` (split)

## Tests des effets de bord du script

* `Kentika_ENSPFICTIF100` :
  * `192$c` vide : plus de 192 (suppression du $c vide, puis suppression de la 192 vide)
  * `194` sans sous-champs : plus de 194
  * `345$a` vide : une `330` avec unqiuement un `$2`
* `Kentika_ENSPFICTIF101` : 4 `099` dont 2 $t : erreur `TOO_MUCH_099`
* `Kentika_ENSPFICTIF102` : Numéro Kentika en `036` : erreur `NO_KENTIKA_NB`
* `Kentika_ENSPFICTIF103` : Pas de `099$t` (type de documetn ArchiRès) : erreur `NO_ARCHIRES_DOCTYPE`
* `Kentika_ENSPFICTIF104` : Pas de `100` : erreur `NO_100`
* `Kentika_ENSPFICTIF105` : Pas de `100$a` : erreur `NO_100_A`
* `Kentika_ENSPFICTIF106` :
  * `210/4` avec beaucoup de dates, ertaines au format incorrectes : dates en `100$a` doivent être `10129999` (plus petite dans la 210, plus grande en 214, d'autres valeurs valides intermédiaires, des valeurs trop petites ou trop longues à ignorer)
* `Kentika_ENSPFICTIF107` : Pas de `971` : erreur `NO_971`
* `Kentika_ENSPFICTIF108` : Pas de `971$a` : erreur `NO_KENTIKA_DOCTYPE`
* `Kentika_ENSPFICTIF109` : Pas de `101` : erreur `NO_101`
* `Kentika_ENSPFICTIF110` : Pas de `101$a` : erreur `NO_101_A`
* `Kentika_ENSPFICTIF111` :
  * `101$c` commençant par 2 espaces + `fre` : devient `$cfre`
  * `101$c` = `francais` : devient `$cund`
  * `101$c` = `FR` : devient `$cund`
  * `101$c` = `ENG` : devient `$cund`
  * 2 `182` : une seule 182 avec des `$62cz`
  * `182` avec `$6` & `$2` = `null` : pas de nouveau `$6` ou `$2`
  * 2 `200` : une seule `200` avec 2 `$a`, 1 `$e` et 1 `$f`
  * `210` sans `$d` : doit être conservée
  * `214` sans `$d` : doit être conservée
  * `214` avec `$d` = 4 espaces puis 0 : $d doit êter supprimé, `$aPekin` doit rester
  * `225` sans `$a` : doit être supprimée
  * `330` sans `$a` (`$fTimid Gaid`) : doit être supprimée
  * `410` sans `$t` : doit être supprimée
  * `463` avec plsuieurs `$t` : dovient être séparées, une par `$t`, toutes avec le `$x0123-4567`
  * `700` avec plusieurs `$a` : doivent être séparés, une `70X$4999` doit être avec `ROSE (Summer)`, l'autre avec `BRANWEN (Qrow)`
  * `701` avec plusieurs `$a` et plusieurs `$4` : doivent être séparés, une `701$aROSE (Ruby)$4070` et l'autre `701$aSHCNEE (Winter)$4651`
  * `711` avec plusieurs `$a`, mais pas assez de `$4` : doivent être spéarées avec `711$aDe La Vallière Louise$4730`, `711$aMARGA (Alice)$4952` et `711$aKIRI (Marisa)$4730`
  * `972` sans `$a` (`$fAn ordeal`) : doit être supprimé
  * `995` avec plusieurs `$k` : deux `995` identique sauf le `$k`
  * `615` après la `995` : toute la notice doit être réordonnée, donc elle doit se trouver avec l'autre `615`
* `Kentika_ENSPFICTIF112` :
  * `700` & `711` have only spaces as `$a` content : doivent être supprimées
  * `701` & `710` n'ont pas de $a : doivent être supprimées