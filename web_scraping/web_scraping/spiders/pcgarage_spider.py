import scrapy
from ..items import OnlineShopItem
from datetime import date

class PcGarageSpider(scrapy.Spider):
    name = 'pc_garage'
    #start url is the smartphone category
    start_urls = [
            'https://www.pcgarage.ro/smartphone/'
    ]
   
    #output file
    custom_settings = { 
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }
    
    def parse(self, response):
        links = response.xpath("//h2[@class='my-0']/a/@href").extract()

        #pagination
        next_page = response.xpath("//a[@class='gradient_half' and text()='›']/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)
   
    def parse_product(self, response):
        item = OnlineShopItem()
        item['name'] = ' '.join(response.xpath("//h1[@id='product_name']/text()").extract_first().strip().split(",")[0].split(" ")[1:]) + " " \
                     + ' '.join(response.xpath("//h1[@id='product_name']/text()").extract_first().strip().split("GB,")[0].split(",")[-1:]).strip()+ " GB " \
                     + ' '.join(response.xpath("//h1[@id='product_name']/text()").extract_first().strip().split(",")[-1:]).strip()
        item['price'] = response.xpath("//span[@class='price_num']/text()").extract_first().split(" ")[0].replace(".", "").replace(",", ".")
        item['url'] = response.url
        item['review_score'] = response.xpath("//div[@class='ar_title rating_bar_inline']/p/b/span/text()").extract_first() or "0"  
        item['review_count'] = response.xpath("//span[@itemprop='reviewCount']/text()").extract_first() or "0"
        item['provider_name'] = self.name
        #error-handling if the field doesn't exist
        try: 
          item['color'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Culoare')]/following-sibling::td/div/text()").extract_first().strip()
        except AttributeError:
          item['color'] = None
        item['display_type'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Ecran')]/following-sibling::td/div/text()").extract_first().strip()
        item['display_resolution'] = ' '.join(response.xpath("//table[@id='specs_table']//td[contains(text(),'Rezolutie')]/following-sibling::td/div/text()").extract_first().strip().split(" ")[0:3])      
        item['display_size'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Marime display')]/following-sibling::td/div/text()").extract_first().strip().split(" ")[0]
        try:
          item['chipset'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Chipset')]/following-sibling::td/div/text()").extract_first().strip() + ' ' \
                          + response.xpath("//table[@id='specs_table']//td[contains(text(),'Model Chipset')]/following-sibling::td/div/text()").extract_first().strip()
        except AttributeError:
          item['chipset'] = None
        item['internal_memory'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Memorie interna flash')]/following-sibling::td/div/text()").extract_first().strip()
        item['ram'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'RAM')]/following-sibling::td/div/text()").extract_first().strip()
        item['main_camera'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Camera foto principala')]/following-sibling::td/div/text()").extract_first().strip()
        item['selfie_camera'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Camera foto secundara')]/following-sibling::td/div/text()").extract_first().strip()
        item['os'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Sistem operare')]/following-sibling::td/div/text()").extract_first().strip()
        item['os_version'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Versiune')]/following-sibling::td/div/text()").extract_first().strip()
        try:
          item['nfc_indicator'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'NFC (Near Field Communication)')]/following-sibling::td/div/text()").extract_first().strip() == "Da"
        except AttributeError:
          item['nfc_indicator'] = None
        try:
          item['battery_type'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Tip acumulator')]/following-sibling::td/div/text()").extract_first().strip()
        except AttributeError:
          item['battery_type'] = None
        try:
          item['battery_capacity'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Capacitate acumulator')]/following-sibling::td/div/text()").extract_first().strip()
        except AttributeError:
          item['battery_capacity'] = None
        item['date'] = date.today().strftime("%d/%m/%Y")

        yield item
