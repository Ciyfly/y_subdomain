#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-08-06 22:12:12
'''

from lib.parser import get_options
from lib.core import EngineScan, ExhaustionScan, SaveDate, print_log, print_info
import time
import sys

def main():
    # 获取命令行参数  
    options,args = get_options()
    scan_domain = options.domain
    domain_file = options.domain_file
    is_html = options.is_html
    is_json = options.is_json
    is_private = options.is_private
    engine = options.engine
    sub_dict = options.sub_dict
    exhaustion = options.exhaustion
    exhaustion_only = options.exhaustion_only
    domains = list()
    if domain_file:
        with open(domain_file, "r") as f:
            for domain in f:
                domains.append(domain.strip())
    else:
        domains.append(scan_domain)
    for scan_domain in domains:
        print_info("scan {0}\n".format(scan_domain))
        
        engine_domain_ips_dict =None # 初始化
        if not exhaustion_only: # 是否只进行穷举解析
            # # 接口解析
            start = time.perf_counter()
            engine_scan = EngineScan(scan_domain, engine, is_private=is_private)
            engine_domain_ips_dict = engine_scan.run()
            print_info(len(engine_domain_ips_dict))
            engine_end = (time.perf_counter() - start)
            print_info(f"引擎接口消耗时间:{engine_end}s")

        exh_domain_ips_dict = None
        if exhaustion or exhaustion_only:
            # 穷举解析
            start = time.perf_counter()
            exhaustion_scan =  ExhaustionScan(
                scan_domain, thread_count=100,
                is_output=True, is_private=is_private,
                sub_dict = sub_dict
                )
            exh_domain_ips_dict = exhaustion_scan.run()
            if exh_domain_ips_dict:
                print_info(len(exh_domain_ips_dict))
                exh_end = (time.perf_counter() - start)
                print_info(f"穷举消耗时间:{exh_end}s")
        
        # 保存结果  
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
