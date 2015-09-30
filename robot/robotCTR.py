# coding=utf-8
__author__ = 'kk'

import os
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'robot.settings') #Must be at the top before other imports



from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from robot.spiders.test_spider import MySpider
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher


def callback_spider(statue):
    print statue

def setup_crawler(domain):
    spider = MySpider(domain=domain)
    spider.callback = callback_spider
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

def stop_reactor():
    reactor.stop()

# Usage
if __name__ == "__main__":
    for domain in ['saraba1st.com']:
        setup_crawler(domain)
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    log.start()

    reactor.run()

# from scrapy.cmdline import execute
#
# if __name__ == "__main__":
#     #execute("crawl myspider".split())
#     execute("scrapy crawl myspider".split())
#     pass