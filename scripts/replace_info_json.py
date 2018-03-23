#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Remplace une information dans le fichier d'information du plugin
"""

import os
import sys

from libs.File import File  # pylint: disable= import-error
from libs.IO import IO  # pylint: disable= import-error


def replace_info_json(plugin_path, key, new_value):
    """Remplace les informations dans le fichier info.json
    :params key:       Clé à modifier
    :params new_value: Nouvelle valeur de la clé
    :type key:         str
    :type new_value:   str
    """
    info_json_path = os.path.join(plugin_path, 'plugin_info', 'info.json')
    if os.path.exists(info_json_path):
        File.sed_replace(
            '\\("' + key + '"[ ]\\{0,1\\}: "\\).*\\("\\)',
            '\\1' + new_value + '\\2',
            info_json_path)
        IO.print_success('L\'information a été modifiée.')
    else:
        IO.print_error('Le fichier info.json n\'a pas été trouvé')


def usage():
    """
    Affichage de l'utilisation du script
    """
    print(sys.argv[0] + ' chemin_du_plugin clé nouvelle_valeur')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()
    else:
        replace_info_json(sys.argv[1], sys.argv[2], sys.argv[3])
