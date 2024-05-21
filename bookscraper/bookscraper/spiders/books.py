import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["bookreadfree.com"]
    start_urls = ["https://bookreadfree.com/book/242741"]

    def parse(self, response):
        pass
