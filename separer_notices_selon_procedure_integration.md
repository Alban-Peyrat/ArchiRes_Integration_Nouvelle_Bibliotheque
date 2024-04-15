# Séparer les notices selon leur procédure d'intégration

Ouvrir MarcEdit et lancer l'outil d'extraction de notices (_Tools → Select MARC Records → Extract Selected Records_) :

* Sélectionner le fichier MARC à diviser (en bas, _Source MARC File)_
* Modifier _Displayed field_ en `035$a`
* Cliquer sur _Import file_
* Rechercher : `F#:001`
* Cliquer sur _Export Selected_
* Cliquer sur _Oui_ (permet de générer les deux fichiers)
* Appeler le premier fichier `items_only.mrc` (qui contiendra les notices où seule l'exemplarisation est nécessaire)
* Appeler le second fichier `whole_records.mrc` (qui contiendra les notices à entièrement intégrer)