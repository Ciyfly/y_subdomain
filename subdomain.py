#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-06-27 19:35:16
'''

from lib.parser import get_options
from lib.core import EngineScan, ExhaustionScan, SaveDate, print_log, print_info
import signal
import time
import sys

def ctrl_c(signum,frame):
    print()
    print("[-] input ctrl c")
    sys.exit()

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

    # # 接口解析
    start = time.perf_counter()
    engine_scan = EngineScan(scan_domain, engine)
    engine_domain_ips_dict = engine_scan.run()
    print_info(len(engine_domain_ips_dict))
    engine_end = (time.perf_counter() - start)
    print_info(f"引擎接口消耗时间:{engine_end}s")

    exh_domain_ips_dict = None
    if exhaustion:
        # 穷举解析
        start = time.perf_counter()
        exhaustion_scan =  ExhaustionScan(scan_domain, thread_count=50, is_output=True)
        exh_domain_ips_dict = exhaustion_scan.run()
        print(len(exh_domain_ips_dict))
        exh_end = (time.perf_counter() - start)
        print_info(f"穷举消耗时间:{exh_end}s")
    
    
    save_data = SaveDate(
        scan_domain,
        engine_domain_ips_dict= engine_domain_ips_dict,
        exh_domain_ips_dict=exh_domain_ips_dict,
        is_text=True,
        is_json=is_json,
        is_html=is_html
        )
    save_data.save_doamin_ips()

if __name__ == "__main__":
    main()
