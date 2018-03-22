# -*- coding: utf-8 -*-
"""
Librairie pour la gestion des entrées sorties
"""

import json
import os
import sys

from .IO import IO


class File(object):
    @staticmethod
    def read_config_data():
        data = {}
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path) as content:
                data = json.load(content)
        except IOError:
            IO.print_error('Le fichier de configuration n\'a pas été trouvé.')
        return data

    @staticmethod
    def sed_replace(regexp, replacement, target_file):
        """Exécute la commande sed sur un fichier
        :params regexp:      Expression régulière
        :params replacement: Chaîne de remplacement
        :params target_file: Fichier cible
        :type regexp:        str
        :type replacement:   str
        :type target_file:   str
        """
        sed_replace_pattern = "sed -i'' 's/{}/{}/g' {} 2> /dev/null"
        if 'darwin' in sys.platform:
            sed_replace_pattern = "sed -i '' 's/{}/{}/g' {} 2> /dev/null"

        os.system(sed_replace_pattern.format(regexp, replacement, target_file))

    @staticmethod
    def replace_in_file(target_file, old_name, new_name):
        """Remplace l'ancien nom par le nouveau
        :param target_file: Fichier à traiter
        :param old_name:    Ancien nom du plugin
        :param new_name:    Nouveau nom du plugin
        :type target_file:  str
        :type old_name:     str
        :type new_name:     str
        """
        File.sed_replace(old_name, new_name, target_file)
        File.sed_replace(old_name[0].lower() + old_name[1:], new_name[
            0].lower() + new_name[1:], target_file)
        File.sed_replace(old_name.lower(), new_name.lower(), target_file)
        File.sed_replace(old_name.upper(), new_name.upper(), target_file)
        File.sed_replace(old_name.capitalize(),
                         new_name.capitalize(),
                         target_file)

    @staticmethod
    def copy_and_replace(src_file, dest_file, old_name, new_name):
        os.system('cp ' + src_file + ' ' + dest_file)
        File.replace_in_file(dest_file, old_name, new_name)


    @staticmethod
    def is_content_in_file(file_path, content):
        """Test si un fichier contient une chaine de caractères
        :param file_path: Chemin du fichier
        :param content:   Contenu à tester
        :type file_path:  str
        :type content:    str
        :return:          True si le contenu a été trouvé
        :rtype:           bool
        """
        result = False
        try:
            with open(file_path, 'r') as file_content:
                if content in file_content.read():
                    result = True
        except FileNotFoundError:
            pass
        return result

