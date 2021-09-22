
import scrapy

from scrapy.spiders import CrawlSpider, Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.item import Item, Field

class MyItems(Item):
    referer =Field() # where the link is extracted
    response= Field() # url that was requested
    status = Field() # status code received

class NotFoundSpider(CrawlSpider):
    name = "test-crawler"
    target_domains = ["dev.to"] # list of domains that will be allowed to be crawled  eg https://dev.to/
    handle_httpstatus_list = [404,410,301,500] # only 200 by default. you can add more status to list

    # Throttle crawl speed to prevent hitting site too hard
    custom_settings = {
        'CONCURRENT_REQUESTS': 2, # only 2 requests at the same time
        'DOWNLOAD_DELAY': 0.5 # delay between requests
    }
    myBaseUrl = ''
    start_urls = []

    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.myBaseUrl = category
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    rules = [
        Rule(
            LinkExtractor( allow_domains=target_domains, deny=('patterToBeExcluded'), unique=('Yes')), 
            callback='parse_my_url', # method that will be called for each request
            follow=True),
        # crawl external links but don't follow them
        Rule(
            LinkExtractor( allow=(''),deny=("patterToBeExcluded"),unique=('Yes')),
            callback='parse_my_url',
            follow=False
        )
    ]

    def parse_my_url(self, response):
      # list of response codes that we want to include on the report, we know that 404
      report_if = [404] 
      if response.status in report_if: # if the response matches then creates a MyItem
          item = MyItems()
          item['referer'] = response.request.headers.get('Referer', None)
          item['status'] = response.status
          item['response']= response.url
          yield item
      yield None # if the response did not match return empty

