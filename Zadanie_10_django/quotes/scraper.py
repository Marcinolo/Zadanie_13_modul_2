import scrapy
from scrapy.crawler import CrawlerProcess

QUOTES_AUTHORS = {"quotes": [], "authors": []}


class QuotesAuthorsSpider(scrapy.Spider):
    name = "scraper_data"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    about_urls = set()
    def parse(self, response):
        if response.xpath("/html//div[@class='quote']"):
            for quote in response.xpath("/html//div[@class='quote']"):
                self.about_urls.add(quote.xpath("span/a/@href").get())
                yield QUOTES_AUTHORS["quotes"].append({
                    "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small/text()").extract_first(),
                    "quote": quote.xpath("span[@class='text']/text()").get().strip(),
                })
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield scrapy.Request(
                    url=self.start_urls[0] + next_link, callback=self.parse
                )
        elif response.xpath("/html//div[@class='author-description']/text()"):
            yield QUOTES_AUTHORS["authors"].append({
                "fullname": response.xpath("/html//h3/text()").get(),
                "born_date": response.xpath(
                    "/html//span[@class='author-born-date']/text()"
                ).get(),
                "born_location": response.xpath(
                    "/html//span[@class='author-born-location']/text()"
                ).get(),
                "description": response.xpath(
                    "/html//div[@class='author-description']/text()"
                ).get().strip(),
            })
        for about_url in self.about_urls:
            yield scrapy.Request(
                url=self.start_urls[0] + about_url, callback=self.parse
            )
    
    def closed(self, reason):
        self.log(f"finished scraping data.")
        self.crawler.engine.close_spider(self, "success.")


def get_data():
    if QUOTES_AUTHORS["authors"] or QUOTES_AUTHORS["quotes"]:
        return QUOTES_AUTHORS["quotes"], QUOTES_AUTHORS["authors"]
    process = CrawlerProcess()
    process.crawl(QuotesAuthorsSpider)
    process.start()
    return QUOTES_AUTHORS["quotes"], QUOTES_AUTHORS["authors"] 