# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

from crawler.models import CrawlResult


class GoogleResultItem(Item):
    link = Field()
    title = Field()
    description = Field()

    def save(self):
        google_result = GoogleResult(
            link=self['link'],
            title=self['title'],
            description=self['description']
        )
        google_result.save()
        return google_result
