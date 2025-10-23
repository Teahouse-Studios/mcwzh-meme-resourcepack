# 语言文件更新工具链

在 Minecraft 字符串更新时，可以使用本工具链将差异加载到工作区，经人工修改后可以patch回模块本体。

## Steps

### 1. 生成差异

命令：`python gen_diff.py <version_id>` or `python gen_diff.py latest`

更新源为对应 Minecraft 版本的**简体中文语言文件 (zh_cn.json)**。

工具链会生成 `pending.json` 和 `filters.json`。

### `pending.json`

在这里对新的字符串进行 memification。

### `filters.json`

考虑到字符串中可能存在NSFW或NSFC内容，可以在该文件中添加映射。例如：

```json
{
    "sfc": {
        "胸部": "切斯特",
        "死": "失败"
    },
    "sfw": {
        "菊♂爆": "举办",
        "♂": ""
    }
}
```

### 2. 应用差异

命令：`python apply_patch.py`

将`pending.json`中的内容插入`meme_resourcepack`模块中的`zh_meme.json`中，并将翻译值排序。

同时，遍历`pending.json`中的翻译，如果包含`sfc`或`sfw`中的映射键，则会将映射后的键值对添加到对应模块中。