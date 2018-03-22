#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ajoute la classe principale d'un plugin
"""

import os
import sys

from libs.File import File
from libs.IO import IO


def add_core_class(path, plugin_name):
    templates_file = os.path.join(os.path.dirname(__file__), 'templates',
                                  'feature_core_class.php')
    target_file = os.path.join(path, 'core', 'class',
                               plugin_name + '.class.php')
    if os.path.exists(target_file):
        IO.print_error('Le fichier existe déjà')
    else:
        File.copy_and_replace(templates_file, target_file, 'PluginName',
                              plugin_name)
        IO.print_success('Le fichier a été créé.')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin nom_du_plugin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        add_core_class(sys.argv[1], sys.argv[2])
