#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ajoute une tâche cron au plugin
"""

import os
import sys

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
    crons_titles = [
        'Toutes les minutes',
        'Toutes les 5 minutes',
        'Toutes les 15 minutes',
        'Toutes les 30 minutes',
        'Toutes les heures',
        'Tous les jours'
    ]
    crons_functions = [
        'cron',
        'cron5',
        'cron15',
        'cron30',
        'cronHourly',
        'cronDaily'
    ]

    choice = IO.get_menu_choice(crons_titles, 'Choix de la récurrence')
    if choice >= 0:
        method_data = MethodData()
        method_data.class_file_path = core_file_path
        method_data.class_name = plugin_name
        method_data.method_name = crons_functions[choice]
        method_data.method_is_static = True
        method_data.method_comment = crons_titles[choice]
        os.system('cat '+core_file_path)
        if PHPFile.add_method(method_data):
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
