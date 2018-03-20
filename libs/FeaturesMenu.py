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
        class_file_path = os.path.join(self.plugin_path,
                                       'core',
                                       'class',
                                       self.plugin_name + '.class.php')
        if os.path.exists(class_file_path):
            if not self.check_class(class_file_path, self.plugin_name):
                self.check_and_write_class(class_file_path,
                                           self.plugin_name, 'eqLogic')
                self.print_success(
                    'La classe ' + self.plugin_name + ' a été créée')
            else:
                self.print_error(
                    'La classe ' + self.plugin_name + ' existe déjà')

    def action_2(self):
        """Créer la classe de gestion des commandes
        """
        class_file_path = os.path.join(self.plugin_path,
                                       'core',
                                       'class',
                                       self.plugin_name + '.class.php')
        if os.path.exists(class_file_path):
            if not self.check_class(class_file_path, self.plugin_name):
                self.check_and_write_class(class_file_path,
                                           self.plugin_name + 'Cmd', 'cmd')
                self.print_success('La classe ' + self.plugin_name +
                                   'Cmd a été créée')
            else:
                self.print_error('La classe ' + self.plugin_name +
                                 'Cmd existe déjà')

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

    @staticmethod
    def add_method(method_data):
        """Ajoute la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        if os.path.exists(method_data.class_file_path):
            if FeaturesMenu.check_class(method_data.class_file_path,
                                        method_data.class_name):
                if not FeaturesMenu.check_if_method_exists(
                        method_data.class_file_path,
                        method_data.class_name):
                    result = FeaturesMenu.write_method_in_class(method_data)
                else:
                    BaseMenu.print_error('La méthode existe déjà')
            else:
                BaseMenu.print_error('La classe n\'existe pas')
        else:
            BaseMenu.print_error('Le fichier n\'existe pas')
        return result

    @staticmethod
    def check_class(class_file_path, class_name):
        """Test si la classe existe
        :params class_file_path: Répertoire de la classe
        :params class_name:      Nom de la classe
        :type class_file_path:   str
        :type class_name:        str
        :return:                 True si la classe existe
        :rtype:                  bool
        """
        result = False
        try:
            with open(class_file_path) as file_content:
                if class_name in file_content.read():
                    result = True
        except FileNotFoundError:
            pass
        return result

    @staticmethod
    def check_if_method_exists(class_file_path, method_name):
        """Test si la classe existe
        :params class_file_path: Répertoire de la classe
        :params method_name:     Nom de la méthode
        :type class_file_path:   str
        :type method_name:       str
        :return:                 True si la méthode existe
        :rtype:                  bool
        """
        result = False
        with open(class_file_path) as file_content:
            if method_name in file_content.read():
                result = True
        return result

    def check_and_write_class(self, file_path, class_name, extends=None):
        """Lancer l'écriture d'une nouvelle classe
        :params file_path:  Chemin du fichier devant contenir la classe
        :params class_name: Nom de la classe à créer
        :params extends:    Nom de la classe héritée
        :type file_path:    str
        :type class_name:   str
        :type extends:      str
        """
        if self.write_class(file_path, class_name, extends):
            self.print_success('La classe ' + class_name + ' a été créée')
        else:
            self.print_success('La classe ' + class_name +
                               ' n\'a pas pu être créée')

    @staticmethod
    def write_class(file_path, class_name, extends=None):
        """Ajoute une classe à un fichier PHP
        :params file_path:  Chemin du fichier devant contenir la classe
        :params class_name: Nom de la classe à créer
        :params extends:    Nom de la classe héritée
        :type file_path:    str
        :type class_name:   str
        :type extends:      str
        """
        result = False
        add_php_tag = False
        if not os.path.exists(file_path):
            add_php_tag = True
        with open(file_path, 'a') as php_file:
            if add_php_tag:
                php_file.write('<?php\n')
            class_declaration = '\n\nclass ' + class_name
            if extends is not None:
                class_declaration += ' extends ' + extends + '\n{\n\n}\n'
            php_file.write(class_declaration)
            result = True
        return result

    @staticmethod
    def write_method_in_class(method_data):
        """Ecrit la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        output = []
        bracket_count = 0
        start_bracket_count = False
        method_added = False
        content = None
        class_declaration = 'class ' + method_data.class_name
        try:
            with open(method_data.class_file_path,
                      'r') as class_file_content:
                content = class_file_content.readlines()
            # Recherche de la dernière accolade de la classe
            for line in content:
                if not start_bracket_count and (
                        class_declaration in line or
                        class_declaration == line):
                    start_bracket_count = True
                if not method_added and start_bracket_count:
                    if '{' in line:
                        bracket_count += 1
                    if '}' in line:
                        bracket_count -= 1
                        # Dernière accolade de la classe
                        if bracket_count == 0:
                            output.append(method_data.get_method_func())
                            method_added = True
                output.append(line)
            # Réécrit le fichier
            with open(method_data.class_file_path,
                      'w') as class_file_content:
                for line in output:
                    class_file_content.write(line)
        except FileNotFoundError:
            pass
        return method_added
