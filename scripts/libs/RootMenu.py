# -*- coding: utf-8 -*-
"""
Menu principal de l'outil.
"""

import os

from .BaseMenu import BaseMenu
from .FeaturesMenu import FeaturesMenu
from .I18nMenu import I18nMenu
from .IO import IO
from .InfoMenu import InfoMenu


class RootMenu(BaseMenu):
    """
    Menu principal de l'outil.
    """
    title = 'Outil de gestion d\'un plugin'
    menu = ['Modifier l\'identifiant du plugin',
            'Modifier les informations du plugin',
            'Ajouter des fonctionnalités',
            'Gestion des traductions']
    plugin_path = ''
    plugin_name = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params plugin_name: Nom du plugin
        :params plugin_path: Chemin du plugin
        :type plugin_name:   str
        :type plugin_path:   str
        """
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Renomme le plugin
        Modifie le nom des répertoires, des fichiers ainsi que le contenu
        des fichiers.
        """
        new_name = IO.get_user_input('Nouveau nom du plugin : ')
        os.system('./scripts/rename_plugin.py "' + self.plugin_path + '" "' +
                  self.plugin_name + '" "' + new_name + '"')
        self.plugin_name = new_name
        self.plugin_path = 'plugin-' + new_name

    def action_2(self):
        """Lance le menu de modification des informations
        """
        info_menu = InfoMenu(self.plugin_path, self.plugin_name)
        info_menu.start()

    def action_3(self):
        """Lance le menu de modification des informations
        """
        features_menu = FeaturesMenu(self.plugin_path, self.plugin_name)
        features_menu.start()

    def action_4(self):
        """Lance le menu de gestion des traductions
        """
        i18n_menu = I18nMenu(self.plugin_path, self.plugin_name)
        i18n_menu.start()
