#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Met à jour les fichiers de traduction d'un plugin
"""

import json
import os
import sys

from libs.Jeedom import Jeedom #pylint: disable= import-error
from libs.IO import IO #pylint: disable= import-error


def update_languages(plugin_path, plugin_name):
    """
    Ajoute la classe pour traiter les requêtes AJAX
    :param plugin_path: Chemin du plugin
    :param plugin_name: Nom du plugin
    :type plugin_path:  str
    :type plugin_name:  str
    """
    i18n_path = Jeedom.get_i18n_path()
    if os.path.exists(i18n_path):
        i18n_list = os.listdir(i18n_path)
        if i18n_list:
            scan_data = Jeedom.scan_for_strings(plugin_path)
            for i18n in i18n_list:
                json_data = {}
                try:
                    with open(i18n_path + os.sep + i18n) as i18n_content:
                        json_data = json.loads(i18n_content.read())
                except ValueError:
                    pass
                json_data = Jeedom.merge_i18n_json(plugin_path, plugin_name, json_data, scan_data)
                Jeedom.write_json_file(i18n_path + os.sep + i18n,
                                         json_data)
        else:
            IO.print_error('Aucune traduction')
    else:
        IO.print_error('Aucun répertoire pour les traductions')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin nom_du_plugin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        update_languages(sys.argv[1], sys.argv[2])
