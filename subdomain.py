#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-05-30 19:48:06
'''
from lib.parser import get_options
from config.config import BANNER
from lib.command import get_output, run_scripts, print_log
from loguru import logger


def main():
    print(BANNER)
    options,args = get_options()
    scan_domain = options.domain
    is_html = options.is_html
    target_output_txt, target_output_html = get_output(scan_domain)
    for i in range(10000):
        print_log("scan scripts: "+str(i))
    print()
    run_scripts(scan_domain)
    

        

if __name__ == "__main__":
    main()