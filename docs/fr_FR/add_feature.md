# Ajouter une fonctionnalité
## Ajouter un script
Pour ajouter un script, il faut le placer dans le répertoire scripts à la racine.
Ce script doit avoir si possible aucune dépendance afin d'être utilisable que le projet ne nécessite pas l'installation de dépendances.

Une fois le fichier présent, il doit être testé depuis la racine par la commande ./scripts/NOM_DU_SCRIPT.
## Ajouter une option dans un menu
Une fois le script présent, ouvrir le fichier du menu où l'on veut ajouter l'accès à la commande.
```python
class ExempleMenu(BaseMenu):
    """Classe d'exemple.
    """
    title = 'Un menu d\'exemple'
    menu = ['Une première fonctionnalité',
            'Une seconde fonctionnalité']
    plugin_name = ''
    plugin_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :param plugin_path: Répertoire du plugin
        :param plugin_name: Nom du plugin
        :type plugin_path:  str
        :type plugin_name:  str
        """
        if sys.version_info[0] < 3:
            super(ExempleMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Première fonctionnalité qui fait ceci
        """
        BaseMenu.start_script('premier_fonctionnalite.py', [self.plugin_path,
                                                            self.plugin_name])

    def action_2(self):
        """Deuxième fonctionnalité qui fait cela
        """
        BaseMenu.start_script('seconde_fonctionnalite.py', [self.plugin_path,
                                                            self.plugin_name])
```
* Dans le tableau __menu__, ajouter le titre de la fonctionnalité,
* Créer une méthode __action_NUMERO__ et indiquer le script à lancer avec les paramètres nécessaires.

Exemple : 
```python
class ExempleMenu(BaseMenu):
    """Classe d'exemple.
    """
    title = 'Un menu d\'exemple'
    menu = ['Une première fonctionnalité',
            'Une seconde fonctionnalité',
            'Ma nouvelle fonctionnalité']
    plugin_name = ''
    plugin_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :param plugin_path: Répertoire du plugin
        :param plugin_name: Nom du plugin
        :type plugin_path:  str
        :type plugin_name:  str
        """
        if sys.version_info[0] < 3:
            super(ExempleMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Première fonctionnalité qui fait ceci
        """
        BaseMenu.start_script('premier_fonctionnalite.py', [self.plugin_path,
                                                            self.plugin_name])

    def action_2(self):
        """Deuxième fonctionnalité qui fait cela
        """
        BaseMenu.start_script('seconde_fonctionnalite.py', [self.plugin_path,
                                                            self.plugin_name])

    def action_3(self):
        """Deuxième fonctionnalité qui fait cela
        """
        BaseMenu.start_script('ma_nouvelle_fonctionnalité.py', [self.plugin_path,
                                                                self.plugin_name])
```

## Ajouter un menu
Pour ajouter un menu, il faut partir d'une classe d'un menu vide :
```python
class NouveauMenu(BaseMenu):
    """Nouveau menu qui va contenir plein de choses
    """
    title = 'Nouveau menu'
    menu = ['Première chose']

    def __init__(self):
        """Constructeur
        :param plugin_path: Répertoire du plugin
        :param plugin_name: Nom du plugin
        :type plugin_path:  str
        :type plugin_name:  str
        """
        if sys.version_info[0] < 3:
            super(NouveauMenu, self).__init__()
        else:
            super().__init__()

    def action_1(self):
        """Première fonctionnalité qui fait ceci
        """
        BaseMenu.start_script('premiere_chose.py')
``` 
Le fichier devra être enregistré dans le répertoire __scripts/libs__.
Pour l'afficher, il faudra aller dans le code du menu parent.
* Ajouter ```from .NouveauMenu import NouveauMenu``` au début du fichier.
* Ajouter une ligne au tableau __menu__
* Ajouter une action qui appelle le menu 
```python
def action_X(self):
    """Lance le menu
    """
    nouveau_menu = NouveauMenu()
    nouveau_menu.start()
```
