#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-05-31 16:24:04
'''
import os
import importlib
import sys
from lib.command import print_log, print_info, print_error

def get_output(domain):
    base_path = os.path.dirname(os.path.abspath(__file__))
    out_put_dir = os.path.join(base_path, "output", domain)
    if not os.path.isdir(out_put_dir):
        os.makedirs(out_put_dir)
    target_output_txt = os.path.join(out_put_dir, domain+".txt")
    target_output_html = os.path.join(out_put_dir, domain+".html")
    return target_output_txt, target_output_html

def run_scripts(scan_domain, exclude):
    base_path = os.path.dirname(os.path.abspath(__file__))
    scripts_path = os.path.join(base_path, "../","scripts")
    # 添加到搜索路径
    sys.path.append(scripts_path)
    scrips_list = list()
    scripts_class = list()
    result_set = set()
    for root, dirs, files in os.walk(scripts_path):  
        for filename in files:
            name = os.path.splitext(filename)[0]
            suffix = os.path.splitext(filename)[1]
            if suffix == '.py' and name not in exclude:
                metaclass=importlib.import_module(os.path.splitext(filename)[0])
                # 通过脚本的 enable属性判断脚本是否执行  
                if metaclass.Scan(scan_domain).enable:
                    print_info("run script: "+metaclass.Scan(scan_domain).name)
                    result = metaclass.Scan(scan_domain).run()
                    result_set = result_set | result
                    print_info("add : {0}   all count: {1}".format(len(result), len(result_set)))

def scan(doamin):
    pass