#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from libs.MethodData import MethodData
from libs.BaseMenu import BaseMenu
from libs.RootMenu import RootMenu
# Pour le debug
from pprint import pprint


############
# Constantes
############
DEFAULT_PLUGIN_NAME_FILE_PATH = '.plugin_name'

##########
# Globales
##########
DEFAULT_PLUGIN_NAME = 'template'


def get_current_plugin_name(plugin_name, plugin_name_file_path):
    """Lit le fichier caché contenant le nom du plugin en cours d'élaboration
    """
    result = plugin_name
    if os.path.isfile(plugin_name_file_path):
        with open(plugin_name_file_path, 'r') as plugin_name_file:
            data = plugin_name_file.read().replace('\n', '')
            if data != '':
                result = data
            plugin_name_file.close()
    return result


def show_help():
    """Affiche l'aide
    """
    print(sys.argv[0]+' [PLUGIN-NAME] [--help]')
    print('  --help :      Affiche de menu.')
    print('  PLUGIN-NAME : Indiquer le nom du plugin à modifier.')


def parse_args(plugin_name, plugin_name_file_path):
    """Analyse les arguments
    """
    result = ""
    if '--help' in sys.argv:
        show_help()
        result = None
    elif len(sys.argv) > 1:
        result = sys.argv[1]
    else:
        result = get_current_plugin_name(plugin_name, plugin_name_file_path)

    return result


if __name__ == '__main__':
    # Point de d'entrée en mode CLI
    readed_plugin_name = parse_args(DEFAULT_PLUGIN_NAME,
                                    DEFAULT_PLUGIN_NAME_FILE_PATH)
    if readed_plugin_name is not None:
        print('\nPlugin en cours de modification : '+readed_plugin_name+'\n')
        root_menu = RootMenu(readed_plugin_name, DEFAULT_PLUGIN_NAME_FILE_PATH)
        root_menu.start()
