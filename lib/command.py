#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-03 19:06:40
'''

def print_log(message):
    print ("\r[*] {0}".format(message), end="")

def print_flush():
    print ("\r\r", end="")

def print_info(message):
    print(("[+] {0}".format(message)))

def print_debug(message):
    print("[-] {0}".format(message))

def print_error(message):
    print(("[error] {0}".format(message)))

