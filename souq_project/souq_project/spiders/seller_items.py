# -*- coding: utf-8 -*-
import scrapy
import re

class SellerItemsSpider(scrapy.Spider):
    name = 'seller_items'
    allowed_domains = ['souq.com/eg-ar']
    count=0
    # start_urls = ['http://souq.com/eg-ar/']

    def start_requests(self) :
        yield scrapy.Request(url="https://egypt.souq.com/eg-ar/{0}/s/?as=1&section=2&page=1".format(self.seller_name), callback=self.parse_links)

    def parse_links(self, response):
        links = response.xpath("//section[@class='filter-group']/ul/li[2]/div/div/ul/li/label/input/@value").getall()
        for link in links :
            new_link = link + '?section=2&page=1'
            print('===============> ONE')
            yield scrapy.Request(new_link, callback=self.parse_items, errback=self.errback_httpbin,  dont_filter=True)

    def parse_items(self, response) :
        # NOTE: Continued OR PAUSE
        print('===============> TOW')
        for item in response.xpath("//div[@class='column column-block block-grid-large single-item']") :
            target_url = item.xpath(".//div/div/div/a/@href").get()
            item_id = item.xpath(".//@data-ean").get()
            item_price = item.xpath(".//div/div[@class='columns small-7 medium-12']/ul/li[2]/div/div/h5[@class='price']/span/span/text()").get()
            print('===============> Three')
            print(self.count)
            yield scrapy.Request(target_url, callback=self.single_item, errback=self.errback_httpbin, dont_filter=True, meta ={'item_id': item_id, 'item_price': item_price})

        next_page = response.xpath("//li[@class='pagination-next goToPage']/a/@href").get()
        if next_page :
            url_next_page = next_page.replace('?', '?section=2&')
            yield scrapy.Request(url_next_page, callback=self.parse_items)


    def single_item(self, response):
        print('===============> FOUR')
        item_id = response.request.meta['item_id']
        item_price = response.request.meta['item_price']

        seller_show = response.xpath(
            "//dl[@class='stats clearfix']/dd[1]/span/a/b/text()").get()
        result = self.chk_if_show_in_offer(seller_show)
        print('================')
        print('result single item')
        print('================')
        if result == False:

            link_other_sellers_container = response.xpath("//div[@class='other-sellers-container']/div/div[@class='show-for-medium']/a/@href").get()

            print('===============> LINK', link_other_sellers_container)
            data = {
                'item_title': response.xpath("//div[@class='small-12 columns product-title']/h1/text()").get(),
                'item_price': item_price,
                'seller_name': seller_show,
                'item_ID': item_id,
                'ur_name': self.seller_name
            }
            if link_other_sellers_container :
                print('===============> FIVE')
                yield scrapy.Request(link_other_sellers_container, callback=self.parse_other_sellers, errback=self.errback_httpbin,  dont_filter=True, meta=data)


        else:
            pass

    def parse_other_sellers(self, response):
        print('===============> SIX')
        ur_offer = ''
        ur_name = ''
        for row in response.xpath("//div[@id='condition-all']/div"):
            print('===============> SEVEN')
            other_sellers = row.xpath(".//div[4]/div[@class='field seller-name']/span/a/text()").get()
            result = self.chk_if_show_in_offer(other_sellers)
            if result == False:
                print('===============> Eight')
                ur_name = other_sellers
                ur_offer = row.xpath(".//div[2]/div[@class='field price-field']/text()").get()
                break
        print('===============> Nigne')
        yield {
            'item_title': response.request.meta['item_title'],
            'item_price': response.request.meta['item_price'],
            'seller_name': response.request.meta['seller_name'],
            'item_ID': response.request.meta['item_ID'],
            'ur_name': ur_name,
            'ur_price': ur_offer
        }

    
    
    def chk_if_show_in_offer(self, seller_show) :
        print('seller show ============ > ', seller_show)
        print('seller name ============ > ', self.seller_name)
        if seller_show != self.seller_name :
            return False
        else :
            return True
    
    def get_numbers_from_text(self, string):
        str = string
        x = re.findall(r'\d+', string)
        nums = ''.join(x)
        return nums

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
