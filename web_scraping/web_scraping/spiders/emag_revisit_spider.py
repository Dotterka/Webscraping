import scrapy
import json
from ..items import OnlineShopItem
from datetime import date

class EmagRevisitSpider(scrapy.Spider):
    name = 'emag_revisit'
    #start url is the smartphone category
    start_urls = [
            'https://www.emag.ro/telefoane-mobile/filter/tip-telefon-f9440,smartphone-v-8546570/sort-iddesc/c?ref=lst_leftbar_9440_-8546570'
    ]
   
    #output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
    
    #send request only to the revisit links
    def parse(self, response):
        with open('emag_revisit_links.json') as f:
            data = json.load(f)
            for url in data:
                yield scrapy.Request(url, callback=self.parse_product)

    def parse_product(self, response): 
        if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Tip display')]/following-sibling::td/text()").get() and response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Memorie RAM')]/following-sibling::td/text()").get():   
            item = OnlineShopItem()
            item['name'] = ' '.join(response.xpath("//h1[@class='page-title']/text()").extract_first().strip().split(",")[0].split(" ")[2:]) \
                            + ' '.join(response.xpath("//h1[@class='page-title']/text()").extract_first().strip().split("GB,")[0].split(",")[-1:]) \
                            + " GB "+ ' '.join(response.xpath("//h1[@class='page-title']/text()").extract_first().strip().split(",")[-1:]).strip()
            item['price'] = response.xpath("//p[@class='product-new-price']/text()").extract()[0].strip().replace(".", "")+ "." + response.xpath("//p[@class='product-new-price']/sup/text()").extract()[0].strip()
            item['url'] = response.url
            item['review_score'] = response.xpath("//div[@class='product-highlight']//span[contains(@class, 'star-rating-text')]/text()").extract_first() or "0"
            item['review_count'] = response.xpath("//p[@class='hidden-xs']/a[@href='#reviews-section']/text()").extract_first() or "0"
            item['review_count'] = item['review_count'].split(" ")[0]
            item['provider_name'] = 'emag'
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Culoare')]/following-sibling::td/text()").get():
                item['color'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Culoare')]/following-sibling::td/text()").extract_first().strip()
            else:
                item['color'] = None
            #checking if the field exist
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Tip display')]/following-sibling::td/text()").get():
                item['display_type'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Tip display')]/following-sibling::td/text()").extract_first().strip()
            else:
                item['display_type'] = None
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Rezolutie (pixeli)')]/following-sibling::td/text()").get():
                item['display_resolution'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Rezolutie (pixeli)')]/following-sibling::td/text()").extract_first().strip()        
            else:
                item['display_resolution'] = None
            item['display_size'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Dimensiune ecran')]/following-sibling::td/text()").extract_first().strip().split(" ")[0]
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Model procesor')]/following-sibling::td/text()").get():
                item['chipset'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Model procesor')]/following-sibling::td/text()").extract_first().strip()
            else:
                item['chipset'] = None
            item['internal_memory'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Memorie interna')]/following-sibling::td/text()").extract_first().strip()
            item['ram'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Memorie RAM')]/following-sibling::td/text()").extract_first().strip()
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Rezolutie camera principala')]/following-sibling::td/text()").get():
                item['main_camera'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Rezolutie camera principala')]/following-sibling::td/text()").extract_first().strip().replace("\n"," + ")
            else:
                item['main_camera'] = None
            item['selfie_camera'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Rezolutie camera frontala')]/following-sibling::td/text()").extract_first().strip()
            item['os'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Sistem de operare')]/following-sibling::td/text()").extract_first().strip()
            item['os_version'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Versiune sistem operare')]/following-sibling::td/text()").extract_first().strip().split(" ")[1]
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Conectivitate')]/following-sibling::td[contains(text(),'NFC')]"):
                item['nfc_indicator'] = True
            else:
                item['nfc_indicator'] = False
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Tip baterie')]/following-sibling::td/text()").get():
                item['battery_type'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Tip baterie')]/following-sibling::td/text()").extract_first().strip()
            else:
                item['battery_type'] = None
            if response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Capacitate baterie')]/following-sibling::td/text()").get():
                item['battery_capacity'] = response.xpath("//table[@class='table table-striped product-page-specifications']//td[contains(text(),'Capacitate baterie')]/following-sibling::td/text()").extract_first().strip()
            else:
                item['battery_capacity'] = None
            item['date'] = date.today().strftime("%m/%d/%Y")

            yield item
   
