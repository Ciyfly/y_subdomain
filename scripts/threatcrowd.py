#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-06-27 17:09:51
'''
from lib.base import Base
import requests
import json

class Scan(Base):
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "threatcrowd"
        self.base_url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={0}"
        self.headers = {
            'authority': 'www.threatcrowd.org',
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        self.enable = False

    def run(self):
        try:
            get_url = self.base_url.format(self.scan_domain)
            response = requests.get(url=get_url, headers = self.headers )
            if response.status_code == 200:
                data = json.loads(response.content).get('subdomains')
                # data = str(data,encoding='utf-8')
                for domain in data:
                    self.sub.add(domain)
                return  self.sub
            else:
                return set()
        except Exception as e:
            print("ERROR: "+self.name+" : "+str(e))
            return set()
