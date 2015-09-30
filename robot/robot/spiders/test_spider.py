# coding=utf-8
__author__ = 'kk'
ISOTIMEFORMAT='%Y-%m-%d %X'


import os
import scrapy
from scrapy.selector import HtmlXPathSelector
import copy
import logging

from robot.items import RobotItem

import urllib2
import urllib
import cookielib

import zlib

import time



__base_dir__ = os.path.dirname(__file__)
__cookies_file__ = os.path.join(__base_dir__, 'cookies.dat')


class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    description = scrapy.Field()


class MySpider(scrapy.Spider):
    def __init__(self,domain=None):
        pass

    name = 'myspider'
    allowed_domains = ['saraba1st.com'] #可选。包含了spider允许爬取的域名列表
    # rules  #CrawlSpider
    # link_extractor 是一个 Link Extractor 对象。 其定义了如何从爬取到的页面提取链接。
    # start_urls = [
    #     'http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1'
    # ]
    base_url = 'http://bbs.saraba1st.com/2b/'

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_2 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8H7 Safari/6533.18.5",
        }

    def parse(self, response):
        self.log('开始解析:%s' %  response.url)
        sel = scrapy.selector.Selector(response)
        div_class = sel.xpath('//div[@class="bm_c"] | //div[@class="bm_c bt"]')
        print "xxxxxxxxx", div_class.extract()

        title_class = div_class.xpath('.//a[contains(@href,"forum.php")]')
        top_len = len(title_class.xpath('.//img[contains(@alt,"%s")]'% u'置顶').extract())
        # top_len = len(title_class.xpath('.//img').extract())
        # title_class = div_class.xpath('.//a/text()')
        print "top_len",top_len

        poster_class = div_class.xpath('.//a[contains(@href,"home.php")]/text()')
        addition_class = div_class.xpath('./span[@class="xg1"]/text()')

        # title_list = title_class.extract()

        poster_list = poster_class.extract()
        addition_list = addition_class.extract()

        print addition_list


        item_list = []
        for index, item in enumerate(title_class):
            if index< top_len+1:
                continue

            href = item.xpath('@href').extract()[0].strip().strip("\r\n")
            print href

            tid = href.replace('forum.php?mod=viewthread&tid=','').replace('&mobile=1','')
            # print tid

            title_list = item.xpath('.//text()').extract()

            title = title_list[0].strip().strip("\r\n")
            if len(title) < 1:
                title = title_list[1].strip().strip("\r\n")
            # print title

            poster = poster_list[index].strip().strip("\r\n")
            # print poster

            otherInfor = addition_list[index*2+1].replace(" ", '').replace("\r\n", '').split(u'回')
            if len(otherInfor) >= 2:
                reply = otherInfor[1]

            # post = {'tid':tid, 'poster':poster, 'title':title, 'post_time':otherInfor[0], 'reply':reply, 'date':Time2ISOString(time.time())}
            post =RobotItem({'tid':tid, 'poster':poster, 'title':title, 'post_time':otherInfor[0], 'reply':int(reply), 'date':Time2ISOString(time.time())})
            item_list.append(post)
            print post
            print "\r\n"
        # for index in xrange(top_len, len(poster_list)):
        #     print "xx",index,poster_list[index]



        self.callback("解析完成")

        if len(item_list):
            print 'item_list111'
            return item_list
        else:
            print 'item_list0'
            return None

        # sel = scrapy.Selector(response)
        # hxs = HtmlXPathSelector(response)
        #
        # # for h3 in response.xpath('//h3').extract():
        # #     yield TestItem(title=h3)
        #
        #
        # # path()：返回selectors列表, 每一个select表示一个xpath参数表达式选择的节点.
        # # extract()：返回一个unicode字符串，该字符串为XPath选择器返回的数据
        # # re()： 返回unicode字符串列表，字符串作为参数由正则表达式提取出来
        # items = []
        # imgs = response.xpath('//div[@id="xcnr_zx"]//img')
        # # for img in div.xpath('//img/@title').extract():
        # #     yield TestItem(img=img)
        # for img in imgs:
        #     item = TestItem()
        #     item['id'] = img.xpath('@alt').extract()
        #     item['img'] = img.xpath('@title').extract()
        #     item['name'] = img.xpath('@class').extract()
        #     items.append(item)
        # print items
        # return items

        # items.extend([self.make_requests_from_url(url).replace(callback=self.parse_post)
        #           for url in posts])



        # for url in response.xpath('//a/@href').extract():
        #     yield scrapy.Request(url, callback=self.parse)

    # def __init__(self, category=None, *args, **kwargs):
    #     super(MySpider, self).__init__(*args, **kwargs)
    #     self.start_urls = ['http://www.geimian.com/%s' % category]

    def start_requests(self):
        self.log('start before,but not run start_urls')

        cJar = cookielib.LWPCookieJar()
        file_object = False
        try:
            file_object = open(__cookies_file__)
            cJar._really_load(file_object, file_object, False, False)
        except :
            print 'cookies not exist '

        cookiess = dict()
        for item in cJar:
            cookiess[item.name] = item.value
        print cookiess

        if file_object:
            file_object.close()

        return [scrapy.Request('http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1', meta={'cookiejar': 1}, cookies=cookiess, headers=self.headers, callback=self.check_login,dont_filter = True)]

    def check_login(self, response):
        sel = scrapy.selector.Selector(response)
        div_class = sel.xpath('//div[@class="pd2"]')

        # print "xxxxxxxxx", div_class.xpath('//a[text()="%s"]/@href' % u'登录').extract()[0]
        if div_class.xpath('.//a/text()').extract()[0] == u'登录':
            print '未登录'
            # l6751902
            login_url = self.base_url + div_class.xpath('.//a[text()="%s"]/@href' % u'登录').extract()[0].encode('utf-8')
            print 'login_url', login_url
            return [scrapy.Request(login_url, meta = {'cookiejar' : response.meta['cookiejar']}, headers = self.headers, callback = self.logged_in,dont_filter = True)]
        else:
            print '登录成功 cookie'
            return self.parse(response)
            # return [scrapy.Request('http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1', meta = {'cookiejar' : response.meta['cookiejar']},callback = self.parse, headers = self.headers,dont_filter = True)]


    def logged_in(self, response):
        sel = scrapy.selector.Selector(response)
        print "xxxxxxxxx", sel.xpath('//input[@name="formhash"]').extract()
        formhash = sel.xpath('//input[@name="formhash"]/@value').extract()[0].encode('utf-8')
        self.log("formhash:%s" % formhash, logging.INFO)

        login_head = copy.deepcopy(self.headers)
        login_head['Origin'] = 'http://bbs.saraba1st.com'
        login_head['Referer'] = 'http://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&mobile=1'
        # http://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LnDKp&mobile=yes
        if self.getCookies(formhash, login_head):
            self.log("重新cookies成功！！~~", logging.INFO)
            return self.start_requests()
        else:
            self.callback("获取coockeis失败")
            self.log("重新获取cookies失败！！~~", logging.ERROR)
        # return [scrapy.FormRequest.from_response(response,
        #                     meta = {'cookiejar' : response.meta['cookiejar']},
        #                     headers = login_head,
        #                     formdata = {
        #                     'formhash': formhash,
        #                     'referer':'http://bbs.saraba1st.com/2b/member.php?mod=clearcookies&formhash=%s&mobile=1' % formhash,
        #                     'fastloginfield':'username',
        #                     'username': 'l6751902',
        #                     'password': 'xx',
        #                     'submit':'登录',
        #                     'questionid':'0',
        #                     'answer':'',
        #                     'cookietime':'2592000'
        #                     },
        #                     callback = self.after_login,
        #                     dont_filter = True
        #                     )]

    # def after_login(self, response):
    #     sel = scrapy.selector.Selector(response)
    #     div_class = sel.xpath('//div[@class="pd2"]')
    #     if div_class.xpath('//a/text()').extract()[0] == u'登录':
    #         self.callback("登录失败")
    #         self.log('登录失败', logging.WARNING)
    #     else:
    #         self.log('登录成功', logging.INFO)
    #         return [scrapy.Request('http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1', meta = {'cookiejar' : response.meta['cookiejar']}, headers = self.headers,dont_filter = True)]


     # def parse_start_url(self, response): #CrawlSpider
     #     # 当start_url的请求返回时，该方法被调用。 该方法分析最初的返回值并必须返回一个 Item对象或者 一个 Request 对象或者 一个可迭代的包含二者对象。
     #     pass

    # def  make_requests_from_url(self, url):
    #     # 该方法接受一个URL并返回用于爬取的 Request 对象。 该方法在初始化request时被start_requests() 调用，也被用于转化url为request。
    #     # 默认未被复写(overridden)的情况下，该方法返回的Request对象中， parse() 作为回调函数，dont_filter参数也被设置为开启。
    #     pass

    def getCookies(self, formhash, login_head):
        data = {'formhash': formhash,
                'referer': 'http://bbs.saraba1st.com/2b/member.php?mod=clearcookies&formhash=%s&mobile=1' % formhash,
                'fastloginfield': 'username',
                'username': 'l6751902',
                'password': 'xx',
                'submit': '登录',
                'questionid': '0',
                'answer': '',
                'cookietime': '2592000'}
        post_data = urllib.urlencode(data)   #将post消息化成可以让服务器编码的方式
        cJar = cookielib.LWPCookieJar()   #获取cookiejar实例
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cJar))
        website = 'http://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LnDKp&mobile=yes'
        req = urllib2.Request(website, post_data, login_head)
        response = opener.open(req)
        cJar.save(__cookies_file__)

        content = response.read()
        gzipped = response.headers.get('Content-Encoding')
        if gzipped:
            html = zlib.decompress(content, 16+zlib.MAX_WBITS)
        else:
            html = content

        # print html
        if 'l6751902' in html:
            return True
        return False

    def callback(self):
        pass


def ISOString2Time(s):
    '''
    convert a ISO format time to second
    from:2006-04-12 16:46:40 to:23123123
    把一个时间转化为秒
    '''
    return time.strptime(s, ISOTIMEFORMAT)


def Time2ISOString(s):
    '''
    convert second to a ISO format time
    from: 23123123 to: 2006-04-12 16:46:40
    把给定的秒转化为定义的格式
    '''
    return time.strftime(ISOTIMEFORMAT, time.localtime(float(s)))


def dateplustime(d, t):
    '''
    d=2006-04-12 16:46:40
    t=2小时
   return  2006-04-12 18:46:40
   计算一个日期相差多少秒的日期,time2sec是另外一个函数，可以处理，3天，13分钟，10小时等字符串，回头再来写这个，需要结合正则表达式。
    '''
    return Time2ISOString(time.mktime(ISOString2Time(d)) + time.time2sec(t))


def dateMinDate(d1, d2):
    '''
    minus to iso format date,return seconds
    计算2个时间相差多少秒
    '''
    d1 = ISOString2Time(d1)
    d2 = ISOString2Time(d2)
    return time.mktime(d1) - time.mktime(d2)

if __name__ == "__main__":
    pass
