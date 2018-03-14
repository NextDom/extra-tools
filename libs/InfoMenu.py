# -*- coding: utf-8 -*-

import os
import sys

from .BaseMenu import BaseMenu


class InfoMenu(BaseMenu):
    """Classe du menu permettant de modifier les informations du plugin.
    """
    title = 'Modifier les informations du plugin'
    menu = ['Modifier le nom affiché dans les menus',
            'Modifier la description',
            'Modifier la licence',
            'Modifier l\'auteur',
            'Modifier la catégorie']
    categories = [
        'security',
        'automation protocol',
        'programming',
        'organization',
        'weather',
        'communication',
        'devicecommunication',
        'multimedia',
        'wellness',
        'monitoring',
        'health',
        'nature',
        'automatisation',
        'energy'
    ]
    plugin_name = ''
    plugin_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :params plugin_name: Nom du plugin
        :type plugin_name:   str
        """
        if sys.version_info[0] < 3:
            super(InfoMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_path = plugin_path
        self.plugin_name = plugin_name

    def action_1(self):
        """Modifier le nom affiché dans les menus
        """
        name = self.get_user_input('Nouveau nom : ')
        self.replace_info('name', name)
        self.print_success('Le nom du plugin a été modifié')

    def action_2(self):
        """Modifier la description
        """
        description = self.get_user_input('Nouvelle description : ')
        self.replace_info('description', description)
        self.print_success('La description du plugin a été modifiée')

    def action_3(self):
        """Modifier la licence
        """
        licence = self.get_user_input('Nouvelle licence : ')
        self.replace_info('licence', licence)
        self.print_success('La licence du plugin a été modifiée')

    def action_4(self):
        """Modifier l'auteur
        """
        author = self.get_user_input('Nouvel auteur : ')
        self.replace_info('author', author)
        self.print_success('L\'auteur du plugin a été modifié')

    def action_5(self):
        """Modifier la catégorie
        """
        category = self.get_menu_choice(self.categories)
        if category >= 0:
            self.replace_info('category', self.categories[category])
        self.print_success('La catégorie du plugin a été modifiée')

    def replace_info(self, key, new_value):
        """Remplace les informations dans le fichier info.json
        :params key:       Clé à modifier
        :params new_value: Nouvelle valeur de la clé
        :type key:         str
        :type new_value:   str
        """
        self.sed_replace(
            '\("' + key + '" : "\).*\(",\)',
            '\\1' + new_value + '\\2',
            os.path.join(self.plugin_path,
                         'plugin_info',
                         'info.json')
        )
