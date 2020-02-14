# 中文Minecraft Wiki 梗体中文资源包 · Unofficial

[![Tencent QQ](https://img.shields.io/static/v1?label=QQ&message=657876815&color=eb1923&style=flat-square&logo=tencent%20qq)](https://jq.qq.com/?_wv=1027&k=5tqdTeR)    [![GitHub issues](https://img.shields.io/github/issues/lakejason0/mcwzh-meme-resourcepack?logo=github&style=flat-square)](https://github.com/lakejason0/mcwzh-meme-resourcepack/issues)    [![GitHub pull requests](https://img.shields.io/github/issues-pr/lakejason0/mcwzh-meme-resourcepack?logo=github&style=flat-square)](https://github.com/lakejason0/mcwzh-meme-resourcepack/pulls)    ![GitHub Licence](https://img.shields.io/github/license/lakejason0/mcwzh-meme-resourcepack?style=flat-square)    [![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/lakejason0/mcwzh-meme-resourcepack?label=latest%20version&style=flat-square)](https://github.com/lakejason0/mcwzh-meme-resourcepack/releases)    [![Minecraft ver](https://img.shields.io/static/v1?label=Minecraft%20version&message=1.12.2-20w06a&color=db2331&style=flat-square&logo=)](https://minecraft.net)

## 作用
这个资源包将一部分译名或其他游戏内字符串替换成了一些知名/不知名的梗或笑话，或将其用诙谐的语言重写了一遍。
## 用法
在[Releases](https://github.com/lakejason0/mcwzh-meme-resourcepack/releases)中下载此资源包。
### 常规
请选择`mcwzh-meme.zip`下载，像其他资源包一样复制到你对应的`.minecraft/resourcepacks/`目录中（[MCBBS上的教程](https://www.mcbbs.net/thread-880869-1-1.html)）（MultiMC或其他分离版本的启动器请自行查找）。资源包新建了一个语言，安装启用后在语言设置中选择“**梗体中文**”即可体验。
### 加载Mod时
普通版本的资源包**无法**覆盖Mod字符串，会导致Mod内容**全部变为英文**。请下载`mcwzh-meme_compatible.zip`，以保证体验。安装流程几乎相同，只是选择的语言应该是**普通的“简体中文”**。
## 鹦鹉通道
### 体验最新内容
想要**抢先体验**最前沿~~整活~~版本，请按以下方法操作：
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
在文件夹中会出现`mcwzh-meme.zip`和`mcwzh-meme_compatible.zip`两个资源包，名称和作用如上所述。

如果只需要常规的资源包，运行：
``` bash
python build.py normal
```
如果只需要加载Mod版的资源包，运行：
``` bash
python build.py compat
```
### 自助跟进游戏版本
此资源包的语言文件顺序与原版的英文顺序并不一致（本资源包是将key按照字母顺序排序）。如果原版的英文译名跟进了，请先将解包的英文语言文件按照前文所述排序，可以参考[这个网站](https://tool.funsmall.cn/jsonsort/)。推荐使用[Visual Studio Code](https://github.com/microsoft/vscode)的比较功能。
## 声明
* 本资源包**仅供娱乐**，请勿当真。
* 若在直播/视频中使用了本资源包，请注明**本包名称**及其**下载地址**。
* 本资源包与Mojang、Minecraft Wiki和Gamepedia无关，原中文翻译版权为Mojang和翻译者所有。
* 本资源包以 ***placeholder*** 协议授权。

![GitHub forks](https://img.shields.io/github/forks/lakejason0/mcwzh-meme-resourcepack?style=social)    ![GitHub stars](https://img.shields.io/github/stars/lakejason0/mcwzh-meme-resourcepack?style=social)    ![GitHub watchers](https://img.shields.io/github/watchers/lakejason0/mcwzh-meme-resourcepack?style=social)
