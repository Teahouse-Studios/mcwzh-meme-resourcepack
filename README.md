# 中文Minecraft Wiki梗体中文资源包 · Unofficial

[![Tencent QQ](https://img.shields.io/static/v1?label=QQ&message=657876815&color=eb1923&style=flat-square&logo=tencent%20qq)](https://jq.qq.com/?_wv=1027&k=5tqdTeR)    [![GitHub issues](https://img.shields.io/github/issues/lakejason0/mcwzh-meme-resourcepack?logo=github&style=flat-square)](https://github.com/lakejason0/mcwzh-meme-resourcepack/issues)    [![GitHub pull requests](https://img.shields.io/github/issues-pr/lakejason0/mcwzh-meme-resourcepack?logo=github&style=flat-square)](https://github.com/lakejason0/mcwzh-meme-resourcepack/pulls)    [![License](https://img.shields.io/static/v1?label=License&message=CC%20BY-NC-SA%204.0&color=db2331&style=flat-square&logo=creative%20commons)](https://creativecommons.org/licenses/by-nc-sa/4.0/)    [![License](https://img.shields.io/static/v1?label=License+for+script&message=GPL+v3.0&color=db2331&style=flat-square&logo=gpl)](https://www.gnu.org/licenses/)    [![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/lakejason0/mcwzh-meme-resourcepack?label=latest%20version&style=flat-square)](https://github.com/lakejason0/mcwzh-meme-resourcepack/releases)    [![Minecraft ver](https://img.shields.io/static/v1?label=Minecraft%20version&message=1.12.2-20w16a&color=db2331&style=flat-square&logo=)](https://minecraft.net)

注：此资源包适用于Java版。有关到基岩版的移植，参见[SkyEye_FAST的基岩版移植Repository](https://github.com/SkyEye-FAST/mcwzh-meme-resourcepack-bedrock)。

**注：若发现自身可能存在该资源包上头的情况，请立刻~~食用~~阅读[译名标准化](https://minecraft-zh.gamepedia.com/Minecraft_Wiki:译名标准化)。**

## 作用
这个资源包将一部分译名或其他游戏内字符串替换成了一些知名/不知名的梗或笑话，或将其用诙谐的语言重写了一遍。
## 用法
在[Releases](https://github.com/lakejason0/mcwzh-meme-resourcepack/releases)中下载此资源包，或在[网页构建](https://download.powerdia.nl)中选择自定义选项下载。
### 常规
请选择`mcwzh-meme.zip`下载，像其他资源包一样复制到你对应的`.minecraft/resourcepacks/`目录中（[MCBBS上的教程](https://www.mcbbs.net/thread-880869-1-1.html)）（MultiMC或其他分离版本的启动器请自行查找）。资源包新建了一个语言，安装启用后在语言设置中选择“**梗体中文**”即可体验。
### 加载Mod时
普通版本的资源包**无法**覆盖所有的Mod字符串，会导致大部分Mod的内容**全部变为英文**。请下载`mcwzh-meme_compatible.zip`，以保证体验。安装流程几乎相同，只是选择的语言应该是**普通的“简体中文”**。

但是如果有遇到支持梗体中文的原版Mod，请下载`mcwzh-meme.zip`以保证体验（目前暂时没有）。
### 1.12.2及以下版本支持
1.13对可翻译字符串进行了一次破坏性更改，这意味着1.12.2及以下无法直接正常使用本资源包。同时，1.12.2及以下版本并不支持读取ASCII格式的Unicode码。通过建立映射表，我们初步实现了1.12.2及以下版本对大部分字符串的支持（也就是除去命令），详见Issue [#34](https://github.com/lakejason0/mcwzh-meme-resourcepack/issues/34)。1.12.2及以下版本请使用带有`_legacy`后缀的自动构建。
### 唱片替换
该资源包将唱片信息修改成了非Minecraft歌曲。由于版权原因，您需要自行制作一个唱片替换资源包（可以参考[这篇文章](https://www.planetminecraft.com/blog/how-to-change-music-discs-to-any-song---easy/)）。一份不受支持的预制版唱片替换包（不允许二次分发）可以在[这里](https://files.lakejason0.ml/images/3/34/%E5%94%B1%E7%89%87%E6%9B%BF%E6%8D%A2.zip)获得。
### 不死图腾替换
该资源包将不死图腾替换成了自定义模型。自定义模型范围为`10800000~10800006`。如果这不适用于你（例如模型出错，游玩自定义地图或装载其他3D资源包），你可以尝试调整载入顺序，或者下载不带自定义模型的自动构建（以`_nofigure`结尾）。如果不想重新下载，你也可以直接删除有自定义模型版本的对应的文件夹。


关于可以直接获取自定义模型的数据包，可以在[这里](https://files.lakejason0.ml/images/e/e5/Figure.zip)找到。
### 可选的文件替换
由于Mojang在20w12a加入了重生锚，`/spawnpoint`现在支持设置重生点到指定维度，这导致翻译字符串出现了一次破坏性更改。你可以在自己构建时在命令结尾加入参数`-i optional/spawnpoint_new.json`或者`-i optional/spawnpoint_old.json`以获取更好的命令使用体验。

关于愚人节快照20w14infinite，请在自己构建时在命令结尾加上`-i optional/20w14infinite.json`来得到有限的梗体中文支持。

由于Mojang在20w14a对字幕进行了一次修正和增补，铁活板门的字幕互换的问题已经被修复。如果你正在使用旧版本，请在自己构建时在命令结尾加入参数`-i optional/trapdoor_mismatch.json`以获取正确的字幕。

### “Suitable for work”替换
我们十分理解，一些字符串可能并不适合公开场合的使用。因此为了规避，请在自己构建时在命令结尾加入参数`-i optional/sfw.json`以获取一个更加安全的版本。带有此可选替换的资源包会自动加上`_sfw`后缀。

## 鹦鹉通道
### 体验最新内容
想要**抢先体验**最前沿~~整活~~版本，请按以下方法操作，或者不会命令行可以前往[网页打包](https://download.powerdia.nl)：
#### 先决条件
请确保已经安装了Python 3.x和Git。如果没有，请到[Python官网](https://www.python.org)和[Git官网](https://www.git-scm.com)下载。
#### 步骤
1. 下载源码：
``` bash
git clone https://github.com/lakejason0/mcwzh-meme-resourcepack.git
```
2. 进入文件夹：
``` bash
cd mcwzh-meme-resourcepack
```
3. 运行Python命令：
``` bash
python build.py all
```
在`builds`文件夹中会出现`mcwzh-meme.zip`、`mcwzh-meme_compatible_sfw.zip`、`mcwzh-meme_compatible_nofigure_legacy_sfw.zip`等资源包，名称和作用如上所述。

如果只需要常规的资源包，运行：
``` bash
python build.py normal
```
如果只需要加载Mod版的资源包，运行：
``` bash
python build.py compat
```
如果不需要自定义模型，添加`-n`选项。

如果需要1.12.2及以下的格式，添加`-l`选项。

更详细的用法请运行以下命令来获取：
``` bash
python build.py -h
```
### 自助跟进游戏版本
此资源包的语言文件顺序与原版的英文顺序并不一致（本资源包是将key按照字母顺序排序）。如果原版的英文译名跟进了，请先将解包的英文语言文件按照前文所述排序，可以参考[这个网站](https://tool.funsmall.cn/jsonsort/)。推荐使用[Visual Studio Code](https://github.com/microsoft/vscode)的比较功能。

如果你是Crowdin上Minecraft项目的翻译者，你也可以随时查看通知来获取新字符串。

### 网页部署
如果你需要在网页Material标题栏下方或者网页脚部自定义内容, 请在`views/custom/`目录下创建`header.html`或`footer.html`

`Vuetify`框架可用


## 贡献
我们欢迎你为这个资源包贡献自己的想法。请参阅`CONTRIBUTING.md`以获取一些建议。

积累一定贡献后我们会邀请你成为Collaborator。优先考虑中文Minecraft Wiki的编辑者。
## 声明
- 本资源包**仅供娱乐**，请勿将其可能存在的误导性内容当真。
- 本资源包与Mojang、Minecraft Wiki和Gamepedia无关，原中文翻译版权为Mojang和翻译者所有。
  - 关于正确的译名，请参见[中文Minecraft Wiki的译名标准化](https://minecraft-zh.gamepedia.com/Minecraft_Wiki:译名标准化)。
- 本资源包的资源包部分（即除去自动构建脚本和Mod内容字符串未经过梗体中文更改的部分）以 ***CC BY-NC-SA 4.0*** 协议授权。
  - 这意味着，你可在署名的情况下自由修改本资源包，但是你再创作的作品必须以本协议发布。
  - 这不是法律建议。
- 本项目附带的Mod内容字符串，未经梗体中文修改过的部分，按照 ***原作品的协议*** 发布。
- 本项目的自动构建脚本以 ***GPL 3.0*** 协议发布。

![GitHub forks](https://img.shields.io/github/forks/lakejason0/mcwzh-meme-resourcepack?style=social)    ![GitHub stars](https://img.shields.io/github/stars/lakejason0/mcwzh-meme-resourcepack?style=social)    ![GitHub watchers](https://img.shields.io/github/watchers/lakejason0/mcwzh-meme-resourcepack?style=social)
