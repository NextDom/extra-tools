# -*- coding: utf-8 -*-

import os
import sys
from BaseMenu import BaseMenu
from MethodData import MethodData


class FonctionnalitiesMenu(BaseMenu):
    """Classe du menu permettant d'ajouter des fonctionnalités.
    """
    title = 'Ajouter des fonctionnalités'
    menu = ['Ajouter la classe générale',
            'Ajouter la classe des commandes',
            'Ajouter une méthode cron']
    plugin_name = ''

    def __init__(self, plugin_name):
        """Constructeur
        """
        if sys.version_info[0] < 3:
            super(FonctionnalitiesMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name

    def action_1(self):
        """Créer la classe principale
        """
        class_file_path = os.path.join('plugin-'+self.plugin_name,
                                       'core',
                                       'class',
                                       self.plugin_name+'.class.php')
        self.start_write_class(class_file_path, self.plugin_name, 'eqLogic')

    def action_2(self):
        """Créer la classe de gestion des commandes
        """
        class_file_path = os.path.join('plugin-'+self.plugin_name,
                                       'core',
                                       'class',
                                       self.plugin_name+'.class.php')
        self.start_write_class(class_file_path, self.plugin_name+'Cmd', 'cmd')

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
                'plugin-'+self.plugin_name,
                'core',
                'class',
                self.plugin_name+'.class.php')
            method_data.class_name = self.plugin_name
            method_data.method_name = crons[keys[choice]]
            method_data.method_is_static = True
            method_data.method_comment = keys[choice]
            if self.add_method(method_data):
                self.print_success('La méthode ' + method_data.method_name +
                                   ' a été ajoutée')

    def add_method(self, method_data):
        """Ajoute la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        if self.check_class_file(method_data):
            if self.check_class(method_data):
                if not self.check_if_method_exists(method_data):
                    result = self.write_method_in_class(method_data)
                else:
                    self.print_error('La méthode existe déjà')
            else:
                self.print_error('La classe n\'existe pas')
        else:
            self.print_error('Le fichier n\'existe pas')
        return result

    def check_class_file(self, method_data):
        """Test si la classe existe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        if os.path.exists(method_data.class_file_path):
            result = True
        return result

    def check_class(self, method_data):
        """Test si la classe existe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        with open(method_data.class_file_path) as file_content:
            if method_data.class_name in file_content.read():
                result = True
        return result

    def check_if_method_exists(self, method_data):
        """Test si la méthode existe déjà
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        with open(method_data.class_file_path) as file_content:
            if method_data.method_name in file_content.read():
                result = True
        return result

    def start_write_class(self, file_path, class_name, extends=None):
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

    def write_class(self, file_path, class_name, extends=None):
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
            class_declaration = '\n\nclass '+class_name
            if extends is not None:
                class_declaration += ' extends ' + extends + '\n{\n\n}\n'
            php_file.write(class_declaration)
            result = True
        return result

    def write_method_in_class(self, method_data):
        """Ecrit la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        output = []
        bracket_count = 0
        start_bracket_count = False
        method_added = False
        content = None
        class_declaration = 'class '+method_data.class_name+' '
        with open(method_data.class_file_path, 'r') as class_file_content:
            content = class_file_content.readlines()
        # Recherche de la dernière accolade de la classe
        for line in content:
            if not start_bracket_count and class_declaration in line:
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
        with open(method_data.class_file_path, 'w') as class_file_content:
            for line in output:
                class_file_content.write(line)
        return method_added
