# 中文Minecraft Wiki梗体中文资源包 · Unofficial

[![GitHub issues](https://img.shields.io/github/issues/Teahouse-Studios/mcwzh-meme-resourcepack?logo=github&style=flat-square)](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack/issues)    [![GitHub pull requests](https://img.shields.io/github/issues-pr/Teahouse-Studios/mcwzh-meme-resourcepack?logo=github&style=flat-square)](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack/pulls)    [![License](https://img.shields.io/static/v1?label=License&message=CC%20BY-SA%204.0&color=db2331&style=flat-square&logo=creative%20commons)](https://creativecommons.org/licenses/by-sa/4.0/)    [![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Teahouse-Studios/mcwzh-meme-resourcepack?label=latest%20version&style=flat-square)](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack/releases)    [![Minecraft ver](https://img.shields.io/static/v1?label=Minecraft%20version&message=1.12.2%2B&color=db2331&style=flat-square&logo=)](https://minecraft.net)

此资源包仅适用于**Minecraft Java版**。**关于适用于Minecraft基岩版的资源包，参见[基岩版梗体中文](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack-bedrock)。**

**注：若发现可能存在该资源包上头的情况，请立刻~~食用~~阅读[译名标准化](https://zh.minecraft.wiki/w/Minecraft_Wiki:译名标准化)。**

[![Banner](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack/blob/master/materials/zh_meme_banner.png?raw=true)](https://www.mcbbs.net/thread-1004643-1-1.html)

## 赞助者
<p align="center">
  <a href="https://afdian.net/@teahouse">
    <img src='https://fe.wd-ljt.com/m3me/sP0ns0r5/sP0ns0r5.svg'>
  </a>
</p>

## 作用

这个资源包将一部分译名或其他游戏内字符串替换成了一些知名/不知名的梗或笑话，或将其用诙谐的语言重写了一遍。

## 用法

在[Releases](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack/releases)中下载此资源包，或在[网页构建](https://meme.teahouse.team/)中选择自定义选项下载。

### 常规

请选择 `mcwzh-meme.zip` 下载，像其他资源包一样复制到你对应的 `.minecraft/resourcepacks/` 目录中（MultiMC或其他分离版本的启动器请自行查找）。资源包新建了一个语言，安装启用后在语言设置中选择“**梗体中文**”即可体验。

### 加载Mod时

普通版本的资源包**无法**覆盖所有的Mod字符串，会导致大部分Mod的内容**全部变为英文**。请下载 `mcwzh-meme_compatible.zip` ，以保证体验。安装流程几乎相同，只是选择的语言应该是**普通的“简体中文”**。

关于支持梗体中文的Mod，请见[支持的Mod](./list_of_supported_mods.md)页面。

### 1.12.2及以下版本支持

1.13对可翻译字符串进行了一次破坏性更改，这意味着1.12.2及以下无法直接正常使用本资源包。同时，1.12.2及以下版本并不支持读取ASCII格式的Unicode码。通过建立映射表，我们初步实现了1.12.2及以下版本对大部分字符串的支持（也就是除去命令），详见Issue [#34](https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack/issues/34)。1.12.2及以下版本请使用带有 `_legacy` 的预设包。

### 对旧版本的兼容

本仓库中的语言文件和最新的Java版的语言文件保持同步。对旧版本，我们采用了“模块”的方式保持兼容。构建时请加入参数 `-r <语言模块名称>` 来将其加入到主语言文件中。[这里](./list_of_language_modules.md)列出了目前所有的语言模块。

### 唱片替换

该资源包将唱片信息修改成了非Minecraft歌曲。由于版权原因，您需要自行制作一个唱片替换资源包（可以参考[这篇文章](https://www.planetminecraft.com/blog/how-to-change-music-discs-to-any-song---easy/)）。一份不受支持的预制版唱片替换包（不允许二次分发）可以在[这里](https://wdf.ink/record-java)获得。

### 不死图腾替换

该资源包将不死图腾替换成了自定义模型。自定义模型范围为 `10800000~10800006` 。如果这不适用于你（例如模型出错，游玩自定义地图或装载其他3D资源包），你可以尝试调整加载顺序，或者下载不带自定义模型的预设构建（以 `_nofigure` 结尾）。如果不想重新下载，你也可以直接删除有自定义模型版本的对应的文件夹。

关于可以直接获取自定义模型的数据包，可以在[这里](https://lakeus.xyz/images/e/e5/Figure.zip)，或是在本repo中的`datapack`目录找到。

### “Suitable for work”替换

我们十分理解，一些字符串可能并不适合公开场合的使用。因此为了规避，请在自己构建时在命令结尾加入参数 `--sfw` 以获取一个更加安全的版本。

## 鹦鹉通道

### 体验最新内容

想要**抢先体验**最前沿~~整活~~版本，我们强烈建议您前往[网页打包](https://meme.teahouse.team/)，那里可以更直观地选择您需要的内容。

若您仍想自己尝试从命令行打包（并不推荐，比较繁琐），可按以下步骤进行：

#### 先决条件

请确保已经安装了NodeJS主流版本和Git。如果没有，请到[NodeJS官网](https://nodejs.org/zh-cn/)和[Git官网](https://www.git-scm.com)下载。

#### 步骤

1. 下载源码；
2. 进入文件夹；
3. 安装相关依赖；
4. 运行预设打包命令。

``` sh
git clone https://github.com/Teahouse-Studios/mcwzh-meme-resourcepack.git
cd mcwzh-meme-resourcepack
npm install
node preset_build.js
```

在 `builds` 文件夹中会生成 `mcwzh-meme.zip` 、 `mcwzh-meme_compatible_sfw.zip` 、 `mcwzh-meme_compatible_nofigure_legacy_sfw.zip` 等预设的资源包，名称和作用如上所述。

### 自助跟进游戏版本

此资源包的语言文件顺序与原版的英文顺序并不一致（本资源包是将key按照字母顺序排序）。如果原版的英文译名跟进了，请先将解包的英文语言文件按照前文所述排序，可以参考[这个网站](https://tool.funsmall.cn/jsonsort/)或本repo中的 `sort.py`。推荐使用[Visual Studio Code](https://github.com/microsoft/vscode)的比较功能以方便查看新字符串。

梗体中文本体文件也可以使用 `sort.py` 进行排序。

如果你是Crowdin上Minecraft项目的翻译者，你也可以随时查看通知来获取新字符串。

## 贡献

我们欢迎你为这个资源包贡献自己的想法。请参阅 [`CONTRIBUTING.md`](./CONTRIBUTING.md) 以获取一些建议。

## 声明

* 本资源包**仅供娱乐**，请勿将其可能存在的误导性内容当真。
* 本资源包与Mojang、Minecraft Wiki和Weird Gloop无关，原中文翻译版权为Mojang和翻译者所有。
  * 关于正确的译名，请参见[中文Minecraft Wiki上的标准译名列表](https://zh.minecraft.wiki/w/Minecraft_Wiki:译名标准化)。
* 本项目文件除另有声明外，均以 ***CC BY-SA 4.0*** 协议授权。
  * 这意味着，你可在署名的情况下自由修改本资源包，但是你再创作的作品必须以本协议发布。
  * 这不是法律建议。
  * `minecraft_cjk_character_supplement` 模块中散有的各个字形以Unifont兼容的协议（GPLv2+ with the GNU Font Embedding Exception及SIL Open Font License）发布；部分压缩文件的协议请参考压缩文件内的协议文件。
* 本项目附带的Mod内容字符串、未经梗体中文修改过的部分，按照 ***原作品的协议*** 发布。
* 本项目 `tools` 目录下的脚本和根目录下的 `preset_build.js` 文件，可选择 ***CC BY-SA 4.0*** 或 ***Apache License 2.0*** 协议之一授权。

![GitHub forks](https://img.shields.io/github/forks/Teahouse-Studios/mcwzh-meme-resourcepack?style=social)    ![GitHub stars](https://img.shields.io/github/stars/Teahouse-Studios/mcwzh-meme-resourcepack?style=social)    ![GitHub watchers](https://img.shields.io/github/watchers/Teahouse-Studios/mcwzh-meme-resourcepack?style=social)
