import scrapy
from ..items import OnlineShopItem

class QuoteSpider(scrapy.Spider):
    name = 'emag'
    #kiindulo link a telefonok kategoria linkje
    start_urls = [
            'https://www.emag.ro/telefoane-mobile/filter/tip-telefon-f9440,smartphone-v-8546570/sort-iddesc/c?ref=lst_leftbar_9440_-8546570'
            #'https://www.emag.ro/homepage'
    ]
   
    #100 begyujtott item utan alljon le, valamint a pipeline a json fajlhoz, amibe irjuk a begyujtott adatokat
    custom_settings = { #'CLOSESPIDER_ITEMCOUNT': 100,
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
        #links = response.xpath("//h2[@class='card-body product-title-zone']/a/@href").extract()
        products = response.xpath("//div[@class='card-item js-product-data']")
        #import ipdb
        #ipdb.set_trace()

        #lapozashoz az oldalakon
        next_page = response.xpath("//li[not(contains(@class, 'disabled'))]/a[@aria-label='Next']/span[text()='Pagina urmatoare']/parent::a/@href").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        for product in products:
            item = OnlineShopItem()
            item['name'] = ' '.join(product.xpath("div[@class='card']//a[@class='product-title js-product-url']/@title").extract_first().split(",")[0].split(" ")[2:])
            item['price'] = product.xpath("div[@class='card']//p[@class='product-new-price']/text()").extract()[0].strip().replace(".", "") + "." + response.xpath("//p[@class='product-new-price']/sup/text()").extract()[0].strip()
            item['url'] = product.xpath("div[@class='card']//a[@class='product-title js-product-url']/@href").extract_first()
            item['review_score'] = product.xpath("div[@class='card']//div[contains(@class, 'star-rating-read')]/@class").extract_first().split(" ")[2].split("-")[-1] 
            item['review_count'] = product.xpath("//div[@class='card']//span[@class='hidden-xs ']/text()").extract_first().split(" ")[0]
            item['color'] = None
            item['display_type'] = None
            item['display_resolution'] = None        
            item['display_size'] = None
            item['chipset'] = None
            item['chipset_model'] = None
            item['internal_memory'] = None
            item['ram'] = None
            item['main_camera'] = None
            item['selfie_camera'] = None
            item['os'] = None
            item['os_version'] = None
            item['nfc_indicator'] = None
            item['battery_type'] = None
            item['battery_capacity'] = None

            #item['review_count'] = item['review_count'].split(" ")[0]
            # import ipdb
            # ipdb.set_trace()
            yield item
   
    # def parse_product(self, response):
    #     #import ipdb
    #     #ipdb.set_trace()
    #     item = OnlineShopItem()
    #     item['name'] = response.xpath("//h1[@class='page-title']/text()").extract_first().strip()
    #     item['price'] = response.xpath("//p[@class='product-new-price']/text()").extract()[0].strip().replace(".", "") + "." + response.xpath("//p[@class='product-new-price']/sup/text()").extract()[0].strip()
    #     item['url'] = response.url
    #     item['review_score'] = response.xpath("//span[contains(@class, 'star-rating-text')]/text()").extract_first() or "0"  
    #     item['review_count'] = response.xpath("//p[@class='hidden-xs']/a[@href='#reviews-section']/text()").extract_first() or "0"
    #     item['review_count'] = item['review_count'].split(" ")[0]
    #     #import ipdb:
    #     #ipdb.set_trace()
    #     yield item
