# /usr/local/bin/python3.3
# coding=utf-8
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
import convertor
from feedparser import parse
from datetime import *
import logging
class apObject():
        type = ''
        def run(self):
                # 验证地址是否可用
                # 读取内容
                # 转换对象
                # 验证对象是否存在
                # 保存

                return

        def validate(self):
                return True
        
class apRss(apObject):
        name = ''
        rss = ''
        xmlrpc = ''
        user = ''
        passwd = ''
        siteurl = ''
        contentlength = 0
        mustimage = False
        __wordpressitems = []
        def __init__(self):
                self.logger = logging.getLogger("ap.apRss")
                self.offset = 1
        def run(self):
                self.logger.info("[%s] running" % self.name)
                
                # 验证地址是否可用
                try:
                        wp = Client(self.xmlrpc, self.user, self.passwd)
                        para = {'number': (self.offset + 1) * 50}
                        self.__wordpressitems = wp.call(posts.GetPosts(para))
                except Exception, x:
                        self.logger.info("[%s] xmlrpc connection or getinfor error" % self.name)
                        self.logger.error(str(x))
                        
                # 读取内容
                rss = parse(self.rss)
                count = 0
                rsscount = len(rss.entries)
                self.logger.info("[%s] read %s rssrecord" % (self.name, rsscount))
                for i in range(0, rsscount):
                        # 转换对象
                        rssitem = rss.entries[i]
                        convert = convertor.rssconvertor(rssitem)
                        convert.client = wp
                        if self.mustimage and len(convert.images) == 0:
                                continue
                        # 验证对象
                        if self.__validateRssItem(convert.post):
                                convert.regexinfo(self.regexitems)
                                convert.setcategorytag(self.categorys)
                                if self.publishstatus:
                                        convert.setpublishstatus()
                                if self.commonstatus:
                                    convert.setcommonopen()
                                convert.saveimages(wp, self.siteurl)
                                # 保存
                                
                                wp.call(NewPost(convert.post))
                                count += 1
                                
                self.logger.info("[%s] Post article %s" % (self.name, count))
        
        def __validateRssItem(self, wordpressobj):
                value = True
                
                if wordpressobj.title.strip() == '' or wordpressobj.content.strip() == '' or len(wordpressobj.content) < int(self.contentlength):
                        value = False
                for item in self.__wordpressitems:
                        if item.title.strip() == wordpressobj.title.strip():
                                value = False
                                break
                        
                return value
        def validate(self):
                value = True
                if self.rss.strip() == '' or self.xmlrpc.strip() == '' or self.user.strip() == '' or self.passwd.strip() == '':
                        value = False
                return value

class apTaobao(apObject):
        add = ''
        def run(self):
                apObject.run(self)
                
