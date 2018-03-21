# -*- coding: utf-8 -*-
"""
Librairie pour la gestion des entrées sorties
"""

import sys


class IO(object):
    cancel_menu = 'Sortir'
    choice_prompt = 'Choix : '
    bad_choice = 'Mauvais choix'

    @staticmethod
    def print_error(msg):
        """Affiche un message d'erreur
        :params msg: Message à afficher
        :type msg:   str
        """
        print('/!\\ ' + msg)

    @staticmethod
    def print_success(msg):
        """Affiche un message de confirmation
        :params msg: Message à afficher
        :type msg:   str
        """
        print('v ' + msg)

    @staticmethod
    def is_string(obj):
        """Test si une variable est une chaine de caractères
        :params obj: Objet à tester
        :return:     True si l'object est une chaine de caractères
        :rtype:      bool
        """
        str_type = str

        if sys.version_info[0] < 3:
            str_type = basestring  # pylint: disable=undefined-variable
        return isinstance(obj, str_type)

    @staticmethod
    def get_user_input(msg):
        """Obtenir une entrée d'un utilisateur
        Compatible Python 2 et 3
        :params msg: Message à afficher
        :type msg:   str
        :return:     Entrée de l'utilisateur
        :rtype:      str
        """
        result = None
        if sys.version_info[0] < 3:
            result = raw_input(msg)  # pylint: disable=undefined-variable
        else:
            result = input(msg)
        return result

    @staticmethod
    def show_menu(menu, title=None, show_cancel=True):
        """Afficher un menu
        :params menu:        Tableau des choix à afficher
        :params show_cancel: Affiche un message pour sortir du menu
        :params title:       Titre du menu
        :type menu:          array
        :type show_cancel:   bool
        :type title:         str
        """
        print('')
        if title is not None:
            print('-=| ' + title + ' |=-\n')
        for index, menu_item in enumerate(menu):
            print('  ' + str(index + 1) + '. ' + menu_item)
        if show_cancel:
            print('  0. ' + IO.cancel_menu)

    @staticmethod
    def get_menu_choice(menu, title=None, show_cancel=True):
        """Demande à l'utilisateur de faire un choix dans un menu
        :params menu:        Tableau des choix à afficher
        :params show_cancel: Affiche le 0 pour sortir
        :params title:       Titre du menu
        :type menu:          List[str]
        :type show_cancel:   bool
        :type title:         str
        :return:             Choix de l'utilisateur ou -1
        :rtype:              int
        """
        loop = True
        user_choice = 9999
        menu_choice_length = len(menu)

        while loop:
            IO.show_menu(menu, title, show_cancel)
            try:
                raw_user_choice = IO.get_user_input(IO.choice_prompt)
                user_choice = int(raw_user_choice)
            except NameError:
                user_choice = 9999
            except ValueError:
                user_choice = 9999
                # Sortir si l'utilisateur appuie sur Enter
                if show_cancel:
                    if IO.is_string(raw_user_choice) and \
                            raw_user_choice == "":
                        user_choice = 0
            if user_choice < menu_choice_length + 1:
                # Choix de l'utilisateur -1 pour retrouver l'index du tableau
                # et -1 si l'utilisateur a choisi 0 (Sortir)
                user_choice -= 1
                loop = False
                # Si l'utilisateur doit répondre, la boucle continue
                if user_choice == -1 and not show_cancel:
                    loop = True
            else:
                IO.print_error(IO.bad_choice)
        return user_choice


    @staticmethod
    def ask_y_n(question, default='o'):
        """Afficher une question dont la réponse est oui ou non
        :param question: Question à afficher
        :param default:  Réponse par défaut. o par défaut
        :type question:  str
        :type default:   str
        :return:         Réponse de l'utilisateur
        :rtype:          str
        """
        choices = 'O/n'
        if default != 'o':
            choices = 'o/N'
        choice = IO.get_user_input(
            '%s [%s] : ' % (question, choices)).lower()
        if choice == default or choice == '':
            return default
        return choice

    @staticmethod
    def ask_with_default(question, default):
        """Affiche une question avec une réponse par défaut
        :param question: Question à afficher
        :param default:  Réponse par défaut
        :type question:  str
        :type default:   str
        :return:         Réponse de l'utilisateur
        :rtype:          str
        """
        answer = IO.get_user_input('%s [%s] : ' % (question, default))
        if answer == '':
            answer = default
        return answer