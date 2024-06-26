import scrapy
import re
import os

# https://bookreadfree.com/book/132266
class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["bookreadfree.com"]
    start_urls = [
        # Stormrage
          "https://bookreadfree.com/all/334520"
        # The Shattering
        , "https://bookreadfree.com/all/508523"
        # Shadows Rising
        , "https://bookreadfree.com/all/62341"
        # World of Warcraft: Vol'jin: Shadows of the Horde
        , "https://bookreadfree.com/all/203708"
        # World of Warcraft: War Crimes
        , "https://bookreadfree.com/all/152886"
        # Jaina Proudmoore: Tides of War
        , "https://bookreadfree.com/all/316405"
        # Before the Storm
        , "https://bookreadfree.com/all/406080"
        
        # Wasp Factory
        , "https://bookreadfree.com/all/132266"
        # Porno For Psychos
        , "https://bookreadfree.com/book/242741"
        # Tetatologist
        , "https://bookreadfree.com/book/251503"
        # The Black Train
        , "https://bookreadfree.com/all/426333"
        # Mangled Meat
        , "https://bookreadfree.com/book/497228"
        # Terra Insanus
        , "https://bookreadfree.com/book/195883"
        # Bullet Through Your Face
        , "https://bookreadfree.com/all/371136"
        # "The Haunter Of The Threshold"
        , "https://bookreadfree.com/all/477396"
        # Header 2
        , "https://bookreadfree.com/all/511045"
        ]

    def parse(self, response):
        title = response.xpath("//article[@class='h']//div[@class='con']//b[@class='t']/text()").extract_first()
        urls = response.xpath("//div[@class='l']//a/@href").extract()
        print("Title: ", title)
        print("URLs: ", urls)
        count = 0
        for url in urls:
            count += 1
            full_url = response.urljoin(url)
            print("Full URL: ", full_url)
            yield scrapy.Request(full_url, callback=self.parse_book, meta={'title': title, 'count': count})

    def parse_book(self, response):
        title = response.meta['title']
        count = response.meta['count']
        first_p = response.xpath("//article[@class='c']/div[@class='con'][2]/p[1]").extract_first().strip().replace('\xa0', '')
        if first_p:
            first_p = '<p>' + re.sub('<br><br>', '</p><p>', str(first_p)) + '</p>'
            html = f"<body style='color: #b1b9c7; background-color: black; max-width: 650px; margin-left: auto; margin-right: auto; font: 1.05rem Arial'>{str(first_p)}</body>"

            dir_name = f"../books/{title}"
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            html_filename = f"{dir_name}/{title}_page{count}.html"
            print("HTML Filename: ", html_filename)
            with open(html_filename, 'w') as f:
                f.write(html)