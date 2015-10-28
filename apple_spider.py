import scrapy

class AppleSpider(scrapy.Spider):
    name = 'apple'
    start_urls = ['http://www.apple.com/hk/']

    def parse(self, response):
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_question)

    def parse_question(self, response):
        yield {
            'body': response.css('a::text').extract(),
            'link': response.url,
        }
