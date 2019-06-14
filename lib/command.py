#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 17:49:08
@LastEditTime: 2019-06-12 19:18:55
'''
from config.html_template import (
    html_head, html_title, html_body_head, html_body_title,
    html_body_a, html_body_end, html_style
                    )
import os
import sys
import shutil
import json

base_path = os.path.dirname(os.path.abspath(__file__))

def print_log(message):
    # ljust(50) 实现长度不够存在显示残留 左对齐以空格达到指定长度
    print ("\r[*] {0}".format(message).ljust(50), end="")
    

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

def get_output_dir(scan_domain, init=False):
    output_dir = os.path.join(base_path, "../", "output", scan_domain)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    else:
        if init:
            shutil.rmtree(output_dir,True)
            os.mkdir(output_dir)
    return output_dir

def del_tmp(scan_domain):
    try:
        tmp_file_path = os.path.join(base_path, "../", "output", scan_domain+".tmp")
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            print_info("del tmpfile success")
    except Exception as e:
        print_error(f"删除临时文件失败: {e}")

def save_text(domain_ips, scan_domain):
    output_dir = get_output_dir(scan_domain, init=True)
    output_path = os.path.join(output_dir, scan_domain+".txt")
    with open(output_path, "w") as f:
        for domain in domain_ips.keys():
            f.write(str(domain)+" "+str(domain_ips[domain])+"\n")
    print_info("save txt success")
    del_tmp(scan_domain)

def save_json(domain_ips, scan_domain):
    output_dir = get_output_dir(scan_domain)
    output_path = os.path.join(output_dir, scan_domain+".json")
    with open(output_path, "w") as f:
        json.dump(domain_ips, f, indent=3)
    print_info("save json success")


def save_html(domain_ips, scan_domain):
    output_dir = get_output_dir(scan_domain)
    output_path = os.path.join(output_dir, scan_domain+".html")
    html = html_head
    html +=  html_title.format(scan_domain)
    html += html_body_head
    html += html_body_title.format(scan_domain)
    for domain in domain_ips.keys():
        html += html_body_a.format(domain)
    html += html_body_end
    html += html_style
    with open(output_path, "w") as f:
        f.write(html)
    print_info("save html success")
    



