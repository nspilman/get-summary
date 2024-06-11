import scrapy
from scrapy.http import HtmlResponse
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, error
import logging

import os
from scrapy.dupefilters import BaseDupeFilter

from datetime import datetime

class CustomDupeFilter(BaseDupeFilter):
    def __init__(self, path='downloads'):
        self.path = path
        self.date_string = datetime.today().strftime("%Y-%m-%d")
        self.filenames_seen = set()

    def open(self):
        if os.path.exists(self.path):
            for directory in os.listdir(self.path):
                for filename in os.listdir(os.path.join(self.path, directory)):
                    self.filenames_seen.add(filename)
            for filename in os.listdir(self.path):
                self.filenames_seen.add(filename)

    def close(self, reason):
        pass

    def request_seen(self, request):
        filename = request.url.split('/')[-1] + '.txt'
        if filename in self.filenames_seen:
            return True
        self.filenames_seen.add(filename)
        return False

class MainebizItem(scrapy.Item):
    filename = scrapy.Field()
    text_content = scrapy.Field()

import os

class MainebizPipeline:
    def process_item(self, item, spider):
        logging.basicConfig(level=logging.INFO, format='PROCESSING!!!!!')

        # Get the filename and text content from the item
        filename = item['filename']
        text_content = item['text_content']
        
        # Create the downloads directory if it doesn't exist
        import datetime
        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        download_dir = os.path.join('downloads', date_string)
        os.makedirs(download_dir, exist_ok=True)
        filepath = os.path.join(download_dir, filename)
        print(filepath)
        
        # Save the text content to a file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text_content)
        
        logging.info(f"Saved file: {filename}")
        return item

class MainebizSpider(scrapy.Spider):
    name = 'mainebiz'
    allowed_domains = ['mainebiz.biz']
    start_urls = ['https://www.mainebiz.biz/']

    custom_settings = {
        'ITEM_PIPELINES': {
            MainebizPipeline: 300
        },
        'DUPEFILTER_CLASS': CustomDupeFilter,
    }
    
    def parse(self, response):
        # Extract all the links from the homepage
        links = response.css('a::attr(href)').getall()
        
        logging.info(f"Found {len(links)} links on the homepage")
        
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
        
        logging.info(f"Parsed page: {response.url}")
        yield item

# Configure logging
# logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

runner = CrawlerRunner(settings={
    'ITEM_PIPELINES': {
        'MainebizPipeline': 300
    }
})


def run_pipeline():
    d = runner.crawl(MainebizSpider)
    d.addBoth(lambda _: reactor.stop())
    
    try:
        reactor.run()
    except error.ReactorAlreadyRunning:
        pass

