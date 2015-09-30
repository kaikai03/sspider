# -*- coding: utf-8 -*-

# Scrapy settings for robot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'robot'

SPIDER_MODULES = ['robot.spiders']
NEWSPIDER_MODULE = 'robot.spiders'

# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True
COOKIES_DEBUG = False

DUPEFILTER_DEBUG = True

#运行顺序 0-1000
ITEM_PIPELINES = {
    'robot.pipelines.S1Pipeline': 300
}

# 图片管道
# http://scrapy-chs.readthedocs.org/zh_CN/latest/topics/images.html

AUTOTHROTTLE_ENABLED = True
# 默认: False
# 启用AutoThrottle扩展。

AUTOTHROTTLE_START_DELAY = 5
# 默认: 5.0
# 初始下载延迟(单位:秒)。

AUTOTHROTTLE_MAX_DELAY = 80
# 默认: 60.0
# 在高延迟情况下最大的下载延迟(单位秒)。

# AUTOTHROTTLE_DEBUG
# 默认: False
# 起用AutoThrottle调试(debug)模式，展示每个接收到的response。 您可以通过此来查看限速参数是如何实时被调整的。


DOWNLOAD_DELAY = 5
# 默认: 0  # 250 ms of delay
# 该设定影响(默认启用的) RANDOMIZE_DOWNLOAD_DELAY 设定。 默认情况下，
# Scrapy在两个请求间不等待一个固定的值， 而是使用0.5到1.5之间的一个随机值 * DOWNLOAD_DELAY 的结果作为等待间隔。


CONCURRENT_REQUESTS_PER_DOMAIN = 2
# 默认: 8
# 对单个网站进行并发请求的最大值。
#
# CONCURRENT_REQUESTS_PER_IP
# 默认: 0
# 对单个IP进行并发请求的最大值。如果非0，则忽略 CONCURRENT_REQUESTS_PER_DOMAIN 设定， 使用该设定。 也就是说，并发限制将针对IP，而不是网站。
# 该设定也影响 DOWNLOAD_DELAY: 如果 CONCURRENT_REQUESTS_PER_IP 非0，下载延迟应用在IP而不是网站上。


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'robot (+http://www.yourdomain.com)'
