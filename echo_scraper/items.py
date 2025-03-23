# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

from crawler.models import GoogleSearchResult


class GoogleResultItem(Item):
    link = Field()
    title = Field()
    description = Field()

    def save(self):
        config = GoogleSearchResult.objects.get(id=self['config'])
        result = GoogleSearchResult(
            config=config,
            link=self['link'],
            title=self['title'],
            description=self['description']
        )
        result.save()
        return result
