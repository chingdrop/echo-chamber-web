import scrapy

from echo_scraper.google import GoogleSearch
from echo_scraper.items import GoogleResultItem


class GoogleSearchSpider(scrapy.Spider):
    name = "google_search"
    custom_settings = {
        "ITEM_PIPELINES": {
            "scrapy_project.pipelines.EchoScraperPipeline": 300,
        },
    }

    def __init__(
        self,
        term: str,
        config_id: int,
        results: int,
        safe: str,
        lang: str,
        region: str,
        *args,
        **kwargs
    ):
        super(GoogleSearchSpider, self).__init__(*args, **kwargs)
        self.term = term
        self.config_id = config_id
        self.results = results
        self.safe = safe
        self.lang = lang
        self.region = region

    def start_requests(self):
        if not self.term:
            self.logger.error(
                "No search query provided. Please provide a search query using -a search_query=your_query"
            )
            return

        goog = GoogleSearch()
        for result in goog.search(self.term, self.results, self.safe, unique=True):
            yield scrapy.Request(
                result.link,
                callback=self.parse,
                meta={"result": result, "config_id": self.config_id},
            )

    def parse(self, response):
        result = response.meta["result"]
        config_id = response.meta["config_id"]
        item = GoogleResultItem()
        item["config"] = config_id
        item["link"] = result["link"]
        item["title"] = result["title"]
        item["description"] = result["description"]
        yield item
