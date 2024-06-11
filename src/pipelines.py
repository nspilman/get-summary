# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PioneerPipeline:
    def process_item(self, item, spider):
        return item


import os

class MainebizPipeline:
    def process_item(self, item, spider):
        # Get the filename and text content from the item
        filename = item['filename']
        text_content = item['text_content']

        # Create the downloads directory if it doesn't exist
        os.makedirs('downloads', exist_ok=True)

        # Save the text content to a file
        with open(os.path.join('downloads', filename), 'w', encoding='utf-8') as file:
            file.write(text_content)

        return item