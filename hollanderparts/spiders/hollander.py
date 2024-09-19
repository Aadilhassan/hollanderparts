# hollander.py in hollanderparts/spiders

import scrapy

class HollanderSpider(scrapy.Spider):
    name = "hollander"
    allowed_domains = ["hollanderparts.com"]
    start_urls = ["https://www.hollanderparts.com/"]

    def parse(self, response):
        # Example: Extracting categories or parts listings from the homepage
        categories = response.xpath("//div[@class='category-list']//a/@href").getall()
        for category in categories:
            category_url = response.urljoin(category)
            yield scrapy.Request(url=category_url, callback=self.parse_category)
    
    def parse_category(self, response):
        # Example: Extract details of individual parts in each category
        parts = response.xpath("//div[@class='part-list-item']")
        for part in parts:
            yield {
                'title': part.xpath(".//h2/a/text()").get(),
                'price': part.xpath(".//div[@class='price']/text()").get(),
                'details_url': response.urljoin(part.xpath(".//h2/a/@href").get())
            }
        
        # Handle pagination if exists
        next_page = response.xpath("//a[@class='next-page']/@href").get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse_category)
