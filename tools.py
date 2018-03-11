#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# Pour le debug
from pprint import pprint

#######################
# Chaînes de caractères
#######################
cancel_menu = 'Sortir'
bad_choice = 'Mauvais choix'
bad_command = 'Mauvaise commande'
choice_prompt = 'Choix : '

############
# Constantes
############
plugin_template_repo = \
    'https://github.com/Jeedom-Plugins-Extra/plugin-template.git'
plugin_name_file_path = '.plugin_name'
sed_replace = "sed -i'' 's/{}/{}/g' {} 2> /dev/null"
# Version Mac OS X
if 'darwin' in sys.platform:
    sed_replace = "sed -i '' 's/{}/{}/g' {} 2> /dev/null"

##########
# Globales
##########
plugin_name = 'template'


class BaseMenu:
    menu = []

    def print_error(self, msg):
        """Affiche un message d'erreur
        :params msg: Message à afficher
        :type msg:   str
        """
        print('/!\\ '+msg)

    def show_menu(self, menu, show_cancel=True):
        """Afficher un menu
        :params menu: Tableau des choix à afficher
        :type menu:   array
        """
        print('')
        for index, menu_item in enumerate(menu):
            print(str(index + 1)+'. '+menu_item)
        if show_cancel:
            print('0. '+cancel_menu)

    def get_menu_choice(self, menu):
        """Demande à l'utilisateur de faire un choix dans un menu
        :params menu: Tableau des choix à afficher
        :type menu:   array
        :return:      Choix de l'utilisateur ou -1
        :rtype:       int
        """
        loop = True
        user_choice = 999
        menu_choice_length = len(menu)

        while (loop):
            self.show_menu(menu)
            try:
                user_choice = int(self.get_user_input(choice_prompt))
            except NameError:
                user_choice = 999
            except ValueError:
                user_choice = 0
            if (user_choice < menu_choice_length + 1):
                return user_choice - 1
            else:
                self.print_error(bad_choice)

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

    def start(self):
        """Démarre l'affiche du menu
        """
        loop = True
        while loop:
            user_choice = self.get_menu_choice(self.menu)
            if user_choice == -1:
                loop = False
            else:
                self.launch(user_choice + 1)

    """Classe contenant les actions du menu racine
    """
    def launch(self, number):
        """Lance une action
        :params number: Numéro de l'action à lancer
        :type number:   int
        :return:        Résultat de l'action
        """
        return_value = None
        method = None
        method_name = 'action_' + str(number)
        try:
            method = getattr(self, method_name)
            return_value = method()
        except AttributeError:
            self.print_error(bad_command)
            return_value = False
        return return_value


class InfoMenu(BaseMenu):
    menu = ['Modifier le nom affiché dans les menus',
            'Modifier la description',
            'Modifier la licence',
            'Modifier l\'auteur',
            'Modifier la catégorie']

    def action_1(self):
        """Modifier le nom affiché dans les menus
        """
        name = self.get_user_input('Nouveau nom : ')
        self.replace_info('name', name)

    def action_2(self):
        """Modifier la description
        """
        description = self.get_user_input('Nouvelle description : ')
        self.replace_info('description', description)

    def action_3(self):
        """Modifier la licence
        """
        licence = self.get_user_input('Nouvelle licence : ')
        self.replace_info('licence', licence)

    def action_4(self):
        """Modifier l'auteur
        """
        author = self.get_user_input('Nouvel auteur : ')
        self.replace_info('author', author)

    def action_5(self):
        """Modifier la catégorie
        """
        categories = [
            'security',
            'automation protocol',
            'programming',
            'organization',
            'weather',
            'communication',
            'devicecommunication',
            'multimedia',
            'wellness',
            'monitoring',
            'health',
            'nature',
            'automatisation',
            'energy'
        ]
        category = self.get_menu_choice(categories)
        if category >= 0:
            self.replace_info('category', categories[category])

    def replace_info(self, key, new_value):
        os.system(sed_replace.format(
            '\("'+key+'" : "\).*\(",\)',
            '\\1'+new_value+'\\2',
            'plugin-'+plugin_name+os.sep+'plugin_info'+os.sep+'info.json'
        ))


class RootMenu(BaseMenu):
    menu = ['Télécharger le plugin Template',
            'Modifier l\'identifiant du plugin',
            'Modifier les informations du plugin']

    def action_1(self):
        """Télécharge une copie du plugin Template
        """
        global plugin_name

        plugin_name = 'template'
        os.system('git clone '+plugin_template_repo)
        write_current_plugin_name()

    def action_2(self):
        """Renomme le plugin
        Modifie le nom des répertoires, des fichiers ainsi que le contenu
        des fichiers.
        """
        global plugin_name

        if 'plugin-'+plugin_name in os.listdir('.'):
            new_name = self.get_user_input('Nouveau nom du plugin : ')
            # Renomme le répertoire racine du plugin
            os.rename('plugin-'+plugin_name, 'plugin-'+new_name)
            self.rename_plugin(
                'plugin-'+new_name, plugin_name, new_name)
            plugin_name = new_name
        else:
            self.print_error('Le plugin '+plugin_name+' n\'a pas été trouvé')

    def action_3(self):
        """Lance le menu de modification des informations
        """
        info_menu = InfoMenu()
        info_menu.start()

    def rename_plugin(self, current_path, old_name, new_name):
        """Remplace les occurences dans les noms des fichiers, les répertoires,
        et au sein des fichiers
        :param current_path: Répertoire courant
        :param old_name:     Ancien nom
        :param new_name:     Nouveau nom
        :type current_path:  str
        :type old_name:      str
        :type new_name:      str
        """
        if old_name != '' and new_name != '':
            # Remplacement des occurences dans les noms des fichiers et
            # des répertoires
            for item in os.listdir(current_path):
                # A enlever quand plugin-template sera renommé plugin-Template
                if 'core/template':
                    item = self.rename_item(current_path+os.sep,
                                            item,
                                            old_name,
                                            new_name)
                if os.path.isdir(current_path+os.sep+item):
                    self.rename_plugin(current_path+os.sep+item,
                                       old_name,
                                       new_name)
                else:
                    # Remplacement des occurences dans le fichier
                    self.replace_in_file(
                        current_path+os.sep+item, old_name, new_name)
            write_current_plugin_name()

    def replace_in_file(self, target_file, old_name, new_name):
        """Remplace l'ancien nom par le nouveau
        :param target_file: Fichier à traiter
        :param old_name:    Ancien nom du plugin
        :param new_name:    Nouveau nom du plugin
        :type target_file:  str
        :type old_name:     str
        :type new_name:     str
        """
        os.system(sed_replace.format(
            old_name,
            new_name,
            target_file))
        os.system(sed_replace.format(
            old_name.upper(),
            new_name.upper(),
            target_file))
        os.system(sed_replace.format(
            old_name.capitalize(),
            new_name.capitalize(),
            target_file))

    def rename_item(self, path, item, old_name, new_name):
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
            os.rename(path+item, path+result)
        # En majuscule
        elif old_name.upper() in item:
            result = item.replace(old_name.upper(), new_name.upper())
            os.rename(path+item, path+result)
        # Avec une majuscule au début
        elif old_name.capitalize() in item:
            result = item.replace(old_name.capitalize(), new_name.capitalize())
            os.rename(path+item, path+result)
        return result


def get_current_plugin_name():
    """Lit le fichier caché contenant le nom du plugin en cours d'élaboration
    """
    global plugin_name

    if os.path.isfile(plugin_name_file_path):
        with open(plugin_name_file_path, 'r') as plugin_name_file:
            data = plugin_name_file.read().replace('\n', '')
            if data != '':
                plugin_name = data
            plugin_name_file.close()


def write_current_plugin_name():
    """Ecrit le nom du plugin dans un fichier caché
    """
    with open(plugin_name_file_path, 'w') as plugin_name_file:
        plugin_name_file.write(plugin_name)
        plugin_name_file.close()


# Point de départ
if __name__ == '__main__':
    get_current_plugin_name()

    root_menu = RootMenu()
    root_menu.start()
