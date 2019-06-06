#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-03 16:46:55
'''
from lib.command import print_log, print_info, print_error
import os
import importlib
import sys
import asyncio
import aiodns


loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)
def get_output(domain):
    base_path = os.path.dirname(os.path.abspath(__file__))
    out_put_dir = os.path.join(base_path, "output", domain)
    if not os.path.isdir(out_put_dir):
        os.makedirs(out_put_dir)
    target_output_txt = os.path.join(out_put_dir, domain+".txt")
    target_output_html = os.path.join(out_put_dir, domain+".html")
    return target_output_txt, target_output_html

def run_scripts(scan_domain, engine):
    base_path = os.path.dirname(os.path.abspath(__file__))
    scripts_path = os.path.join(base_path, "../","scripts")
    # 添加到搜索路径
    sys.path.append(scripts_path)
    scrips_list = list()
    scripts_class = list()
    result_set = set()
    if not engine: # 没有指定引擎 遍历scrips文件夹
        for root, dirs, files in os.walk(scripts_path):  
            for filename in files:
                name = os.path.splitext(filename)[0]
                suffix = os.path.splitext(filename)[1]
                if suffix == '.py':
                    metaclass=importlib.import_module(os.path.splitext(filename)[0])
                    # 通过脚本的 enable属性判断脚本是否执行  
                    if metaclass.Scan(scan_domain).enable:
                        print_info("run script: "+metaclass.Scan(scan_domain).name)
                        result = metaclass.Scan(scan_domain).run()
                        result_set = result_set | result
                        print_info("add : {0}   all count: {1}".format(len(result), len(result_set)))
    else: # 指定了引擎
        for name in engine: # 这里不判断是否开启引擎 直接使用
            metaclass=importlib.import_module(name)
            print_info("run script: "+metaclass.Scan(scan_domain).name)
            result = metaclass.Scan(scan_domain).run()
            result_set = result_set | result
            print_info("add : {0}   all count: {1}".format(len(result), len(result_set)))
    return result_set
                    
async def dns_query(domain, query_type='A'):
    try:
        q = await resolver.query(domain, query_type)
    except aiodns.error.DNSError:
        return None
    return q


def is_analysis(domain):
    """ 
    泛解析判断 
    通过不存在
    """
    false_domain = "Recar."+domain
    result = loop.run_until_complete(dns_query(false_domain))
    if not false_domain:
        print("[-] 泛解析 ")
        return True


# aiodns解析域名 获取ip
def asyn_dns(domains):
    domain_ips =dict()
    for domain in domains:
        result = loop.run_until_complete(dns_query(domain))
        if result:
            print_log(domain)
            domain_ips[domain] = result[0].host
    return domain_ips


