# Modifications des paramétrages de Matomo

## Objectifs

* Créer un nouvel objectif :
  * Nom de l'objectif : `Nouvelles acquisitions ({nom de l'école})`
  * Description : `Accès à une notice depuis les nouvelles acquisitions`
  * L'objectif est déclenché :
    * _Quand les visiteurs_
    * _Visitent une URL donnée (page ou groupe de pages)_
    * Où le URL
    * _correspond à l'expression_
    * `.*archires\.archi\.fr\/recherche\/viewnotice.*id_catalogue[\/|=]{ID du domaine des nouveautés dans Bokeh}.*`
    * _Autoriser un objectif à être converti plus d'une fois par visite_
* Créer un nouvel objectif :
  * Nom de l'objectif : `Accès rapides ({nom de l'école})`
  * Description : `Clic sur les accès rapides de {nom de l'école}`
  * L'objectif est déclenché :
    * _Manuellement_
    * _Autoriser un objectif à être converti plus d'une fois par visite_
