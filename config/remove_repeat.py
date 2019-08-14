#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-06-11 18:04:51
@LastEditTime: 2019-06-11 18:18:57
'''
import os
import sys

def main(add_subdomains_path):
    print("start ")
    subs = set()
    base_path  = os.path.dirname(os.path.abspath(__file__))
    big_subdomains_path = os.path.join(base_path, "big_subdomains.txt")
    tmp_file_path = os.path.join(base_path, "tmp.txt")

    with open(big_subdomains_path, "r") as f:
        line = f.readline()
        while line:
            subs.add(line)
            line = f.readline()
    old_dic_len = len(subs)
    with open(add_subdomains_path, "r") as f:
        line = f.readline()
        while line:
            subs.add(line)
            line = f.readline()
    print(f"add dict: {len(subs) - old_dic_len}")
    print("remove repeat after: {0} ".format(len(subs)))
    with open(tmp_file_path, "w") as f:
        for sub in subs:
            f.write(str(sub))
    os.remove(big_subdomains_path)
    print(big_subdomains_path)
    os.rename(tmp_file_path, big_subdomains_path)
    print("end ")

if __name__ == "__main__":
    add_subdomains_path = sys.argv[1]
    print(f"merge {add_subdomains_path}")
    main(add_subdomains_path)