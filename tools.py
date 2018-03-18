#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

from libs.WizardMenu import WizardMenu

# Gestion des accents pour python 2
if sys.version_info[0] < 3:
    reload(sys) #pylint: disable=undefined-variable
    sys.setdefaultencoding('utf8') #pylint: disable=no-member

def show_help():
    """Affiche l'aide
    """
    print(sys.argv[0] + ' [PLUGIN-NAME] [--help]')
    print('  --help :      Affiche de menu.')
    print('  PLUGIN-NAME : Indiquer le nom du plugin à modifier.')


def parse_args(argv):
    """Analyse les arguments
    """
    result = ''
    if '--help' in argv or len(argv) > 2:
        show_help()
        result = None
    elif len(argv) > 1:
        result = argv[1]

    return result


def is_plugin_dir(path):
    """Test si le répertoire contient un plugin
    :param path: Chemin à tester
    :return:     True si c'est un plugin
    """
    info_path = os.path.join(path, 'plugin_info', 'info.json')
    return os.path.exists(info_path)


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


def get_plugins_in_dir(path):
    """Obtenir la liste des plugins dans un répertoire
    :param path: Répertoire parent
    :return:     Liste des plugins
    :rtype:      list
    """
    result = []
    for item in os.listdir(path):
        item_path = path+os.sep+item
        if os.path.isdir(item_path):
            if is_plugin_dir(item_path):
                plugin = get_plugin_data(item_path)
                if plugin is not None:
                    result.append(plugin)
    return result


if __name__ == '__main__':
    # Point de d'entrée en mode CLI
    readed_plugin_name = parse_args(sys.argv)
    if readed_plugin_name is not None:
        plugins_list = []
        if readed_plugin_name == '':
            plugins_list = get_plugins_in_dir('.')
        wizard_menu = WizardMenu(plugins_list)
        wizard_menu.start()
