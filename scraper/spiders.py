import datetime

from pymaybe import maybe
import scrapy

from scraper.items import AdItem


class OlxSpider(scrapy.Spider):
    name = 'olx'
    start_urls = [
        'https://www.olx.pt/imoveis/apartamento-casa-a-venda/?search[photos]=1',
        'https://www.olx.pt/imoveis/casas-moradias-para-arrendar-vender/?search[photos]=1',
    ]

    def parse(self, response):
        for ad in response.css('table[summary="Anúncio"]:not(.promoted-list)'):
            details = ad.css('.detailsLink').attrib['href']
            yield scrapy.Request(
                details, self.parse_imovirtual
                if 'imovirtual.com' in details else self.parse_olx)

        # next_page_el = response.css('a[data-cy="page-link-next"]')
        # if next_page_el:
        #     yield scrapy.Request(next_page_el.attrib['href'], self.parse)

    def parse_imovirtual(self, response):
        overview = {
            field.css('*::text').get()[:-2]: field.css('strong::text').get()
            for field in response.css('.section-overview li')
        }

        # [1, 'hora']
        amount, unit = response.xpath(
            '/html/body/div/article/div[3]/div[1]/div[3]/div/div[2]/text()[1]'
        ).get().split()[-2:]

        posted_at = datetime.date.today()
        if any(x in unit for x in ('hora', 'horas')):
            posted_at -= datetime.timedelta(hours=int(amount))
        elif any(x in unit for x in ('dia', 'dias')):
            posted_at -= datetime.timedelta(days=int(amount))
        elif any(x in unit for x in ('mês', 'meses')):
            posted_at -= datetime.timedelta(days=int(amount) * 30)
        elif any(x in unit for x in ('ano', 'anos')):
            posted_at -= datetime.timedelta(days=int(amount) * 365)

        yield AdItem(
            # 'Charneca de Caparica e Sobreda, Almada, Setúbal'
            location=response.css('a[href="#map"]::text').get(),
            # '490 € /mês' ou '160 000 €'
            price=response.xpath(
                '/html/body/div/article/header/div[2]/div[1]/div[2]/text()').
            get(),
            for_sale=not response.xpath(
                '/html/body/div/article/header/div[2]/div[1]/div[2]/small/text()'
            ),
            image_urls=[response.css('picture img').attrib['src']],
            # 'T1'
            tipologia=overview.get('Tipologia'),
            bedrooms=None,
            bathrooms=overview.get('Casas de Banho'),
            title=response.css('h1::text').get(),
            description='\n'.join(
                response.css('.section-description p::text, '
                             '.section-description div::text').getall()),
            posted_at=posted_at,
            source='IMOVIRTUAL',
            url=response.url.split('?')[0])

    _MONTHS = [
        None, 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ]

    def parse_olx(self, response):
        overview = {
            item.css('.offer-details__name::text').get():
            item.css('.offer-details__value::text').get()
            for item in response.css('.offer-details__item')
        }

        # ['12', 'Junho', '2020']
        day, month, year = response.css('.offer-bottombar__item strong::text'
                                        ).get().split(', ')[1].split()
        posted_at = datetime.date(int(year), self._MONTHS.index(month),
                                  int(day))

        yield AdItem(
            # 'Massamá E Monte Abraão, Sintra, Lisboa'
            location=response.css('address p::text').get(),
            price=response.css('.pricelabel__value::text').get(),
            # Terá que ser determinado posteriormente através do
            # título/descrição/preço.
            for_sale=None,
            image_urls=[response.css('#descImage img').attrib['src']],
            tipologia=overview.get('Tipologia'),
            bedrooms=overview.get('Quartos de dormir'),
            bathrooms=overview.get('Casas de Banho'),
            title=response.css('.offer-titlebox h1::text').get().strip(),
            description=''.join(
                response.css('#textContent::text').getall()).strip(),
            posted_at=posted_at,
            source='OLX',
            url=response.url)


class CustoJustoSpider(scrapy.Spider):
    name = 'custo_justo'
    start_urls = [
        'https://www.custojusto.pt/portugal/apartamentos',
        'https://www.custojusto.pt/portugal/moradias',
    ]

    _MONTHS = [
        None, 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set',
        'Out', 'Nov', 'Dez'
    ]

    def parse(self, response):
        for url in response.css('.container_related > a::attr(href)').getall():
            yield scrapy.Request(url, self.parse_detail)

        # next_page = response.css('.pagination.pull-right a::attr(href)').get()
        # if not next_page:
        #     yield scrapy.Request(next_page, self.parse)

    def parse_detail(self, response):
        overview = dict(
            zip(
                response.css('.gbody li::text').getall(),
                response.css('.gbody .value *::text').getall()))

        image = response.css('.main-slide::attr(src)').get()

        tipo = overview['Tipo'].strip()
        for_sale = (True if tipo == 'Venda' else
                    False if tipo == 'Arrendar' else None)

        # 'Hoje', 'Ontem', '13 Jun'
        date = response.css('.title-1 div strong::text').get().strip()
        if date == 'Hoje':
            posted_at = datetime.date.today()
        elif date == 'Ontem':
            posted_at = datetime.date.today() - datetime.timedelta(days=1)
        else:
            day, month = date.split()
            today = datetime.date.today()
            posted_at = datetime.date(today.year, self._MONTHS.index(month),
                                      int(day))

        yield AdItem(
            location=(maybe(overview.get('Freguesia')).strip(),
                      overview['Concelho'].strip()),
            price=maybe(response.css('.real-price::text').get()).strip(),
            for_sale=for_sale,
            image_urls=[image] if image else [],
            tipologia=overview['Tipologia'],
            bedrooms=None,
            bathrooms=None,
            title=response.css('.title-1 h1::text').get(),
            description='\n'.join(response.css('.lead.words::text').getall()),
            posted_at=posted_at,
            source='CUSTO_JUSTO',
            url=response.url)
