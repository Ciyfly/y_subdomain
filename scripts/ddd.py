#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-05-30 19:45:44
'''
from lib.base import Base
class Scan(Base):
    def __init__(self, scan_domain):
        super().__init__(scan_domain)
        self.name = "ddd"

    def run(self):
        print("run ddd")
    
    
