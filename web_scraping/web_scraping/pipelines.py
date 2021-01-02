# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

#class EmagPipeline:
#    def open_spider(self, spider):
#        self.f = open("emag_items.csv", "w+")
#        self.posts_writer = csv.writer(self.f)
#        self.posts_writer.writerow(['name',
#                                    'price',
#                                    'url',
#                                    'review_score',
#                                    'review_count'])
#    def process_item(self, item, spider):
#        self.posts_writer.writerow([item.['name'],
#                                    item.['price'],
#                                    item.['url'],
#                                   item.['review_score'],
#                                    item.['review_count']])
#    def close_spider(self, spider):
#        self.f.close()

class EmagPipeline:

    def open_spider(self, spider):
        self.file = open('emag_items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


