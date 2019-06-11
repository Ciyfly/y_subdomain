#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-06-11 18:04:51
@LastEditTime: 2019-06-11 18:18:57
'''

print("start ")
subs = set()
with open("./sub_all.txt", "r") as f:
    line = f.readline()
    while line:
        subs.add(line)
        line = f.readline()
print("remove repeat after: {0} ".format(len(subs)))
print("start write sub.txt")
with open("sub.txt", "w") as f:
    for sub in subs:
        f.write(str(sub))
print("end ")