import scrapy
from ..items import BiofuelItem

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    page_number = 1
    article_index = 0
    start_urls = [
        'https://www.biofuelsdigest.com/bdigest/category/chemicals-materials/'
    ]

    def parse(self, response):
        if self.page_number < 3:
            elements = response.css('#content .category-chemicals-materials')
            #for element in elements:
            for i in range(0, 3):
                element = elements[i]
                item = BiofuelItem()
                title = element.css('.post-title a::text').extract_first()
                url = element.css('.more-link::attr(href)').extract_first()
                # Items
                if title and url:
                    item['index'] = self.article_index
                    item['title'] = title
                    item['url'] = url
                    yield response.follow(url, callback = self.parseArticle, 
                        meta = {'item':item })
                self.article_index = self.article_index + 1
                yield item
            # Next page
            self.page_number = self.page_number + 1
            next_page = "https://www.biofuelsdigest.com/bdigest/category/chemicals-materials/page/{}/".format(str(self.page_number))
            yield response.follow(next_page, callback = self.parse)

    def parseArticle(self, response):
        article = {}
        item = response.meta['item']
        article['index'] = item['index']
        article['title'] = item['title']
        article['date'] = response.css('.meta-date::text').extract_first()
        article['author'] = response.css('.meta-author a::text').extract_first()
        article['text'] = ''.join(response.css('.p1::text').extract())
        yield article