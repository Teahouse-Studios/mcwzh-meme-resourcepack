import argparse
import json
import os
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="输入文件，编码必须为UTF-8")
parser.add_argument("outfile", help="输出文件，编码为UTF-8")
parser.add_argument("--indent", "-i", help="格式化json", type=int, default=2)
parser.add_argument("--reverse", "-r", help="反转，即json转lang", action="store_true")
args = parser.parse_args()

if not os.path.isfile(args.infile):
    print(f"文件:", args.infile, "不存在！")
    sys.exit(-1)

with open(args.infile, encoding='utf8') as ifile:
    if args.reverse:
        json = json.load(ifile)
        with open(args.outfile, 'w', encoding='utf8') as f:
            for key, value in json.items():
                f.write(f"{key}={value}\n")
    else:
        obj = {}
        for i in ifile.readlines():
            result = re.match("(.+)=(.+)", re.sub("#.*\n?", "", i))
            if not result:
                continue
            obj[result.group(1)] = result.group(2)
        json.dump(obj, open(args.outfile, 'w', encoding="utf8"), ensure_ascii=False, indent=args.indent)
