# Modifications des fichiers sur le Git de Bokeh 

## Formulaire de recherche avancée (`formulaire → formulaire_prod.php`)

__[Si profil spécifique]__ Ajouter une nouvelle ligne dans le `multiOptions` de `custom_multifacets_bibliotheque` :

``` PHP
                                   '{Code facette}' => ' - {Nom du domaine}' ,
// Où "Nom du domaine" est le nom du domaine du Filtres écoles
// Où "Code facette" est le code facette de la facette dans la facette dynamique "Dans toutes les bibliothèques"
// (Se trouve dans la partie d'administration → Catalogues → Parcourir les codifications → Thesaurus → Dans toutes les bibliothèques)
```

## Réécriture des liens spécifiques (`JS → account-links.js`)

__[Si profil spécifique]__ Ajouter la réécriture des liens vers la page des accès thématiques :

``` JS
            $(".profil_{profil_id Accueil école} a[href='/recherche/simple/id_catalogue/13/id_module/10']").attr('href', "/acces-thematiques-{qualificatif court école}#actu");
            $(".profil_{profil_id Accès thématiques école} a[href='/recherche/simple/id_catalogue/13/id_module/10']").attr('href', "/acces-thematiques-{qualificatif court école}#actu");
            $(".profil_{profil_id FAQ école} a[href='/recherche/simple/id_catalogue/13/id_module/10']").attr('href', "/acces-thematiques-{qualificatif court école}#actu");
// Où "profil_id Accueil école" est l'identifiant de la page d'accueil (idem pour les deux autres)
// (Se trouve dans la partie d'adminsitration → Mise en page → Profils)
// où "Qualificatif court école" lié à "acces-thematiques-" correspond à l'URL de la page des accès thématiques de l'école
// ---------- À REPRODUIRE POUR CHAQUE ANCRE (ici, #actu, faire aussi pour #architecture, etc.) ----------
```

__[Si profil spécifique]__ Ajouter la réécriture des liens vers la FAQ :

``` JS
            $(".profil_{profil_id Accueil école} a[href='/accueil/faq']").attr('href', "/faq-{qualificatif court}");
            $(".profil_{profil_id Accès thématiques école} a[href='/accueil/faq']").attr('href', "/faq-{qualificatif court}");
            $(".profil_{profil_id FAQ école} a[href='/accueil/faq']").attr('href', "/faq-{qualificatif court}");
// Où "profil_id Accueil école" est l'identifiant de la page d'accueil (idem pour les deux autres)
// (Se trouve dans la partie d'adminsitration → Mise en page → Profils)
// où "Qualificatif court école" lié à "acces-thematiques-" correspond à l'URL de la page des accès thématiques de l'école
```

## Mapping des bibliothèques (`JS → bib-mapping.js`)

Ajouter une bibliothèque au mapping des bibliothèques _(probablement facultatif pour les laboratoires)_ :

``` JS
bib_mapping.push(JSON.parse('{"code":"{code site}", "profil":"{profil_id Accueil école}", "priority":{int priorité}, "label":"{Nom public}","ip_ranges":[{"start":"XXX.XXX.XX.X", "end":"XXX.XXX.XXX.XXX"}]}'));
// ---------- L'ORDRE DANS L'ARRAY EST IMPORTANT si plusieurs codes sites partagent le même identifian profil ----------
// En effet, rechercher une bibliothèque par sa propriété "profil" renvoie le premier match dans l'array
// Où "code site" est le code du site dans Koha
// Où "profil_id Accueil école" est l'identifiant de la page d'accueil
// (Se trouve dans la partie d'adminsitration → Mise en page → Profils)
// Où "int priorité" est un int gérant la priorité des affichages, intercaler entre ceux existants en laissant de la marge si possible
// Où "Nom public" est le nom public de la bibliothèque
// Où "ip_ranges" correspond aux IP PUBLIQUES des écoles (pour la reconnaissance IP)
// (pour une IP publiqu unique, la renseigner en dévut et en fin)
```

## Page de pré-inscription (`JS - preregistration.js`)

Selon si la bibliothèque doit apparaître ou non sur le formulaire de pré-inscription, modifier (ou non) le sélecteur CSS :

``` JS
$('select#library_id option:not([label^="ENSA"], [label^="IMVT"], [label^="ENSP V"])').add('select#library_id option[label="ENSA de Marseille"]').remove();
```

## CSS (`CSS → ensa.css`)

__[Si profil spécifique]__ Masquer le bouton de retour à l'école sur la page d'accueil de l'école

``` CSS
.profil_{profil_id Accueil école} a.backtoschool[href*="/{profil_id Accueil école}"] {
    display: none;
}
/* Où "profil_id Accueil école" est l'identifiant de la page d'accueil
(Se trouve dans la partie d'adminsitration → Mise en page → Profils) */
```
