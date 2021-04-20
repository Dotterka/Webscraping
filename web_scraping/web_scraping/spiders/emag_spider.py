import scrapy
from ..items import OnlineShopItem
from datetime import date

class EmagSpider(scrapy.Spider):
    name = 'emag'
    #start url is the smartphone category
    start_urls = [
            'https://www.emag.ro/telefoane-mobile/filter/tip-telefon-f9440,smartphone-v-8546570/sort-iddesc/c?ref=lst_leftbar_9440_-8546570'
    ]
   
    #output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
    
    def parse(self, response):
        products = response.xpath("//div[@class='card-item js-product-data']")
        # import ipdb
        # ipdb.set_trace()

        #pagination
        next_page = response.xpath("//li[not(contains(@class, 'disabled'))]/a[@aria-label='Next']/span[text()='Pagina urmatoare']/parent::a/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        for product in products:
            item = OnlineShopItem()
            item['name'] = ' '.join(product.xpath("div[@class='card']//a[@class='product-title js-product-url']/@title").extract_first().split(",")[0].split(" ")[2:]).strip() \
                           + " " + ' '.join(product.xpath("div[@class='card']//a[@class='product-title js-product-url']/@title").extract_first().split("GB,")[0].split(",")[-1:]).strip() \
                           + " GB "+ ' '.join(product.xpath("div[@class='card']//a[@class='product-title js-product-url']/@title").extract_first().split(",")[-1:]).strip()
            item['price'] = product.xpath("div[@class='card']//p[@class='product-new-price']/text()").extract()[0].strip().replace(".", "") + "." + response.xpath("//p[@class='product-new-price']/sup/text()").extract()[0].strip()
            item['url'] = product.xpath("div[@class='card']//a[@class='product-title js-product-url']/@href").extract_first()
            item['review_score'] = product.xpath("div[@class='card']//div[contains(@class, 'star-rating-read')]/@class").extract_first().split(" ")[2].split("-")[-1] 
            item['review_count'] = product.xpath("//div[@class='card']//span[@class='hidden-xs ']/text()").extract_first().split(" ")[0]
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
            item['date'] = date.today().strftime("%m/%d/%Y")

            yield item
