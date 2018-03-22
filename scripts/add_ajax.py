#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ajoute la classe principale d'un plugin
"""

import os
import sys

from libs.IO import IO
from libs.File import File

from libs.PHPFile import PHPFile

def add_ajax(plugin_path, plugin_name):
    templates_cmd_file = os.path.join(os.path.dirname(__file__), 'templates',
                                      'feature_ajax.php')
    ajax_path = os.path.join(plugin_path + os.sep, 'core', 'ajax')
    ajax_file_path = ajax_path + os.sep + plugin_name + '.php'
    add_content = True
    if not os.path.exists(ajax_path):
        os.mkdir(ajax_path)
    if os.path.exists(ajax_file_path):
        IO.print_error('Le fichier existe déjà')
    else:
        os.system('cp '+templates_cmd_file+' '+ajax_file_path)
        IO.print_success('Le fichier a été créé')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin nom_du_plugin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        add_ajax(sys.argv[1], sys.argv[2])
