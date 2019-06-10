#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-06-03 16:49:17
@LastEditTime: 2019-06-05 18:08:06
'''

from lib.base import Base
from lib.command import print_error, print_debug, print_log, print_flush
from config.config import WEIBU_APIKEY
# from gevent import monkey;monkey.patch_all()
import requests
import re
import gevent

class Scan(Base):
    """ 爬虫 输入域名获取网页上的子域名
        默认爬取三层页面
    """
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "Spider"
        self.enable = False
        self.headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding':'gzip, deflate',
            'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
        self.one_domain = set()
        self.two_domain = set()
        self.three_domain = set()

    def run(self):
        try:
            # 这里只跑三次 
            # 第一次根
            self.scan(self.scan_domain, 1)
            if self.one_domain:
                self.sub = self.sub | self.one_domain
                # 遍历第一次的进行爬取
                tasks=[gevent.spawn(self.scan, d, 2)  for d in self.one_domain]
                gevent.joinall(tasks)

                if self.two_domain:
                    self.sub = self.sub | self.two_domain # 有就合并
                    tasks=[gevent.spawn(self.scan, dd, 3)  for dd in self.two_domain]
                    gevent.joinall(tasks)

                    if self.three_domain:
                        self.sub = self.sub | self.three_domain # 结束 求并集
            print_flush()
            # print(self.sub)
            return self.sub
        except Exception as e:
            print_error("ERROR: "+self.name+" : "+str(e))

    def scan(self, domain, flag):
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
                print_log(d[0])
                spider_domain.add(d[0])
            # print(spider_domain)
            if flag == 1:                
                self.one_domain = self.one_domain | spider_domain 
            if flag == 2:
                self.two_domain = self.two_domain | spider_domain 
            if flag == 3:
                self.three_domain = self.three_domain | spider_domain 
        except TimeoutError:
            pass
        except Exception as e:
            pass
