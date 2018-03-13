# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint
from BaseMenu import BaseMenu
from RootMenu import RootMenu


class WizardMenu(BaseMenu):
    plugins_list = []
    actions = []
    plugin_template_repo = \
        'https://github.com/Jeedom-Plugins-Extra/plugin-template.git'

    def __init__(self, plugins_list):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params plugin_list:           Liste des plugins disponibles
        :type plugin_list:             str
        """
        if sys.version_info[0] < 3:
            super(WizardMenu, self).__init__()
        else:
            super().__init__()

        # Configuration du menu
        # Premier choix : Assistant
        self.plugins_list = plugins_list
        self.menu.append('Démarrer l\'assistant')
        self.actions.append([self.start_wizard, None])
        # Recherche si le plugin template existe déjà
        add_template_download = True
        for plugin in self.plugins_list:
            if plugin[1] == 'template' or plugin[1] == 'Template':
                add_template_download = False
        if add_template_download:
            self.menu.append('Télécharger le plugin Template')
            self.actions.append([self.git_template, None])
        # Ajout de la liste des plugins dans le répertoire
        for plugin in plugins_list:
            self.menu.append('Modifier le plugin '+plugin[1])
            self.actions.append([self.start_tools, plugin])

    def start(self):
        """Démarre l'affichage du menu
        """
        loop = True
        while loop:
            user_choice = self.get_menu_choice(self.menu)
            if user_choice == -1:
                loop = False
            else:
                # Debug
                return_value = self.actions[user_choice][0](
                    self.actions[user_choice][1])
#                try:
#                    return_value = self.actions[user_choice][0](
#                        self.actions[user_choice][1])
#                except AttributeError:
#                    self.print_error(self.bad_command)
#                    return_value = False
        return return_value

    def start_wizard(self, data):
        """Lance l'assistant
        :params data: Inutilisé
        """
        print("Assistant")

    def git_template(self, data):
        """Télécharge une copie du plugin Template
        :params data: Inutilisé
        """
        sys_return = os.system('git clone ' + self.plugin_template_repo +
                               ' 2> /dev/null')
        if sys_return == 0:
            self.print_success('Le plugin plugin-template a été téléchargé')
        else:
            self.print_error('Le plugin plugin-template est déjà téléchargé.')
        self.start_tools(['plugin-template', 'template'])

    def start_tools(self, plugin_data):
        """Lance l'outil
        :params plugin_data: Tableau contenant le chemin et le nom du plugin
        :type plugin_data:   str
        """
        root_menu = RootMenu(plugin_data[0], plugin_data[1])
        root_menu.start()
