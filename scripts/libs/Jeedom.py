# -*- coding: utf-8 -*-
"""
Librairie pour la gestion des informations spécifiques à Jeedom
"""

import os
import re

from .File import File
from .IO import IO


class Jeedom(object):
    """s
    Librairie pour la gestion des informations spécifiques à Jeedom
    """

    @staticmethod
    def ask_for_i18n_folder_creation(i18n_path):
        """
        Demande pour ajouter le répertoire de traduction
        :param path: Chemin du plugin
        :type path:  str
        """
        if not os.path.exists(i18n_path):
            answer = IO.ask_y_n('Voulez-vous créer le répertoire ' \
                                'core/i18n ?')
            if answer == 'o':
                os.mkdir(i18n_path)

    @staticmethod
    def add_language(plugin_path):
        """
        Ajout un language
        :param plugin_path: Chemin du plugin
        :type plugin_path:  str
        :return:            True si la traduction a été rajoutée
        :rtype:             bool
        """
        i18n_path = Jeedom.get_i18n_path(plugin_path)
        i18n_list = os.listdir(i18n_path)
        if i18n_list:
            print('Liste des traductions présentes : ')
            for i18n in i18n_list:
                print(' - ' + i18n)
        loop = True
        language = ''
        while loop:
            language = IO.get_user_input('Nom de la traduction : ')
            if language == '':
                loop = False
            elif Jeedom.is_valid_i18n_name(language):
                if language+'.json' in os.listdir(i18n_path):
                    IO.print_error(language + ' existe déjà.')
                else:
                    loop = False
            else:
                IO.print_error('La langue doit être au format fr_FR.')
        if language != '':
            scan_data = Jeedom.scan_for_strings(plugin_path)
            json_data = Jeedom.merge_i18n_json(plugin_path, {}, scan_data)
            File.write_json_file(i18n_path + os.sep + language + '.json',
                                 json_data)
            IO.print_success('La langue ' + language + ' a été ajoutée')

    @staticmethod
    def get_i18n_path(plugin_path):
        """
        Renvoie le chemin du répertoire contenant les traductions du plugin
        :return: Chemin vers le répertoire des traductions
        :rtype:  str
        """
        return os.path.join(plugin_path, 'core', 'i18n')

    @staticmethod
    def merge_i18n_json(plugin_path, base_json, scan_data):
        """
        Fusionne les anciennes données avec les nouvelles
        :param base_json: Données présentes
        :param scan_data: Données scannées
        :type base_json:  dict
        :type scan_data:  List(dict)
        :return:          Données fusionnées
        :rtype:           dict
        """
        for data in scan_data:
            file_path = Jeedom.transform_path_to_i18n_path(plugin_path,
                                                           data['file_path'])
            # Python décode les \\ à la lecture du JSON
            #            key_file_path = file_path.replace('\\', '')
            # Décode l'unicode si besoin
            if not isinstance(file_path, str):
                file_path = file_path.encode('ascii')

            # Création du dictionnaire vide
            if file_path not in base_json.keys():
                base_json[file_path] = {}

            # Ajoute les éléments
            for item in data['items']:
                if item not in base_json[file_path].keys():
                    base_json[file_path][item] = item
            # Renomme la clé pour Jeedom
            base_json[file_path] = base_json.pop(file_path)
        return base_json

    @staticmethod
    def transform_path_to_i18n_path(plugin_path, file_path):
        """
        Transforme le chemin pour qu'il soit compatible avec Jeedom
        :param path: Chemin à convertir
        :type path:  str
        :return:     Chemin converti
        :rtype:      str
        """
        file_path_striped = file_path.replace(plugin_path, '')
        normal_path = 'plugins' + os.sep + os.path.basename(plugin_path) + \
                      os.sep + file_path_striped
        # En fonction du path fournit, il peut y avoir des doublons
        normal_path = normal_path.replace('//', '/')
        return normal_path.replace('/', '\\/')

    @staticmethod
    def scan_for_strings(path, result=None):
        """
        Parcourt un répertoire à la recherche de chaines à traduire
        :param path:   Chemin du répertoire à parcourir
        :param result: Résultat compléter par recursion
        :type path:    str
        :type result:  list
        :return:       Liste des chaines à traduire
        :rtype:        list
        """
        if result is None:
            result = []
        for item in os.listdir(path):
            item_path = path + os.sep + item
            if os.path.isdir(item_path):
                Jeedom.scan_for_strings(item_path, result)
            else:
                if item.endswith('php'):
                    content = Jeedom.scan_file_for_strings(item_path)
                    if content:
                        result.append({
                            'file_path': item_path,
                            'items': list(set(content))
                        })
        return result

    @staticmethod
    def scan_file_for_strings(file_path):
        """
        Parcourt les fichiers à la recherche de chaînes à traduire
        :param file_path: Fichier à parcourir
        :type file_path:  str
        :return:          Liste des chaines à traduire
        :rtype:           list
        """
        result = []
        with open(file_path, 'r') as file_content:
            readed_content = file_content.read()
            # noinspection RegExpRedundantEscape
            result.extend(re.findall('\\{\\{(.*?)\\}\\}', readed_content))
            result.extend(re.findall('__\\(\'(.*?)\'', readed_content))
        result.extend(re.findall('__\\("(.*?)"', readed_content))
        return result

    @staticmethod
    def is_valid_i18n_name(name):
        """
        Test si la langue est au bon format
        :param name: Nom à tester
        :type name:  str
        :return:     True si le format est correct
        :rtype:      bool
        """
        result = False
        re_search = re.search('^[a-z]{2}_[A-Z]{2}$', name)
        if re_search is not None:
            result = True
        return result
