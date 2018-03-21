#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Renomme un plugin
"""

import os
import sys

from .libs.File import File
from .libs.IO import IO


def start_rename_plugin(path, old_name, new_name):
    """Renomme le plugin
    Modifie le nom des répertoires, des fichiers ainsi que le contenu
    des fichiers.
    """
    path = os.path.abspath(path)
    new_path = os.path.abspath(path + os.sep + '..' + os.sep + 'plugin-' +
                               new_name)
    if os.path.exists(path):
        if 'plugin-' + new_name not in os.listdir('.'):
            # Renomme le répertoire racine du plugin
            os.rename(path, new_path)
            # Renomme le contenu du plugin
            rename_plugin(new_path, old_name, new_name)
            IO.print_success('Le plugin ' + old_name + ' a été renommé en ' +
                             new_name)
        else:
            IO.print_error('Le répertoire  plugin-' + new_name +
                           ' existe déjà')
    else:
        IO.print_error('Le plugin ' + path + ' n\'a pas été trouvé')


def rename_plugin(current_path, old_name, new_name):
    """Remplace les occurences dans les noms des fichiers, les répertoires,
    et au sein des fichiers
    :param current_path: Répertoire courant
    :param old_name:     Ancien nom
    :param new_name:     Nouveau nom
    :type current_path:  str
    :type old_name:      str
    :type new_name:      str
    """
    core_template_test = 'core' + os.sep + 'template'
    if old_name != '' and new_name != '':
        # Remplacement des occurences dans les noms des fichiers et
        # des répertoires
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            # A enlever quand plugin-template sera renommé plugin-Template
            if not item_path.endswith(core_template_test):
                item = rename_item(current_path + os.sep,
                                   item,
                                   old_name,
                                   new_name)
            if os.path.isdir(current_path + os.sep + item):
                rename_plugin(current_path + os.sep + item,
                              old_name,
                              new_name)
            else:
                # Remplacement des occurences dans le fichier
                File.replace_in_file(
                    current_path + os.sep + item, old_name, new_name)


def rename_item(path, item, old_name, new_name):
    """Renomme un élément si besoin
    :param path:     Chemin courant
    :param item:     Fichier à tester
    :param old_name: Ancien nom du plugin
    :param new_name: Nouveau nom du plugin
    :type path:      str
    :type item:      str
    :type old_name:  str
    :type new_name:  str
    :return:         Fichier avec le nouveau nom si il a été renommé
    :rtype:          str
    """
    result = item
    # Cas simple
    if old_name in item:
        result = item.replace(old_name, new_name)
        os.rename(path + item, path + result)
    # En majuscule
    elif old_name.upper() in item:
        result = item.replace(old_name.upper(), new_name.upper())
        os.rename(path + item, path + result)
    # En minuscule
    elif old_name.lower() in item:
        result = item.replace(old_name.lower(), new_name.lower())
        os.rename(path + item, path + result)
    # Avec une majuscule au début
    elif old_name.capitalize() in item:
        result = item.replace(old_name.capitalize(), new_name.capitalize())
        os.rename(path + item, path + result)
    return result


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin ancien_nom nouveau_nom')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    else:
        start_rename_plugin(sys.argv[1], sys.argv[2], sys.argv[3])
