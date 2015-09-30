# coding=utf-8
__author__ = 'kk'

__cookies_file__ = './cookies.dat'

import scrapy
from scrapy.selector import HtmlXPathSelector
import copy
import logging

import urllib2
import urllib
import cookielib

import zlib


class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    description = scrapy.Field()


class MySpider(scrapy.Spider):
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
        print response.meta

        sel = scrapy.selector.Selector(response)
        div_class = sel.xpath('//div[@class="bm_c"]')
        print "xxxxxxxxx", div_class.extract()

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
            print 'wenjian bucunzai '

        cookiess = dict()
        for item in cJar:
            cookiess[item.name] = item.value
        print cookiess

        if file_object:
            file_object.close()
        return [scrapy.Request('http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1', meta={'cookiejar': 1}, cookies=cookiess, headers=self.headers, callback=self.check_login)]

    def check_login(self, response):
        sel = scrapy.selector.Selector(response)
        div_class = sel.xpath('//div[@class="pd2"]')

        # print "xxxxxxxxx", div_class.xpath('//a[text()="%s"]/@href' % u'登录').extract()[0]
        if div_class.xpath('//a/text()').extract()[0] == u'登录':
            print '未登录'
            # l6751902
            login_url = self.base_url + div_class.xpath('//a[text()="%s"]/@href' % u'登录').extract()[0].encode('utf-8')
            print 'login_url', login_url
            return [scrapy.Request(login_url, meta = {'cookiejar' : response.meta['cookiejar']}, headers = self.headers, callback = self.logged_in)]
        else:
            print '登录成功 cookie'
            self.parse(response)
            # return [scrapy.Request('http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1', meta = {'cookiejar' : 1}, headers = self.headers,dont_filter = True)]


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
            self.start_requests()
        else:
            self.log("重新获取cookies失败！！~~", logging.ERROR)
        # return [scrapy.FormRequest.from_response(response,
        #                     meta = {'cookiejar' : response.meta['cookiejar']},
        #                     headers = login_head,
        #                     formdata = {
        #                     'formhash': formhash,
        #                     'referer':'http://bbs.saraba1st.com/2b/member.php?mod=clearcookies&formhash=%s&mobile=1' % formhash,
        #                     'fastloginfield':'username',
        #                     'username': 'l6751902',
        #                     'password': 'l35331963',
        #                     'submit':'登录',
        #                     'questionid':'0',
        #                     'answer':'',
        #                     'cookietime':'2592000'
        #                     },
        #                     callback = self.after_login,
        #                     dont_filter = True
        #                     )]

    def after_login(self, response):
        sel = scrapy.selector.Selector(response)
        div_class = sel.xpath('//div[@class="pd2"]')
        if div_class.xpath('//a/text()').extract()[0] == u'登录':
            self.log('登录失败', logging.WARNING)
        else:
            self.log('登录成功', logging.INFO)
            return [scrapy.Request('http://bbs.saraba1st.com/2b/forum-75-1.html?mobile=1', meta = {'cookiejar' : response.meta['cookiejar']}, headers = self.headers,dont_filter = True)]


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
                'password': 'l35331963',
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



if __name__ == "__main__":
    pass
