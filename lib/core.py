#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-07-10 21:29:18
'''

from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from collections import defaultdict
from config.html_template import (
    html_head, html_title, html_body_head, html_body_title,
    html_body_a, html_body_end, html_style
                )
from config.config import DNS_THRESHOLD
from dns import resolver
import dns
import os
import importlib
import sys
import re
import json
import random
import string
import queue
import threading
import time
import signal


def ctrl_c(signum,frame):
    print()
    print("[-] input ctrl c")
    sys.exit()

def print_queue_size(signum, frame):
    print()
    print(f"[debug] queue size: {frame.f_locals['self'].sub_dict_queue.qsize()}")

# ctrl+c
signal.signal(signal.SIGINT, ctrl_c)
# HUP
signal.signal(signal.SIGHUP, print_queue_size)

def print_log(message):
    # ljust(50) 实现长度不够存在显示残留 左对齐以空格达到指定长度
    print ("\r[*] {0}".format(message).ljust(50), end="")

def print_flush():
    print ("\r\r", end="")

def print_info(message):
    print(("[+] {0}".format(message)))

def print_debug(message):
    print("[-] {0}".format(message))

def print_error(message):
    print(("[error] {0}".format(message)))

class SaveDate(object):
    """用于保存域名结果"""
    def __init__(
        self, scan_domain, engine_domain_ips_dict=None, exh_domain_ips_dict=None,
              is_text=False, is_json=False, is_html=False
              ):
        self.engine_domain_ips_dict = engine_domain_ips_dict
        self.exh_domain_ips_dict = exh_domain_ips_dict
        self.clean_data()
        self.scan_domain = scan_domain
        self.is_text = is_text
        self.is_json = is_json
        self.is_html = is_html
        self.get_output()

    def clean_data(self):
        if self.engine_domain_ips_dict and self.exh_domain_ips_dict is None:
            # 只有 engine_domain_ips_dict
            self.domain_ips_dict = self.engine_domain_ips_dict
        elif self.exh_domain_ips_dict and self.engine_domain_ips_dict is None:
            # 只有 exh_domain_ips_dict
            self.domain_ips_dict = self.exh_domain_ips_dict
        elif self.engine_domain_ips_dict and self.exh_domain_ips_dict:
            # 都有
            for domain, ips in self.engine_domain_ips_dict.items():
                if domain in self.exh_domain_ips_dict.keys():
                    self.exh_domain_ips_dict[domain] = self.exh_domain_ips_dict[domain] + ips
                else:
                    self.exh_domain_ips_dict[domain] = ips
            self.domain_ips_dict = self.exh_domain_ips_dict

    def get_output(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_path, "../", "output", self.scan_domain)
        print_info(f"output_dir {output_dir}")
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        self.output_txt = os.path.join(output_dir, self.scan_domain+".txt")
        self.output_html = os.path.join(output_dir, self.scan_domain+".html")
        self.output_json = os.path.join(output_dir, self.scan_domain+".json")

    def save_text(self):
        with open(self.output_txt, "w") as f:
                for domain, ips in self.domain_ips_dict.items():
                    f.write(f"{domain}    {ips}\n")
        print_info("save txt success")

    def save_json(self):
        with open(self.output_json, "w") as f:
            json.dump(self.domain_ips_dict, f, indent=3)
        print_info("save json success")

    def save_html(self):
        html = html_head
        html +=  html_title.format(self.scan_domain)
        html += html_body_head
        html += html_body_title.format(self.scan_domain)
        for domain in self.domain_ips_dict.keys():
            html += html_body_a.format(domain)
        html += html_body_end
        html += html_style
        with open(self.output_html, "w") as f:
            f.write(html)
        print_info("save html success")

    def save_doamin_ips(self):
        if self.is_text:
            self.save_text()
        if self.is_json:
            self.save_json()
        if self.is_html:
            self.save_html()

class EngineScan(object):
    """接口解析类"""
    def __init__(self, scan_domain, engine=None, thread_count=100, get_black_ip=False):
        self.scan_domain = scan_domain
        self.engine = engine
        self.thread_count = thread_count
        # dns
        self.resolver = resolver
        self.resolver.nameservers=['8.8.8.8', '114.114.114.114']
        # 存储变量
        self.domains_set = set()
        self.domain_ips_dict = defaultdict(list)
        self.get_black_ip = get_black_ip
        # 去除泛解析
        self.black_ip = list()
        # {ip:{ domains: [域名], count: 计数}  }
        self.ip_domain_count_dict = dict()

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
                    if suffix == '.py' and name!="base":
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
                        if hasattr(j, "address"):
                            self.domain_ips_dict[domain].append(j.address)
        except dns.resolver.NoAnswer:
            pass
        except dns.exception.Timeout:
            pass
        except Exception as e:
            pass
    
    def remove_black_ip(self):
        # 对于接口返回域名的泛解析结果的去除  
        for domain, ips in self.domain_ips_dict.items():
            for ip in ips:
                if ip in self.ip_domain_count_dict.keys():
                    self.ip_domain_count_dict[ip]["count"] +=1
                    self.ip_domain_count_dict[ip]["domains"].append(domain)
                else:
                    self.ip_domain_count_dict[ip] = {"domains": [domain], "count": 1}
        # remove
        for ip, domains_count in self.ip_domain_count_dict.items():
            if domains_count["count"] > DNS_THRESHOLD: # 有50个域名指向了同一个ip jd的有大量指向一个ip 
                # 将泛解析的ip存下来 返回回去 
                self.black_ip.append(ip)
                for domain in domains_count["domains"]:
                    if domain in self.domain_ips_dict.keys():
                        # print(domain,  ip, domains_count["count"])
                        self.domain_ips_dict.pop(domain)

    def run(self):
        # 先用script下的接口获取子域名
        self.run_scripts()
        # 对这些接口进行dns解析 获取对应的ip列表
        self.threadpool_dns()
        # 对接口返回含有泛解析的域名去除  
        self.remove_black_ip()
        if self.get_black_ip: # 是否返回泛解析的ip  
            return self.domain_ips_dict, self.black_ip
        else:
            return self.domain_ips_dict


# 穷举类 
class ExhaustionScan(object):
    """暴力穷举"""
    def __init__ (self, scan_domain, thread_count=100,is_output=False, black_ip=list()):
        self.base_path  = os.path.dirname(os.path.abspath(__file__))
        self.resolver = resolver
        self.resolver.nameservers=['8.8.8.8', '114.114.114.114']
        self.scan_domain = scan_domain
        # 默认线程100个
        self.thread_count = thread_count
        self.is_output = is_output
        self.domain_ips_dict = defaultdict(list)
        self.sub_dict_queue = queue.Queue()
        self.load_subdomain_dict()
        self.all_size = self.sub_dict_queue.qsize()
        # 泛解析的ip 默认是空 可以将接口返回的 black_ip 传入这里 
        self.black_ip = black_ip
        # {ip:{ domains: [域名], count: 计数}  }
        self.ip_domain_count_dict = dict()

    def load_subdomain_dict(self):
        print_info("load sub dict")
        dict_path = os.path.join(self.base_path, "../","config", "sub.txt")
        with open(dict_path, "r") as f:
            for sub in f:
                self.sub_dict_queue.put(f"{sub.strip()}.{self.scan_domain}")
        print_info(f"quque all size: {self.sub_dict_queue.qsize()}")

    def is_analysis(self):
        """ 
        泛解析判断 
        通过不存在的域名进行判断
        """
        try:
            ans = self.resolver.query(
                ''.join(random.sample(string.ascii_lowercase,5))+"."+self.scan_domain , "A"
                )
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
            # print(domain)
            ans = resolver.query(domain, "A")
            if ans:
                ips = list()
                for i in ans.response.answer:
                    for j in i.items:
                        if hasattr(j, "address"):
                            # 增加对泛解析的操作
                            if self.remove_black_ip(domain, j.address):
                                self.domain_ips_dict[domain].append(j.address)
        except dns.resolver.NoAnswer:
            pass
        except dns.exception.Timeout:
            pass
        except Exception as e:
            pass

    def remove_black_ip(self, domain, ip):
        """ 对解析后的域名ip判断是否是泛解析 超过阈值进行忽略和删除"""
        if ip in self.black_ip:
            return False
        if ip in self.ip_domain_count_dict.keys():
            self.ip_domain_count_dict[ip]["count"] +=1
            self.ip_domain_count_dict[ip]["domains"].append(domain)
        else:
            self.ip_domain_count_dict[ip] = {"domains": [domain], "count": 1}
        # 判断是否达到泛解析ip阈值 达到则删除记录下来的并增加黑ip  
        if self.ip_domain_count_dict[ip]["count"] > DNS_THRESHOLD:
            for domain in self.ip_domain_count_dict[ip]["domains"]:
                if domain in self.domain_ips_dict.keys():
                    self.domain_ips_dict.pop(domain)
            self.black_ip.append(ip)
            return False
        else:# 没有达到阈值
            return True
                
    def worker(self):
        while not self.sub_dict_queue.empty():
            domain = self.sub_dict_queue.get()
            if domain is None:
                break
            self.analysis_dns(domain)
            self.sub_dict_queue.task_done()

    def run(self):
        # 先进行泛解析判断
        if self.is_analysis():
            print_debug("存在泛解析")
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.worker)
            t.setDaemon(True)
            t.start()
            threads.append(t)
        # 阻塞 等待队列消耗完
        print_info("start thread ")
        start = time.perf_counter()
        while not self.sub_dict_queue.empty():
            time.sleep(1)
            if self.is_output:
                out_u = int(self.sub_dict_queue.qsize()/self.all_size*50) # ##
                out_l = 50 - out_u
                percentage = 100-(self.sub_dict_queue.qsize()/self.all_size*100)
                print(
                    '\r'+'[' + '>' * out_l + '-' * out_u +']'
                    + f'{percentage:.2f}%'
                    + f'|size: {self.sub_dict_queue.qsize()}'
                    + f'|use time: {time.perf_counter() - start:.2f}s', end="")
        print()
        self.sub_dict_queue.join()
        return self.domain_ips_dict

