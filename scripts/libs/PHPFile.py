# -*- coding: utf-8 -*-
"""
Librairie pour la gestion des entrées sorties
"""

import os

from .IO import IO


class PHPFile(object):
    @staticmethod
    def add_line_under(core_file, needle, line_to_add):
        result = False
        lines = []
        with open(core_file, 'r') as core_file_content:
            lines = core_file_content.readlines()
        output = []
        for line in lines:
            output.append(line)
            if needle in line and not result:
                output.append(line_to_add)
                result = True
        with open(core_file, 'w') as core_file_content:
            for line in output:
                core_file_content.write(line)
        return result

    @staticmethod
    def add_method(method_data):
        """Ajoute la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        if os.path.exists(method_data.class_file_path):
            if PHPFile.check_class(method_data.class_file_path,
                                   method_data.class_name):
                if not PHPFile.check_if_method_exists(
                        method_data.class_file_path,
                        method_data.method_name):
                    result = PHPFile.write_method_in_class(method_data)
                else:
                    IO.print_error('La méthode existe déjà')
            else:
                IO.print_error('La classe n\'existe pas')
        else:
            IO.print_error('Le fichier n\'existe pas')
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
            if method_name + '()' in file_content.read():
                result = True
        return result

    @staticmethod
    def check_and_write_class(file_path, class_name, extends=None):
        """Lancer l'écriture d'une nouvelle classe
        :params file_path:  Chemin du fichier devant contenir la classe
        :params class_name: Nom de la classe à créer
        :params extends:    Nom de la classe héritée
        :type file_path:    str
        :type class_name:   str
        :type extends:      str
        """
        if PHPFile.write_class(file_path, class_name, extends):
            IO.print_success('La classe ' + class_name + ' a été créée')
        else:
            IO.print_success('La classe ' + class_name +
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
