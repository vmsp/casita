import io
import os

from PIL import Image
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from app import models


class DiscardPipeline:
    def process_item(self, item, spider):
        if not item.get('Price'):
            raise DropItem('No price')
        return item


class ResizeImagesPipeline(ImagesPipeline):
    """Override of ImagesPipeline that discards the full image and only keeps
    the thumbnails.
    """
    def get_images(self, response, request, info):
        orig_image = Image.open(io.BytesIO(response.body))
        for thumb_id, size in self.thumbs.items():
            thumb_path = self.thumb_path(request, thumb_id, response, info)
            thumb_image, thumb_buf = self.convert_image(orig_image, size)
            yield thumb_path, thumb_image, thumb_buf

    def item_completed(self, results, item, info):
        thumb_paths = [
            os.path.join('thumbs/small',
                         os.path.split(x['path'])[1]) for ok, x in results
            if ok
        ]
        if not thumb_paths:
            raise DropItem('Ad contained no images')
        item['thumb_paths'] = thumb_paths
        return item


class ParsePipeline:
    def process_item(self, item, spider):
        # ['Freguesia', 'Concelho', 'Distrito'] ou ['Freguesia', 'Concelho'].
        location = item['location']
        if isinstance(location, str):
            item['location'] = [
                x.strip() for x in item['location'].rsplit(',', 2)
            ]

        # 160 000 € -> int(160000)
        # 160.000 € -> int(160000)
        # 160,60 €  -> int(   160)
        item['price'] = self._parse_price(item['price'])

        if 'for_sale' is not None:
            item['for_sale'] = self._is_sale(item)

        if not item['bedrooms']:
            if item['tipologia']:
                item['bedrooms'] = int(item['tipologia'][1:3])
        else:
            item['bedrooms'] = int(item['bedrooms'][0:2])

        if item['bathrooms']:
            item['bathrooms'] = int(item['bathrooms'][0:2])

        item['title'] = item['title'].lower()
        item['description'] = item['description'].lower()

        return item

    def _parse_price(self, price):
        return int(
            price.split(',')[0].translate({ord(c): None
                                           for c in ' .€'}))

    def _is_sale(self, item):
        if ('vendo' in item['title'] or 'vende' in item['title']
                or 'vendo' in item['description']
                or 'vende' in item['description']):
            return True
        if ('arrendo' in item['title'] or 'renda' in item['title']
                or 'arrendo' in item['description']
                or 'renda' in item['description']):
            return False
        return item['price'] > 20000


class DatabasePipeline:
    def process_item(self, item, spider):
        location = models.Location.objects.filter(
            freguesia__trigram_similar=item['location'][0]).first()
        if not location:
            location = models.Location.objects.filter(
                freguesia__trigram_similar=item['location'][1]).first()

        tipologia = models.Ad.Tipologia.APARTAMENTO
        if 'moradia' in item['title'] or 'casa' in item['title']:
            tipologia = models.Ad.Tipologia.MORADIA

        item['source'] = models.Ad.Source[item['source']]
        item['location'] = location
        item['tipologia'] = tipologia
        item['cover_photo'] = item['thumb_paths'][0]

        del item['image_urls']
        del item['thumb_paths']

        models.Ad.objects.update_or_create(url=item['url'], defaults=item)

        return item
