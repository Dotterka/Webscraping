import scrapy
from ..items import OnlineShopItem
from datetime import date

class FlancoSpider(scrapy.Spider):
    name = 'flanco'
    #start url is the smartphone category
    start_urls = [
            'https://www.flanco.ro/telefoane-tablete/smartphone.html'
    ]
   
    #output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
    
    def __init__(self, *args, **kwargs):
        super(FlancoSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        products = response.xpath("//div[@class='produs']")
        # import ipdb; ipdb.set_trace()
        #pagination
        next_page = response.xpath("//a[@class='next i-next']/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        for product in products:
            item = OnlineShopItem()
                
            item['name'] = ' '.join(product.xpath("div[@class='produs-title']//a[@class='product-new-link']/@title").extract_first().split(",")[0].split(" ")[2:]).strip() \
                           + " " + ' '.join(product.xpath("div[@class='produs-title']//a[@class='product-new-link']/@title").extract_first().split("GB,")[0].split(",")[-1:]).strip() \
                           + " GB " + ' '.join(product.xpath("div[@class='produs-title']//a[@class='product-new-link']/@title").extract_first().strip().split(",")[-1:]).strip()
            #checking if the field exist
            if product.xpath("div[@itemprop='offers']//span[@itemprop='price']/@content").get():
                item['price'] = product.xpath("div[@itemprop='offers']//span[@itemprop='price']/@content").extract_first().strip()
            else:
                item['price'] = None
            item['url'] = product.xpath("div[@class='produs-title']//a[@class='product-new-link']/@href").extract_first()
            item['review_score'] = product.xpath("div[@class='rating']//div[@class='ezfull']/@style").extract_first().split(":")[1].split("%")[0] 
            item['review_score'] = int(item['review_score']) * 5 / 100
            item['review_count'] = product.xpath("div[@class='rating']//span[@class='count']/text()").extract_first().split("(")[1].split(")")[0].strip()
            if item['review_count'] != "0":
                item['review_count'] = product.xpath("div[@class='rating']//span[@class='count']/text()").extract_first().split("(")[1].split(" ")[0].strip()
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
   
