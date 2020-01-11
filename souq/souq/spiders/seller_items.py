# -*- coding: utf-8 -*-
import scrapy


class SellerItemsSpider(scrapy.Spider):
    name = 'seller_items'
    allowed_domains = ['egypt.souq.com/eg-ar']

    def start_requests(self):
        yield scrapy.Request(url='https://egypt.souq.com/eg-ar/seller70/s/?as=1&section=2&page=1', callback=self.parse, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        })

    def parse(self, response):
        for prod in response.xpath("//div[@class='column column-block block-grid-large single-item']") :
            prod_title=prod.xpath(".//div/div[2]/a/ul/li[1]/h6[@class='title itemTitle']/text()").get()
            prod_price=prod.xpath(".//div/div[2]/a/ul/li[2]/div/div[1]/h5[@class='price']/span[@class='is block sk-clr1']/span/text()").get()
            single_prod_url=prod.xpath('.//div/div[2]/a/@href').get()
            special_num=prod.xpath('.//@data-ean').get()

            yield {
                'item ID' : special_num,
                'item Title': prod_title,
                'item price': prod_price,
                'href-url': single_prod_url,
                'user-agent': response.request.headers['user-agent']
            }
        
        next_page = response.xpath("//div[@class='showMore']/ul/li[@class='pagination-next goToPage']/a/@href").get()
        if next_page :
            new_url = self.replacewith(next_page, 'page', 'section=2&page')
            print('=======================')
            print('working')
            print('=======================')

            yield scrapy.Request(url=new_url, callback=self.parse, dont_filter=True)
            
    def replacewith(self, input, pattern, replaceWith):
	    return input.replace(pattern, replaceWith)
