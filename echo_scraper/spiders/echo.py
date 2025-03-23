import scrapy
from fake_useragent import UserAgent

from crawler.api_utils import GoogleSearch
from crawler.models import GoogleSearchConfig
from echo_scraper.items import GoogleResultItem


class GoogleSearchSpider(scrapy.Spider):
    name = 'google_search'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_project.pipelines.DjangoPipeline': 300,
        },
    }
    
    def __init__(
            self,
            term: str,
            results: int=10,
            safe: str='active',
            lang: str='en',
            region: str='us',
            *args,
            **kwargs
    ):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.term = term
        self.results = results
        self.safe = safe
        self.lang = lang
        self.region = region

    def start_requests(self):
        if not self.term:
            self.logger.error("No search query provided. Please provide a search query using -a search_query=your_query")
            return
        
        config = GoogleSearchConfig.objects.create(
            term=self.term,
            results=self.results,
            safe=self.safe,
            lang=self.lang,
            region=self.region
        )
        
        goog = GoogleSearch()
        for result in goog.search(self.term, self.results, self.safe, unique=True):
            yield scrapy.Request(result.link, callback=self.parse, meta={'result': result, 'config_id': config.id})

    def parse(self, response):
        result = response.meta['result']
        config_id = response.meta['search_config_id']
        item = GoogleResultItem()
        item['config'] = config_id
        item['link'] = result['link']
        item['title'] = result['title']
        item['description'] = result['description']
        yield item
