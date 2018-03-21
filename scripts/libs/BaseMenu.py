# -*- coding: utf-8 -*-
"""
Classe mère des menus
"""

import sys

from .IO import IO


# noinspection PyUnresolvedReferences
class BaseMenu(object):
    """Classe mère des menus
    Fournit les méthodes nécessaire à l'affichage des menus et des actions
    courantes.
    """
    title = None
    menu = []
    bad_command = 'Mauvaise commande'
    php_include_core_3 = \
        "require_once dirname(__FILE__).'/../../../core/php/core.inc.php';\n\n"
    php_include_core_4 = \
        "require_once dirname(__FILE__).'/../../../../core/php/core.inc.php" \
        "';\n\n"
    php_header = "<?php\n\n"
    php_check_user_connect = \
        "include_file('core', 'authentification', 'php');\n\n" \
        "if (!isConnect('admin')) {\n" \
        "    throw new Exception('{{401 - Refused access}}');\n" \
        "}\n"

    def start(self):
        """Démarre l'affichage du menu
        """
        loop = True
        while loop:
            user_choice = IO.get_menu_choice(self.menu, self.title)
            if user_choice == -1:
                loop = False
            else:
                self.launch(user_choice + 1)

    @staticmethod
    def is_content_in_file(file_path, content):
        """Test si un fichier contient une chaine de caractères
        :param file_path: Chemin du fichier
        :param content:   Contenu à tester
        :type file_path:  str
        :type content:    str
        :return:          True si le contenu a été trouvé
        :rtype:           bool
        """
        result = False
        try:
            with open(file_path, 'r') as file_content:
                if content in file_content.read():
                    result = True
        except FileNotFoundError:
            pass
        return result

    def launch(self, number):
        """Lance une action
        :params number: Numéro de l'action à lancer
        :type number:   int
        :return:        Résultat de l'action
        :rtype:         bool
        """
        return_value = None
        method_name = 'action_' + str(number)
        # DEBUG
        method = getattr(self, method_name)
        return_value = method()
        # try:
        #    method = getattr(self, method_name)
        #    return_value = method()
        # except AttributeError:
        #    self.print_error(self.bad_command)
        #    return_value = False
        return return_value
