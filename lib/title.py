#!/usr/bin/python
# coding=UTF-8
'''
Author: Recar
Date: 2020-09-02 10:31:45
LastEditTime: 2021-03-25 18:25:54
'''
from optparse import OptionParser
import traceback
import threading
import urllib3
import logging
import signal
try:
    import queue
except:
    import Queue as queue
import time
import sys
import re
import os


logging.getLogger("urllib3").setLevel(logging.ERROR)                    
urllib3.disable_warnings()
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'}

result = []

def ctrl_c(signum, frame):
    print()
    print("ctrl c")
    sys.exit()
# ctrl+c
signal.signal(signal.SIGINT, ctrl_c)

class BaseWork(object):
    def __init__(self, consumer_count=50):
        self.consumer_count = consumer_count
        self.work_queue = queue.Queue()

    def put(self, item):
        '''
        @params item 数据
        '''        
        try:
            if type(item) == list:
                for d in item:
                    self.work_queue.put(d)
            else:
                self.work_queue.put(item)
        except Exception as e:
            pass

    def producer(self, func):
        pass

    def consumer(self, func):
        '''
        消费者
        @params func 消费者函数
        '''
        while not self.work_queue.empty():
            item = self.work_queue.get(timeout=3)
            if item is None:
                break
            func(item)

    def run(self, consumer_func):
        '''
        运行方法
        @params consumer_func 消费者函数
        '''
        start_time = time.time()
        threads = []
        for i in range(self.consumer_count):
            t = threading.Thread(target=self.consumer,args=(consumer_func,))
            t.setDaemon(True)
            t.start()
            threads.append(t)
        while not self.work_queue.empty():
            # logging.debug("queue size: {0}".format(self.work_queue.qsize()))
            time.sleep(1)
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)
        use_time = time.time() - start_time

class Worker(BaseWork):
    '''普通消费队列'''
    def __init__(self, consumer_count=50):
        super(Worker, self).__init__(consumer_count)

class WorkerPrior(BaseWork):
    '''优先消费队列'''
    def __init__(self, consumer_count=50):
        super(WorkerPrior, self).__init__(consumer_count)
        from queue import PriorityQueue
        self.work_queue = PriorityQueue()

    def put(self, item, priority=1):
        '''
        @params item 数据
        @params priority 优先级 默认是1
        '''
        try:
            if type(item) == list:
                for d in item:
                    self.work_queue.put((priority, d))
            else:
                self.work_queue.put((priority, item))
        except Exception as e:
            pass
       
    def consumer(self, func):
        '''
        消费者
        @params func 消费者函数
        '''
        while not self.work_queue.empty():
            item = self.work_queue.get(timeout=3)
            priority, data = item
            if data is None:
                break
            func(data)


class GetTitle(object):
    def __init__(self, urls, logger=logging):
        self.urls = urls
        self.logger = logger
        self.result = list()

    def get_title(self, url):
        try:
            http = urllib3.PoolManager()
            response = http.request('GET',url,headers=header,timeout=1)
            re_title =  re.findall("<title>(.+)</title>", response.data.decode())
            title = re_title[0] if re_title else ""
            info = {
                "status_code": response.status,
                "title": title,
            }
            return info
        except Exception as e:
            return None
            
    def create_worker(self):
        worker = Worker(consumer_count=100)
        for url in self.urls:
            worker.put({
                "url": url
            })
        return worker

    def consumer(self, data):
        url = data["url"]
        info = self.get_title(url)
        if not info:
            return
        output = "{:30}\t{:5}\t{:30}\n".format(url, info["status_code"], info["title"])
        self.logger.info("[+] {0}".format(output))
        self.result.append(output)

    def run(self):
        worker = self.create_worker()
        self.logger.info("[*] task create success {0}".format(worker.work_queue.qsize()))
        output = "{:30}\t{:5}\t{:30}".format("url","status", "title")
        self.logger.info("[*] {0}".format(output))
        worker.run(self.consumer)
        self.logger.info("[+] find title: {0}".format(len(self.result)))
        return self.result

