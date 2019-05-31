#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-05-31 15:33:00
'''

def print_log(message):
    print ("\r [*] {0}".format(message), end="")

def print_info(message):
    print(("[+] {0}".format(message)))

def print_error(message):
    print(("[-] {0}".format(message)))

