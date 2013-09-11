# /usr/local/bin/python3.3
# coding=utf-8
from pyquery import PyQuery as pq
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.compat import xmlrpc_client
import urllib
import types
import os
import mimetypes
import re
import lxml.html
import jieba
import jieba.analyse
class convertor(object):
    post = WordPressPost()
    def convertToWordPressPost(self, object):
        return post
class rssconvertor(convertor):
    
    def __init__(self, rssitem):
        self.images = []
        self.post = WordPressPost()
        self.post.title = rssitem.title
        self.__doc__ = ""
        
        # 过滤内容链接
        # rex=r'<a.+?href=.+?>|</a>'
        # r=re.compile(rex)
        # self.post.content=r.sub("",rssitem.description)
        self.post.content = rssitem.description
        self.__doc__ = pq(self.post.content)
        imgs = self.__doc__.find("img[src!='']")
        for i in imgs:
            e = pq(i)
            img = imageobj()
            img.oldurl = pq(e).attr("src")
            self.images.append(img)
    def setcategorytag(self, categorys):
        tmpdoc = pq(self.post.content)
        text = tmpdoc.text()
        tags = jieba.analyse.extract_tags(text, 3)
        self.post.terms_names = {'post_tag': tags, 'category': categorys}
        
    def setcommonopen(self):
        self.post.comment_status = 'open'
        
    def setpublishstatus(self):
        self.post.post_status = 'publish'
        
    def regexinfo(self, regexitems):
        print(self.post.content)
        for i in regexitems:
            r = re.compile(i, re.DOTALL)
            self.post.content = r.sub("", self.post.content)
        print(self.post.content)
    def saveimages(self, client, siteurl):
        

        # 保存图片
        for i in self.images:
            imgurl = urllib.urlopen(i.oldurl)
            if imgurl.getcode() == 200:
                imgdata = imgurl.read()
                if len(imgdata) > 0:
                    filename = os.path.basename(i.oldurl)
                    data = {
                        'name': filename,
                        'bits': xmlrpc_client.Binary(imgdata),
                        'type': mimetypes.read_mime_types(filename) or mimetypes.guess_type(filename)[0],
                    }
                    response = client.call(media.UploadFile(data))
                    i.newurl = response["url"]
                    i.id = response["id"]
        # 替换
        for i in self.images:
            strinfo = re.compile(i.oldurl)
            self.post.content = strinfo.sub(i.newurl, self.post.content)
            
        # 给图片加链接
        
        imgs = pq(self.post.content).find("img[src!='']")
        
        for i in imgs:
            e = pq(i)
            imgobj = ""
            item = filter(lambda x:x.newurl == e.attr("src"), self.images)
            
            if len(item) > 0:
                imgobj = item[0]
            
            if imgobj != "":
                oldimg = lxml.html.tostring(i)
                newimg = "<a href='%s%s' target='_blank'>%s</a>" % (siteurl, imgobj.getimageurl(), oldimg)
                strinfo = re.compile("""<img\s.*?\s?src\s*=\s*['|"]?(%s).*?>""" % imgobj.newurl)
                self.post.content = strinfo.sub(newimg, self.post.content)

        # 清空
        self.images = []
        

class imageobj():
    def __init__(self):
        self.oldurl = ''
        self.newurl = ''
        self.id = ''
        self.siteurl = ''
    def getimageurl(self):
        return "?attachment_id=%s" % self.id
