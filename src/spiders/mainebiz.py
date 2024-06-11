import scrapy
from scrapy.http import HtmlResponse
from ..items import MainebizItem

class MainebizSpider(scrapy.Spider):
    name = 'mainebiz'
    allowed_domains = ['mainebiz.biz']
    start_urls = ['https://www.mainebiz.biz/']

    def parse(self, response):
        # Extract all the links from the homepage
        links = response.css('a::attr(href)').getall()

        # Follow each link and parse the text content
        for link in links:
            if link.startswith('/'):
                # Construct the absolute URL
                url = response.urljoin(link)
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        # Create an HtmlResponse object from the response body
        html_response = HtmlResponse(url=response.url, body=response.body, encoding='utf-8')

        # Extract the text content using XPath
        text_content = ' '.join(html_response.xpath('//body//text()').getall())

        # Remove excessive whitespace and newline characters
        text_content = ' '.join(text_content.split())

        # Generate a unique filename for each page
        filename = response.url.split('/')[-1] + '.txt'

        # Create a MainebizItem and populate its fields
        item = MainebizItem()
        item['filename'] = filename
        item['text_content'] = text_content

        yield item