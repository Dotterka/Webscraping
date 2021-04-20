import scrapy
from ..items import OnlineShopItem
from datetime import date

class PcGarageRevisitSpider(scrapy.Spider):
    name = 'pc_garage_revisit'
    #start url is the smartphone category
    start_urls = [
            'https://www.pcgarage.ro/smartphone/'
    ]
   
    #output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
    
    def __init__(self, *args, **kwargs):
        super(PcGarageRevisitSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        products = response.xpath("//div[@class='product_box_container']")

        #pagination
        next_page = response.xpath("//a[@class='gradient_half' and text()='›']/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)    
        for product in products:
            item = OnlineShopItem()
            item['name'] = ' '.join(product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/text()").extract_first().strip().split(",")[0].split(" ")[1:]) + " " \
                         + ' '.join(product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/text()").extract_first().strip().split("GB,")[0].split(",")[-1:]).strip()+ " GB " \
                         + ' '.join(product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/text()").extract_first().strip().split(",")[-1:]).strip()
            item['price'] = product.xpath("div[@class='product_box']//p[@class='price']/text()").extract_first().split(" ")[0].replace(".", "").replace(",", ".")
            item['url'] = product.xpath("div[@class='product_box']//div[@class='product_box_name']//a/@href").extract_first()
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

            yield item
