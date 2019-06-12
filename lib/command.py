#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-12 19:18:55
'''
import os
import shutil

base_path = os.path.dirname(os.path.abspath(__file__))

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

def splist(l, s):
    return [l[i:i+s] for i in range(len(l)) if i%s==0]

def init_output_dir(domain):
    output_dir = os.path.join(base_path, "../", "output", domain)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        shutil.rmtree(output_dir,True)
        os.mkdir(output_dir)
    return output_dir
def save_text(domain_ips, domain):
    output_dir = init_output_dir(domain)
    output_path = os.path.join(output_dir, domain+".txt")
    with open(output_path, "w") as f:
        for domain in domain_ips.keys():
            f.write(str(domain)+" "+domain_ips[domain]+"\n")
    print_info("save txt success")

def save_json(domain_ips, domain):
    output_dir = init_output_dir(domain)
    output_path = os.path.join(output_dir, domain+".json")
    with open(output_path, "w") as f:
        json.dump(domain_ips, f, indent=4)
    print_info("save json success")


def save_html(domain_ips, domain)
    output_dir = init_output_dir(domain)
    output_path = os.path.join(output_dir, domain+".html")
    # TODO 生成html报告
