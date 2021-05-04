import scrapy
from ..items import OnlineShopItem
from datetime import date
import cfscrape
from lxml import html

# returns a CloudflareScraper instance
scraper = cfscrape.create_scraper()

class PcGarageRevisitSpider(scrapy.Spider):
    name = 'pc_garage_revisit'
    # start url is wikipedia, because pc_garage url at this point isn't available
    start_urls = ['https://www.wikipedia.org']
   
    # output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
        

    def parse(self, response):
        response = scraper.get("https://www.pcgarage.ro/smartphone/").content
        item = OnlineShopItem()
        items = self.get_items_from_response(response)
        for item in items:
            yield item

    def get_items_from_response(self, response, items=[]):
        products = html.fromstring(response).xpath("//div[@class='product_box_container']")
        for product in products:
            if product.xpath("div[@class='product_box']//p[@class='price']/text()"):
                item = OnlineShopItem()
                # import ipdb; ipdb.set_trace()
                    
                item['name'] = ' '.join(product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/text()")[0].strip().split(",")[0].split(" ")[1:]) + " " \
                             + ' '.join(product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/text()")[0].strip().split("GB,")[0].split(",")[-1:]).strip()+ " GB " \
                             + ' '.join(product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/text()")[0].strip().split(",")[-1:]).strip()
                item['price'] = product.xpath("div[@class='product_box']//p[@class='price']/text()")[0].split(" ")[0].replace(".", "").replace(",", ".")
                item['url'] = product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/@href")[0]
                item['review_score'] = None 
                item['review_count'] = None
                item['provider_name'] = "pc_garage"
                item['color'] = None
                item['display_type'] = None
                item['display_resolution'] = None        
                item['display_size'] = None
                item['chipset'] = None
                item['internal_memory'] = None
                item['ram'] = None
                item['main_camera'] = None
                item['selfie_camera'] = None
                item['os'] = None
                item['os_version'] = None
                item['nfc_indicator'] = None
                item['battery_type'] = None
                item['battery_capacity'] = None
                item['date'] = date.today().strftime("%m/%d/%Y")
                items.append(item)
        # pagination
        next_page = html.fromstring(response).xpath("//a[@class='gradient_half' and text()='›']/@href")
        if next_page:
            response = scraper.get(next_page[0]).content
            items = self.get_items_from_response(response, items)
        return items
