import scrapy


class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'
    allowed_domains = ['google.com']
    
    def __init__(self, search_query='', *args, **kwargs):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.search_query = search_query

    def start_requests(self):
        if not self.search_query:
            self.logger.error("No search query provided. Please provide a search query using -a search_query=your_query")
            return
        
        url = f'https://www.google.com/search?q={self.search_query}'
        yield scrapy.Request(url, callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def parse(self, response):
        for result in response.xpath('//div[@class="tF2Cxc"]'):
            title = result.xpath('.//h3/text()').get()
            link = result.xpath('.//a/@href').get()
            description = result.xpath('.//div[@class="IsZvec"]/text()').get()

            yield {
                'title': title,
                'link': link,
                'description': description
            }
        
        next_page = response.xpath('//a[@id="pnnext"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)
