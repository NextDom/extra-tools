# -*- coding: utf-8 -*-
"""
Classe mère des menus
"""

import os

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

    @staticmethod
    def start_script(script_name, params):
        """
        Lance un script des outils
        :param script_name: Nom du script
        :param params:      Paramètres du script
        :type script_name:  str
        :type params:       List(str)
        :return:
        """
        cmd = './scripts/' + script_name + ' '.join(params)
        os.system(cmd)
