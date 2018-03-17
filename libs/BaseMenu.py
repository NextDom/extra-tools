# -*- coding: utf-8 -*-

import os
import sys


class BaseMenu(object):
    """Classe mère des menus
    Fournit les méthodes nécessaire à l'affichage des menus et des actions
    courantes.
    """
    title = None
    menu = []
    cancel_menu = 'Sortir'
    choice_prompt = 'Choix : '
    bad_choice = 'Mauvais choix'
    bad_command = 'Mauvaise commande'
    sed_replace_pattern = "sed -i'' 's/{}/{}/g' {} 2> /dev/null"

    def __init__(self):
        """Constructeur
        Initialise la commande sed pour être compatible avec Mac OS X
        """
        if 'darwin' in sys.platform:
            self.sed_replace_pattern = "sed -i '' 's/{}/{}/g' {} 2> /dev/null"

    def print_error(self, msg):
        """Affiche un message d'erreur
        :params msg: Message à afficher
        :type msg:   str
        """
        print('/!\\ ' + msg)

    def print_success(self, msg):
        """Affiche un message de confirmation
        :params msg: Message à afficher
        :type msg:   str
        """
        print('v ' + msg)

    def is_string(self, obj):
        """Test si une variable est une chaine de caractères
        :params obj: Objet à tester
        :return:     True si l'object est une chaine de caractères
        :rtype:      bool
        """
        str_type = str

        if sys.version_info[0] < 3:
            str_type = basestring
        return isinstance(obj, str_type)

    def show_menu(self, menu, show_cancel=True):
        """Afficher un menu
        :params menu:        Tableau des choix à afficher
        :params show_cancel: Affiche un message pour sortir du menu
        :type menu:          array
        :type show_cancel:   bool
        """
        print('')
        if self.title is not None:
            print('-=| ' + self.title + ' |=-\n')
        for index, menu_item in enumerate(menu):
            print('  ' + str(index + 1) + '. ' + menu_item)
        if show_cancel:
            print('  0. ' + self.cancel_menu)

    def get_menu_choice(self, menu, show_cancel=True):
        """Demande à l'utilisateur de faire un choix dans un menu
        :params menu:        Tableau des choix à afficher
        :params show_cancel: Affiche le 0 pour sortir
        :type menu:          List[str]
        :type show_cancel:   bool
        :return:             Choix de l'utilisateur ou -1
        :rtype:              int
        """
        loop = True
        user_choice = 9999
        menu_choice_length = len(menu)

        while loop:
            self.show_menu(menu, show_cancel)
            try:
                raw_user_choice = self.get_user_input(self.choice_prompt)
                user_choice = int(raw_user_choice)
            except NameError:
                user_choice = 9999
            except ValueError:
                user_choice = 9999
                # Sortir si l'utilisateur appuie sur Enter
                if show_cancel:
                    if self.is_string(raw_user_choice) and \
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
                self.print_error(self.bad_choice)
        return user_choice

    def get_user_input(self, msg):
        """Obtenir une entrée d'un utilisateur
        Compatible Python 2 et 3
        :params msg: Message à afficher
        :type msg:   str
        :return:     Entrée de l'utilisateur
        :rtype:      str
        """
        result = None
        if sys.version_info[0] < 3:
            result = raw_input(msg)
        else:
            result = input(msg)
        return result

    def ask_y_n(self, question, default='o'):
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
        choice = self.get_user_input('%s [%s] : ' % (question, choices)).lower()
        if choice == default or choice == '':
            return default
        return choice

    def ask_with_default(self, question, default):
        """Affiche une question avec une réponse par défaut
        :param question: Question à afficher
        :param default:  Réponse par défaut
        :type question:  str
        :type default:   str
        :return:         Réponse de l'utilisateur
        :rtype:          str
        """
        answer = self.get_user_input('%s [%s] : ' % (question, default))
        if answer == '':
            answer = default
        return answer

    def start(self):
        """Démarre l'affichage du menu
        """
        loop = True
        while loop:
            user_choice = self.get_menu_choice(self.menu)
            if user_choice == -1:
                loop = False
            else:
                self.launch(user_choice + 1)

    def sed_replace(self, regexp, replacement, target_file):
        """Exécute la commande sed sur un fichier
        :params regexp:      Expression régulière
        :params replacement: Chaîne de remplacement
        :params target_file: Fichier cible
        :type regexp:        str
        :type replacement:   str
        :type target_file:   str
        """
        os.system(self.sed_replace_pattern.format(
            regexp,
            replacement,
            target_file))

    def launch(self, number):
        """Lance une action
        :params number: Numéro de l'action à lancer
        :type number:   int
        :return:        Résultat de l'action
        :rtype:         bool
        """
        return_value = None
        method_name = 'action_' + str(number)
        try:
            method = getattr(self, method_name)
            return_value = method()
        except AttributeError:
            self.print_error(self.bad_command)
            return_value = False
        return return_value
