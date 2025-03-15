import scrapy


class EchoSpider(scrapy.Spider):
    name = "echo"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass
