import scrapy
from ..items import OnlineShopItem
from datetime import date

class CelSpider(scrapy.Spider):
    name = 'cel'
    #start url is the smartphone category
    start_urls = [
            'https://www.cel.ro/telefoane-mobile/tip-telefon-i2762/smartphone/4d-1'
    ]
   
    #output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
    
    def parse(self, response):
        products = response.xpath("//div[@cat_nam='Telefoane Mobile']")

        #pagination
        next_page = response.xpath("//a[@class='last']/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        for product in products:
            item = OnlineShopItem()
            item['name'] = ' '.join(product.xpath("div[@class='productListingWrapper']//span/text()").extract_first().split(" ")[2:]).split("GB ")[0] + " GB " \
                            + product.xpath("div[@class='productListingWrapper']//span/text()").extract_first().split(" ")[-1]
            item['price'] = product.xpath("div[@class='productListingWrapper']//div[@class='pretWrapper']//b/text()").extract_first()
            item['url'] = product.xpath("div[@class='productListingWrapper']//@href").extract_first()
            item['review_score'] = None 
            item['review_count'] = None
            item['provider_name'] = self.name
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
            item['date'] = date.today().strftime("%d/%m/%Y")

            yield item
   
