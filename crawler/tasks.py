from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from echo_scraper.spiders.echo import GoogleSearchSpider


@shared_task
def run_spider(
    term: str,
    config_id: int,
    results: int=10,
    safe: str='active',
    lang: str='en',
    region: str='us'
):
    process = CrawlerProcess(get_project_settings())
    process.crawl(GoogleSearchSpider,
                  term=term,
                  config_id=config_id,
                  results=results,
                  safe=safe,
                  start=0,
                  lang=lang,
                  region=region,
                  unique=False)
    process.start()