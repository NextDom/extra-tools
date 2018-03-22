#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ajoute la classe cmd d'un plugin
"""

import os
import sys

from libs.File import File
from libs.IO import IO
from libs.MethodData import MethodData
from libs.PHPFile import PHPFile


def add_cmd_class(path, plugin_name):
    templates_cmd_file = os.path.join(os.path.dirname(__file__), 'templates',
                                      'feature_cmd_class.php')
    target_core_file = os.path.join(path, 'core', 'class',
                                    plugin_name + '.class.php')
    target_cmd_file = os.path.join(path, 'core', 'class',
                                   plugin_name + 'Cmd.class.php')
    if is_core_class_exists(path, plugin_name, target_core_file):
        separated = IO.ask_y_n('Utiliser des fichiers séparés ?')
        if separated == 'o':
            insert_require_in_core(target_core_file, plugin_name)
            File.copy_and_replace(templates_cmd_file, target_cmd_file,
                                  'PluginName', plugin_name)
        else:
            PHPFile.write_class(target_core_file, plugin_name + 'Cmd', 'cmd')

            method_data = MethodData()
            method_data.class_file_path = target_core_file
            method_data.class_name = plugin_name + 'Cmd'
            method_data.method_name = 'execute'
            method_data.method_params = '$_options = array()'
            method_data.method_visibility = 'public'
            PHPFile.write_method_in_class(method_data)


def is_core_class_exists(path, plugin_name, core_file):
    result = False
    if os.path.exists(core_file):
        if PHPFile.check_class(core_file, plugin_name):
            result = True
    else:
        create = IO.ask_y_n('Le fichier de la classe principale n\'existe pas, '
                            'voulez-vous le créer ?')
        if create == 'o':
            os.system('./scripts/add_core_class.py ' + path + ' ' + plugin_name)
            result = True
    return result


def insert_require_in_core(core_file, plugin_name):
    PHPFile.add_line_under(core_file,
                           'require_once dirname(__FILE__)',
                           'require_once \'./' + plugin_name +
                           'Cmd.class.php\';\n')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin nom_du_plugin')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
    else:
        add_cmd_class(sys.argv[1], sys.argv[2])
