# -*- coding: utf-8 -*-
"""
Menu principal de l'outil.
"""

import os
import sys

from .BaseMenu import BaseMenu
from .FeaturesMenu import FeaturesMenu
from .InfoMenu import InfoMenu


class RootMenu(BaseMenu):
    """
    Menu principal de l'outil.
    """
    title = 'Outil de gestion d\'un plugin'
    menu = ['Modifier l\'identifiant du plugin',
            'Modifier les informations du plugin',
            'Ajouter des fonctionnalités']
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
        if sys.version_info[0] < 3:
            super(RootMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Renomme le plugin
        Modifie le nom des répertoires, des fichiers ainsi que le contenu
        des fichiers.
        """
        if os.path.exists(self.plugin_path):
            new_name = self.get_user_input('Nouveau nom du plugin : ')
            if 'plugin-' + new_name not in os.listdir('.'):
                # Renomme le répertoire racine du plugin
                os.rename(self.plugin_path, 'plugin-' + new_name)
                # Renomme le contenu du plugin
                self.rename_plugin(
                    'plugin-' + new_name, self.plugin_name, new_name)

                self.print_success('Le plugin ' + self.plugin_name +
                                   ' a été renommé en ' + new_name)
                self.plugin_name = new_name
                self.plugin_path = 'plugin-' + new_name
            else:
                self.print_error('Le répertoire  plugin-' + new_name +
                                 ' existe déjà')
        else:
            self.print_error('Le plugin ' + self.plugin_path +
                             ' n\'a pas été trouvé')

    def action_2(self):
        """Lance le menu de modification des informations
        """
        info_menu = InfoMenu(self.plugin_path, self.plugin_name)
        info_menu.start()

    def action_3(self):
        """Lance le menu de modification des informations
        """
        fonctionnalities_menu = FeaturesMenu(self.plugin_path,
                                             self.plugin_name)
        fonctionnalities_menu.start()

    def rename_plugin(self, current_path, old_name, new_name):
        """Remplace les occurences dans les noms des fichiers, les répertoires,
        et au sein des fichiers
        :param current_path: Répertoire courant
        :param old_name:     Ancien nom
        :param new_name:     Nouveau nom
        :type current_path:  str
        :type old_name:      str
        :type new_name:      str
        """
        core_template_test = 'core' + os.sep + 'template'
        if old_name != '' and new_name != '':
            # Remplacement des occurences dans les noms des fichiers et
            # des répertoires
            for item in os.listdir(current_path):
                item_path = os.path.join(current_path, item)
                # A enlever quand plugin-template sera renommé plugin-Template
                if not item_path.endswith(core_template_test):
                    item = self.rename_item(current_path + os.sep,
                                            item,
                                            old_name,
                                            new_name)
                if os.path.isdir(current_path + os.sep + item):
                    self.rename_plugin(current_path + os.sep + item,
                                       old_name,
                                       new_name)
                else:
                    # Remplacement des occurences dans le fichier
                    self.replace_in_file(
                        current_path + os.sep + item, old_name, new_name)

    def replace_in_file(self, target_file, old_name, new_name):
        """Remplace l'ancien nom par le nouveau
        :param target_file: Fichier à traiter
        :param old_name:    Ancien nom du plugin
        :param new_name:    Nouveau nom du plugin
        :type target_file:  str
        :type old_name:     str
        :type new_name:     str
        """
        self.sed_replace(old_name, new_name, target_file)
        self.sed_replace(old_name.lower(), new_name.lower(), target_file)
        self.sed_replace(old_name.upper(), new_name.upper(), target_file)
        self.sed_replace(old_name.capitalize(),
                         new_name.capitalize(),
                         target_file)

    @staticmethod
    def rename_item(path, item, old_name, new_name):
        """Renomme un élément si besoin
        :param path:     Chemin courant
        :param item:     Fichier à tester
        :param old_name: Ancien nom du plugin
        :param new_name: Nouveau nom du plugin
        :type path:      str
        :type item:      str
        :type old_name:  str
        :type new_name:  str
        :return:         Fichier avec le nouveau nom si il a été renommé
        :rtype:          str
        """
        result = item
        # Cas simple
        if old_name in item:
            result = item.replace(old_name, new_name)
            os.rename(path + item, path + result)
        # En majuscule
        elif old_name.upper() in item:
            result = item.replace(old_name.upper(), new_name.upper())
            os.rename(path + item, path + result)
        # En minuscule
        elif old_name.lower() in item:
            result = item.replace(old_name.lower(), new_name.lower())
            os.rename(path + item, path + result)
        # Avec une majuscule au début
        elif old_name.capitalize() in item:
            result = item.replace(old_name.capitalize(), new_name.capitalize())
            os.rename(path + item, path + result)
        return result
