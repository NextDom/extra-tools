#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys

from libs.WizardMenu import WizardMenu


def show_help():
    """Affiche l'aide
    """
    print(sys.argv[0] + ' [PLUGIN-NAME] [--help]')
    print('  --help :      Affiche de menu.')
    print('  PLUGIN-NAME : Indiquer le nom du plugin à modifier.')


def parse_args():
    """Analyse les arguments
    """
    result = ''
    if '--help' in sys.argv:
        show_help()
        result = None
    elif len(sys.argv) > 1:
        result = sys.argv[1]

    return result


def is_plugin_dir(path):
    info_path = os.path.join(path, 'plugin_info', 'info.json')
    return os.path.exists(info_path)


def get_plugin_data(path):
    result = None
    info_path = os.path.join(path, 'plugin_info', 'info.json')
    with open(info_path) as info_json:
        info_json_data = json.load(info_json)
        if 'id' in info_json_data.keys():
            result = [path, info_json_data['id']]
    return result


def get_plugins_in_dir():
    result = []
    for item in os.listdir('.'):
        if os.path.isdir(item):
            if is_plugin_dir(item):
                plugin = get_plugin_data(item)
                if plugin is not None:
                    result.append(plugin)
    return result


if __name__ == '__main__':
    # Point de d'entrée en mode CLI
    readed_plugin_name = parse_args()
    if readed_plugin_name is not None:
        plugins_list = []
        if readed_plugin_name == '':
            plugins_list = get_plugins_in_dir()
        wizard_menu = WizardMenu(plugins_list)
        wizard_menu.start()
