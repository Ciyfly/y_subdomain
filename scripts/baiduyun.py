#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-06-27 17:09:20
'''
from lib.base import Base
import requests
import json

class Scan(Base):
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "百度云观测"
        self.base_url = "http://ce.baidu.com/index/getRelatedSites?site_address={0}"

    def run(self):
        try:
            get_url = self.base_url.format(self.scan_domain)
            response = requests.get(get_url)
            if response.status_code == 200:
                data = json.loads(response.content)['data']
                for domain in data:
                    self.sub.add(domain['domain'])
                return  self.sub
            else:
                return set()
        except Exception as e:
            "ERROR: "+self.name+" : "+str(e)
            return set()
