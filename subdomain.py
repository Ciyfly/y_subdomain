#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-06-27 17:02:56
'''

from lib.parser import get_options
from lib.core import EngineScan, ExhaustionScan, SaveDate, print_log, print_info
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
    engine_scan = EngineScan(scan_domain, engine)
    engine_domain_ips_dict = engine_scan.run()
    print_info(len(engine_domain_ips_dict))
    engine_end = (time.perf_counter() - start)
    print_info(f"引擎接口消耗时间:{engine_end}s")

    exh_domain_ips_dict = None
    if exhaustion:
        # 穷举解析
        start = time.perf_counter()
        exhaustion_scan =  ExhaustionScan(scan_domain, thread_count=50)
        exh_domain_ips_dict = exhaustion_scan.run()
        print(len(exh_domain_ips_dict))
        exh_end = (time.perf_counter() - start)
        print_info(f"穷举消耗时间:{exh_end}s")
    
    
    save_data = SaveDate(
        scan_domain,
        engine_domain_ips_dict= engine_domain_ips_dict,
        exh_domain_ips_dict=exh_domain_ips_dict,
        is_text=True,
        is_json=True,
        is_html=True
        )
    save_data.save_doamin_ips()
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
