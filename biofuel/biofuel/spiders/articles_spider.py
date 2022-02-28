import scrapy
from ..items import BiomassItem

class ArticlesSpider(scrapy.Spider):
    name = "articles"
    start_urls = [
        'https://www.biofuelsdigest.com/bdigest/category/chemicals-materials/'
    ]

    def parse(self, response):
        elements = response.css('#colLeft a')
        #for element in elements:
        for i in range(0, 10):
            element = elements[i]
            week = element.css('::text').extract_first()
            url = element.css('::attr(href)').extract_first()
            # Items
            if week and url:
                yield response.follow(url, callback = self.parseArticles, 
                    meta = {'week_index':i, 'week':week, 'url':url })

    def parseArticles(self, response):
        # Articles
        elements = response.css('#articles div')
        articles = 0
        for index, element in enumerate(elements):
            article = {}
            article['week_index'] = response.meta['week_index']
            article['article_index'] = index
            article['title'] = element.css('h3::text').extract_first()
            article['description'] = element.css('span::text').extract_first()
            article['url'] = element.css('br+ a::attr(href)').extract_first()
            articles = articles + 1
            yield response.follow(article['url'], callback = self.parseArticle, 
                meta = {
                    'article_index':index,
                    'article':article
                })
        # Yield item
        item = BiomassItem()
        item['week_index'] = response.meta['week_index']
        item['week'] = response.meta['week']
        item['url'] = response.meta['url']
        item['articles'] = articles
        yield item

    def parseArticle(self, response):
        article = response.meta['article']
        # Elements
        elements = response.css('.post')
        article['author'] = elements.css('.author .author a::text').extract_first()
        article['text'] = ''.join(elements.css('p::text').extract())
        yield article