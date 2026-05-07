#!/usr/bin/env python3
# 在更新26.1.x的字符串时，26.2-snapshot-2已发布。
# 本工具的初始目的，是为了筛选掉26.2的字符串。
import json
import sys

def filter_json_by_keys(zh_cn_path, en_us_path, output_path):
    """
    筛选 zh_cn.json，只保留 en_us.json 中存在的键
    """
    try:
        # 读取中文JSON文件
        with open(zh_cn_path, 'r', encoding='utf-8') as f:
            zh_cn_data = json.load(f)
        
        # 读取英文JSON文件
        with open(en_us_path, 'r', encoding='utf-8') as f:
            en_us_data = json.load(f)
        
        # 获取英文JSON的所有键
        en_keys = set(en_us_data.keys())
        
        # 筛选中文JSON，只保留英文中存在的键
        filtered_data = {key: zh_cn_data[key] for key in zh_cn_data if key in en_keys}
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=2)
        
        print(f"处理完成！")
        print(f"原始中文键数量: {len(zh_cn_data)}")
        print(f"英文键数量: {len(en_keys)}")
        print(f"筛选后键数量: {len(filtered_data)}")
        print(f"输出文件: {output_path}")
        
    except FileNotFoundError as e:
        print(f"错误: 找不到文件 - {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) != 4:
        print("用法: python filter_json.py <zh_cn.json> <en_us.json> <output.json>")
        print("示例: python filter_json.py zh_cn.json en_us.json filtered_zh_cn.json")
        sys.exit(1)
    
    # 获取参数
    zh_cn_file = sys.argv[1]
    en_us_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # 执行筛选
    filter_json_by_keys(zh_cn_file, en_us_file, output_file)
