#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 16:07:49
LastEditTime: 2021-05-20 14:56:30
'''
from optparse import OptionParser
from config.config import VERSION, BANNER
USAGE = "python domain -d xxx.com"
import sys
def get_options():
    print(BANNER)
    parser = OptionParser(usage=USAGE,version=VERSION)

    parser.add_option('-d', type=str, dest="domain", help="指定要测试的域名")
    
    parser.add_option('-e', type=str, dest="engine", help="指定使用的引擎 逗号间隔")

    parser.add_option('-c', type=str, dest="sub_dict", help="指定使用的字典 不指定默认使用默认的")

    parser.add_option('-f', type=str, dest="domain_file", help="指定域名列表文件 默认使用小字典2w")

    parser.add_option('-t', type=int, dest="thread_count", help="指定线程数 默认500")

    parser.add_option('--private',action='store_true', dest="is_private", default=False, help="是否对内网ip进行清除")
    
    parser.add_option('--title',action='store_true', dest="get_title", default=False, help="是否直接获取域名的title信息")

    parser.add_option('--gen',action='store_true', dest="gen_rule", default=False, help="是否加上动态规则生成的字典")

    parser.add_option('--exh',action='store_true', dest="exhaustion", default=False, help="是否进行暴力穷举")
    
    parser.add_option('--exo',action='store_true', dest="exhaustion_only", default=False, help="只进行暴力穷举")
    
    parser.add_option('--next',action='store_true', dest="next_sub", default=False, help="默认穷举到三级域名 开启则穷举到四级域名")

    parser.add_option('--big_dict',action='store_true', dest="big_dict", default=False, help="默认使用小字典2w 开启则使用大字典200w")
    
    parser.add_option('--json',action='store_true', dest="is_json", default=False, help="是否生成json报告")

    parser.add_option('--html',action='store_true', dest="is_html", default=False, help="是否生成html报告")
    (options,args) = parser.parse_args()
    if  options.domain==None and options.domain_file==None:
        parser.print_help()
        sys.exit(0)
    if options.domain:
        if "www" in options.domain or "http://" in options.domain :
            options.domain =options.domain.replace("www.","").replace("http://", "")
    if options.engine:
        options.engine = options.engine.split(",")

    return options,args
