from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapers.items import SitemapItem

class MySitemapSpider(CrawlSpider):
    name = 'sitemap'
    allowed_domains = ['adamsllc.net']
    start_urls = ['https://adamsllc.net/']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def __init__(self, *args, **kwargs):
        super(MySitemapSpider, self).__init__(*args, **kwargs)
        self.items = []
        self.count = 0

    def parse_item(self, response):
        item = SitemapItem()
        item['loc'] = response.url
        item['priority'] = '0.5'
        self.items.append(item)
        self.count += 1

        if self.count % 100 == 0:
            self.write_sitemap(self.count // 100)
            self.items = []

    def closed(self, reason):
        if self.items:
            self.write_sitemap((self.count // 100) + 1)

    def write_sitemap(self, index):
        with open(f'sitemaps/sitemap_{index}.xml', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for item in self.items:
                f.write('<url>\n')
                f.write('<loc>{}</loc>\n'.format(item['loc']))
                f.write('<priority>{}</priority>\n'.format(item['priority']))
                f.write('</url>\n')
            f.write('</urlset>\n')