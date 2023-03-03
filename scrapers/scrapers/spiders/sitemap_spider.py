from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapers.items import SitemapItem
import random

a = 40000


class MySitemapSpider(CrawlSpider):
    name = 'sitemap'
    url = 'https://turktedarikci.com/'
    allowed_domains = ['turktedarikci.com']
    start_urls = [url]
    rules = (Rule(LinkExtractor(allow=()), callback='parse_item', follow=True),)

    def __init__(self, *args, **kwargs):
        super(MySitemapSpider, self).__init__(*args, **kwargs)
        self.items = []
        self.count = 0

    def parse_item(self, response):
        if '&' in response.url:
            return

        item = SitemapItem()
        item['loc'] = response.url
        item['lastmod'] = '2022-10-10'
        item['changefreq'] = 'never'
        item['priority'] = str(random.randint(1, 10)/10)

        self.items.append(item)
        self.count += 1

        if self.count % a == 0:
            self.write_sitemap(self.count // a)
            self.items = []


    def write_sitemap(self, index):
        with open(f'sitemaps/sitemap{index}.xml', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for item in self.items:
                f.write('<url>\n')
                f.write('<loc>{}</loc>\n'.format(item['loc']))
                f.write('<lastmod>{}</lastmod>\n'.format(item['lastmod']))
                f.write('<changefreq>{}</changefreq>\n'.format(item['changefreq']))
                f.write('<priority>{}</priority>\n'.format(item['priority']))
                f.write('</url>\n')
            f.write('</urlset>\n')

    def create_sitemap_index(self, num_sitemaps):
        with open('sitemaps/sitemap.xml', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            for i in range(1, num_sitemaps+1):
                f.write('<sitemap>\n')
                f.write(f'<loc>{self.url}sitemap{i}.xml</loc>\n')
                f.write('</sitemap>\n')
            f.write('</sitemapindex>\n')

    def report(self):
        response_count = self.crawler.stats.get_value('downloader/response_count')
        response_status_count_200 = self.crawler.stats.get_value('downloader/response_status_count/200')
        response_status_count_404 = self.crawler.stats.get_value('downloader/response_status_count/404')
        response_status_count_301 = self.crawler.stats.get_value('downloader/response_status_count/301')
        with open('report.txt', 'w', encoding='utf-8') as f:
            f.write(f'{self.url}\n')
            f.write(f'Taranan URL sayısı: {response_count}\n')
            f.write(f'200 başarılı url sayısı: {response_status_count_200}\n')
            f.write(f'301 yönlendirmesi veren URL sayısı: {response_status_count_301}\n')
            f.write(f'404 sayfa bulunamadı hatası veren URL sayısı: {response_status_count_404}\n')


    def closed(self, reason):
        if self.items:
            self.write_sitemap((self.count // a) + 1)
        self.create_sitemap_index((self.count // a) + 1)
        self.report()

