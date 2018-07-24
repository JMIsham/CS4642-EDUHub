# -*- coding: utf-8 -*-
from scrapy.spiders import Rule, CrawlSpider
from scrapy.item import Item, Field
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import re

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
        Rule(LinkExtractor(allow =('^.*computing/.*',
                                   '^.*engineering/.*',
                                   '^.*business/.*',
                                   '^.*science-education/.*',
                                   '^.*graduate-studies-research/.*')), 
    follow=True, callback="parse1")
      
    ]
    def parse1(self, response):
        print("***************************** VISITED *********************************************")
        aTags = re.compile(r'<a.*?/a>')
        responseBody = aTags.sub('',response.text)
        soup = BeautifulSoup(responseBody, 'html.parser')
        soup.a.com
        list_of_section = soup.find_all("section")
        p = re.compile('\n(\n| )*')
        sections = ""
        for section in list_of_section:
            current = p.sub('\n',aTags.sub('',str(section.get_text())))
            if (("\t" not in current) & ("\r" not in current)): 
                sections += current 
        item = Page()
        item['Content'] = sections
        item['City'] = {'Kandy', 'Colombo', 'Kuruegala'}
        item['Institute'] = {'SLIIT', 'Sri Lanka Institute of Information Technology'}
        item['URL'] = response.request.url
        yield(item)
        

class SaitmSpider(CrawlSpider):
    name = 'saitm'
    allowed_domains = ['saitm.edu.lk']
    start_urls = ['http://www.saitm.edu.lk/e/UoS.htm',
                  'http://www.saitm.edu.lk/fac_of_medicine/fac_of_medicine.htm',
                  'http://www.saitm.edu.lk/fac_of_media/fac_of_media.htm',
                  'http://www.saitm.edu.lk/fac_of_mgt/fac_of_mgt.htm',
                  'http://www.saitm.edu.lk/fac_of_AHBS/fac_of_AHBS.htm'
                 
                  ]
    
    rules = [
            Rule(LinkExtractor(allow = (
                    '^.*fac_of.*','^.*/e/'
                    )), 
    follow = True , callback = 'parseSaitm')
            ]
    
    
    def parseSaitm(self, response):
        print("***************************** VISITED *********************************************")
        aTags = re.compile(r'<a.*?/a>')
        script = re.compile('<script*?</script>')
        style = re.compile('<style*?</style>')
        code = re.compile('\t.*\n')
        comment = re.compile('<!--(\n|.)*-->')
        responseBody = aTags.sub('',response.text)
        responseBody =code.sub('',responseBody)
        responseBody =comment.sub('',responseBody)
        soup = BeautifulSoup(responseBody, 'html.parser')
        p = re.compile('\n(\n| )*')
        current = p.sub('\n',aTags.sub('',str(soup.get_text())))
        item = Page()
        item['Content'] = current
        item['City'] = {'Kandy', 'Colombo', 'Kuruegala'}
        item['Institute'] = {'SAITM', 'South Asian Institute of Technology and Medicine '}
        item['URL'] = response.request.url
        yield(item)
    
    
