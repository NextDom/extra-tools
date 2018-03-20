# -*- coding: utf-8 -*-
"""
Classe mère des menus
"""
import os
import sys


# noinspection PyUnresolvedReferences
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

    def __init__(self):
        """Constructeur
        Initialise la commande sed pour être compatible avec Mac OS X
        """
        if 'darwin' in sys.platform:
            BaseMenu.sed_replace_pattern = "sed -i '' 's/{}/{}/g' {} 2> /dev/null"

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
                raw_user_choice = BaseMenu.get_user_input(self.choice_prompt)
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
        choice = BaseMenu.get_user_input(
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
        answer = BaseMenu.get_user_input('%s [%s] : ' % (question, default))
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

    @staticmethod
    def sed_replace(regexp, replacement, target_file):
        """Exécute la commande sed sur un fichier
        :params regexp:      Expression régulière
        :params replacement: Chaîne de remplacement
        :params target_file: Fichier cible
        :type regexp:        str
        :type replacement:   str
        :type target_file:   str
        """
        os.system(BaseMenu.sed_replace_pattern.format(
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
        # DEBUG
        method = getattr(self, method_name)
        return_value = method()
        #try:
        #    method = getattr(self, method_name)
        #    return_value = method()
        #except AttributeError:
        #    self.print_error(self.bad_command)
        #    return_value = False
        return return_value
