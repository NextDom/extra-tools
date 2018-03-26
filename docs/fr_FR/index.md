# Documentation
Extra-tools est une agrégation de scripts pour faciliter la modification des plugins.

## Utilisation
__./tools.py__ permet de lancer l'ensemble des scripts grâce à un menu en ligne de commande.

Chaque script se trouve dans le répertoire __scripts__ et peut être lancé indépendamment.

## Description des fonctionnalités
L'arborescence complète de ce menu peut être trouvée [ici](https://github.com/Jeedom-Plugins-Extra/extra-tools/blob/master/docs/fr_FR/features_tree.md) 

### Menu d'accueil
#### Lancer l'assistant
Générer un squelette de plugin à partir de questions préliminaires.
#### Télécharger le plugin-Template
Télécharger le plugin-Template pour le modifier par la suite.
#### Modifier les plugins présents
Permet d'accéder au menu principal permettant de modifier le plugin sélectionné.

### Menu principal
#### Modifier l'identifiant du plugin
Renomme le plugin et tous les fichiers associés
#### Modifications les informations du plugin
Modifier les informations du fichier __plugin-info/info.json__

#### Ajouter des fonctionnalités au plugin
##### Ajouter la classe générale
Création du fichier __core/class/PluginId.class.php__.
##### Ajouter la classe des commandes
Création d'une classe se trouvant par défaut dans __core/class/pluginId.class.php__ ou __core/class/pluginCmd.class.php__.
##### Ajouter la fonctionnalité cron
Ajout de méthodes appelées à des intervales prédéfinis.
##### Ajouter la réponse aux requêtes Ajax
Création du fichier __core/ajax/PluginId.ajax.php__

#### Gestion des traductions
##### Ajouter une traduction
Ajoute une langue et ajoute les chaines de caractères trouvées.
##### Mettre à jour les fichiers
Met à jour l'ensemble des fichiers de traduction en ajoutant les chaines de caractères manquantes.

## Ajouter une fonctionnalité
La procédure d'ajout d'une nouvelle fonctionnalité est expliquée [ici](https://github.com/Jeedom-Plugins-Extra/extra-tools/blob/master/docs/fr_FR/add_feature.md)