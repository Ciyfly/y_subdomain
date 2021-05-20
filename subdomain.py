#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-08-13 10:08:29
'''

from lib.parser import get_options
from lib.core import (
    EngineScan, ExhaustionScan, SaveDate,
    print_log, print_info, print_progress
    )
from lib.title import GetTitle
import time
import sys
import os

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
    big_dict = options.big_dict
    exhaustion = options.exhaustion
    exhaustion_only = options.exhaustion_only
    get_title = options.get_title
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
        all_exh_domain_ips_dict = dict()
        if exhaustion or exhaustion_only:
            # 穷举解析
            start = time.perf_counter()
            exhaustion_scan =  ExhaustionScan(
                scan_domain, thread_count=100,
                is_output=True, is_private=is_private,
                sub_dict = sub_dict, big_dict=big_dict
                )
            exh_domain_ips_dict = exhaustion_scan.run()
            if exh_domain_ips_dict:
                print_info(f"穷举发现 : {len(exh_domain_ips_dict)}")
                all_exh_domain_ips_dict.update(exh_domain_ips_dict)
                exh_end = (time.perf_counter() - start)
                print_info(f"穷举消耗时间:{exh_end}s")
                print_info(f"开始三级域名穷举")
                engine_exh_domain = set()
                # 先去重
                if engine_domain_ips_dict:
                    for domain in engine_domain_ips_dict.keys():
                        engine_exh_domain.add(domain)
                for domain in exh_domain_ips_dict.keys():
                    engine_exh_domain.add(domain)
                    
                # 三级域名穷举
                three_exh_domain_ips_dict = dict()
                # all size 用于输出进度条
                all_size = len(engine_exh_domain)
                start = time.perf_counter()
                for i, domain in enumerate(engine_exh_domain):
                    
                    next_exhaustion_scan =  ExhaustionScan(
                        domain, thread_count=100,
                        is_output=False, is_private=is_private,
                        next_sub=True
                        )
                    # run & update result echo progress
                    next_exh_domain_ips_dict = next_exhaustion_scan.run()
                    three_exh_domain_ips_dict.update(next_exh_domain_ips_dict)
                    all_exh_domain_ips_dict.update(next_exh_domain_ips_dict)
                    # 输出进度条
                    print_progress(all_size-i, all_size, start, len(three_exh_domain_ips_dict))
                print()
                print_info(f"三级域名穷举发现 : {len(three_exh_domain_ips_dict)}")
                # 如果穷举的三级域名有结果则进行四级域名穷举
                four_exh_domain_ips_dict = dict()
                all_size = len(three_exh_domain_ips_dict)
                start = time.perf_counter()
                if three_exh_domain_ips_dict:
                    print_info("开始四级域名穷举")
                    for i, domain in enumerate(three_exh_domain_ips_dict.keys()):
                        next_exhaustion_scan =  ExhaustionScan(
                            domain, thread_count=100,
                            is_output=False, is_private=is_private,
                            next_sub=True
                            )
                        next_exh_domain_ips_dict = next_exhaustion_scan.run()
                        four_exh_domain_ips_dict.update(next_exh_domain_ips_dict)
                        all_exh_domain_ips_dict.update(next_exh_domain_ips_dict)
                    # 输出进度条
                    print_progress(all_size-i, all_size, start, len(four_exh_domain_ips_dict))
                    print()
                    print_info(f"四级域名穷举发现: {len(four_exh_domain_ips_dict)}")
            print_info(f"所有穷举发现: {len(all_exh_domain_ips_dict)}")
        
        # 保存结果  
        save_data = SaveDate(
            scan_domain,
            engine_domain_ips_dict= engine_domain_ips_dict,
            exh_domain_ips_dict=all_exh_domain_ips_dict,
            is_text=True,
            is_json=is_json,
            is_html=is_html
            )
        # 增加title
        if not get_title:
            return
        domain_ips_dict = save_data.save_doamin_ips()
        urls = domain_ips_dict.keys()
        print_info("get title")
        title_result = GetTitle(urls).run()
        print_info(f"title get count: {len(title_result)}")
        title_path = os.path.join(save_data.out_out_dir, "title.txt")
        with open(title_path, "w") as f:
            for title in title_result:
                f.write(title)
        print_info(f"title save: {title_path}")
if __name__ == "__main__":
    main()
