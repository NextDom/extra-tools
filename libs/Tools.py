# -*- coding: utf-8 -*-
"""
Classe facilitant l'initialisation de l'outil
"""

import json
import os
import sys


class Tools(object):
    """
    Classe facilitant l'initialisation de l'outil
    """

    @staticmethod
    def show_help():
        """Affiche l'aide
        """
        print(sys.argv[0] + ' [PLUGIN-NAME] [--help]')
        print('  --help :      Affiche de menu.')
        print('  PLUGIN-NAME : Indiquer le nom du plugin à modifier.')

    @staticmethod
    def parse_args(argv):
        """Analyse les arguments
        :params argv: Arguments
        :type argv:   list
        :return:      Liste ou None si le programme doit quitter
        """
        result = ''
        if '--help' in argv or len(argv) > 2:
            Tools.show_help()
            result = None
        elif len(argv) > 1:
            result = argv[1]

        return result

    @staticmethod
    def is_plugin_dir(path):
        """Test si le répertoire contient un plugin
        :param path: Chemin à tester
        :return:     True si c'est un plugin
        """
        info_path = os.path.join(path, 'plugin_info', 'info.json')
        return os.path.exists(info_path)

    @staticmethod
    def get_plugin_data(path):
        """Lire les informations du plugin
        :param path: Chemin du plugin
        :return:     Informations du plugin
        :rtype:      dict
        """
        result = None
        info_path = os.path.join(path, 'plugin_info', 'info.json')
        try:
            with open(info_path) as info_json:
                info_json_data = json.load(info_json)
                if 'id' in info_json_data.keys():
                    result = [path, info_json_data['id']]
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        return result

    @staticmethod
    def get_plugins_in_dir(path):
        """Obtenir la liste des plugins dans un répertoire
        :param path: Répertoire parent
        :return:     Liste des plugins
        :rtype:      list
        """
        result = []
        for item in os.listdir(path):
            item_path = path + os.sep + item
            if os.path.isdir(item_path):
                if Tools.is_plugin_dir(item_path):
                    plugin = Tools.get_plugin_data(item_path)
                    if plugin is not None:
                        result.append(plugin)
        return result
