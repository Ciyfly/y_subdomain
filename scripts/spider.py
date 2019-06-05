#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-06-03 16:49:17
@LastEditTime: 2019-06-05 10:38:11
'''

from lib.base import Base
from lib.command import print_error, print_debug, print_log, print_flush
from config.config import WEIBU_APIKEY
import requests
import re

class Scan(Base):
    """ 爬虫 输入域名获取网页上的子域名
        默认爬取三层页面
    """
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "Spider"
        self.headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding':'gzip, deflate',
            'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    def run(self):
        try:
            # 这里只跑三次 
            # 第一次根
            spider_domain = self.scan(self.scan_domain)
            if spider_domain:
                
                self.sub = self.sub | spider_domain
                for d in spider_domain:
                    spider_domain_next = self.scan(d)  # 遍历第一次的进行爬取

                    if spider_domain_next:
                        self.sub = self.sub | spider_domain_next # 有就合并
                        for dd in spider_domain_next: # 遍历每个第二次返回的
                            spider_domain_over = self.scan(dd) # 对第二次的进行第三次 爬取
                            if spider_domain_over:
                                self.sub = self.sub | spider_domain_over # 结束 求并集
            print_flush()
            # print(self.sub)
            return self.sub
        except Exception as e:
            print_error("ERROR: "+self.name+" : "+str(e))

    def scan(self, domain):
        try:
            spider_domain = set()
            p = re.compile(u'((http|https)://(?:\w+\.)*?{0})'.format(self.scan_domain))
            if "http" in domain:
                url = domain
            else:
                url = "http://{0}".format(domain)
            response = requests.get(url, headers = self.headers ,timeout=3)
            result = p.findall(response.text)
            for d in result:
                print_log(url)
                spider_domain.add(d[0])
            # print(spider_domain)
            return spider_domain 
        except Exception as e:
            pass
