import re

path_pattern_regex = re.compile(r"^((?:\/(?:(?:[^\/%?#=<>]|%[a-zA-Z0-9]{2})+|<[a-zA-Z_][a-zA-Z0-9_]*>))+\/?|\/)(?:\?((?:[^\/%?#=<>]|%[a-zA-Z0-9]{2})+=<[a-zA-Z_][a-zA-Z0-9_]*>(?:&(?:[^\/%?#=<>]|%[a-zA-Z0-9]{2})+=<[a-zA-Z_][a-zA-Z0-9_]*>)*))?$")

class RelativeURLPattern:
    """
    A pattern that may be used to match relative URL.

    The syntax is very similar to the one used for defining Flask routes, but this class also accepts placeholders on query string arguments.
    """

    def __init__(self, pattern):
        matched = path_pattern_regex.match(pattern)
        if matched is None:
            raise ValueError('Illegal pattern!')

        self._variables = {}

        self._pattern = pattern
        self._path_pattern = matched[1]

        self._path_elements = matched[1][1:].split(sep='/') if len(matched[1]) > 0 else []
        for i in range(0, len(self._path_elements)):
            path_element = self._path_elements[i]
            if len(path_element) > 0 and path_element[0] == '<':
                variable_name = path_element[1:-1]
                if variable_name in self._variables:
                    raise ValueError(
                        'Variable ' + variable_name + ' defined twice!')
                self._variables[variable_name] = {
                    'where': 'path',
                    'index': i
                }

        if matched[2] is not None and len(matched[2]) > 0:
            query_elements = matched[2].split(sep='&')
            for query_element in query_elements:
                name_and_value = query_element.split(sep='=')
                variable_name = name_and_value[1][1:-1]
                query_element_name = name_and_value[0]
                if variable_name in self._variables:
                    raise ValueError(
                        'Variable ' + variable_name + ' defined twice!')
                self._variables[variable_name] = {
                    'where': 'querystring',
                    'name': query_element_name
                }

    @property
    def path_pattern(self):
        return self._path_pattern

    @property
    def path_variables(self):
        result = []
        for variable_name in self._variables:
            variable = self._variables[variable_name]
            if variable['where'] == 'path':
                result.append(variable_name)
        return result

    @property
    def query_string_variables(self):
        result = []
        for variable_name in self._variables:
            variable = self._variables[variable_name]
            if variable['where'] == 'querystring':
                result.append(variable_name)
        return result

    def query_string_variable_from_key(self, key):
        for variable_name in self._variables:
            variable = self._variables[variable_name]
            if variable['where'] == 'querystring' and variable['name'] == key:
                return variable_name
        return None

    def replace(self, **kwargs):
        path_elements = self._path_elements[:]
        query_values = {}
        for variable_name in kwargs:
            if variable_name in self._variables:
                variable = self._variables[variable_name]
                if variable['where'] == 'querystring':
                    query_values[variable['name']] = kwargs[variable_name]
                if variable['where'] == 'path':
                    path_elements[variable['index']] = kwargs[variable_name]
        result = '/' + '/'.join(path_elements)
        if len(query_values) > 0:
            result += '?' + \
                '&'.join((x + '=' + query_values[x]) for x in query_values)
        return result

    def __repr__(self):
        return self._pattern