#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 18:05:15
@LastEditTime: 2019-05-30 19:45:05
'''
class Base(object):
    def __init__(self, scan_domain):
        self.scan_domain = scan_domain
    
    def run(self):
        print("base")
    
    
