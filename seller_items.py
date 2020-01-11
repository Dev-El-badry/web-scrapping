# -*- coding: utf-8 -*-
import scrapy


class SellerItemsSpider(scrapy.Spider):
    name = 'seller_items'
    allowed_domains = ['www.egypt.souq.com/eg-ar/seller70/s/?as=1']
    start_urls = ['http://www.egypt.souq.com/eg-ar/seller70/s/?as=1/']

    def parse(self, response):
        pass
