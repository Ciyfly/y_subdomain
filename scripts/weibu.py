#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-05-31 16:34:32
'''
from lib.base import Base
from lib.command import print_error
from config.config import WEIBU_APIKEY
import requests
import json

class Scan(Base):
    """一分钟只能使用六次"""
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "微步"
        self.base_url = 'https://x.threatbook.cn/api/v1/domain/query'
        self.enable = False
        
    def run(self):
        try:
            params = {'apikey': WEIBU_APIKEY,'domain': self.scan_domain, "field": "sub_domains"}
            response = requests.post(self.base_url, params=params)
            if response.status_code == 200:
                data = json.loads(response.content).get("sub_domains").get("data")
                # data = json.loads(response.content).get("sub_domains").get("data")
                for domain in data:
                    self.sub.add(domain)
                return  self.sub
            else:
                return set()
        except Exception as e:
            print_error("ERROR: "+self.name+" : "+str(e))

