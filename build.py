import zipfile
import json
import argparse
import os
import hashlib

# Lincese: Apache-2.0


def main():
    parser = generate_parser()
    args = vars(parser.parse_args())
    if args['type'] == 'clean':
        for i in os.listdir('builds/'):
            os.remove('builds/' + i)
        print("\n[INFO] Deleted all packs built.")
    else:
        pack_builder = builder()
        pack_builder.set_args(args)
        pack_builder.build()


class builder(object):
    '''Build packs.'''

    def __init__(self):
        self.__args = {}
        self.__warning = 0
        self.__error = 0
        self.__logs = ""
        self.__filename = ""

    def set_args(self, new_args: dict):
        self.__args = new_args

    def get_warning_count(self):
        return self.__warning

    def get_filename(self):
        if self.__filename == "":
            return "Did not build any packs."
        else:
            return self.__filename

    def get_logs(self):
        if self.__logs == "":
            return "Did not build any packs."
        else:
            return self.__logs

    def clean_status(self):
        self.__warning = 0
        self.__error = 0
        self.__logs = ""
        self.__filename = ""

    def build(self):
        self.clean_status()
        args = self.__args
        # checking module names first, prevent name conflict
        checker = module_checker()
        if checker.check_module():
            # process args
            # get language supplement
            lang_supp = self.__parse_includes(
                args['language'], checker.get_module_list('language'))
            # merge sfw into lang_supp
            if args['sfw']:
                if not 'sfw' in lang_supp:
                    lang_supp.append('sfw')
            # get resource supplement
            res_supp = self.__parse_includes(
                args['resource'], checker.get_module_list('resource'))
            # get mods strings
            mod_supp = self.__parse_mods(args['mod'])
            # merge language supplement
            # TODO: split mod strings into namespaces
            main_lang_data = self.__merge_language(lang_supp, mod_supp)
            # get realms strings
            with open("assets/realms/lang/zh_meme.json", 'r', encoding='utf8') as f:
                realms_lang_data = json.load(f)
            # process pack name
            if args['hash']:
                sha256 = hashlib.sha256(json.dumps(
                    args).encode('utf8')).hexdigest()
                pack_name = "mcwzh-meme." + sha256[:7] + ".zip"
            else:
                pack_name = "mcwzh-meme.zip"
            self.__filename = pack_name
            # process mcmeta
            mcmeta = self.__process_meta(args['type'])
            # decide language file name & ext
            lang_file_name = self.__get_lang_file_name(args['type'])
            # create pack
            info = f"Building pack {pack_name}"
            print(info)
            self.__logs += f"{info}\n"
            pack_name = os.path.join("builds", pack_name)
            pack = zipfile.ZipFile(
                pack_name, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=5)
            pack.write("pack.png")
            pack.write("LICENSE")
            pack.writestr("pack.mcmeta", json.dumps(
                mcmeta, indent=4, ensure_ascii=False))
            # dump lang file into pack
            if args['type'] != 'legacy':
                # normal/compat
                pack.writestr("assets/minecraft/lang/" + lang_file_name,
                              json.dumps(main_lang_data, indent=4, ensure_ascii=True))
                pack.writestr("assets/realms/lang/" + lang_file_name,
                              json.dumps(realms_lang_data, indent=4, ensure_ascii=True))
            else:
                # legacy
                main_lang_data.update(realms_lang_data)
                legacy_content = self.__generate_legacy_content(main_lang_data)
                pack.writestr("assets/minecraft/lang/" +
                              lang_file_name, legacy_content)
            # dump resources
            for item in res_supp:
                base_folder = os.path.join("modules", item)
                for root, dirs, files in os.walk(base_folder):
                    for file in files:
                        if file != "manifest.json":
                            path = os.path.join(root, file)
                            arcpath = path[path.find(
                                base_folder) + len(base_folder) + 1:]
                            testpath = arcpath.replace(os.sep, "/")
                            # prevent duplicates
                            if testpath not in pack.namelist():
                                pack.write(os.path.join(
                                    root, file), arcname=arcpath)
            pack.close()
            print("Build successful.")
        else:
            error = "Error: " + checker.get_info()
            print(f"\033[1;31m{error}\033[0m")
            self.__logs += f"{error}\n"
            self.__error += 1
            print("Terminate building because an error occurred.")

    def __process_meta(self, type: str) -> dict:
        with open('pack.mcmeta', 'r', encoding='utf8') as f:
            data = json.load(f)
        if type == 'compat':
            data.pop('language')
        elif type == 'legacy':
            data['pack'].update({"pack_format": 3})
        return data

    def __get_lang_file_name(self, type: str):
        if type == 'normal':
            return 'zh_meme.json'
        elif type == 'compat':
            return 'zh_cn.json'
        else:
            return 'zh_cn.lang'

    def __parse_includes(self, includes: list, fulllist: list) -> list:
        if 'none' in includes:
            return []
        elif 'all' in includes:
            return fulllist
        else:
            include_list = []
            for item in includes:
                if item in fulllist:
                    include_list.append(item)
                else:
                    warning = f"Warning: {item} does not exist, skipping."
                    print(f"\033[33m{warning}\033[0m")
                    self.__logs += f"{warning}\n"
                    self.__warning += 1
            return include_list

    def __parse_mods(self, mods: list) -> list:
        existing_mods = os.listdir("mods")
        if 'none' in mods:
            return []
        elif 'all' in mods:
            return existing_mods
        else:
            mods_list = []
            for item in mods:
                if item in existing_mods:
                    mods_list.append(item)
                else:
                    warning = f"Warning: {item} does not exist, skipping."
                    print(f"\033[33m{warning}\033[0m")
                    self.__logs += f"{warning}\n"
                    self.__warning += 1
            return mods_list

    def __merge_language(self, language_supp: list, mod_supp: list) -> dict:
        # load basic strings
        with open("assets/minecraft/lang/zh_meme.json", 'r', encoding='utf8') as f:
            lang_data = json.load(f)
        for item in language_supp:
            add_file = os.path.join("modules", item, "add.json")
            remove_file = os.path.join("modules", item, "remove.json")
            if os.path.exists(add_file):
                with open(add_file, 'r', encoding='utf8') as add:
                    supp_data = json.load(add)
            if os.path.exists(remove_file):
                with open(remove_file, 'r', encoding='utf8') as remove:
                    remove_list = json.load(remove)
            for key in remove_list:
                if key in lang_data.keys():
                    lang_data.pop(key)
            lang_data.update(supp_data)
        lang_data.update(self.__get_mod_content(mod_supp))
        return lang_data

    def __get_mod_content(self, mods: list) -> dict:
        mods = {}
        for file in mods:
            if file.endswith(".json"):
                with open(file, 'r', encoding='utf8') as f:
                    mods.update(json.load(f))
            elif file.endswith(".lang"):
                with open(file, 'r', encoding='utf8') as f:
                    items = [i for i in f.read().splitlines() if (
                        i != '' and not i.startswith('#'))]
                mods.update(dict(i.split("=", 1) for i in items))
            else:
                warning = f'Warning: File type "{file[file.rfind(".") + 1:]}" is not supported, skipping'
                print(
                    f'\033[33m{warning}\033[0m')
                self.__warning += 1
                self.__logs += f"{warning}\n"
        return mods

    def __generate_legacy_content(self, content: dict) -> str:
        # get mappings list
        with open(os.path.join("mappings", "all_mappings"), 'r', encoding='utf8') as f:
            mappings = json.load(f)['mappings']
        legacy_lang_data = {}
        for item in mappings:
            mapping_file = item + ".json"
            if mapping_file not in os.listdir("mappings"):
                warning = f"Warning: Missing mapping '{mapping_file}', skipping"
                print(f"\033[33m{warning}\033[0m")
                self.__logs += f"{warning}\n"
                self.__warning += 1
            else:
                with open(os.path.join("mappings", mapping_file), 'r', encoding='utf8') as f:
                    mapping = json.load(f)
                for k, v in mapping.items():
                    if v not in content.keys():
                        warning = f"Warning: Corrupted key-value pair in file {mapping_file}: {{'{k}': '{v}'}}"
                        print(
                            f"\033[33m{warning}\033[0m")
                        self.__logs += f"{warning}\n"
                        self.__warning += 1
                    else:
                        legacy_lang_data.update({k: content[v]})
        out_content = ""
        for k, v in legacy_lang_data.items():
            out_content += f"{k}={v}\n"
        return out_content


class module_checker(object):
    def __init__(self):
        self.__status = True
        self.__lang_list = []
        self.__res_list = []
        self.__manifests = {}
        self.__info = ''

    def get_info(self):
        return self.__info

    def check_module(self):
        base_folder = 'modules'
        lang_list = []
        res_list = []
        for module in os.listdir(base_folder):
            with open(os.path.join(base_folder, module, "manifest.json"), 'r', encoding='utf8') as f:
                data = json.load(f)
            name = data['name']
            module_type = data['type']
            if name in lang_list or name in res_list:
                self.__status = False
                self.__info = f"conflict name '{name}'"
                return False
            else:
                self.__manifests[name] = data['description']
                if module_type == 'language':
                    lang_list.append(name)
                elif module_type == 'resource':
                    res_list.append(name)
        self.__status = True
        self.__lang_list = lang_list
        self.__res_list = res_list
        return True

    def get_module_list(self, type):
        self.check_module()
        if not self.__status:
            return []
        else:
            if type == 'language':
                return self.__lang_list
            elif type == 'resource':
                return self.__res_list
            else:
                return []

    def get_manifests(self):
        self.check_module()
        if not self.__status:
            return {}
        else:
            return self.__manifests


def generate_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automatically build resourcepacks")
    parser.add_argument('type', default='normal', choices=[
                        'normal', 'compat', 'legacy', 'clean'], help="Build type. Should be 'normal', 'compat', 'legacy' or 'clean'. If it's 'clean', all packs in 'builds/' directory will be deleted.")
    parser.add_argument('-r', '--resource', nargs='*', default='all',
                        help="(Experimental) Include resource modules. Should be module names, 'all' or 'none'. Defaults to 'all'.")
    parser.add_argument('-l', '--language', nargs='*', default='none',
                        help="(Experimental) Include language modules. Should be module names, 'all' or 'none'. Defaults to 'none'.")
    parser.add_argument('-s', '--sfw', action='store_true',
                        help="Use 'suitable for work' strings, equals to '--language sfw'.")
    parser.add_argument('-m', '--mod', nargs='*', default='none',
                        help="(Experimental) Include mod string files. Should be file names in 'mods/' folder, 'all' or 'none'. Defaults to 'none'.")
    parser.add_argument('--hash', action='store_true',
                        help="Add a hash into file name.")
    return parser


if __name__ == "__main__":
    main()
