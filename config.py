# /usr/local/bin/python3.3
# coding=utf-8
import sys
import os
import ConfigParser

import ap
from datetime import *
import log
import logging

class apSystem():
        __items = []
        def __init__(self):
                # 设置logging
                log.logconfig()
                self.logger = logging.getLogger("ap.system")
                self.logger.info("prcess config.ini file")
                cfg = ConfigParser.ConfigParser()
                # 加载配置
                if os.path.isfile('config.ini'):
                        cfg.read("config.ini")
                        v = cfg.sections()
                        offsetcount = len(v)
                        for f in v:
                                if f.startswith('rssconfig'):
                                        rss = ap.apRss()
                                        rss.offset = offsetcount
                                        rss.name = f
                                        rss.mustimage = bool(cfg.get(f, 'mustimage'))
                                        rss.siteurl = cfg.get(f, 'siteurl')
                                        rss.contentlength = cfg.get(f, 'contentlength')
                                        rss.rss = cfg.get(f, 'rss')
                                        rss.xmlrpc = cfg.get(f, 'xmlrpc')
                                        rss.user = cfg.get(f, 'user')
                                        rss.passwd = cfg.get(f, 'passwd')
                                        rss.publishstatus = bool(cfg.get(f, 'publishstatus'))
                                        rss.commonstatus = bool(cfg.get(f, 'commonstatus'))
                                        rss.regexitems = []
                                        rss.categorys = []
                                        for key, value in cfg.items(f):
                                                if key.startswith('regexitem'):
                                                    rss.regexitems.append(value)
                                                if key.startswith("category"):
                                                    va = value.decode('gbk', 'ignore').encode('utf8', 'ignore')
                                                    rss.categorys.append(va)
                                        self.__items.append(rss)
                else:
                        self.logger.info("config.ini not exist")
                        
        def __validateconfig(self):
                self.logger.info("validate config")
                value = True
                for i in self.__items:
                         if not i.validate():
                                 value = False
                                 break
                return value
        
        def run(self):
                self.logger.info("system run")
                
                # 验证配置是否正常
                if not self.__validateconfig():
                        self.logger.info("system config error")
                        return
                # FOR 任务[]
                for item in self.__items:
                        if item.validate():
                                item.run()

                self.logger.info("system end")
                

                


