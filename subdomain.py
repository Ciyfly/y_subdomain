#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-15 18:40:51
@LastEditTime: 2019-06-11 18:42:58
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
    engine = options.engine
    print_info("scan {0}\n".format(scan_domain))
    target_output_txt, target_output_html = get_output(scan_domain)
    # for i in range(10000):
    #     print_log("scan scripts: "+str(i))
    # print()
    start = time.perf_counter()
    # engine_result = run_scripts(scan_domain, engine)
    # engine_end = (time.perf_counter() - start)
    # print_info(f"引擎接口消耗时间:{engine_end}s")
    # domain_ips = thread_dns(engine_result)
    # print("\n"+str(domain_ips))
    # print(len(domain_ips))
    # end = (time.perf_counter() - start)
    # print_info(f"程序消耗时间: {end}s")
    exh = Exhaustion(scan_domain)
    exh.run()
    end = (time.perf_counter() - start)
    print_info(f"程序消耗时间: {end}s")
        

if __name__ == "__main__":
    main()
