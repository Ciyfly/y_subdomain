#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-05-31 12:44:15
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
            'accept': 'application/json',
            'content-type': 'application/json',
            'cookie': '__cfduid=da77cc76b1c87e5c582cf3e500d67eac61557832243; cf_clearance=a4210874de44788c6b7f1fd0d4d2b3878676687e-1559272290-14400-150; _ga=GA1.2.1253679075.1559272407; _gid=GA1.2.1976762282.1559272407',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }

    def run(self):
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

