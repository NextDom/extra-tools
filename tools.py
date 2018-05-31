#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour la génération et la modification de plugins pour Jeedom.
"""

import json
import os
import re
import sys

##########
# Config #
##########
config = {
    "plugin_template_repo": "https://github.com/NextDom/plugin-ExtraTemplate"
                            ".git",
    "default_package_name": "Exemple",
    "default_changelog_url": "https://nextdom.github.io/plugin-%s/#language"
                             "#/changelog",
    "default_documentation_url":
        "https://nextdom.github.io/plugin-%s/#language#/",
    "jeedom_categories": [
        "security",
        "automation protocol",
        "programming",
        "organization",
        "weather",
        "communication",
        "devicecommunication",
        "multimedia",
        "wellness",
        "monitoring",
        "health",
        "nature",
        "automatisation",
        "energy"
    ]
}

#################
# Templates PHP #
#################
php_header = """<?php

/* This file is part of Jeedom.
 *
 * Jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
 */

"""

feature_ajax = """
try {
    require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';
    include_file('core', 'authentification', 'php');

    if (!isConnect('admin')) {
        throw new \\Exception(__('401 - Accès non autorisé', __FILE__));
    }

    ajax::init();

    throw new \\Exception(__('Aucune méthode correspondante à : ', __FILE__) . 
    init('action'));
    /*     * *********Catch exeption*************** */
} catch (\\Exception $e) {
    ajax::error(displayException($e), $e->getCode());
}
"""

feature_cmd_class = """
require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';

class PluginNameCmd extends cmd
{
    public function execute($_options = array())
    {

    }
}
"""

feature_core_class = """
require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';

class PluginName extends eqLogic
{

}
"""

wizard_configuration = """
require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';
include_file('core', 'authentification', 'php');
if (!isConnect()) {
    include_file('desktop', '404', 'php');
    die();
}
"""

wizard_core_class = """
/* * ***************************Includes********************************* */
require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';
require_once 'PluginNameCmd.class.php';

class PluginName extends eqLogic
{
    /*     * *************************Attributs****************************** */



    /*     * ***********************Methode static*************************** */

    /*
     * Fonction exécutée automatiquement toutes les minutes par Jeedom
      public static function cron() {

      }
     */


    /*
     * Fonction exécutée automatiquement toutes les heures par Jeedom
      public static function cronHourly() {

      }
     */

    /*
     * Fonction exécutée automatiquement tous les jours par Jeedom
      public static function cronDaily() {

      }
     */



    /*     * *********************Méthodes 
    d'instance************************* */

    public function preInsert()
    {
        
    }

    public function postInsert()
    {
        
    }

    public function preSave()
    {
        
    }

    public function postSave()
    {
        
    }

    public function preUpdate()
    {
        
    }

    public function postUpdate()
    {
        
    }

    public function preRemove()
    {
        
    }

    public function postRemove()
    {
        
    }

    /*
     * Non obligatoire mais permet de modifier l'affichage du widget si vous 
     en avez besoin
      public function toHtml($_version = 'dashboard') {

      }
     */

    /*
     * Non obligatoire mais ca permet de déclencher une action après 
     modification de variable de configuration
      public static function postConfig_<Variable>() {
      }
     */

    /*
     * Non obligatoire mais ca permet de déclencher une action avant 
     modification de variable de configuration
      public static function preConfig_<Variable>() {
      }
     */

    /*     * **********************Getteur Setteur*************************** */
}
"""

wizard_core_cmd_class = """
/* * ***************************Includes********************************* */
require_once dirname(__FILE__) . '/../../../../core/php/core.inc.php';

class PluginNameCmd extends cmd
{
    /*     * *************************Attributs****************************** */
    /*     * ***********************Methode static*************************** */
    /*     * *********************Methode d'instance************************* */
    /*
     * Non obligatoire permet de demander de ne pas supprimer les commandes 
     même si elles ne sont pas dans la nouvelle configuration de l'équipement 
     envoyé en JS
      public function dontRemoveCmd() {
      return true;
      }
     */

    public function execute($_options = array())
    {
        
    }

    /*     * **********************Getteur Setteur*************************** */
}
"""

wizard_desktop_php = """
if (!isConnect('admin')) {
    throw new Exception('{{401 - Accès non autorisé}}');
}
"""

wizard_install = """
require_once dirname(__FILE__) . '/../../../core/php/core.inc.php';

function PluginName_install() {
    
}

function PluginName_update() {
    
}


function PluginName_remove() {
    
}
"""


#######################
# Classes utilitaires #
#######################
class File(object):
    """
    Librairie pour la gestion des fichiers
    """

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
        sed_replace_pattern = "sed -i'' 's/{}/{}/g' {} 2> /dev/null"
        if 'darwin' in sys.platform: # pragma: no cover
            sed_replace_pattern = "sed -i '' 's/{}/{}/g' {} 2> /dev/null"

        os.system(sed_replace_pattern.format(regexp, replacement, target_file))

    @staticmethod
    def replace_in_file(target_file, old_name, new_name):
        """Remplace l'ancien nom par le nouveau
        :param target_file: Fichier à traiter
        :param old_name:    Ancien nom du plugin
        :param new_name:    Nouveau nom du plugin
        :type target_file:  str
        :type old_name:     str
        :type new_name:     str
        """
        File.sed_replace(old_name, new_name, target_file)
        File.sed_replace(old_name[0].lower() + old_name[1:], new_name[
            0].lower() + new_name[1:], target_file)
        File.sed_replace(old_name.lower(), new_name.lower(), target_file)
        File.sed_replace(old_name.upper(), new_name.upper(), target_file)
        File.sed_replace(old_name.capitalize(),
                         new_name.capitalize(),
                         target_file)

    @staticmethod
    def create_php_file(content, dest_file):
        """
        Créé un fichier PHP et son en-tête puis ajoute le contenu.
        :param content:   Contenu PHP
        :param dest_file: Fichier destination
        """
        with open(dest_file, 'w') as dest:
            dest.write(php_header)
            dest.write(content)

    @staticmethod
    def create_php_file_and_replace(content, dest_file, old_name, new_name):
        """
        Créé un fichier PHP et son en-tête, ajoute le contenu, puis remplace
        les valeurs nécessaires.
        :param content:   Contenu PHP
        :param dest_file: Fichier destination
        :param old_name:  Ancien nom du plugin
        :param new_name:  Nouveau nom du plugin
        """
        File.create_php_file(content, dest_file)
        File.replace_in_file(dest_file, old_name, new_name)

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
    def add_line_under(path_file, needle, line_to_add):
        """
        Ajoute une ligne après que le champ needle est été trouvé
        :param path_file:   Chemin du fichier à traiter
        :param needle:      Elément à rechercher
        :param line_to_add: Contenu de la ligne à ajouter
        :return:
        """
        result = False
        lines = []
        with open(path_file, 'r') as core_file_content:
            lines = core_file_content.readlines()
        output = []
        for line in lines:
            output.append(line)
            if needle in line and not result:
                output.append(line_to_add + '\n')
                result = True
        with open(path_file, 'w') as core_file_content:
            for line in output:
                core_file_content.write(line)
        return result

    @staticmethod
    def write_json_file(file_path, json_data):
        """
        Ecrit le fichier au format JSON
        :param file_path: Chemin du fichier
        :param json_data: Données à écrire
        :type file_path:  str
        :type json_data:  dict
        :return:          True si l'écriture à réussie
        :rtype:           bool
        """
        result = False
        with open(file_path, 'w') as dest:
            if sys.version_info[0] < 3: # pragma: no cover
                dump = json.dumps(json_data, sort_keys=True, indent=4,
                                  ensure_ascii=False)
                dump = dump.encode('utf-8').decode('string-escape')
            else:
                dump = json.dumps(json_data, sort_keys=True, indent=4)
                dump = dump.encode('utf-8').decode('unicode-escape')
            dest.write(dump + '\n')
            result = True
        return result


class IO(object):
    """
    Librairie pour la gestion des entrées sorties
    """

    # Message afficher pour sortir du menu
    cancel_menu = 'Sortir'
    # Message affiché lors d'un choix
    choice_prompt = 'Choix : '
    # Message affiché lors d'un mauvais choix
    bad_choice = 'Mauvais choix'
    ############################
    # Couleur pour l'affichage #
    ############################
    red_color = '\033[31m'
    yellow_color = '\033[93m'
    green_color = '\033[92m'
    end_color = '\033[0m'

    @staticmethod
    def print_error(msg):
        """Affiche un message d'erreur
        :params msg: Message à afficher
        :type msg:   str
        """
        print(IO.red_color + '/' + IO.yellow_color + '!' + IO.red_color + '\\' +
              IO.end_color + ' ' + msg)

    @staticmethod
    def print_success(msg):
        """Affiche un message de confirmation
        :params msg: Message à afficher
        :type msg:   str
        """
        print(IO.green_color + 'v' + IO.end_color + ' ' + msg)

    @staticmethod
    def is_string(obj):
        """Test si une variable est une chaine de caractères
        :params obj: Objet à tester
        :return:     True si l'object est une chaine de caractères
        :rtype:      bool
        """
        str_type = str

        if sys.version_info[0] < 3: # pragma: no cover
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
        if sys.version_info[0] < 3: # pragma: no cover
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


class Jeedom(object):
    """
    Librairie pour la gestion des informations spécifiques à Jeedom
    """

    @staticmethod
    def ask_for_i18n_folder_creation(i18n_path):
        """
        Demande pour ajouter le répertoire de traduction
        :param i18n_path: Chemin du plugin
        :type i18n_path:  str
        """
        if not os.path.exists(i18n_path):
            answer = IO.ask_y_n('Voulez-vous créer le répertoire core/i18n ?')
            if answer == 'o':
                os.mkdir(i18n_path)

    @staticmethod
    def add_language(plugin_path):
        """
        Ajout un language
        :param plugin_path: Chemin du plugin
        :type plugin_path:  str
        :return:            True si la traduction a été rajoutée
        :rtype:             bool
        """
        i18n_path = Jeedom.get_i18n_path(plugin_path)
        i18n_list = filter(lambda item: not item.startswith('.'),
                           os.listdir(i18n_path))
        if i18n_list:
            print('Liste des traductions présentes : ')
            for i18n in i18n_list:
                print(' - ' + i18n)
        loop = True
        language = ''
        while loop:
            language = IO.get_user_input('Nom de la traduction : ')
            if language == '':
                loop = False
            elif Jeedom.is_valid_i18n_name(language):
                if language + '.json' in os.listdir(i18n_path):
                    IO.print_error(language + ' existe déjà.')
                else:
                    loop = False
            else:
                IO.print_error('La langue doit être au format fr_FR.')
        if language != '':
            scan_data = Jeedom.scan_for_strings(plugin_path)
            json_data = Jeedom.merge_i18n_json(plugin_path, {}, scan_data)
            File.write_json_file(i18n_path + os.sep + language + '.json',
                                 json_data)
            IO.print_success('La langue ' + language + ' a été ajoutée')

    @staticmethod
    def get_i18n_path(plugin_path):
        """
        Renvoie le chemin du répertoire contenant les traductions du plugin
        :return: Chemin vers le répertoire des traductions
        :rtype:  str
        """
        return os.path.join(plugin_path, 'core', 'i18n')

    @staticmethod
    def merge_i18n_json(plugin_path, base_json, scan_data):
        """
        Fusionne les anciennes données avec les nouvelles
        :param plugin_path: Chemin du plugin
        :param base_json:   Données présentes
        :param scan_data:   Données scannées
        :type plugin_path:  str
        :type base_json:    dict
        :type scan_data:    List(dict)
        :return:            Données fusionnées
        :rtype:             dict
        """
        for data in scan_data:
            file_path = Jeedom.transform_path_to_i18n_path(plugin_path,
                                                           data['file_path'])
            # Décode l'unicode si besoin
            if not isinstance(file_path, str): # pragma: no cover
                file_path = file_path.encode('ascii')

            # Création du dictionnaire vide
            if file_path not in base_json.keys():
                base_json[file_path] = {}

            # Ajoute les éléments
            for item in data['items']:
                if item not in base_json[file_path].keys():
                    base_json[file_path][item] = item
            # Renomme la clé pour Jeedom
            base_json[file_path] = base_json.pop(file_path)
        return base_json

    @staticmethod
    def transform_path_to_i18n_path(plugin_path, file_path):
        """
        Transforme le chemin pour qu'il soit compatible avec Jeedom
        :param plugin_path: Chemin du plugin
        :param file_path:   Chemin du fichier
        :type plugin_path:  str
        :type file_path:    str
        :return:     Chemin converti
        :rtype:      str
        """
        file_path_striped = file_path.replace(plugin_path, '')
        normal_path = 'plugins' + os.sep + os.path.basename(plugin_path) + \
                      os.sep + file_path_striped
        # En fonction du path fournit, il peut y avoir des doublons
        normal_path = normal_path.replace('//', '/')
        return normal_path  # .replace('/', '\/')

    @staticmethod
    def scan_for_strings(path, result=None):
        """
        Parcourt un répertoire à la recherche de chaines à traduire
        :param path:   Chemin du répertoire à parcourir
        :param result: Résultat compléter par recursion
        :type path:    str
        :type result:  list
        :return:       Liste des chaines à traduire
        :rtype:        list
        """
        if result is None:
            result = []
        for item in os.listdir(path):
            item_path = path + os.sep + item
            if os.path.isdir(item_path):
                Jeedom.scan_for_strings(item_path, result)
            else:
                if item.endswith('php'):
                    content = Jeedom.scan_file_for_strings(item_path)
                    if content:
                        result.append({
                            'file_path': item_path,
                            'items': list(set(content))
                        })
        return result

    @staticmethod
    def scan_file_for_strings(file_path):
        """
        Parcourt les fichiers à la recherche de chaînes à traduire
        :param file_path: Fichier à parcourir
        :type file_path:  str
        :return:          Liste des chaines à traduire
        :rtype:           list
        """
        result = []
        with open(file_path, 'r') as file_content:
            readed_content = file_content.read()
            # noinspection RegExpRedundantEscape
            result.extend(re.findall('\\{\\{(.*?)\\}\\}', readed_content))
            result.extend(re.findall('__\\(\'(.*?)\'', readed_content))
        result.extend(re.findall('__\\("(.*?)"', readed_content))
        return result

    @staticmethod
    def is_valid_i18n_name(name):
        """
        Test si la langue est au bon format
        :param name: Nom à tester
        :type name:  str
        :return:     True si le format est correct
        :rtype:      bool
        """
        result = False
        re_search = re.search('^[a-z]{2}_[A-Z]{2}$', name)
        if re_search is not None:
            result = True
        return result


class MethodData:
    """
    Classe contenant les informations d'une méthode
    """
    class_file_path = ''
    class_name = ''
    method_name = ''
    method_visibility = 'public'
    method_is_static = False
    method_comment = ''
    method_params = ''

    def get_method_declaration(self):
        """Obtenir la déclaration de la classe dans le fichier
        """
        return 'class ' + self.class_name + ' '

    def get_method_func(self):
        """Obtenir la déclaration de la méthode données
        """
        output = '\n'
        if self.method_comment != '':
            output += '    /**\n     * ' + self.method_comment + '\n     */\n'
        output += '    ' + self.method_visibility + ' '
        if self.method_is_static:
            output += 'static '
        output += 'function ' + self.method_name + '('
        if self.method_params != '':
            output += self.method_params
        output += ')\n    {\n\n    }\n'
        return output


class PHPFile(object):
    """
    Librairie pour la gestion des fichiers PHP
    """

    @staticmethod
    def add_method(method_data):
        """Ajoute la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        result = False
        if os.path.exists(method_data.class_file_path):
            if PHPFile.check_class(method_data.class_file_path,
                                   method_data.class_name):
                if not PHPFile.check_if_method_exists(
                        method_data.class_file_path,
                        method_data.method_name):
                    result = PHPFile.write_method_in_class(method_data)
                else:
                    IO.print_error('La méthode existe déjà')
            else:
                IO.print_error('La classe n\'existe pas')
        else:
            IO.print_error('Le fichier global n\'existe pas')
        return result

    @staticmethod
    def check_class(class_file_path, class_name):
        """Test si la classe existe
        :params class_file_path: Répertoire de la classe
        :params class_name:      Nom de la classe
        :type class_file_path:   str
        :type class_name:        str
        :return:                 True si la classe existe
        :rtype:                  bool
        """
        result = False
        try:
            with open(class_file_path) as file_content:
                if class_name in file_content.read():
                    result = True
        except FileNotFoundError:
            pass
        return result

    @staticmethod
    def check_if_method_exists(class_file_path, method_name):
        """Test si la classe existe
        :params class_file_path: Répertoire de la classe
        :params method_name:     Nom de la méthode
        :type class_file_path:   str
        :type method_name:       str
        :return:                 True si la méthode existe
        :rtype:                  bool
        """
        result = False
        with open(class_file_path) as file_content:
            if method_name + '()' in file_content.read():
                result = True
        return result

    @staticmethod
    def check_and_write_class(file_path, class_name, extends=None):
        """Lancer l'écriture d'une nouvelle classe
        :params file_path:  Chemin du fichier devant contenir la classe
        :params class_name: Nom de la classe à créer
        :params extends:    Nom de la classe héritée
        :type file_path:    str
        :type class_name:   str
        :type extends:      str
        """
        if PHPFile.write_class(file_path, class_name, extends):
            IO.print_success('La classe ' + class_name + ' a été créée')
        else:
            IO.print_success('La classe ' + class_name +
                             ' n\'a pas pu être créée')

    @staticmethod
    def write_class(file_path, class_name, extends=None):
        """Ajoute une classe à un fichier PHP
        :params file_path:  Chemin du fichier devant contenir la classe
        :params class_name: Nom de la classe à créer
        :params extends:    Nom de la classe héritée
        :type file_path:    str
        :type class_name:   str
        :type extends:      str
        """
        result = False
        add_php_tag = False
        if not os.path.exists(file_path):
            add_php_tag = True
        with open(file_path, 'a') as php_file:
            if add_php_tag:
                php_file.write('<?php\n')
            class_declaration = '\n\nclass ' + class_name
            if extends is not None:
                class_declaration += ' extends ' + extends + '\n{\n\n}\n'
            php_file.write(class_declaration)
            result = True
        return result

    @staticmethod
    def write_method_in_class(method_data):
        """Ecrit la méthode à la classe
        :params method_data: Données de la méthode
        :type method_data:   MethodData
        """
        output = []
        bracket_count = 0
        start_bracket_count = False
        method_added = False
        class_declaration = 'class ' + method_data.class_name
        try:
            content = None
            with open(method_data.class_file_path,
                      'r') as class_file_content:
                content = class_file_content.readlines()
            # Recherche de la dernière accolade de la classe
            for line in content:
                if not start_bracket_count and (
                        class_declaration in line or
                        class_declaration == line):
                    start_bracket_count = True
                if not method_added and start_bracket_count:
                    if '{' in line:
                        bracket_count += 1
                    if '}' in line:
                        bracket_count -= 1
                        # Dernière accolade de la classe
                        if bracket_count == 0:
                            output.append(method_data.get_method_func())
                            method_added = True
                output.append(line)
            # Réécrit le fichier
            with open(method_data.class_file_path,
                      'w') as class_file_content:
                for line in output:
                    class_file_content.write(line)
        except FileNotFoundError:
            pass
        return method_added


class Tools(object):
    """
    Classe facilitant l'initialisation de l'outil
    """

    @staticmethod
    def show_help():
        """Affiche l'aide
        """
        print(sys.argv[0] + ' [PLUGIN-NAME] [--help]')
        print('  --help :      Affiche de menu.')
        print('  PLUGIN-NAME : Indiquer le nom du plugin à modifier.')

    @staticmethod
    def parse_args(argv):
        """Analyse les arguments
        :params argv: Arguments
        :type argv:   list
        :return:      Liste ou None si le programme doit quitter
        """
        result = ''
        if '--help' in argv or len(argv) > 2:
            Tools.show_help()
            result = None
        elif len(argv) > 1:
            result = argv[1]

        return result

    @staticmethod
    def is_plugin_dir(path):
        """Test si le répertoire contient un plugin
        :param path: Chemin à tester
        :return:     True si c'est un plugin
        """
        info_path = os.path.join(path, 'plugin_info', 'info.json')
        return os.path.exists(info_path)

    @staticmethod
    def get_plugin_data(path):
        """Lire les informations du plugin
        :param path: Chemin du plugin
        :return:     Informations du plugin
        :rtype:      dict
        """
        result = None
        info_path = os.path.join(path, 'plugin_info', 'info.json')
        try:
            with open(info_path) as info_json:
                info_json_data = json.load(info_json)
                if 'id' in info_json_data.keys():
                    result = [path, info_json_data['id']]
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            pass
        return result

    @staticmethod
    def get_plugins_in_dir(path):
        """Obtenir la liste des plugins dans un répertoire
        :param path: Répertoire parent
        :return:     Liste des plugins
        :rtype:      list
        """
        result = []
        abspath = os.path.abspath(path)
        for item in os.listdir(abspath):
            item_path = abspath + os.sep + item
            if os.path.isdir(item_path):
                if Tools.is_plugin_dir(item_path):
                    plugin = Tools.get_plugin_data(item_path)
                    if plugin is not None:
                        result.append(plugin)
        return result


#####################
# Classes des menus #
#####################
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
        return_value = False
        method_name = 'action_' + str(number)
        # DEBUG
        # method = getattr(self, method_name)
        # return_value = method()
        try:
            method = getattr(self, method_name)
            return_value = method()
        except AttributeError:
            IO.print_error(self.bad_command)
        return return_value


class FeaturesMenu(BaseMenu):
    """Classe du menu permettant d'ajouter des fonctionnalités.
    """
    title = 'Ajouter des fonctionnalités'
    menu = ['Ajouter la classe générale',
            'Ajouter la classe des commandes',
            'Ajouter une méthode cron',
            'Ajouter la réponse aux requêtes Ajax']
    plugin_name = ''
    plugin_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :param plugin_path: Répertoire du plugin
        :param plugin_name: Nom du plugin
        :type plugin_path:  str
        :type plugin_name:  str
        """
        if sys.version_info[0] < 3: # pragma: no cover
            super(FeaturesMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Créer la classe principale
        """
        self.add_core_class()

    def action_2(self):
        """Créer la classe de gestion des commandes
        """
        self.add_cmd_class()

    def action_3(self):
        """Ajouter une tâche cron au plugin
        """
        self.add_cron()

    def action_4(self):
        """Créer la classe de gestion des requêtes Ajax
        """
        self.add_ajax()

    def add_core_class(self):
        """
        Ajoute la classe core d'un plugin
        """
        target_file = os.path.join(self.plugin_path, 'core', 'class',
                                   self.plugin_name + '.class.php')
        if os.path.exists(target_file):
            IO.print_error('Le fichier existe déjà')
        else:
            File.create_php_file_and_replace(feature_core_class, target_file,
                                             'PluginName',
                                             self.plugin_name)
            IO.print_success('Le fichier a été créé.')

    def add_cmd_class(self):
        """
        Ajoute la classe cmd d'un plugin
        """
        target_core_file = os.path.join(self.plugin_path, 'core', 'class',
                                        self.plugin_name + '.class.php')
        target_cmd_file = os.path.join(self.plugin_path, 'core', 'class',
                                       self.plugin_name + 'Cmd.class.php')
        if self.is_core_class_exists(target_core_file):
            separated = IO.ask_y_n('Utiliser des fichiers séparés ?')
            if separated == 'o':
                self.insert_require_in_core(target_core_file)
                File.create_php_file_and_replace(feature_cmd_class,
                                                 target_cmd_file,
                                                 'PluginName', self.plugin_name)
            else:
                PHPFile.write_class(target_core_file, self.plugin_name + 'Cmd',
                                    'cmd')

                method_data = MethodData()
                method_data.class_file_path = target_core_file
                method_data.class_name = self.plugin_name + 'Cmd'
                method_data.method_name = 'execute'
                method_data.method_params = '$_options = array()'
                method_data.method_visibility = 'public'
                PHPFile.write_method_in_class(method_data)

    def is_core_class_exists(self, core_file):
        """
        Test si le fichier core du plugin existe.
        :param core_file:   Chemin du fichier core
        :type core_file:    str
        :return:            True si le fichier de la classe a été créée
        :rtype:             bool
        """
        result = False
        if os.path.exists(core_file):
            if PHPFile.check_class(core_file, self.plugin_name):
                result = True
        else:
            create = IO.ask_y_n(
                'Le fichier de la classe principale n\'existe pas, '
                'voulez-vous le créer ?')
            if create == 'o':
                self.add_core_class()
                result = True
        return result

    def insert_require_in_core(self, core_file):
        """
        Ajoute l'inclusion du fichier
        :param core_file:   Chemin du fichier core
        :type core_file:    str
        """
        File.add_line_under(core_file, 'require_once dirname(__FILE__)',
                            'require_once \'./' + self.plugin_name +
                            'Cmd.class.php\';\n')

    def add_cron(self):
        """
        Ajoute une tâche cron au plugin
        :return:
        """
        core_file_path = os.path.join(self.plugin_path, 'core', 'class',
                                      self.plugin_name +
                                      '.class.php')

        crons_titles = [
            'Toutes les minutes',
            'Toutes les 5 minutes',
            'Toutes les 15 minutes',
            'Toutes les 30 minutes',
            'Toutes les heures',
            'Tous les jours'
        ]
        crons_functions = [
            'cron',
            'cron5',
            'cron15',
            'cron30',
            'cronHourly',
            'cronDaily'
        ]

        choice = IO.get_menu_choice(crons_titles, 'Choix de la récurrence')
        if choice >= 0:
            method_data = MethodData()
            method_data.class_file_path = core_file_path
            method_data.class_name = self.plugin_name
            method_data.method_name = crons_functions[choice]
            method_data.method_is_static = True
            method_data.method_comment = crons_titles[choice]
            if PHPFile.add_method(method_data):
                IO.print_success('La méthode ' + method_data.method_name +
                                 ' a été ajoutée')

    def add_ajax(self):
        """
        Ajoute la classe pour traiter les requêtes AJAX
        """
        ajax_path = os.path.join(self.plugin_path, 'core', 'ajax')
        ajax_file_path = ajax_path + os.sep + self.plugin_name + '.ajax.php'
        if not os.path.exists(ajax_path):
            os.mkdir(ajax_path)
        if os.path.exists(ajax_file_path):
            with open(ajax_file_path) as ajax_content:
                if 'ajax::init' in ajax_content.read():
                    IO.print_error('Le fichier existe déjà')
        else:
            File.create_php_file(feature_ajax, ajax_file_path)
            IO.print_success('Le fichier a été créé')


class I18nMenu(BaseMenu):
    """
    Menu de l'internationalisation
    """
    title = 'Gestion des traductions'
    menu = ['Ajouter une traduction',
            'Mettre à jour les fichiers']
    plugin_name = ''
    plugin_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :param plugin_path: Répertoire du plugin
        :param plugin_name: Nom du plugin
        :type plugin_path:  str
        :type plugin_name:  str
        """
        if sys.version_info[0] < 3:
            super(I18nMenu, self).__init__()
        else:
            super().__init__()
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """
        Ajout d'un répertoire pour les traductions
        :return: True si une langue a été rajoutée
        :rtype:  bool
        """
        self.add_language()

    def action_2(self):
        """
        Met à jour les traductions
        """
        self.update_languages()

    def add_language(self):
        """
        Ajoute la classe pour traiter les requêtes AJAX
        """
        i18n_path = Jeedom.get_i18n_path(self.plugin_path)
        if not os.path.exists(i18n_path):
            Jeedom.ask_for_i18n_folder_creation(i18n_path)
        if os.path.exists(i18n_path):
            Jeedom.add_language(self.plugin_path)

    def update_languages(self):
        """
        Ajoute la classe pour traiter les requêtes AJAX
        """
        i18n_path = Jeedom.get_i18n_path(self.plugin_path)
        if os.path.exists(i18n_path):
            i18n_list = os.listdir(i18n_path)
            if i18n_list:
                scan_data = Jeedom.scan_for_strings(self.plugin_path)
                for i18n in i18n_list:
                    json_data = {}
                    try:
                        with open(i18n_path + os.sep + i18n) as i18n_content:
                            json_data = json.loads(i18n_content.read())
                    except ValueError:
                        pass
                    json_data = Jeedom.merge_i18n_json(self.plugin_path,
                                                       json_data,
                                                       scan_data)
                    # Json retire le \ avant les / à la lecture
                    parsed_json_data = {}
                    for key in json_data.keys():
                        parsed_json_data[key.replace('/', '\\/')] = json_data[
                            key]
                    File.write_json_file(i18n_path + os.sep + i18n,
                                         parsed_json_data)
            else:
                IO.print_error('Aucune traduction')
        else:
            IO.print_error('Aucun répertoire pour les traductions')


class InfoMenu(BaseMenu):
    """Classe du menu permettant de modifier les informations du plugin.
    """
    title = 'Modifier les informations du plugin'
    menu = ['Modifier le nom affiché dans les menus',
            'Modifier la description',
            'Modifier la licence',
            'Modifier l\'auteur',
            'Modifier la catégorie']
    plugin_name = ''
    plugin_path = ''
    plugin_info_path = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        :params plugin_name: Nom du plugin
        :type plugin_name:   str
        """
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path
        self.plugin_info_path = os.path.join(plugin_path, 'plugin_info',
                                             'info.json')

    def action_1(self):
        """Modifier le nom affiché dans les menus
        """
        name = IO.get_user_input('Nouveau nom : ')
        self.replace_info_json('name', name)

    def action_2(self):
        """Modifier la description
        """
        description = IO.get_user_input('Nouvelle description : ')
        self.replace_info_json('description', description)

    def action_3(self):
        """Modifier la licence
        """
        licence = IO.get_user_input('Nouvelle licence : ')
        self.replace_info_json('licence', licence)

    def action_4(self):
        """Modifier l'auteur
        """
        author = IO.get_user_input('Nouvel auteur : ')
        self.replace_info_json('author', author)

    def action_5(self):
        """Modifier la catégorie
        """
        category = IO.get_menu_choice(config['jeedom_categories'],
                                      'Choix de la catégorie')
        if category >= 0:
            self.replace_info_json('category',
                                   config['jeedom_categories'][category])

    def replace_info_json(self, key, new_value):
        """Remplace les informations dans le fichier info.json
        :params key:       Clé à modifier
        :params new_value: Nouvelle valeur de la clé
        :type key:         str
        :type new_value:   str
        """
        info_json_path = os.path.join(self.plugin_path, 'plugin_info',
                                      'info.json')
        if os.path.exists(info_json_path):
            File.sed_replace(
                '\\("' + key + '"[ ]\\{0,1\\}: "\\).*\\("\\)',
                '\\1' + new_value + '\\2',
                info_json_path)
            IO.print_success('L\'information a été modifiée.')
        else:
            IO.print_error('Le fichier info.json n\'a pas été trouvé')


class RootMenu(BaseMenu):
    """
    Menu principal de l'outil.
    """
    title = 'Outil de gestion d\'un plugin'
    menu = ['Modifier l\'identifiant du plugin',
            'Modifier les informations du plugin',
            'Ajouter des fonctionnalités',
            'Gestion des traductions']
    plugin_path = ''
    plugin_name = ''

    def __init__(self, plugin_path, plugin_name):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params plugin_name: Nom du plugin
        :params plugin_path: Chemin du plugin
        :type plugin_name:   str
        :type plugin_path:   str
        """
        self.plugin_name = plugin_name
        self.plugin_path = plugin_path

    def action_1(self):
        """Renomme le plugin
        Modifie le nom des répertoires, des fichiers ainsi que le contenu
        des fichiers.
        """
        new_name = IO.get_user_input('Nouveau nom du plugin : ')
        self.rename_plugin(new_name)
        self.plugin_name = new_name
        self.plugin_path = 'plugin-' + new_name

    def action_2(self):
        """Lance le menu de modification des informations
        """
        info_menu = InfoMenu(self.plugin_path, self.plugin_name)
        info_menu.start()

    def action_3(self):
        """Lance le menu de modification des informations
        """
        features_menu = FeaturesMenu(self.plugin_path, self.plugin_name)
        features_menu.start()

    def action_4(self):
        """Lance le menu de gestion des traductions
        """
        i18n_menu = I18nMenu(self.plugin_path, self.plugin_name)
        i18n_menu.start()

    def rename_plugin(self, new_name):
        """Renomme le plugin
        Modifie le nom des répertoires, des fichiers ainsi que le contenu
        des fichiers.
        """
        result = False
        path = os.path.abspath(self.plugin_path)
        new_path = os.path.abspath(path + os.sep + '..' + os.sep + 'plugin-' +
                                   new_name)
        if os.path.exists(path):
            if not os.path.exists(new_path):
                # Renomme le répertoire racine du plugin
                os.rename(path, new_path)
                # Renomme le contenu du plugin
                self.start_rename_plugin(new_path, self.plugin_name, new_name)
                IO.print_success(
                    'Le plugin ' + self.plugin_name + ' a été renommé en ' +
                    new_name)
                result = True
            else:
                IO.print_error('Le répertoire  plugin-' + new_name +
                               ' existe déjà')
                result = False
        else:
            IO.print_error('Le plugin ' + path + ' n\'a pas été trouvé')
            result = False
        return result

    def start_rename_plugin(self, current_path, old_name, new_name):
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
                    item = self.rename_item(current_path + os.sep,
                                            item,
                                            old_name,
                                            new_name)
                if os.path.isdir(current_path + os.sep + item):
                    self.start_rename_plugin(current_path + os.sep + item,
                                             old_name,
                                             new_name)
                else:
                    # Remplacement des occurences dans le fichier
                    File.replace_in_file(
                        current_path + os.sep + item, old_name, new_name)

    @staticmethod
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


class WizardMenu(BaseMenu):
    """
    Classe du menu de l'assistant
    """
    plugins_list = []
    actions = []

    def __init__(self, initial_plugins_list):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params initial_plugins_list: Liste des plugins disponibles
        :type initial_plugins_list:   List
        """
        # Configuration du menu
        # Premier choix : Assistant
        self.plugins_list = initial_plugins_list
        self.actions = []
        self.menu = []
        self.menu.append('Démarrer l\'assistant')
        self.actions.append([WizardMenu.start_wizard, None])
        # Recherche si le plugin template existe déjà
        add_template_download = True
        for plugin in self.plugins_list:
            if 'template' in plugin[1] or 'Template' in plugin[1]:
                add_template_download = False
        if add_template_download:
            self.menu.append('Télécharger le plugin ExtraTemplate')
            self.actions.append([WizardMenu.git_extratemplate, None])
        # Ajout de la liste des plugins dans le répertoire
        for plugin in self.plugins_list:
            self.menu.append('Modifier le plugin ' + plugin[1])
            self.actions.append([WizardMenu.start_tools, plugin])

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
                # if self.actions[user_choice][1] is None:
                #     return_value = self.actions[user_choice][0]()
                # else:
                #     return_value = self.actions[user_choice][0](
                #     self.actions[user_choice][1])
                try:
                    if self.actions[user_choice][1] is None:
                        return_value = self.actions[user_choice][0]()
                    else:
                        return_value = self.actions[user_choice][0](
                            self.actions[user_choice][1])
                except AttributeError:
                    IO.print_error(self.bad_command)
                    return_value = False
        return return_value

    @staticmethod
    def start_wizard():
        """Lance l'assistant
        """
        plugin_data = WizardMenu.ask_plugin_informations()
        if plugin_data is not None:
            WizardMenu.create_folder_struct(plugin_data)
            WizardMenu.gen_info_json(plugin_data)
            WizardMenu.gen_installation_php(plugin_data)
            WizardMenu.gen_configuration(plugin_data)
            WizardMenu.gen_desktop_php(plugin_data)
            WizardMenu.gen_core_php(plugin_data)
        exit(0)

    @staticmethod
    def ask_plugin_informations():
        """Obtenir les informations pour le futur plugin.
        :return: Informations compilées
        :rtype:  dict
        """
        data = {}

        print(' - Le nom apparait dans l\'interface de Jeedom')
        data['name'] = IO.ask_with_default('Nom',
                                           config['default_package_name'])
        plugin_id = data['name'].lower().replace(' ', '_').capitalize()

        print(' - L\'identifiant différencie le plugin des autres.')
        data['id'] = IO.ask_with_default('ID', plugin_id)

        # Test si le répertoire existe à ce niveau pour éviter la suite du
        # questionnaire
        if os.path.exists('plugin-' + data['id']):
            IO.print_error('Le répertoire du plugin existe déjà')
            data = None
        else:
            data['description'] = IO.get_user_input(
                'Description (optional) : ')
            data['license'] = IO.ask_with_default('Licence', 'GPL')
            data['author'] = IO.get_user_input('Auteur (optionnal) : ')
            data['require'] = IO.ask_with_default('Version requise de Jeedom',
                                                  '3.0')
            data['version'] = IO.ask_with_default('Version du plugin', '1.0')
            category_choice = IO.get_menu_choice(config['jeedom_categories'],
                                                 'Choix de la catégorie', False)
            data['category'] = config['jeedom_categories'][category_choice]
            configuration = None

            if IO.ask_y_n('Générer la page de configuration ?', 'o') == 'o':
                configuration = []
                loop = True
                menu = ['Champ texte',
                        'Case à cocher']
                values = ['text',
                          'checkbox']
                while loop:
                    print('Ajouter un champ ?')
                    result = IO.get_menu_choice(menu)
                    if result == -1:
                        loop = False
                    else:
                        label = IO.get_user_input('Label : ')
                        code = IO.get_user_input('Code : ')
                        configuration.append({
                            'type': values[result],
                            'label': label,
                            'code': code})
            data['configuration'] = configuration
            data['documentation_language'] = IO.ask_with_default(
                'Langue de la documentation (fr_FR, en_US)', 'fr_FR')

            # Generate shortcuts
            plugin_path = 'plugin-' + data['id']
            data[
                'plugin_info_path'] = plugin_path + os.sep + 'plugin_info' + \
                                      os.sep
            data['core_path'] = plugin_path + os.sep + 'core' + os.sep
            data['desktop_path'] = plugin_path + os.sep + 'desktop' + os.sep

        return data

    @staticmethod
    def create_folder_struct(plugin_data):
        """Créé la structure de répertoires
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        subfolders = [
            'core',
            'desktop',
            'docs',
            'plugin_info'
        ]
        desktop_subfolders = [
            'css',
            'js',
            'modal',
            'php'
        ]
        core_subfolders = [
            'ajax',
            'class',
            'php',
        ]
        # Parent folder
        plugin_dir = 'plugin-' + plugin_data['id']
        os.mkdir(plugin_dir)
        # First level subfolders
        for subfolder in subfolders:
            os.mkdir(plugin_dir + os.sep + subfolder)
        # Desktop subfolders
        for desktop_subfolder in desktop_subfolders:
            os.mkdir(
                plugin_dir + os.sep + 'desktop' + os.sep + desktop_subfolder)
        # Core subfolders
        for core_subfolder in core_subfolders:
            os.mkdir(plugin_dir + os.sep + 'core' + os.sep + core_subfolder)
        # license file
        license_file = open(plugin_dir + os.sep + 'LICENSE', 'w')
        license_file.close()
        # Documentation folder
        os.mkdir(plugin_dir + os.sep + 'docs' + os.sep +
                 plugin_data['documentation_language'])

    @staticmethod
    def gen_info_json(plugin_data):
        """Ecrit le fichier d'information du plugin
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        with open(plugin_data['plugin_info_path'] + 'info.json', 'w') as dest:
            dest.write(
                '{\n'
                '  "id": "%s",\n'
                '  "name": "%s",\n'
                '  "licence": "%s",\n'
                '  "require": "%s",\n'
                '  "version": "%s",\n'
                '  "category": "%s",\n'
                '  "hasDependency": false,\n'
                '  "hasOwnDaemon": false,\n'
                '  "maxDependancyInstallTime": 0,\n'
                '  "documentation": "%s",\n'
                '  "changelog": "%s"' % (
                    plugin_data['id'],
                    plugin_data['name'],
                    plugin_data['license'],
                    plugin_data['require'],
                    plugin_data['version'],
                    plugin_data['category'],
                    config['default_documentation_url'] % (plugin_data['id']),
                    config['default_changelog_url'] % (plugin_data['id'])
                )
            )
            if plugin_data['description'] != '':
                dest.write(
                    ',\n  "description": "%s"' % (plugin_data['description']))
            if plugin_data['author'] != '':
                dest.write(',\n  "author": "%s"' % (plugin_data['author']))
            dest.write('\n}\n')
            dest.close()

    @staticmethod
    def gen_installation_php(plugin_data):
        """Ecrit la classe d'installation du plugin dans plugin_info
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        target_file = plugin_data['plugin_info_path'] + 'install.php'
        File.create_php_file_and_replace(wizard_install, target_file,
                                         'PluginName',
                                         plugin_data['id'])

    @staticmethod
    def gen_configuration(plugin_data):
        """Ecrit le formulaire de configuration du plugin dans plugin_info
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        if plugin_data['configuration']:
            target_file = plugin_data['plugin_info_path'] + 'configuration.php'
            File.create_php_file(wizard_configuration, target_file)
            with open(target_file, 'a') as dest:
                dest.write('<form class="form-horizontal">\n  <fieldset>\n')
                for item in plugin_data['configuration']:
                    dest.write('    <div class="form-group">\n'
                               '      <label class="col-sm-3 control-label">\n'
                               '        {{%s}}\n'
                               '      </label>\n'
                               '      <div class="col-sm-9">\n'
                               '        <input class="configKey form-control" '
                               '' % (item['label']))
                    if item['type'] == 'checkbox':
                        dest.write('type="checkbox" ')
                    dest.write('data-l1key="%s" />\n'
                               '      </div>\n'
                               '    </div>\n'
                               '' % (item['code']))
                dest.write('  </fieldset>\n</form>\n')

    @staticmethod
    def gen_desktop_php(plugin_data):
        """Ecrit le fichier PHP du desktop pour le rendu
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        target_file = plugin_data['desktop_path'] + os.sep + 'php' + os.sep + \
                      plugin_data['id'] + '.php'
        File.create_php_file(wizard_desktop_php, target_file)

    @staticmethod
    def gen_core_php(plugin_data):
        """Ecrit le fichier PHP du core
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        target_file = plugin_data['core_path'] + os.sep + 'class' + os.sep + \
                      plugin_data['id'] + '.class.php'
        File.create_php_file_and_replace(wizard_core_class,
                                         target_file,
                                         'PluginName',
                                         plugin_data['id'])

        target_file = plugin_data['core_path'] + os.sep + 'class' + os.sep + \
                      plugin_data['id'] + 'Cmd.class.php'
        File.create_php_file_and_replace(wizard_core_cmd_class,
                                         target_file,
                                         'PluginName',
                                         plugin_data['id'])

    @staticmethod
    def git_extratemplate():
        """Télécharge une copie du plugin ExtraTemplate
        :params data: Inutilisé
        """
        if not os.path.exists('plugin-ExtraTemplate'):
            sys_return = os.system(
                'git clone ' + config['plugin_template_repo'] +
                ' 2> /dev/null')
            if sys_return == 0:
                IO.print_success(
                    'Le plugin plugin-ExtraTemplate a été téléchargé')
            else:
                IO.print_error('Erreur dans le téléchargement de '
                               'plugin-ExtraTemplate.')
        else:
            IO.print_error(
                'Le plugin plugin-ExtraTemplate est déjà téléchargé.')

        WizardMenu.start_tools(['plugin-ExtraTemplate', 'ExtraTemplate'])

    @staticmethod
    def start_tools(plugin_data):
        """Lance l'outil
        :params plugin_data: Tableau contenant le chemin et le nom du plugin
        :type plugin_data:   List[str]
        """
        root_menu = RootMenu(plugin_data[0], plugin_data[1])
        root_menu.start()


def start():
    """
    Point de d'entrée en mode CLI
    """

    readed_args = Tools.parse_args(sys.argv)
    if readed_args is not None:
        plugins_list = []
        if readed_args == '':
            plugins_list = Tools.get_plugins_in_dir('.')
        wizard_menu = WizardMenu(plugins_list)
        wizard_menu.start()


# Gestion des accents pour python 2
if sys.version_info[0] < 3: # pragma: no cover
    reload(sys)  # pylint: disable=undefined-variable
    sys.setdefaultencoding('utf8')  # pylint: disable=no-member

if __name__ == '__main__':
    start() # pragma: no cover
