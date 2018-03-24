#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ajoute une tâche cron au plugin
"""

import os
import sys
from pprint import pprint

from libs.IO import IO  # pylint: disable= import-error
from libs.MethodData import MethodData  # pylint: disable= import-error
from libs.PHPFile import PHPFile  # pylint: disable= import-error


def add_cron(plugin_path, plugin_name):
    """
    Ajoute une tâche cron au plugin
    :param plugin_path: Chemin du plugin
    :param plugin_name: Nom du plugin
    :type plugin_name:  str
    :type plugin_name:  str
    :return:
    """
    core_file_path = os.path.join(plugin_path, 'core', 'class', plugin_name +
                                  '.class.php')

    print(core_file_path)
    crons = {
        'Toutes les minutes': 'cron',
        'Toutes les 5 minutes': 'cron5',
        'Toutes les 15 minutes': 'cron15',
        'Toutes les 30 minutes': 'cron30',
        'Toutes les heures': 'cronHourly',
        'Tous les jours': 'cronDaily'
    }

    keys = crons.keys()
    pprint(keys)
    choice = IO.get_menu_choice(keys, 'Choix de la récurrence')
    if choice >= 0:
        print(choice)
        method_data = MethodData()
        method_data.class_file_path = core_file_path
        method_data.class_name = plugin_name
        method_data.method_name = crons[keys[choice]]
        method_data.method_is_static = True
        method_data.method_comment = keys[choice]
        pprint(keys[choice])
        os.system('cat '+core_file_path)
        if PHPFile.add_method(method_data):
            print('Add')
            IO.print_success('La méthode ' + method_data.method_name +
                             ' a été ajoutée')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin nom_du_plugin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        add_cron(sys.argv[1], sys.argv[2])
