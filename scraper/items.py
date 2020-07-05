import scrapy


class AdItem(scrapy.Item):
    location = scrapy.Field()
    price = scrapy.Field()
    for_sale = scrapy.Field()
    image_urls = scrapy.Field()
    thumb_paths = scrapy.Field()
    cover_photo = scrapy.Field()
    tipologia = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    posted_at = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
