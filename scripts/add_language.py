#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ajoute une langue au plugin
"""

import os
import sys

from libs.Jeedom import Jeedom  # pylint: disable= import-error

# Gestion des accents pour python 2
if sys.version_info[0] < 3:
    reload(sys)  # pylint: disable=undefined-variable
    sys.setdefaultencoding('utf8')  # pylint: disable=no-member


def add_language(plugin_path, plugin_name):
    """
    Ajoute la classe pour traiter les requêtes AJAX
    :param plugin_path: Chemin du plugin
    :param plugin_name: Nom du plugin
    :type plugin_path:  str
    :type plugin_name:  str
    """
    i18n_path = Jeedom.get_i18n_path(plugin_path)
    if not os.path.exists(i18n_path):
        Jeedom.ask_for_i18n_folder_creation(i18n_path)
    if os.path.exists(i18n_path):
        Jeedom.add_language(plugin_path)


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin nom_du_plugin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        add_language(sys.argv[1], sys.argv[2])
