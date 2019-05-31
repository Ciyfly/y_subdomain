#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-05-31 16:10:57
'''
from lib.base import Base
from lib.command import print_error
from config.config import VIRUSTOTAL_APIKEY
import requests
import json

class Scan(Base):
    """一分钟只能使用四次"""
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "virustotal"
        self.base_url = 'https://www.virustotal.com/vtapi/v2/domain/report'

    def run(self):
        try:
            params = {'apikey': VIRUSTOTAL_APIKEY,'domain': self.scan_domain}
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = json.loads(response.content).get("subdomains")
                for domain in data:
                    self.sub.add(domain)
                return  self.sub
            else:
                return set()
        except Exception as e:
            print_error("ERROR: "+self.name+" : "+str(e))
