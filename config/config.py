#!/usr/bin/python
# coding=UTF-8
'''
@Author: recar
@Date: 2019-05-30 16:08:13
@LastEditTime: 2019-06-26 15:20:44
'''

VERSION = "0.1"

BANNER = """

__   __     _____       _    ______                      _       
\ \ / /    /  ___|     | |   |  _  \                    (_)      
 \ V /_____\ `--. _   _| |__ | | | |___  _ __ ___   __ _ _ _ __  
  \ /______|`--. \ | | | '_ \| | | / _ \| '_ ` _ \ / _` | | '_ \ 
  | |      /\__/ / |_| | |_) | |/ / (_) | | | | | | (_| | | | | |
  \_/      \____/ \__,_|_.__/|___/ \___/|_| |_| |_|\__,_|_|_| |_|
      https://github.com/Ciyfly/Y-SubDomain  By Recar                                                          
"""


VIRUSTOTAL_APIKEY = ""
WEIBU_APIKEY = ""
# 是对重复的ip达到多少进行删除数据 jd的话差不多超过50个域名指向一个ip就可以删除了  
DNS_THRESHOLD = 50