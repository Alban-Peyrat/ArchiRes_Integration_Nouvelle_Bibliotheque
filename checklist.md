# Listes des points à traiter lors de l'intégration

## Intégration des notices bibliographiques & exemplaires dans Koha

* [] Modifier les données MARC pour une intégration dans ArchiRès (hors `4XX`, code-barres et biblionumbers)
* [] Valider les données MARC pour la base de données ArchiRès
* [] Ajouter les liens aux `4XX` sur les données existantes
* [] Identifier les code-barres déjà présents dans Koha
* [] Alignement des notices via FCR
* [] Génération du fichier d'alignements à partir des fichiers d'analyse de FCR
* [] Générer les code-barres fictifs et ajouter les biblionumbers aux notices
* [] Générer le fichier CSV des exemplaires
* [] Identifier à nouveau si des code-barres sont déjà présents dans Koha
* [] Intégrer les nouvelles notices bibliographiques
* [] Exemplariser les documents déjà présents dans Koha
* [] Vérifier que tout s'est correctement déroulé
* [] _Facultatif_ Modifier les notices avec des `4XX` non liées

## Configuration de Matomo

* [] __[Si profil spécifique]__ Créer l'objectif pour les nouvelles acquisitions
* [] __[Si profil spécifique]__ Créer l'objectif pour les accès rapides
* [] __[Si profil spécifique]__ Ajouter l'identifiant de l'objectif des accès rapides à la liste dans la documentation des accès rapides et dans la macro pour l'utilitaire (`ArchiRès_Structure_Technique / Bokeh / articles / acces_rapides.md`)

## Configuration de RESANA

* [] __[Si profil spécifique]__ modifier macro + créer feuille

## Configuration de Bokeh

### Partie Administration

* [] Explorateur de fichiers :
  * [] __[Si profil spécifique]__ Téléverser le logo de l'école
  * [] Téléverser une illustration de la bibliothèque
* [] Champs personnalisés :
  * [] Créer le _Tag bibliothèque_ qui renvoie sur le site de la bibliothèque
  * [] __[Si profil spécifique]__ Créer le _Tag bibliothèque_ qui renvoie sur le profil de l'école
* [] Lieux :
  * [] Ajouter les lieux nécessaires _(non pertinent dans le cas d'un laboratoire par exemple)_
* [] Bibliothèques :
  * [] Ajouter autant de bibliothèques que de lieux dans Koha
  * [] Remplir les plages d'ouverture
* [] Articles :
  * [] Attribuer les permissions aux _Admin bib_ pour le dossier de l'école
  * [] Créer les sous-dossiers
  * [] __[Si profil spécifique]__ Créer l'article des accès rapides
  * [] Modifier l'article sur comment se connecter à ArchiRès dans `ArchiRes_Structure_Technique`
  * [] Modifier sur Bokeh l'article sur comment se connecter à ArchiRès dans `ArchiRes_Structure_Technique`
* [] Domaines :
  * [] __[Si profil spécifique]__ Creér le domaine dans _Portail → Filtres écoles_
  * [] Modifier le domaine _Catalogue commun des ENSA_
  * [] Créer le domaine des nouveautés pour chaque bibliothèque
* [] Facettes dynamiques :
  * [] __[Si profil spécifique]__ Ajouter le domaine _Portail → Filtres écoles_ à la facette _Dans toutes les bibliothèques_
* [] Profil :
  * [] Profil général : Ajouter les articles réseau de la biblitohèques aux _Actualités du réseau_
  * [] Profil général : Ajouter la bibliothèque aux bibliothèques affichées dans les _Informations pratiques_
  * [] Profil général : Ajouter un lien vers la page d'information de la bibliothèque dans le menu listant les bibliothèques des ENSAP
  * [] __[Si profil spécifique]__ Dupliquer un profil école
  * [] __[Si profil spécifique]__ Profil école : Modifier la page d'accueil
  * [] __[Si profil spécifique]__ Profil école : Modifier la page de FAQ
  * [] __[Si profil spécifique]__ Profil école : Modifier la page des accès thématiques
* [] Comptes :
  * [] Créer des comptes contributeurs

### Partie Cosmogramme

* [] Ajouter autant d'annexes que de sites Koha

## Configuration du Git de Bokeh

* [] __[Si profil spécifique]__ Ajouter la facette au sélecteur des catalogues dans le formulaire de recherche avancée
* [] __[Si profil spécifique]__ Ajouter la réécriture des liens vers les accès thématiques de l'école
* [] __[Si profil spécifique]__ Ajouter la réécriture des liens vers la FAQ de l'école
* [] Ajouter une bibliothèque au mapping des bibliothèques _(probablement facultatif pour les laboratoires)_
* [] Vérifier & modifier si nécessaire le sélecteur CSS pour le formulaire de pré-inscription
* [] __[Si profil spécifique]__ Masquer le bouton de retour à l'école sur la page d'accueil de l'école
