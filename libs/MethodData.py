# -*- coding: utf-8 -*-


class MethodData:
    """Classe contenant les informations d'une méthode
    """
    class_file_path = ''
    class_name = ''
    method_name = ''
    method_visibility = 'public'
    method_is_static = False
    method_comment = ''

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
        output += 'function ' + self.method_name + '()\n    {\n\n    }\n'
        return output
