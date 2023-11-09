# Tests pour le mapping
# Plan de test pour le mapping

* Notice 10001 :
  * Type de document (livre) : 995$hLIV + 075$a0 → 099$tLIV
  * Résumé : 330$a$z → 330$a$z + 972$9NOMBDD$a
  * Mots sujets : 606$x$y → 615$x$y
  * Nombres de prêts : 995$p → _Plus de $p en 995_
  * Export Omeka-S (non) : ø → ø
  * Collection (sans modification) : 358$aLove colored Master Spark → 225$aLove Colored Master Spark
* Notice 10003 :
  * Type de document (ebook) : 995$hLIV + 075$a1 → 099$tELIV
  * Export Omeka-S (oui) : ø → 099$x
  * Collection (parenthèses, virgule, no + espace) : 358$a(Fantasy Seal, n° 155) → 225$aFantasy Seal$i155
* Notice 10005 :
  * Type de document (thèse, sans 029) : 995$hTHESE → 099$tTE + 029$wTHESE
  * Collection (n° sans espace) : 358$aFake Apollo n°569 → 225$aFake Apollo$i569