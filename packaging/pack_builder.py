from hashlib import sha256
from json import load, dumps
from os import listdir, remove, walk, sep, mkdir
from os.path import join, basename, normpath, exists, isdir
from sys import stderr
from zipfile import ZipFile, ZIP_DEFLATED


class pack_builder(object):
    '''
    Build packs.
    The builder accepts the building args, then build the packs on demand.
    '''

    def __init__(self, main_res_path: str, module_info: dict, mods_path: str, legacy_mapping_path: str):
        self.__args = {}
        self.__warning = 0
        self.__error = False
        self.__log_list = []
        self.__filename = ""
        self.__main_res_path = main_res_path
        self.__module_info = module_info
        self.__mods_path = mods_path
        self.__legacy_mapping_path = legacy_mapping_path

    @property
    def args(self):
        return self.__args

    @args.setter
    def args(self, value: dict):
        self.__args = value

    @property
    def warning_count(self):
        return self.__warning

    @property
    def error(self):
        return self.__error

    @property
    def filename(self):
        return self.__filename

    @property
    def main_resource_path(self):
        return self.__main_res_path

    @property
    def module_info(self):
        return self.__module_info

    @property
    def mods_path(self):
        return self.__mods_path

    @property
    def legacy_mapping_path(self):
        return self.__legacy_mapping_path

    @property
    def log_list(self):
        return self.__log_list

    def clean_status(self):
        self.__warning = 0
        self.__error = False
        self.__log_list = []
        self.__filename = ""

    def build(self):
        self.clean_status()
        args = self.args
        # args validation
        status, info = self.__check_args()
        if status:
            # process args
            # get language modules
            lang_supp = self.__parse_includes("language")
            # get resource modules
            res_supp = self.__parse_includes("resource")
            # get mixed modules
            mixed_supp = self.__parse_includes("mixed")
            # get module collections
            module_collection = self.__parse_includes("collection")
            # add modules to respective list
            self.__handle_modules(res_supp, lang_supp,
                                  mixed_supp, module_collection)
            # get mods strings
            mod_supp = self.__parse_mods()
            # merge language supplement
            # TODO: split mod strings into namespaces
            main_lang_data = self.__merge_language(
                lang_supp, mod_supp)
            # get realms strings
            realms_lang_data = load(open(join(
                self.main_resource_path, "assets/realms/lang/zh_meme.json"), 'r', encoding='utf8'))
            # process pack name
            digest = sha256(dumps(args).encode('utf8')).hexdigest()
            pack_name = args['hash'] and f"mcwzh-meme.{digest[:7]}.zip" or "mcwzh-meme.zip"
            self.__filename = pack_name
            # process mcmeta
            mcmeta = self.__process_meta(args)
            # decide language file name & ext
            lang_file_name = self.__get_lang_filename(args['type'])
            # set output dir
            pack_name = join(args['output'], pack_name)
            # mkdir
            if exists(args['output']) and not isdir(args['output']):
                remove(args['output'])
            if not exists(args['output']):
                mkdir(args['output'])
            # create pack
            info = f"Building pack {pack_name}"
            print(info)
            self.__log_list.append(info)
            pack = ZipFile(
                pack_name, 'w', compression=ZIP_DEFLATED, compresslevel=5)
            pack.write(join(self.main_resource_path,
                            "pack.png"), arcname="pack.png")
            pack.write(join(self.main_resource_path,
                            "LICENSE"), arcname="LICENSE")
            pack.writestr("pack.mcmeta", dumps(
                mcmeta, indent=4, ensure_ascii=False))
            # dump lang file into pack
            if args['type'] != 'legacy':
                # normal/compat
                pack.writestr(f"assets/minecraft/lang/{lang_file_name}",
                              dumps(main_lang_data, indent=4, ensure_ascii=True, sort_keys=True))
                pack.writestr(f"assets/realms/lang/{lang_file_name}",
                              dumps(realms_lang_data, indent=4, ensure_ascii=True, sort_keys=True))
            else:
                # legacy
                main_lang_data |= realms_lang_data
                legacy_content = self.__generate_legacy_content(main_lang_data)
                pack.writestr(
                    f"assets/minecraft/lang/{lang_file_name}", legacy_content)
            # dump resources
            self.__dump_resources(res_supp, pack)
            pack.close()
            self.__log_list.append(f"Successfully built {pack_name}.")
            print(f"Successfully built {pack_name}.")
        else:
            self.__raise_error(info)

    def __dump_resources(self, modules: list, pack: ZipFile):
        excluding = ('module_manifest.json', 'add.json', 'remove.json')
        module_path = self.module_info['path']
        for item in modules:
            base_folder = join(module_path, item)
            for root, _, files in walk(base_folder):
                for file in files:
                    if file not in excluding:
                        path = join(root, file)
                        arcpath = path[path.find(
                            base_folder) + len(base_folder) + 1:]
                        # prevent duplicates
                        if (testpath := arcpath.replace(sep, "/")) not in pack.namelist():
                            pack.write(join(
                                root, file), arcname=arcpath)
                        else:
                            self.__raise_warning(
                                f'Duplicated file "{testpath}", skipping')

    def __raise_warning(self, warning: str):
        print(f'\033[33mWarning: {warning}\033[0m', file=stderr)
        self.__log_list.append(f'Warning: {warning}')
        self.__warning += 1

    def __raise_error(self, error: str):
        print(f'\033[1;31mError: {error}\033[0m', file=stderr)
        print("\033[1;31mTerminate building because an error occurred.\033[0m")
        self.__log_list.append(f'Error: {error}')
        self.__log_list.append("Terminate building because an error occurred.")
        self.__error = True

    def __check_args(self):
        args = self.args
        # check essential arguments
        for key in ('type', 'modules', 'mod', 'output', 'hash'):
            if key not in args:
                return False, f'Missing required argument "{key}"'
        # check "format"
        if 'format' not in args or args['format'] is None:
            # did not specify "format", assume a value
            format = args['type'] == 'legacy' and 3 or 6
            self.__raise_warning(
                f'Did not specify "pack_format". Assuming value is "{format}"')
            args['format'] = format
        else:
            if (args['type'] == 'legacy' and args['format'] > 3) or (args['type'] in ('normal', 'compat') and args['format'] <= 3):
                return False, f'Type "{args["type"]}" does not match pack_format {args["format"]}'
        return True, None

    def __handle_modules(self, resource_list: list, language_list: list, mixed_list: list, collection_list: list):
        # get all resource, language and mixed modules supplied by collection
        collection_info = {
            k.pop('name'): k for k in self.module_info['modules']['collection']}
        for collection in collection_list:
            for module_type, module_list in (('language', language_list), ('resource', resource_list), ('mixed', mixed_list)):
                if module_type in collection_info[collection]['contains']:
                    module_list.extend(
                        collection_info[collection]['contains'][module_type])
        # mixed_modules go to resource and language, respectively
        resource_list.extend(mixed_list)
        language_list.extend(mixed_list)

    def __process_meta(self, args: dict) -> dict:
        data = load(open(join(self.main_resource_path,
                              'pack.mcmeta'), 'r', encoding='utf8'))
        pack_format = args['type'] == 'legacy' and 3 or (
            'format' in args and args['format'] or None)
        data['pack']['pack_format'] = pack_format or data['pack']['pack_format']
        if args['type'] == 'compat':
            data.pop('language')
        return data

    def __get_lang_filename(self, type: str) -> str:
        return type == 'normal' and 'zh_meme.json' or (
            type == 'compat' and 'zh_cn.json' or 'zh_cn.lang')

    def __parse_includes(self, type: str) -> list:
        includes = self.args['modules'][type]
        full_list = list(
            map(lambda item: item['name'], self.module_info['modules'][type]))
        if 'none' in includes:
            return []
        elif 'all' in includes:
            return full_list
        else:
            include_list = []
            for item in includes:
                if item in full_list:
                    include_list.append(item)
                else:
                    self.__raise_warning(
                        f'Module "{item}" does not exist, skipping')
            return include_list

    def __parse_mods(self) -> list:
        mods = self.args['mod']
        existing_mods = listdir(self.mods_path)
        if 'none' in mods:
            return []
        elif 'all' in mods:
            return existing_mods
        else:
            mods_list = []
            for item in mods:
                if item in existing_mods:
                    mods_list.append(item)
                elif (normed_path := basename(normpath(item))) in existing_mods:
                    mods_list.append(normed_path)
                else:
                    self.__raise_warning(
                        f'Mod file "{item}" does not exist, skipping')
            return mods_list

    def __merge_language(self, language_supp: list, mod_supp: list) -> dict:
        # load basic strings
        lang_data = load(open(join(self.main_resource_path,
                                   "assets/minecraft/lang/zh_meme.json"), 'r', encoding='utf8'))
        module_path = self.module_info['path']
        for item in language_supp:
            add_file = join(module_path, item, "add.json")
            remove_file = join(module_path, item, "remove.json")
            if exists(add_file):
                lang_data |= load(open(add_file, 'r', encoding='utf8'))
            if exists(remove_file):
                for key in load(open(remove_file, 'r', encoding='utf8')):
                    if key in lang_data:
                        lang_data.pop(key)
                    else:
                        self.__raise_warning(
                            f'Key "{key}" does not exist, skipping')
        lang_data |= self.__get_mod_content(mod_supp)
        return lang_data

    def __get_mod_content(self, mod_list: list) -> dict:
        mods = {}
        for file in mod_list:
            if file.endswith(".json"):
                mods |= load(
                    open(join(self.mods_path, file), 'r', encoding='utf8'))
            elif file.endswith(".lang"):
                with open(join(self.mods_path, file), 'r', encoding='utf8') as f:
                    mods |= (line.strip().split(
                        "=", 1) for line in f if line.strip() != '' and not line.startswith('#'))
            else:
                self.__raise_warning(
                    f'File type "{file[file.rfind(".") + 1:]}" is not supported, skipping')
        return mods

    def __generate_legacy_content(self, content: dict) -> str:
        # get mappings list
        mappings = load(open(join(self.legacy_mapping_path,
                                  "all_mappings"), 'r', encoding='utf8'))
        legacy_lang_data = {}
        for item in mappings:
            if (mapping_file := f"{item}.json") not in listdir(self.legacy_mapping_path):
                self.__raise_warning(
                    f'Missing mapping "{mapping_file}", skipping')
            else:
                mapping = load(
                    open(join(self.legacy_mapping_path, mapping_file), 'r', encoding='utf8'))
                for k, v in mapping.items():
                    if v not in content:
                        self.__raise_warning(
                            f'In file "{mapping_file}": Corrupted key-value pair {{"{k}": "{v}"}}')
                    else:
                        legacy_lang_data[k] = content[v]
        return ''.join(f'{k}={v}\n' for k, v in legacy_lang_data.items())
