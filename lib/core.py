#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-26 16:43:57
'''
from lib.command import print_log, print_info, print_error, splist
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from collections import defaultdict
from config.html_template import (
    html_head, html_title, html_body_head, html_body_title,
    html_body_a, html_body_end, html_style
                )
from dns import resolver
import dns
import os
import importlib
import sys
import re
import json



# 获取输出路径 这里应该可以指定路径来输出  
def get_output(domain):
    base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, "../", "output", domain)
    print(f"output_dir {output_dir}")
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    target_output_txt = os.path.join(output_dir, domain+".txt")
    target_output_html = os.path.join(output_dir, domain+".html")
    target_output_json = os.path.join(output_dir, domain+".json")
    return target_output_txt, target_output_html, target_output_json


def save_text(domain_ips_dict, target_output_txt):
    with open(target_output_txt, "w") as f:
            for domain, ips in domain_ips_dict.items():
                f.write(f"{domain}    {ips}\n")
    print_info("save txt success")

def save_json(domain_ips_dict, target_output_json):
    with open(target_output_json, "w") as f:
        json.dump(domain_ips_dict, f, indent=3)
    print_info("save json success")

def save_html(domain_ips_dict, scan_domain, target_output_html):
    html = html_head
    html +=  html_title.format(scan_domain)
    html += html_body_head
    html += html_body_title.format(scan_domain)
    for domain in domain_ips_dict.keys():
        html += html_body_a.format(domain)
    html += html_body_end
    html += html_style
    with open(target_output_html, "w") as f:
        f.write(html)
    print_info("save html success")



class EngineScan(object):
    """接口解析类"""
    def __init__(
        self, scan_domain, engine, thread_count=100, is_output=False,
        is_txt=False, is_json=False, is_html=False
                ):
        self.scan_domain = scan_domain
        self.engine = engine
        self.thread_count = thread_count
        # 输出相关
        self.is_output = is_output
        self.is_txt = is_txt
        self.is_json = is_json
        self.is_html = is_html
        # dns
        self.resolver = resolver
        self.resolver.nameservers=['8.8.8.8', '114.114.114.114']
        # 存储变量
        self.domains_set = set()
        self.domain_ips_dict = defaultdict(list)

    def run_scripts(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        scripts_path = os.path.join(base_path, "../","scripts")
        # 添加到搜索路径
        sys.path.append(scripts_path)
        scrips_list = list()
        scripts_class = list()
        if not self.engine: # 没有指定引擎 遍历scrips文件夹
            for root, dirs, files in os.walk(scripts_path):  
                for filename in files:
                    name = os.path.splitext(filename)[0]
                    suffix = os.path.splitext(filename)[1]
                    if suffix == '.py':
                        metaclass=importlib.import_module(os.path.splitext(filename)[0])
                        # 通过脚本的 enable属性判断脚本是否执行  
                        if metaclass.Scan(self.scan_domain).enable:
                            print_info("run script: "+metaclass.Scan(self.scan_domain).name)
                            result = metaclass.Scan(self.scan_domain).run()
                            self.domains_set = self.domains_set | result
                            print_info(f"add: {len(result)}  all count: {len(self.domains_set)}")
        else: # 指定了引擎
            for name in self.engine: # 这里不判断是否开启引擎 直接使用
                metaclass=importlib.import_module(name)
                print_info("run script: "+metaclass.Scan(scan_domain).name)
                result = metaclass.Scan(scan_domain).run()
                self.domains_set = self.domains_set | result
                print_info(f"add {len(result)}  all count: {len(self.domains_set)}")
                        
    def threadpool_dns(self):
        pool = ThreadPoolExecutor(self.thread_count) # 定义线程池
        all_task = list()
        for domain in self.domains_set:
            all_task.append(pool.submit(self.analysis_dns, domain))
        for task in all_task:
            task.result()

    def analysis_dns(self, domain):
        try:
            ans = self.resolver.query(domain, "A")
            if ans:
                ips = list()
                for i in ans.response.answer:
                    for j in i.items:
                            ip = j.to_text()
                            if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip):
                                self.domain_ips_dict[domain].append(ip)
        except dns.resolver.NoAnswer:
            pass
        except dns.exception.Timeout:
            pass
        except Exception as e:
            pass

    def save_doamin_ips(self):
        target_output_txt, target_output_html, target_output_json = get_output(
                    self.scan_domain
                )
        print(target_output_txt)
        if self.is_txt:
            save_text(self.domain_ips_dict, target_output_txt)
        if self.is_json:
            save_json(self.domain_ips_dict, target_output_json)
        if self.is_html:
            save_html(self.domain_ips_dict, self.scan_domain, target_output_html)

    def run(self):
        # 先用script下的接口获取子域名
        self.run_scripts()
        # 对这些接口进行dns解析 获取对应的ip列表
        self.threadpool_dns()
        # 判断是不是直接输出结果文件
        if self.is_output:
            self.save_doamin_ips()
        return self.domain_ips_dict


# 穷举类 
class ExhaustionScan(object):
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
                data = line.replace("\n", "").split("    ")
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
            ans = resolver.query("recar123456."+self.scan_domain , "A")
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
            print(e)
            return True
    
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
            pass
        
    def run(self):
        # 先进行泛解析判断
        print("is_analysis")
        if self.is_analysis():
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
