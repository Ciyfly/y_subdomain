#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 16:07:49
@LastEditTime: 2019-06-26 16:43:50
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

    parser.add_option('--exh',action='store_true', dest="exhaustion", default=False, help="是否进行暴力穷举")
    
    parser.add_option('--json',action='store_true', dest="is_json", default=False, help="是否生成json报告")

    parser.add_option('--html',action='store_true', dest="is_html", default=False, help="是否生成html报告")
    (options,args) = parser.parse_args()
    if  options.domain==None:
        parser.print_help()
        sys.exit(0)
    if "www" in options.domain or "http://" in options.domain :
        options.domain =options.domain.replace("www.","").replace("http://", "")
    if options.engine:
        options.engine = options.engine.split(",")

    return options,args