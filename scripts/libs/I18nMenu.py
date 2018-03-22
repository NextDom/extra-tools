# -*- coding: utf-8 -*-
"""
Menu de l'internationalisation
"""
import json
import os
import re
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
        i18n_path = self.get_i18n_path()
        I18nMenu.ask_for_i18n_folder_creation(i18n_path)
        if os.path.exists(i18n_path):
            self.add_language(i18n_path)

    def action_2(self):
        """
        Met à jour les traduction
        """
        i18n_path = self.get_i18n_path()
        if os.path.exists(i18n_path):
            i18n_list = os.listdir(i18n_path)
            if i18n_list:
                scan_data = I18nMenu.scan_for_strings(self.plugin_path)
                for i18n in i18n_list:
                    json_data = {}
                    try:
                        with open(i18n_path + os.sep + i18n) as i18n_content:
                            json_data = json.loads(i18n_content.read())
                    except ValueError:
                        pass
                    json_data = self.merge_i18n_json(json_data, scan_data)
                    I18nMenu.write_json_file(i18n_path + os.sep + i18n,
                                             json_data)
            else:
                BaseMenu.print_error('Aucune traduction')
        else:
            BaseMenu.print_error('Aucun répertoire pour les traductions')

    @staticmethod
    def ask_for_i18n_folder_creation(path):
        """
        Demande pour ajouter le répertoire de traduction
        :param path: Chemin du répertoire
        :type path:  str
        """
        if not os.path.exists(path):
            answer = BaseMenu.ask_y_n('Voulez-vous créer le répertoire ' \
                                      'core/i18n ?')
            if answer == 'o':
                os.mkdir(path)

    def add_language(self, i18n_path):
        """
        Ajout un language
        :param i18n_path: Chemin du répertoire des traductions
        :type i18n_path:  str
        :return:          True si la traduction a été rajoutée
        :rtype:           bool
        """
        i18n_list = os.listdir(i18n_path)
        if i18n_list:
            print('Liste des traductions présentes : ')
            for i18n in i18n_list:
                print(' - ' + i18n)
        loop = True
        language = ''
        while loop:
            language = BaseMenu.get_user_input('Nom de la traduction : ')
            if language == '':
                loop = False
            elif I18nMenu.is_valid_i18n_name(language):
                if language in os.listdir(i18n_path):
                    BaseMenu.print_error(language + ' existe déjà.')
                else:
                    loop = False
            else:
                BaseMenu.print_error('La langue doit être au format fr_FR.')
        if language != '':
            scan_data = I18nMenu.scan_for_strings(self.plugin_path)
            json_data = self.merge_i18n_json({}, scan_data)
            I18nMenu.write_json_file(i18n_path + os.sep + language + '.json',
                                     json_data)
            BaseMenu.print_success('La langue ' + language + ' a été ajoutée')

    def get_i18n_path(self):
        """
        Renvoie le chemin du répertoire contenant les traductions du plugin
        :return: Chemin vers le répertoire des traductions
        :rtype:  str
        """
        return os.path.join(self.plugin_path, 'core', 'i18n')

    @staticmethod
    def write_json_file(file_path, json_data):
        """
        Ecrit le fichier au format JSON
        :param file_path: Chemin du fichier
        :param json_data: Données à écrire
        :type file_path:  str
        :type json_data:  dict
        :return:          True si l'écriture à réussie
        :rtype:           bool
        """
        result = False
        with open(file_path, 'w') as dest:
            if sys.version_info[0] < 3:
                dump = json.dumps(json_data, sort_keys=True, indent=4,
                                  ensure_ascii=False)
                dump = dump.encode('utf-8').decode('string-escape')
            else:
                dump = json.dumps(json_data, sort_keys=True, indent=4)
                dump = dump.encode('utf-8').decode('unicode-escape')
            dest.write(dump + '\n')
            result = True
        return result

    def merge_i18n_json(self, base_json, scan_data):
        """
        Fusionne les anciennes données avec les nouvelles
        :param base_json: Données présentes
        :param scan_data: Données scannées
        :type base_json:  dict
        :type scan_data:  dict
        :return:          Données fusionnées
        :rtype:           dict
        """
        for data in scan_data:
            file_path = self.transform_path_to_i18n_path(data['file_path'])
            # Python décode les \\ à la lecture du JSON
            key_file_path = file_path.replace('\\', '')
            # Décode l'unicode si besoin
            if not isinstance(key_file_path, str):
                key_file_path = key_file_path.encode('ascii')

            # Création du dictionnaire vide
            if key_file_path not in base_json.keys():
                base_json[key_file_path] = {}

            # Ajoute les éléments
            for item in data['items']:
                if item not in base_json[key_file_path].keys():
                    base_json[key_file_path][item] = item
            # Renomme la clé pour Jeedom
            base_json[file_path] = base_json.pop(key_file_path)
        return base_json

    def transform_path_to_i18n_path(self, path):
        """
        Transforme le chemin pour qu'il soit compatible avec Jeedom
        :param path: Chemin à convertir
        :type path:  str
        :return:     Chemin converti
        :rtype:      str
        """
        normal_path = 'plugins' + os.sep + self.plugin_name + \
                      path.replace(self.plugin_path, '')
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
                I18nMenu.scan_for_strings(item_path, result)
            else:
                if item.endswith('php'):
                    content = I18nMenu.scan_file_for_strings(item_path)
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
