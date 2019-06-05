#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-06-05 10:33:13
'''
from lib.parser import get_options
from config.config import BANNER
from lib.core import get_output, run_scripts
from lib.command import print_log, print_info

def main():
    print(BANNER)
    options,args = get_options()
    scan_domain = options.domain
    is_html = options.is_html
    engine = options.engine
    print_info("scan {0}\n".format(scan_domain))
    target_output_txt, target_output_html = get_output(scan_domain)
    # for i in range(10000):
    #     print_log("scan scripts: "+str(i))
    # print()
    run_scripts(scan_domain, engine)
    

        

if __name__ == "__main__":
    main()