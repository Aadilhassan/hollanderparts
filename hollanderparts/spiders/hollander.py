# hollander.py in hollanderparts/spiders

import scrapy

class HollanderSpider(scrapy.Spider):
    name = "hollander"
    allowed_domains = ["hollanderparts.com"]
    start_urls = ["https://www.hollanderparts.com/"]

    def parse(self, response):
        # Save the HTML content of the current page
        page = response.url.split("/")[-2]
        filename = f"hollander-{page}.html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        # Find all the links on the page and follow them
        links = response.css('a::attr(href)').getall()
        for link in links:
            # Ensure links are within the allowed domains and are complete URLs
            if link and "hollanderparts.com" in link:
                yield response.follow(link, self.parse)
            elif link and link.startswith('/'):
                # For relative links, add the domain
                yield response.follow(response.urljoin(link), self.parse)
