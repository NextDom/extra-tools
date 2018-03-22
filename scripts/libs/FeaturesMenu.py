# -*- coding: utf-8 -*-
"""
Menu des fonctionnalités
"""
import os
import sys

from .BaseMenu import BaseMenu
from .MethodData import MethodData


class FeaturesMenu(BaseMenu):
    """Classe du menu permettant d'ajouter des fonctionnalités.
    """
    title = 'Ajouter des fonctionnalités'
    menu = ['Ajouter la classe générale',
            'Ajouter la classe des commandes',
            'Ajouter une méthode cron',
            'Ajouter la réponse aux requêtes Ajax']
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
            super(FeaturesMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Créer la classe principale
        """
        os.system('./scripts/add_core_class.py ' + self.plugin_path + ' '
                                                                      '' +
                  self.plugin_name)

    def action_2(self):
        """Créer la classe de gestion des commandes
        """
        os.system('./scripts/add_cmd_class.py ' + self.plugin_path + ' '
                                                                     '' +
                  self.plugin_name)

    def action_3(self):
        """Modifier le nom affiché dans les menus
        """
        crons = {
            'Toutes les minutes': 'cron',
            'Toutes les 5 minutes': 'cron5',
            'Toutes les 15 minutes': 'cron15',
            'Toutes les 30 minutes': 'cron30',
            'Toutes les heures': 'cronHourly',
            'Tous les jours': 'cronDaily'
        }
        keys = crons.keys()
        choice = self.get_menu_choice(keys)
        if choice >= 0:
            method_data = MethodData()
            method_data.class_file_path = os.path.join(
                self.plugin_path,
                'core',
                'class',
                self.plugin_name + '.class.php')
            method_data.class_name = self.plugin_name
            method_data.method_name = crons[keys[choice]]
            method_data.method_is_static = True
            method_data.method_comment = keys[choice]
            if FeaturesMenu.add_method(method_data):
                self.print_success('La méthode ' + method_data.method_name +
                                   ' a été ajoutée')

    def action_4(self):
        """Créer la classe de gestion des requêtes Ajax
        """
        directory_path = os.path.join(self.plugin_path,
                                      'core',
                                      'ajax')
        class_file_path = os.path.join(self.plugin_path,
                                       'core',
                                       'ajax',
                                       self.plugin_name + '.ajax.php')
        add_content = True
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        if os.path.exists(class_file_path):
            if BaseMenu.is_content_in_file(class_file_path, 'ajax::init()'):
                self.print_error('Le fichier existe déjà')
                add_content = False
        if add_content:
            with open(class_file_path, 'a') as dest:
                dest.write(BaseMenu.php_header)
                dest.write('try {\n')
                for line in BaseMenu.php_check_user_connect.split('\n'):
                    dest.write('    ' + line + '\n')
                dest.write('\n    ajax::init();\n')
                dest.write(
                    "    throw new \\Exception(__('Aucune méthode "
                    "correspondante à : ', __FILE__) . init('action'));\n/*   "
                    "  * *********Catch exeption*************** */\n} catch ("
                    "\\Exception $e) {\n    ajax::error(displayException($e), "
                    "$e->getCode());\n}")
