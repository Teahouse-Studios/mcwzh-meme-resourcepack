import json,re,os,sys,argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile",help="输入文件，编码必须为UTF-8")
parser.add_argument("outfile",help="输出文件，编码为UTF-8")
parser.add_argument("--indent","-i",help="格式化json",action="store_true")
parser.add_argument("--reverse","-r",help="反转，即json转lang",action="store_true")
args = parser.parse_args()
if not os.path.exists(args.infile):
	print(f"文件{args.infile}不存在！")
	sys.exit(-1)
f=open(args.infile,encoding='utf8')
if args.reverse:
	json=json.load(f)
	f.close()
	f=open(args.outfile,'w',encoding='utf8')
	for key,value in json.items():
		f.write(f"{key}={value}\n")
	f.close()
else:
	obj={}
	for i in f.readlines():
		result=re.match("(.+)=(.+)",re.sub("#.*\n?","",i))
		if not result:
			continue
		obj[result.group(1)]=result.group(2)
	f.close()
	f=open(args.outfile,'w',encoding="utf8")
	json.dump(obj,f,ensure_ascii=False,indent=args.indent)
	f.close()