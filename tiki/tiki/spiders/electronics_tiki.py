# -*- coding: utf-8 -*-
import scrapy


class ElectronicsTikiSpider(scrapy.Spider):
    name = 'electronics_tiki'
    allowed_domains = ['www.tiki.vn']
    # start_urls = ['https://https://tiki.vn/dien-thoai-may-tinh-bang/c1789?src=c.1789.hamburger_menu_fly_out_banner&utm_expid=.RasMS6yQTZOPoupXgn8U5A.0&utm_referrer=https%3A%2F%2Ftiki.vn%2F']

    def start_requests(self):
        yield scrapy.Request(url='https://tiki.vn/dien-thoai-may-tinh-bang/c1789?utm_expid=.RasMS6yQTZOPoupXgn8U5A.0&utm_referrer=https%3A%2F%2Ftiki.vn%2Fdien-thoai-may-tinh-bang%2Fc1789', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        })

    def parse(self, response):
        for product in response.xpath("//div[@class='product-box-list']/div"):
            yield {
                'title': product.xpath("normalize-space(.//p[@class='title']/text())").get(),
                'url': response.urljoin(product.xpath(".//div[@class='product-box-list']/div/a/@href").get()),
                'original_price': product.xpath(".//span[@class='price-regular']/text()").get(),
                'discount_price': product.xpath("normalize-space(.//span[@class='final-price']/text())").get(),
            }
        next_page_button = response.xpath("//a[@class='next']/@href").get()
        next_page_url = 'https://tiki.vn' + next_page_button
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
            })
