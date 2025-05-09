# Tests list

_Using `Kentika_` as prefix for origin database ID, nothing for target database ID, `ENSP_` as barcode prefix & `V` as city barcode_

* Record `035$a (OCoLC)0000000000` : no error & nothing happening
* Record n°2 :
  * No `001` or `035` : error `NO_RECORD_ID`
* Record n°3 :
  * No `001`,  `035` without `$a` : error `NO_RECORD_ID`
* Record `035 $a(OCoLC)0000000010` : no error on the ID retrieval
* Record `001  000000100` :
  * `035$aENSP10009` : `001` replaced with `535587`
  * `995$f` equals only the prefix : `995$fENSP_AV10009I0`
* Record `001  000000101` :
  * `001` present : `001` removed
  * `995` with multiples `$f` : error `TOO_MUCH_BARCODES`
* Record `035$a ENSP75625` :
  * `035$a ENSP75625` : `001` added with `493179`
  * 3 `995`, the first has no `$f` the second one is OK, the 3rd has only the prefix : first `995` has `$fENSP_AV00001I0`, second did not change, third has `$fENSP_AV00001I2`
* Record `035$a ENSP80000` :
  * `035$a ENSP80000` : record is deleted
* Record `035$a ENSP80001` :
  * `035$a ENSP80001` : record is deleted with a warning saying it was matched with biblbionomber `650000`