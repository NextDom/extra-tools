# -*- coding: utf-8 -*-
"""
Menu de l'internationalisation
"""
import sys

from .BaseMenu import BaseMenu


class I18nMenu(BaseMenu):
    """
    Menu de l'internationalisation
    """
    title = 'Gestion des traductions'
    menu = ['Ajouter une traduction',
            'Mettre à jour les fichiers']
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
            super(I18nMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """
        Ajout d'un répertoire pour les traductions
        :return: True si une langue a été rajoutée
        :rtype:  bool
        """
        BaseMenu.start_script('add_language',
                              [self.plugin_path, self.plugin_name])

    def action_2(self):
        """
        Met à jour les traductions
        """
        BaseMenu.start_script('update_languages',
                              [self.plugin_path, self.plugin_name])
