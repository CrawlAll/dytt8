# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dytt8.items import Dytt8Item


class MoviesSpider(CrawlSpider):
    name = 'movies'
    allowed_domains = ['dytt8.net']
    start_urls = ['http://dytt8.net/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/index\.html', deny=r'.*game.*')),  # 每个导航分类首页
        Rule(LinkExtractor(restrict_xpaths=u'//a[text()="下一页"]')),  # 导航分类下一页
        Rule(LinkExtractor(allow=r'.*/\d+/\d+\.html', deny=r".*game.*"), callback='parse_item', follow=True)
        # 提取文章页链接，交由解析函数处理
    )

    def parse_item(self, response):
        item = Dytt8Item()
        item['title'] = response.xpath('//div[@class="title_all"]/h1/font/text()').get('')
        item['publish_time'] = response.xpath(
            '//div[@class="co_content8"]/ul/text()').get('').strip().replace('发布时间：', '')
        imgs_xpath = response.xpath('//div[@id="Zoom"]//img')
        item['images'] = [i.xpath('./@src').get('') for i in imgs_xpath if i.xpath('./@src')]
        item['download_links'] = re.findall('<a href="(ftp://.*?)">', response.text)
        item['contents'] = [i.strip().replace('\n', '').replace('\r', '') for i in
                            response.xpath('string(//div[@id="Zoom"])').getall()]
        yield item
