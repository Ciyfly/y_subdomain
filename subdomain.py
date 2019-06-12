#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-06-12 19:24:31
'''
from lib.parser import get_options
from config.config import BANNER
# from lib.core import get_output, run_scripts, asyn_dns, thread_dns
from lib.core import get_output, Exhaustion
from lib.command import print_log, print_info
# from gevent import monkey;monkey.patch_all()
import signal
import time
def ctrl_c(signum,frame):
    print()
    print("[-] input ctrl c")
    exit(1)

signal.signal(signal.SIGINT, ctrl_c)


def main():
    print(BANNER)
    options,args = get_options()
    scan_domain = options.domain
    is_html = options.is_html
    is_json = options.is_json
    engine = options.engine
    exhaustion = options.exhaustion
    print_info("scan {0}\n".format(scan_domain))
    target_output_txt, target_output_html = get_output(scan_domain)
    # 接口解析
    start = time.perf_counter()
    engine_result = run_scripts(scan_domain, engine)
    engins_domain_ips = thread_dns(engine_result)
    print("\n"+str(domain_ips))
    print(len(domain_ips))
    engine_end = (time.perf_counter() - start)
    print_info(f"引擎接口消耗时间:{engine_end}s")
    # 开始穷举
    if exhaustion:
        start = time.perf_counter()
        print_info("开始进行暴力穷举")
        exh = Exhaustion(scan_domain)
        exh_domain_ips = exh.run()
        end = (time.perf_counter() - start)
        print_info(f"暴力穷举程序消耗时间: {end}s")
    else:
        exh_domain_ips = None
    # 合并两个数据 
    if exh_domain_ips:
        exh_keys = exh_domain_ips.keys()
        for domain in engins_domain_ips.keys():
            if domain not in exh_keys:
                engins_domain_ips[domain] = engins_domain_ips[domain]
    
    # 输出 txt结果 输出json 输出html
    # TODO 将结果进行保存


if __name__ == "__main__":
    main()
