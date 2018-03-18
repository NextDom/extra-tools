# -*- coding: utf-8 -*-
"""
Classe du menu de l'assistant
"""
import os
import sys

from .BaseMenu import BaseMenu
from .InfoMenu import InfoMenu
from .RootMenu import RootMenu


class WizardMenu(BaseMenu):
    """
    Classe du menu de l'assistant
    """
    plugins_list = []
    actions = []
    plugin_template_repo = \
        'https://github.com/Jeedom-Plugins-Extra/plugin-template.git'
    default_package_name = 'Exemple'
    default_changelog_url = \
        'https://jeedom.github.io/plugin-%s/#language#/changelog'
    default_documentation_url = \
        'https://jeedom.github.io/plugin-%s/#language#/'
    php_include_core_3 = "" \
                         "require_once dirname(__FILE__).'/../../../core/php/core.inc.php';\n\n"
    php_include_core_4 = "" \
                         "require_once dirname(__FILE__).'/../../../../core/php/core.inc.php';\n\n"
    php_header = "<?php\n\n"
    php_check_user_connect = "" \
                             "include_file('core', 'authentification', 'php');\n\n" \
                             "if (!isConnect('admin')) {\n" \
                             "    throw new Exception('{{401 - Refused access}}');\n" \
                             "}\n"

    def __init__(self, plugins_list):
        """Constructeur
        Initialise le chemin vers le fichier qui stocke le nom du plugin.
        :params plugins_list:  Liste des plugins disponibles
        :type plugins_list:    List
        """
        if sys.version_info[0] < 3:
            super(WizardMenu, self).__init__()
        else:
            super().__init__()

        # Configuration du menu
        # Premier choix : Assistant
        self.plugins_list = plugins_list
        self.menu = []
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
            self.menu.append('Modifier le plugin ' + plugin[1])
            self.actions.append([self.start_tools, plugin])

    def start(self):
        """Démarre l'affichage du menu
        """
        loop = True
        return_value = False
        while loop:
            user_choice = self.get_menu_choice(self.menu)
            if user_choice == -1:
                loop = False
            else:
                # DEBUG
                if user_choice[1] is None:
                    return_value = self.actions[user_choice][0]()
                else:
                    return_value = self.actions[user_choice][0](self.actions[user_choice][1])

#                try:
#                    return_value = self.actions[user_choice][0](
#                        self.actions[user_choice][1])
#                except AttributeError:
#                    self.print_error(self.bad_command)
#                    return_value = False
        return return_value

    def start_wizard(self):
        """Lance l'assistant
        :params data: Inutilisé
        """
        plugin_data = self.ask_plugin_informations()
        if plugin_data is not None:
            self.create_folder_struct(plugin_data)
            self.gen_info_json(plugin_data)
            self.gen_installation_php(plugin_data)
            self.gen_configuration(plugin_data)
            self.gen_desktop_php(plugin_data)
            self.gen_core_php(plugin_data)
            self.start_tools(['plugin-' + plugin_data['id'], plugin_data['id']])

    def git_template(self):
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

    @staticmethod
    def start_tools(plugin_data):
        """Lance l'outil
        :params plugin_data: Tableau contenant le chemin et le nom du plugin
        :type plugin_data:   List[str]
        """
        root_menu = RootMenu(plugin_data[0], plugin_data[1])
        root_menu.start()

    def ask_plugin_informations(self):
        """Obtenir les informations pour le futur plugin.
        :return: Informations compilées
        :rtype:  dict
        """
        data = {}

        print(' - Le nom apparait dans l\'interface de Jeedom')
        data['name'] = self.ask_with_default('Nom',
                                             self.default_package_name)
        plugin_id = data['name'].lower().replace(' ', '_').capitalize()

        print(' - L\'identifiant différencie le plugin des autres.')
        data['id'] = self.ask_with_default('ID', plugin_id)

        # Test si le répertoire existe à ce niveau pour éviter la suite du
        # questionnaire
        if os.path.exists('plugin-' + data['id']):
            self.print_error('Le répertoire du plugin existe déjà')
            data = None
        else:
            data['description'] = self.get_user_input(
                'Description (optional) : ')
            data['license'] = self.ask_with_default('Licence', 'GPL')
            data['author'] = self.get_user_input('Auteur (optionnal) : ')
            data['require'] = self.ask_with_default('Version requise de Jeedom',
                                                    '3.0')
            data['version'] = self.ask_with_default('Version du plugin', '1.0')
            category_choice = self.get_menu_choice(InfoMenu.categories, False)
            data['category'] = InfoMenu.categories[category_choice]
            configuration = None

            if self.ask_y_n('Générer la page de configuration ?', 'o') == 'o':
                configuration = []
                loop = True
                menu = ['Champ texte',
                        'Case à cocher']
                values = ['text',
                          'checkbox']
                while loop:
                    print('Ajouter un champ ?')
                    result = self.get_menu_choice(menu)
                    if result == -1:
                        loop = False
                    else:
                        label = self.get_user_input('Label : ')
                        code = self.get_user_input('Code : ')
                        configuration.append({
                            'type': values[result],
                            'label': label,
                            'code': code})
            data['configuration'] = configuration
            data['documentation_language'] = self.ask_with_default(
                'Langue de la documentation (fr_FR, en_US)', 'fr_FR')

            # Generate shortcuts
            plugin_path = 'plugin-' + data['id']
            data['plugin_info_path'] = plugin_path + os.sep + \
                                       'plugin_info' + os.sep
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

    def gen_info_json(self, plugin_data):
        """Ecrit le fichier d'information du plugin
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        with open(plugin_data['plugin_info_path'] + 'info.json', 'w') as dest:
            dest.write(
                '{\n'
                '  "id" : "%s",\n'
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
                    self.default_documentation_url % (plugin_data['id']),
                    self.default_changelog_url % (plugin_data['id'])
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
        funcs = ['install', 'update', 'remove']

        with open(plugin_data['plugin_info_path'] + 'installation.php',
                  'w') as dest:
            print('coucou')
            dest.write(WizardMenu.php_header + WizardMenu.php_include_core_3)
            for func in funcs:
                dest.write('function ' + plugin_data['id'] +
                           '_' + func + '()\n{\n\n}\n\n')

    @staticmethod
    def gen_configuration(plugin_data):
        """Ecrit le formulaire de configuration du plugin dans plugin_info
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        if plugin_data['configuration']:
            with open(plugin_data['plugin_info_path'] + 'configuration.php',
                      'w') as dest:
                dest.write(WizardMenu.php_header)
                dest.write(WizardMenu.php_include_core_3)
                dest.write(WizardMenu.php_check_user_connect)
                dest.write("?>\n")
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
        with open(plugin_data['desktop_path'] + 'php' + os.sep + plugin_data[
            'id'] + '.php',
                  'w') as dest:
            dest.write('<?php\n')
            dest.write(WizardMenu.php_check_user_connect + '\n')
            dest.close()

    @staticmethod
    def gen_core_php(plugin_data):
        """Ecrit le fichier PHP du core
        :param plugin_data: Données du plugin
        :type plugin_data:  dict
        """
        with open(plugin_data['core_path'] + 'class' + os.sep + plugin_data[
            'id'] + '.class.php',
                  'w') as dest:
            dest.write(WizardMenu.php_header+WizardMenu.php_include_core_4)
            dest.write(''
                       'class %s extends eqLogic\n{\n\n'
                       '    /*************** Attributs ***************/\n\n'
                       '    /************* Static methods ************/\n\n'
                       '    /**************** Methods ****************/\n\n'
                       '    /********** Getters and setters **********/\n\n'
                       '}\n\n'
                       'class %sCmd extends cmd\n{\n\n'
                       '    /*************** Attributs ***************/\n\n'
                       '    /************* Static methods ************/\n\n'
                       '    /**************** Methods ****************/\n\n'
                       '    public function execute($_options = array())\n'
                       '    {\n\n'
                       '    }\n\n'
                       '    /********** Getters and setters **********/\n\n'
                       '}\n' % (plugin_data['id'], plugin_data['id']))
            dest.close()
