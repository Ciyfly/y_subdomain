#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-06-26 16:38:17
'''
from lib.parser import get_options

from lib.core import  EngineScan
from lib.command import print_log, print_info
import signal
import time


def ctrl_c(signum,frame):
    print()
    print("[-] input ctrl c")
    exit(1)

signal.signal(signal.SIGINT, ctrl_c)


def main():
    # 获取命令行参数  
    options,args = get_options()
    scan_domain = options.domain
    is_html = options.is_html
    is_json = options.is_json
    engine = options.engine
    exhaustion = options.exhaustion

    print_info("scan {0}\n".format(scan_domain))

    start = time.perf_counter()
    # 接口解析
    engine_scan = EngineScan(scan_domain, engine, is_output=True, is_txt=True, is_json=True, is_html=True)
    domain_ips_dict = engine_scan.run()
    print_info(len(domain_ips_dict))
    engine_end = (time.perf_counter() - start)
    print_info(f"引擎接口消耗时间:{engine_end}s")
    
    # start = time.perf_counter()
    # engine_result = run_scripts(scan_domain, engine)
    # engins_domain_ips = thread_dns(engine_result)
    # # print("\n"+str(engins_domain_ips))
    # print_info(len(engins_domain_ips))
    # engine_end = (time.perf_counter() - start)
    # print_info(f"引擎接口消耗时间:{engine_end}s")
    # # 开始穷举
    # if exhaustion:
    #     start = time.perf_counter()
    #     print_info("开始进行暴力穷举")
    #     exh = Exhaustion(scan_domain)
    #     exh_domain_ips = exh.run()
    #     end = (time.perf_counter() - start)
    #     print_info(f"暴力穷举程序消耗时间: {end}s")
    # else:
    #     exh_domain_ips = None
    # # 合并两个数据 
    # if exh_domain_ips:
    #     exh_keys = exh_domain_ips.keys()
    #     for domain in engins_domain_ips.keys():
    #         if domain not in exh_keys:
    #             engins_domain_ips[domain] = engins_domain_ips[domain]
    
    # # 输出 txt结果 输出json 输出html
    # # 保存txt
    # save_text(engins_domain_ips, scan_domain)
    # if is_json:
    #     save_json(engins_domain_ips, scan_domain)
    # if is_html:
    #     save_html(engins_domain_ips, scan_domain)

if __name__ == "__main__":
    main()
