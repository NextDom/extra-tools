#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialise l'outil pour les plugins
"""
import sys

from libs.Tools import Tools
from libs.WizardMenu import WizardMenu

# Gestion des accents pour python 2
if sys.version_info[0] < 3:
    reload(sys) #pylint: disable=undefined-variable
    sys.setdefaultencoding('utf8') #pylint: disable=no-member

if __name__ == '__main__':
    tools = Tools()
    # Point de d'entrée en mode CLI
    readed_plugin_name = tools.parse_args(sys.argv)
    if readed_plugin_name is not None:
        plugins_list = []
        if readed_plugin_name == '':
            plugins_list = tools.get_plugins_in_dir('.')
        wizard_menu = WizardMenu(plugins_list)
        wizard_menu.start()
