# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.contrib.spiders import Rule
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from urllib.parse import urljoin
import re
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor

class Page(Item):
    Institute = Field()
    City = Field()
    Content = Field()
    URL = Field()
    
    


class SliitSpider(scrapy.Spider):
    name = 'sliit'
    allowed_domains = ['sliit.lk']
    start_urls = ['https://www.sliit.lk/computing/programms',
                  'https://www.sliit.lk/engineering/programms',
                  'https://www.sliit.lk/business/programms', 
                  'https://www.sliit.lk/science-education/undergraduate-degree-programs']
    
    seen = set()
    rules=(
        Rule(LinkExtractor(deny=('.+\.lk', ))),
    )
    
    def parse(self, response):
        if response.url in self.seen:
            self.log('already seen  %s' % response.url)
        else:
            self.log('parsing  %s' % response.url)
            self.seen.add(response.url)
            
        hxs = HtmlXPathSelector(response)
        item = Page()
        item['Content'] = hxs.select('//body').extract()
        item['City'] = {'Kandy', 'Colombo', 'Kuruegala'}
        item['Institute'] = {'SLIIT', 'Sri Lanka Institute of Information Technology'}
        item['URL'] = response.request.url
        yield(item)
        
        for url in hxs.select('//a/@href').extract():
            url = urljoin(response.url, url)
            if not url in self.seen and not re.search(r'.(pdf|zip|jar|jpg)$', url):
                self.log("yielding request " + url)
                yield Request(url, callback=self.parse)
        
