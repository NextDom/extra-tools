#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Assistant pour la création d'un plugin
"""

import os

from libs.File import File
from libs.IO import IO


def start_wizard():
    """Lance l'assistant
    :params data: Inutilisé
    """
    config = File.read_config_data()
    templates_path = os.path.dirname(__file__) + os.sep + 'templates'
    plugin_data = ask_plugin_informations(config)
    if plugin_data is not None:
        create_folder_struct(plugin_data)
        gen_info_json(plugin_data, config)
        gen_installation_php(plugin_data, templates_path)
        gen_configuration(plugin_data, templates_path)
        gen_desktop_php(plugin_data, templates_path)
        gen_core_php(plugin_data, templates_path)


def ask_plugin_informations(config):
    """Obtenir les informations pour le futur plugin.
    :return: Informations compilées
    :rtype:  dict
    """
    data = {}

    print(' - Le nom apparait dans l\'interface de Jeedom')
    data['name'] = IO.ask_with_default('Nom', config['default_package_name'])
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


def gen_info_json(plugin_data, config):
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


def gen_installation_php(plugin_data, templates_path):
    """Ecrit la classe d'installation du plugin dans plugin_info
    :param plugin_data: Données du plugin
    :type plugin_data:  dict
    """
    target_file = plugin_data['plugin_info_path'] + 'install.php'
    File.copy_and_replace(templates_path + os.sep + 'wizard_install.php',
                          target_file, 'PluginName', plugin_data['id'])


def gen_configuration(plugin_data, templates_path):
    """Ecrit le formulaire de configuration du plugin dans plugin_info
    :param plugin_data: Données du plugin
    :type plugin_data:  dict
    """
    if plugin_data['configuration']:
        target_file = plugin_data['plugin_info_path'] + 'configuration.php'
        os.system(
            'cp ' + templates_path + os.sep + 'wizard_configuration.php ' +
            target_file)
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


def gen_desktop_php(plugin_data, templates_path):
    """Ecrit le fichier PHP du desktop pour le rendu
    :param plugin_data: Données du plugin
    :type plugin_data:  dict
    """
    target_file = plugin_data['desktop_path'] + os.sep + 'php' + os.sep + \
                  plugin_data['id'] + '.php'
    os.system(
        'cp ' + templates_path + os.sep + 'wizard_desktop_php.php ' +
        target_file)


def gen_core_php(plugin_data, templates_path):
    """Ecrit le fichier PHP du core
    :param plugin_data: Données du plugin
    :type plugin_data:  dict
    """
    target_file = plugin_data['core_path'] + os.sep + 'class' + os.sep + \
                  plugin_data['id'] + '.class.php'
    os.system(
        'cp ' + templates_path + os.sep + 'wizard_core_class.php ' +
        target_file)
    File.replace_in_file(target_file, 'PluginName', plugin_data['id'])

    target_file = plugin_data['core_path'] + os.sep + 'class' + os.sep + \
                  plugin_data['id'] + 'Cmd.class.php'
    os.system(
        'cp ' + templates_path + os.sep + 'wizard_core_cmd_class.php ' +
        target_file)
    File.replace_in_file(target_file, 'PluginName', plugin_data['id'])


if __name__ == '__main__':
    start_wizard()
