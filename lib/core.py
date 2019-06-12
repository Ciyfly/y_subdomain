#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-12 19:23:10
'''
from lib.command import print_log, print_info, print_error, splist
from tqdm import tqdm
from dns import resolver
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from collections import defaultdict
import os
import importlib
import sys
import dns
import re


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

class Exhaustion(object):
    """暴力穷举"""
    def __init__ (self, scan_domain):
        print("init")
        self.base_path  = os.path.dirname(os.path.abspath(__file__))
        self.scan_domain = scan_domain
        self.domain_ips = defaultdict(list)
        self.sub_dict = list()
        self.load_subdomain_dict()
        self.tmp_file = self.get_tmpfile()
        print("load over")

    def get_tmpfile(self):
        output_path = os.path.join(self.base_path, "../","output")
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        tmp_file = os.path.join(output_path, self.scan_domain+".tmp")
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        return tmp_file

    def save_tmp_file(self):
        with open(self.tmp_file, "a+") as f:
            domain_ips_keys = list(self.domain_ips.keys())
            for key in domain_ips_keys:
                data = key+"    "+str(self.domain_ips.pop(key))+"\n"
                f.write(data)

    def load_subdomain_dict(self):
        dict_path = os.path.join(self.base_path, "../","config", "sub.txt")
        with open(dict_path, "r") as f:
            line = f.readline()
            while line:
                self.sub_dict.append(line.replace("\n", ""))
                line = f.readline()
    
    def read_tmp_file(self):
        with open(self.tmp_file, "r") as f:
            line = f.readline()
            while line:
                data = line.replace("\n").splist(" ")
                domain = data[0]
                ips = eval(data[1])
                self.domain_ips[domain] = ips
                line = f.readline()

    def is_analysis(self):
        """ 
        泛解析判断 
        通过不存在
        """
        try:
            ans = resolver.query("recar123456"+self.scan_domain , "A")
            if ans:
                ips = list()
                for i in ans.response.answer:
                    for j in i.items:
                            ip = j.to_text()
                            if ip:
                                return False
        except dns.resolver.NoAnswer:
            return True
        except dns.exception.Timeout:
            return True
        except Exception as e:
            print_error(e)
    
    def analysis_dns(self, domain):
        try:
            ans = resolver.query(domain, "A")
            if ans:
                ips = list()
                for i in ans.response.answer:
                    for j in i.items:
                            ip = j.to_text()
                            if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
                                self.domain_ips[domain].append(ip)
        except dns.resolver.NoAnswer:
            pass
        except dns.exception.Timeout:
            pass
        except Exception as e:
            print_error(e)
        
    def run(self):
        # 先进行泛解析判断
        print("is_analysis")
        if not self.is_analysis():
            pool = ThreadPoolExecutor(80) # 配置80个线程
            # 对字典进行切割 每5000个为一组进行解析
            splist_sub_dict = splist(self.sub_dict, 5000)
            for sub_dict in splist_sub_dict:
                all_task = list()
                for sub in  sub_dict:
                    domain = sub+"."+self.scan_domain
                    print(domain)
                    all_task.append(pool.submit(self.analysis_dns, domain))
                for task in all_task:
                    task.result()
                self.save_tmp_file()
            # 最后解析tmp文件然后返回数据进行封装
            self.read_tmp_file()
            return self.domain_ips
        else:
            print_error("域名有泛解析 不会执行穷举")
            return None

