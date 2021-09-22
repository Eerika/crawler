
import scrapy

class OdaSpider(scrapy.Spider):
    name="odaspider"
    allowed_domains = ["oda.com"]
    myBaseUrl = ''
    start_urls = []

    def __init__(self, category='', **kwargs): # The category variable will have the input URL.
        self.myBaseUrl = category
        self.start_urls.append(self.myBaseUrl)
        super().__init__(**kwargs)

    def parse(self, response):
        products = response.css('div.product-list-item')
        for product in products:
            yield {
                'price': product.css('.unit-price::text').get(),
                'name': product.css('.name-main::text').get(),
                'origin': product.css('.name-extra::text').get(),
            }


