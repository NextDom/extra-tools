# -*- coding: utf-8 -*-
"""
Menu des informations
"""
import os

from .BaseMenu import BaseMenu
from .File import File
from .IO import IO


class InfoMenu(BaseMenu):
    """Classe du menu permettant de modifier les informations du plugin.
    """
    title = 'Modifier les informations du plugin'
    menu = ['Modifier le nom affiché dans les menus',
            'Modifier la description',
            'Modifier la licence',
            'Modifier l\'auteur',
            'Modifier la catégorie']
    plugin_name = ''
    plugin_path = ''
    plugin_info_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :params plugin_name: Nom du plugin
        :type plugin_name:   str
        """
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path
        self.plugin_info_path = os.path.join(plugin_path, 'plugin_info',
                                             'info.json')

    def action_1(self):
        """Modifier le nom affiché dans les menus
        """
        name = IO.get_user_input('Nouveau nom : ')
        BaseMenu.start_script('replace_info_json.py',
                              [self.plugin_name, 'name', name])

    def action_2(self):
        """Modifier la description
        """
        description = IO.get_user_input('Nouvelle description : ')
        BaseMenu.start_script('replace_info_json.py',
                              [self.plugin_name, 'description', description])

    def action_3(self):
        """Modifier la licence
        """
        licence = IO.get_user_input('Nouvelle licence : ')
        BaseMenu.start_script('replace_info_json.py',
                              [self.plugin_name, 'licence', licence])

    def action_4(self):
        """Modifier l'auteur
        """
        author = IO.get_user_input('Nouvel auteur : ')
        BaseMenu.start_script('replace_info_json.py',
                              [self.plugin_name, 'author', author])

    def action_5(self):
        """Modifier la catégorie
        """
        config = File.read_config_data()
        category = IO.get_menu_choice(config['jeedom_categories'],
                                      'Choix de la catégorie')
        if category >= 0:
            BaseMenu.start_script('replace_info_json.py',
                                  [self.plugin_name, 'category',
                                   config['jeedom_categories'][category]])
