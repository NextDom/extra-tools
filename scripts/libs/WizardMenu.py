# -*- coding: utf-8 -*-
"""
Classe du menu de l'assistant
"""
import os

from .BaseMenu import BaseMenu
from .File import File
from .IO import IO
from .RootMenu import RootMenu


class WizardMenu(BaseMenu):
    """
    Classe du menu de l'assistant
    """
    plugins_list = []
    actions = []

    def __init__(self, plugins_list):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params plugins_list:  Liste des plugins disponibles
        :type plugins_list:    List
        """
        # Configuration du menu
        # Premier choix : Assistant
        self.plugins_list = plugins_list
        self.menu = []
        self.menu.append('Démarrer l\'assistant')
        self.actions.append([WizardMenu.start_wizard, None])
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
            self.menu.append('Modifier le plugin ' + plugin[1])
            self.actions.append([self.start_tools, plugin])

    def start(self):
        """Démarre l'affichage du menu
        """
        loop = True
        return_value = False
        while loop:
            user_choice = IO.get_menu_choice(self.menu)
            if user_choice == -1:
                loop = False
            else:
                # DEBUG
                if self.actions[user_choice][1] is None:
                    return_value = self.actions[user_choice][0]()
                else:
                    return_value = self.actions[user_choice][0](
                        self.actions[user_choice][1])
        #                try:
        #                    if self.actions[user_choice][1] is None:
        #                        return_value = self.actions[user_choice][0]()
        #                    else:
        #                        return_value = self.actions[user_choice][0](
        #                            self.actions[user_choice][1])
        #                except AttributeError:
        #                    IO.print_error(self.bad_command)
        #                    return_value = False
        return return_value

    @staticmethod
    def start_wizard():
        """Lance l'assistant
        """
        os.system('./scripts/wizard.py')
        exit(0)

    def git_template(self):
        """Télécharge une copie du plugin Template
        :params data: Inutilisé
        """
        config = File.read_config_data()
        sys_return = os.system('git clone ' + config['plugin_template_repo'] +
                               ' 2> /dev/null')
        if sys_return == 0:
            IO.print_success('Le plugin plugin-template a été téléchargé')
        else:
            IO.print_error('Le plugin plugin-template est déjà téléchargé.')
        self.start_tools(['plugin-template', 'template'])

    @staticmethod
    def start_tools(plugin_data):
        """Lance l'outil
        :params plugin_data: Tableau contenant le chemin et le nom du plugin
        :type plugin_data:   List[str]
        """
        root_menu = RootMenu(plugin_data[0], plugin_data[1])
        root_menu.start()
