import scrapy
from ..items import OnlineShopItem

class QuoteSpider(scrapy.Spider):
    name = 'pc_garage'
    #kiindulo link a telefonok kategoria linkje
    start_urls = [
            'https://www.pcgarage.ro/smartphone/'
            #'https://www.emag.ro/homepage'
    ]
   
    #100 begyujtott item utan alljon le, valamint a pipeline a json fajlhoz, amibe irjuk a begyujtott adatokat
    custom_settings = { 'CLOSESPIDER_ITEMCOUNT': 100,
                        'ITEM_PIPELINES': {'web_scraping.pipelines.MobilePhonePipeline': 300}
                        }

    #def parse(self, response):
        #items = OnlineShopItem()
     #   links = response.xpath("//li[contains(@class, 'megamenu')]/a/@href").extract()
      #  good_links = []
       # for link in links:
        #    if link != 'javascript:void(0)':
         #       good_links.append(response.urljoin(link))

       # for link in good_links:
        #    yield scrapy.Request(link, callback=self.parse_main_category)
    
  #  def parse_main_category(self, response):
   #     links = response.xpath("//ul[@class='emg-aside-links']//a/@href").extract()
        #import ipdb
        #ipdb.set_trace()
    #    for link in links:
     #       if 'reincarcare-cartele' not in link:
      #          yield scrapy.Request(response.urljoin(link), callback=self.parse_sub_category) 

  #  def parse_sub_category(self, response):
        #import ipdb
        #ipdb.set_trace()
   #     links = response.xpath("//ul[@class='emg-aside-links']//a/@href").extract()
    #    for link in links:
     #       yield scrapy.Request(response.urljoin(link), callback=self.parse_products)
    
    def parse(self, response):
        links = response.xpath("//h2[@class='my-0']/a/@href").extract()
        #import ipdb
        #ipdb.set_trace()

        #lapozashoz az oldalakon
        next_page = response.xpath("//a[@class='gradient_half' and text()='›']/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)
   
    def parse_product(self, response):
        # import ipdb
        # ipdb.set_trace()
        item = OnlineShopItem()
        item['name'] = ' '.join(response.xpath("//h1[@id='product_name']/text()").extract_first().strip().split(",")[0].split(" ")[1:])
        item['price'] = response.xpath("//span[@class='price_num']/text()").extract_first().split(" ")[0].replace(".", "").replace(",", ".")
        item['url'] = response.url
        item['review_score'] = response.xpath("//div[@class='ar_title rating_bar_inline']/p/b/span/text()").extract_first() or "0"  
        item['review_count'] = response.xpath("//span[@itemprop='reviewCount']/text()").extract_first() or "0"
        item['color'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Culoare')]/following-sibling::td/text()").extract_first().strip()
        item['display_type'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Ecran')]/following-sibling::td/text()").extract_first().strip()
        item['display_resolution'] = ' '.join(response.xpath("//table[@id='specs_table']//td[contains(text(),'Rezolutie')]/following-sibling::td/text()").extract_first().strip().split(" ")[0:3])        
        item['display_size'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Marime display')]/following-sibling::td/text()").extract_first().strip().split(" ")[0]
        item['chipset'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Chipset')]/following-sibling::td/text()").extract_first().strip()
        item['chipset_model'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Model Chipset')]/following-sibling::td/text()").extract_first().strip()
        item['internal_memory'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Memorie interna flash')]/following-sibling::td/text()").extract_first().strip()
        item['ram'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'RAM')]/following-sibling::td/text()").extract_first().strip()
        item['main_camera'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Camera foto principala')]/following-sibling::td/text()").extract_first().strip()
        item['selfie_camera'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Camera foto secundara')]/following-sibling::td/text()").extract_first().strip()
        item['os'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Sistem operare')]/following-sibling::td/text()").extract_first().strip()
        item['os_version'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Versiune')]/following-sibling::td/text()").extract_first().strip()
        item['nfc_indicator'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'NFC (Near Field Communication)')]/following-sibling::td/text()").extract_first().strip() == "Da"
        item['battery_type'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Tip acumulator')]/following-sibling::td/text()").extract_first().strip()
        item['battery_capacity'] = response.xpath("//table[@id='specs_table']//td[contains(text(),'Capacitate acumulator')]/following-sibling::td/text()").extract_first().strip()



        #item['review_count'] = item['review_count'].split(" ")[0]
        #item['name'] = None
        #import ipdb
        #ipdb.set_trace()
        yield item
