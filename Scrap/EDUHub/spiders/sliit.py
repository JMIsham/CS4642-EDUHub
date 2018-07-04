# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.selector import Selector
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from urllib.parse import urljoin
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
class Page(Item):
    Institute = Field()
    City = Field()
    Content = Field()
    URL = Field()
    
    


class SliitSpider(CrawlSpider):
    name = 'sliit'
    allowed_domains = ['sliit.lk']
    start_urls = ['https://www.sliit.lk',]
    
    rules = [
        Rule(LinkExtractor(deny =('/staff/'))),
        Rule(LinkExtractor(allow =('computing/|engineering/|business/|science-education/|graduate-studies-research/')), follow=True, callback="parse1")
      
    ]

    
    def parse1(self, response):
        print(response.request.url)    
        hxs = HtmlXPathSelector(response)
        item = Page()
        item['Content'] = hxs.select('//section').extract()
        item['City'] = {'Kandy', 'Colombo', 'Kuruegala'}
        item['Institute'] = {'SLIIT', 'Sri Lanka Institute of Information Technology'}
        item['URL'] = response.request.url
        yield(item)
        
