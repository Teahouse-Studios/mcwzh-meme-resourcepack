import os
from json import load
from os.path import exists, isfile, join, split
from sys import stderr


class module_checker(object):
    def __init__(self):
        self.__status = True
        self.__checked = False
        self.__module_path = ''
        self.__parsed_modules = {}
        self.__info = []

    @property
    def info_list(self):
        return self.__info

    @property
    def module_list(self):
        if not self.__checked:
            self.check_module()
        return self.__status and self.__parsed_modules or {}

    @property
    def module_path(self):
        return self.__module_path

    @module_path.setter
    def module_path(self, value: str):
        self.__module_path = value

    def clean_status(self):
        self.__status = True
        self.__checked = False
        self.__parsed_modules = {}
        self.__info = []

    def check_module(self):
        self.clean_status()
        modules = {
            'language': [],
            'resource': [],
            'mixed': []
        }
        for module in os.listdir(self.module_path):
            status, info, data = self.__analyze_module(
                join(self.module_path, module))
            if status:
                modules[data.pop('type')].append(data)
            else:
                self.__info.append(f"Warning: {info}")
                print(f"\033[33mWarning: {info}\033[0m", file=stderr)
                self.__status = False
        if modules['language'] or modules['resource'] or modules['mixed']:
            self.__parsed_modules = modules
        self.__checked = True

    def __analyze_module(self, path: str):
        manifest = join(path, "manifest.json")
        dir_name = split(path)[1]
        if exists(manifest) and isfile(manifest):
            data = load(open(manifest, 'r', encoding='utf8'))
            for key in ('name', 'type', 'description'):
                if key not in data:
                    return False, f"In path '{dir_name}': Incomplete manifest.json", None
            if dir_name != data['name']:
                return False, f"In path '{dir_name}': Does not match module name '{data['name']}'", None
            if data['type'] == 'language':
                if not (exists(join(path, "add.json")) or exists(join(path, "remove.json"))):
                    return False, f"In path '{dir_name}': Expected a language module, but couldn't find 'add.json' or 'remove.json'", None
            elif data['type'] == 'resource':
                if not exists(join(path, "assets")):
                    return False, f"In path '{dir_name}': Expected a resource module, but couldn't find 'assets' directory", None
            elif data['type'] == 'mixed':
                if not (exists(join(path, "assets")) and (exists(join(path, "add.json")) or exists(join(path, "remove.json")))):
                    return False, f"In path '{dir_name}': Expected a mixed module, but couldn't find 'assets' directory and either 'add.json' or 'remove.json'", None
            else:
                return False, f"In path '{dir_name}': Unknown module type '{data['type']}'", None
            return True, None, data
        else:
            return False, f"In module '{dir_name}': No manifest.json", None
