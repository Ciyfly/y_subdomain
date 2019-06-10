#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-10 19:55:00
'''
from lib.command import print_log, print_info, print_error
from tqdm import tqdm
from dns import resolver
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from collections import defaultdict
import os
import importlib
import sys
import dns
import re
#import asyncio
#import aiodns
#import uvloop
#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# servers = ['114.114.114.114','8.8.8.8', '202.38.64.1', '119.23.248.241']
servers = ['114.114.114.114']
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# loop = asyncio.get_event_loop()
# resolver = aiodns.DNSResolver(loop=loop,servers=servers)

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
        return q
    except aiodns.error.DNSError:
        return None
    except Exception as e:
        print_error(e)


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
    for domain in tqdm(domains):
        result = loop.run_until_complete(dns_query(domain))
        if result:
            domain_ips[domain] = result[0].host
    return domain_ips

def thread_dns(domains):
    pool = ThreadPoolExecutor(50) # 定义线程池
    domain_ips = defaultdict(list)
    all_task = list()
    for domain in domains:
        all_task.append(pool.submit(analysis_dns, domain, domain_ips))
    for task in all_task:
        task.result()
     
    return domain_ips

def analysis_dns(domain, domain_ips):
    try:
        ans = resolver.query(domain, "A")
        if ans:
            ips = list()
            for i in ans.response.answer:
                for j in i.items:
                        ip = j.to_text()
                        if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
                            domain_ips[domain].append(ip)
    except dns.resolver.NoAnswer:
        pass
    except dns.exception.Timeout:
        pass
    except Exception as e:
        print_error(e)

