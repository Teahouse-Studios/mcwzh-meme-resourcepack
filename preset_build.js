const { JavaPackBuilder, ModuleParser, Logger } = require('memepack-builder')
const { readFileSync, fstat, writeFileSync } = require('fs')
const { resolve } = require('path')
const glob = require('glob')
const PACK_VERSION = '1.6.1'

const preset_args = [
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': [], 'collection': [
                'choice_modules_1']
        }, 'mod': [], 'format': 7, compatible: false
    },
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': ['lang_sfw'], 'collection': [
                'choice_modules_1']
        }, 'mod': ['all'], 'format': 7, compatible: false
    },
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': [
                'lang_sfw'], 'collection': []
        }, 'mod': [], 'format': 7, compatible: false
    },
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': [
                'lang_sfw'], 'collection': []
        }, 'mod': [], 'format': 7, compatible: false
    },
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': ['lang_sfw'], 'collection': [
                'choice_modules_1']
        }, 'mod': ['all'], 'format': 7, compatible: true
    },
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': ['lang_sfw'], 'collection': [
                'choice_modules_1']
        }, 'mod': [], 'format': 7, compatible: true
    },
    {
        'platform': 'java', 'type': 'normal', 'modules': {
            'resource': [
                'lang_sfw'], 'collection': []
        }, 'mod': [], 'format': 7, compatible: true
    },
    {
        'platform': 'java', 'type': 'legacy', 'modules': {
            'resource': ['lang_sfw'], 'collection': [
                'version_1.12.2-1.15.2']
        }, 'mod': [], 'format': 3, compatible: false
    }
]
const preset_name = [
    `mcwzh-meme_v${PACK_VERSION}.zip`,
    `mcwzh-meme_sfw_v${PACK_VERSION}.zip`,
    `mcwzh-meme_nomod_sfw_v${PACK_VERSION}.zip`,
    `mcwzh-meme_nomod_noresource_sfw_v${PACK_VERSION}.zip`,
    `mcwzh-meme_compatible_sfw_v${PACK_VERSION}.zip`,
    `mcwzh-meme_compatible_nomod_sfw_v${PACK_VERSION}.zip`,
    `mcwzh-meme_compatible_nomod_noresource_sfw_v${PACK_VERSION}.zip`,
    `mcwzh-meme_legacy_nomod_noresource_sfw_v${PACK_VERSION}.zip`
]


async function start() {
    const jeModules = new ModuleParser(resolve(__dirname, './modules'))
    const je = new JavaPackBuilder(await jeModules.moduleInfo(), resolve(__dirname, './meme_resourcepack'), {
        modFiles: glob.sync('./mods/*.json')
    })
    for (const [i, arg] of preset_args.entries()) {
        try {
            let r = await je.build(arg)
            console.log(arg, preset_name[i])
            writeFileSync(resolve(__dirname, `./builds/${preset_name[i]}`), r.content)

        } catch (e) {
            console.error(Logger.log, e)
            Logger.clearLog()
            process.exit(1)
        }
    }
    process.exit(0)
}

start()