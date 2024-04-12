# Modifications des paramétrages de Bokeh 

## Dans l'interface d'administration

### Exporateur de fichiers

* __[Si profil spécifique]__ Dans le sous-dossier _bannieres_, téléverser le logo de l'école
* Dans le sous-dossier _photobib_ (utilsier la recherche), téléverser une illustration de la bibliothèque

### Champs personnalisés

Ajouter les liens vers le site des bibliothèques et le profil si nécessaire (voir `ArchiRes_Structure_Technique / Bokeh / champs_personnalises.md`), copie du contenu au 2024-04-10 :

* _Dans Bibliothèques → Tags bibliothèques_
* Lien vers le site de la bibliothèque : `<a href="{page dédiée à la bibliothèque du site de l'école}" target="_blank"> Consulter le site de la bibliothèque de {ville}</a>`
* __[Si profil spécifique]__ Lien vers le profil ArchiRès : `<a href="/{URL profil}"> visiter la page ArchiRès de la bibliothèque</a>`

### Lieux

Ajouter autant de lieux que nécessaire (si nécessaire, un laboratoire situé au sein d'une école n'a pas a donné lieu à un nouveau _lieu_).

_Gestionnaire de contenu → Lieux → Creér un lieu_ :

* Libellé : _Nom de l'école_
* Site web : _Site web de l'école_
* Téléphone : _Téléphone de contact, peut être vide_ 
* E-Mail : _E-Mail de contact, peut être vide_
* Adresse : _Adresse, peut être sur plusieurs lignes_
* Code postal : _Code postal_
* Ville : _Ville_
* Pays : _Pays, en majuscule_
* Latitude : _Latitude_
* Longitude : _Longitude_

### Bibliothèques

Ajouter autant de bibliothèques que de sites Koha ont été créés.

_Administration du portail → Bibliothèques → Ajouter une bibliothèque_ :

* Onglet _Bibliothèque_ :
    * Nom : _Nom de la bibliothèque, pour une école, on mettre le nom de l'école_
    * URL personnalisée : _En miniscule, utiliser le nom du lieu de l'école, en cas de doublon, rajouter un préfixe aux nouveaux arrivants (exemple : `pay-versailles`). Peut être laisser si non pertinent_ 
    * Photo : _illustration, déposée dans `/userfiles/photobib`_
* Onglet _Lieu_ :
    * Lieu : _Lieu précédemment défini ou déjà existant s'il n'était pas pertinent d'en créer un nouveau)_
* Onglet _Adresse_ :
    * Adresse : _Adresse de la bibliothèque, peut être sur plusieurs lignes_
    * Code postal : _Code postal_
    * Ville : _Ville_
    * Téléphone : _Téléphone de la bibliothèque, voir le site configuré dans Koha_
    * Mail : _Adresse email de la bibliothèque, voir le site configuré dans Koha_
* Onglet _Informations_ :
  * Inscription : _à remplir en lien / par l'équipe de la bibliothèque_
  * Prêt : _à remplir en lien / par l'équipe de la bibliothèque_
  * Fonds : _à remplir en lien / par l'équipe de la bibliothèque_
* Onglet _Territoire_ :
  * Territoire : _ArchiRès_
* Onglet _Configuration_ :
  * Statut de la bib : `Envoie des données`
  * Interdire les réservations : _Non_
* Onglet _Champs personnalisés_ :
  * Matériauthèque : _à remplir en lien / par l'équipe de la bibliothèque_
  * Fonds spécifique : _à remplir en lien / par l'équipe de la bibliothèque_
  * Services : _à remplir en lien / par l'équipe de la bibliothèque_
  * Laboratoires de recherche : _à remplir en lien / par l'équipe de la bibliothèque_
  *  Site Web à remplir : _à remplir en lien / par l'équipe de la bibliothèque_
  * Tags bibliothèque : sélectionner le tag pointant sur le site de la bibliothèque puis celui pointant vers le profil ArchiRès pertinent

Une fois validées, sur la page listant les bibliothèques, remplir les plages d'ouvertures en lien / par l'équipe de la bibliothèque.

### Articles

* Dans la catégorie portant le nom de la bibliothèque, attribuer les deux permissions aux _Admin bib_
* Créer quatre sous-dossiers à cette catégorie :
  * __[Si profil spécifique]__ _Accueil_
  * _Actualités_
  * _Actualités : réseau_
  * _FAQ_
* __[Si profil spécifique]__ Créer un article dans le sous-dossier _Accueil_ :
  * Onglet _Publication_ :
    * Titre : _Accès rapides_
  * Onglet _Article_ :
    * Cliquez sur _Source_
    * Coller l'accès rapide (voir l'utilitaire dans RESANA)


### Article d'aide à l'activation de son compte

* _Modifier l'article à la source (`ArchiRes_Structure_Techinque → Bokeh → Articles → HTML_files → infos_compte → inscrits_ensa.html`) puis appliquer les changements sur l'article en production_
* Ajouter les identifiants utilisés dans la partie Javacript de l'article :

``` JS
let ar_userids = { // Dans cette variable
    CODE:"prenom.nom",
};
// Où "CODE" est le code site de Koha
// Où "prenom.nom" est la forme utilisée (voir la variable juste en-dessous ↓)

// ----- Si la forme utilisé n'existe pas déjà, rajouter un exemple -----
let ar_userid_examples = {
    "prenom.nom":"louise.valliere"
};
```

* Modifier l'article _Portail → Infos-compte → inscrits_ensa_ :
  * Cliquez sur _Source_
  * Coller le contenu du fichier HTML qui vient d'être modifié

### Domaines

* __[Si profil spécifique]__ Dans _Portail → Filtre écoles_, ajouter un sous-domaine :
  * Libellé : ` - {libellé public}` __(il y a un espace avant le tiret)__
  * Onglet _Localisations_ → __Bibliothèques__ : ajouter la bibliothèque (et d'autres si nécessaires)
  * Onglet _Autres_ → _Peut être un favori utilisateur_ : _Oui_
* Dans _Portail → Filtre écoles_, modifier _Catalogue commun des ENSA_ :
  * Localisations → __Annexes__ : rajouter la bibliothèque (et d'autres si nécessaires)
* Pour le dossier de la bibliothèque, créer un nouveau domaine :
  * Libellé : `Nouvelles acquisitions`
  * Copier les paramètres des domaines des nouveautés (voir `ArchiRes_Structure_Technique / Bokeh / nouveautes.md`), copie du contenu au 2024-03-29 :
    * Formulaire personnalisé : _AlP_Domain_Nouveautes_
    * Année de parution >= : __2023__ (année à modifier selon l'année)
    * Nouveauté uniquement : __OUI__
    * Bibliothèques :
      * profil commun : les 17 écoles
      * profil école : la bibliothèque concernée
    * Tous les types de documents __sauf__ :
      * Article de revue
      * articles du portail
      * non identifié
      * Ancien travaux étudiants
    * Multi axes :
      * __ET__ Etat Exemplaire __Empruntable__
      * __OU__ Etat Exemplaire __Exclu du prêt__
      * __OU__ Etat Exemplaire __Consultable en ligne__
      * __OU__ Etat Exemplaire __Consultable sur place__

### Facettes dynamiques

_Rappel : elles se définissent dans l'entrée de menu_ Domaines

* __[Si profil spécifique]__ Modifier _Dans toutes les bibliothèques_ et ajouter au bon emplacement le domaine qui a été ajouté à _Portail → Filtres écoles_

### Profil

Modifier la page d'accueil du profil général :

* Ajouter dans la boîte d'articles _Actualités du réseau_ le dossier des actualités du réseau de la bibliothèque
* Modifier la liste des bibliothèques affichées dans la boîte des bibliothèques _La bibliothèque Accès & Horaires d'Ouverture_ pour y rajouter la bibliothèque

Configurer le menu du profil général, spécifiquement le _Menu principal_ :

* Ajouter au sous menu _Réseau ArchiRès → Les bibliothèques des ENSAP_ un lien vers un site
* Modifier le nouveau lien :
  * Texte du lien : `{libellé publique de l'école}`
  * Adresse web : `/{URL personnalisée de la bibliothèque}`
  * Navigation : `Rester sur le même onglet`

__[Si profil spécifique]__ Dupliquer le profil de l'ENSA de Bretagne :

* Libellé : `{libellé publique de l'école}`
* URL du profil : `{nom de l'école séparés avec des tirets (sauf lavillette et valdeseine)}`
* Onglet _Filtrage du contenu_ :
  * __Si version simple__ : sélectionner dans les _Sites (annexes)_ la(es) bibliothèque(s) et _Tous sites_
  * __Si cas complexe__ : sélectionner le domaine créés pouvant êtr favori des utilisateurs
* Onglet _Adminsitration_ :
  * Email du webmestre : _Adresse email de la bibliothèque, voir le site configuré dans Koha_
* Onglet _Affichage_ :
  * Vérifier que le CSS soit correctement `/userfiles/css/profil_ecole.css`

Modifier la page d'accueil du nouveau profil :

* Modifier la boîte de recherche _Trouver un document_ :
  * Onglet _Sélection_ :
    * Retirer le domaine _Filtre écoles / ENSA Bretagne_
    * Rajouter le filtre école pertinent
* Modifier la boite image _Logo Ecole_ :
  * Onglet _Sélection_ :
    * Sélectionner une image : `/userfiles/bannieres/{logo de l'école}`
    * Lien de l'image : `/{URL du profil}`
* Modifier la boite de notices _Nouvelles acquisition de l'ENSA de Bretagne_ :
  * Titre : `Nouvelles acquisition de l'{école}`
  * Onglet _Sélection_ :
    * Sélection : les nouvelles acquisitions de l'école
* Modifier la boite de notices _Actualités_ :
  * Onglet _Sélection_ :
    * Supprimer les _Actualités_ et _Actualités : Réseau_ __de l'ENSA de Bretagne__
    * Rajouter les _Actualités_ et _Actualités : Réseau_ de l'école
* Modifier la boîtes des bibliothèques :
  * Onglet _Sélection_ :
    * Bibliothèque affichée : uniquement l'école
* Modifier la boite d'articles _FAQ_ :
  * Supprimer le dossier _FAQ_ __de l'ENSA de Bretagne__
  * Rajouter le dossier _FAQ_ de l'école

Modifier la page _FAQ - Bretagne_ du nouveau profil :

* Libellé : `FAQ - {qualificatif court}`
* URL de la page : `faq-{qualificatif court}`
* __Valider__ (sinon les modifications ne seront pas enregistrées)
* Modifier la boîte d'articles _FAQ_ :
  * Supprimer le dossier _FAQ_ __de l'ENSA de Bretagne__
  * Rajouter le dossier _FAQ_ de l'école

Modifier la page _Accès Thématiques - Bretagne_ du nouveau profil :

* Libellé : `Accès Thématiques - {qualificatif court}`
* URL de la page : `acces-thematiques-{qualificatif court}`

### Comptes contributeurs

* Créer des comptes contibuteurs pour les professionnels qui en auront le besoin (voir `ArchiRes_Structure_Technique / Gestion_comptes / role_et_droits / Bokeh_comptes_professionnels.md`), copie du contenu au 2024-04-10 :
  * Onglet Droits :
    * Niveau d'accès = `Administrateur bibliothèque`
    * Bibliothèque = la bibliothèque du contributeur
    * Groupes : se rempliront automatiquement de :
      * `Admin Bib` (_Groupes → Droits d'accès aux articles_)
      * `Administrateur bibliothèque` (_Groupes → Accès aux lettres d'informations_)

## Dans le Cosmogramme

### Annexes

Ajouter autant d'annexes que de sites Koha ont été créés.

_Configuration → Annexes → Ajouter une annexe_ :

* Bibliothèque : _Nom de la "Bibliothèque" définie dans la partie administration_
* Code SIGB : `{branchcode de Koha}`
* Libellé : _Nom public de la bibliothèque_
* Rejeter les exemplaires : _Ø_
* Exclu du PEB : _Ø_
