import scrapy
from selenium import webdriver
import time
import re
import json

class FooSpider(scrapy.Spider):
    name = 'foo'
    allow_domains = 'www.newegg.com'
    #&Order=5 sort by most reviews
    start_urls = ['https://www.newegg.com/Electronics/Store/ID-10']
    #start_urls = ['https://www.newegg.com/presto-electric-tilt-n-fold-griddle-19-black-07073/p/238-007S-00001']
    
    def __init__(self):
       # super(FooSpider, self).__init__(*args, **kwargs)
        self.download_delay = 0.25
        self.browser = webdriver.Chrome('C:\\Users\\kubix\\Documents\\GitHub\\srcap nlp\\chromedriver.exe')
        self.browser.implicitly_wait(60)
        
    def use_browser(self, response):
        self.browser.get(response.url)  # load response to the browser
        while 'Are you a human?' in self.browser.page_source:
            time.sleep(.3)
        source = self.browser.page_source # get source of the loaded page
        return scrapy.http.TextResponse(url=self.browser.current_url, body=source, encoding='utf-8')

    def get_product(self, response, it):
        #self.browser.get(response.url)  # load response to the browser
        #while 'Are you a human?' in self.browser.page_source:
        #    time.sleep(.3)
        #tabs = self.browser.find_elements_by_css_selector('div.tab-nav')
        #for tab in tabs:
        #    if 'Reviews' in tab.text:
        
        #self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight);var tet = document.getElementsByClassName(\'tab-nav\');for (var i =0; i<tet.length;i++){if(tet[i].firstChild.textContent.includes(\'Reviews\')){tet[i].click();break;}}')
        #        time.sleep(.5)
        #        tab.click() # click
        #while True:
        #    time.sleep(.3)
        #    if 'class="rating-views"' in self.browser.page_source or 'There are no' in self.browser.page_source:
        #        break
        
        #source = self.browser.page_source # get source of the loaded page
        #response = scrapy.http.TextResponse(url=self.browser.current_url, body=source, encoding='utf-8')
        
        #temp_browser = webdriver.Chrome('C:\\Users\\kubix\\Documents\\GitHub\\srcap nlp\\chromedriver.exe')
        #temp_browser.implicitly_wait(60)
        #temp_browser.get(response.url)
        #source = temp_browser.page_source # get source of the loaded page
        #sel = scrapy.Selector(text=source) # create a Selector object
        #for title in response.css('.product-title'):

        desc_text =  response.css('#product-overview').get()
        if not desc_text:
            desc_text = ''
        else:
            desc_text = re.sub(re.compile('<style.*?/ *?style>', re.DOTALL),'', desc_text)
            desc_text = re.sub(re.compile('< *?script(?:.*?)< *?/ *?script>', re.DOTALL),'', desc_text)
            desc_text = re.sub(r'<br>|<br\/>|<br \/>','\r\n', desc_text)
            desc_text = re.sub(r'<.*?>',' ', desc_text)
            desc_text = re.sub(r'\\t','', desc_text)
            desc_text = re.sub(r'\t','', desc_text)
            desc_text = re.sub(r'(?: *\\n){2,}',' \r\n', desc_text)
            desc_text = re.sub(r'(?: *\n){2,}',' \r\n', desc_text)            
            desc_text = re.sub(r'(?: *\r\n){2,}',' \r\n', desc_text)
            desc_text = re.sub(r'(?: *\\r\\n){2,}',' \r\n', desc_text)
            desc_text = re.sub(r' {2,}',' ', desc_text)

        photos_count = response.css('#product-overview').get()
        if not photos_count:
            photos_count = '0'
        else:
            photos_count =str(photos_count.count('<img'))

        it['desc'] = response.css('#product-overview').get()
        it['desc_text'] = desc_text
        it['photos_count'] = photos_count

        f = open("products_full.json", "a")
        json.dump(it, f)
        f.write('\n')
        f.close()

        yield   {'title': response.css('.product-title::text').get(),
        'desc': response.css('#product-overview').get(),
        'desc_text': desc_text,
        'photos_count': photos_count,
        'url': response.url,
        }

    def get_products(self, response):
        self.browser.get(response.url+'&Order=5')  # load response to the browser
        while 'Are you a human?' in self.browser.page_source:
            time.sleep(.3)
        response = scrapy.http.TextResponse(url=self.browser.current_url, body=self.browser.page_source, encoding='utf-8')
        time.sleep(1)
        products = []
        for i in range(0,100):
            # the element to click to
            if 'onetrust-close-btn-handler onetrust-close-btn-ui banner-close-button onetrust-lg ot-close-icon' in self.browser.page_source:
                cookies = self.browser.find_element_by_css_selector('.onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.onetrust-lg.ot-close-icon')
                cookies.click()
            button = False
            if 'title="Next"' in self.browser.page_source:
                button = self.browser.find_element_by_css_selector('button[title="Next"]') # find 
            #source = self.browser.page_source # get source of the loaded page
            #sel = scrapy.Selector(text=source) # create a Selector object
            for title in response.css('.item-container'):
                #yield {'title': title.css('::text').get()}
                #if  title.css('::text').get() != "Yes":
                rating = title.css('.rating::attr(aria-label)').get()
                if rating:
                    product = {'title': title.css('.item-title::text').get(), 'rating': rating,'rating_count':title.css('.item-rating-num::text').get(),'url': title.css('.item-img::attr(href)').get()}
                    products.append(product)
                #yield { 'href': title.css('::attr(href)').get()}
                    #yield response.follow(title, self.get_product)
            if 'title="Next" disabled' in self.browser.page_source:
                break
            if button != False:
                #self.browser.execute_script('arguments[0].scrollIntoView();',button)
                button = self.browser.find_element_by_css_selector('button[title="Next"]')
                button.click() # click
                time.sleep(2) # wait until the page is fully loaded
            else:
                break
        f = open("products_partial_deduped.json", "a")
        json.dump(products, f)
        f.write('\n')
        f.close()

    def get_subcategory(self, response):
        #response = self.use_browser(response)
        subcategories = response.css('a.filter-box-label')
        if(len(subcategories) > 0):
            for category in subcategories:
                if category.css('a.filter-box-label::attr(href)').get() != '':
                    yield {'subcategory': category.css('a.filter-box-label::attr(title)').get(), 'href' : category.css('a.filter-box-label::attr(href)').get()}
                    yield response.follow(category, self.get_subcategory)
        else:
            yield self.get_products(response)

    def parse(self, response):
        with open('products_partial_deduped.json') as json_file:
            data = json.load(json_file)
        
            # Print the type of data variable
            for i in range(0,len(data)):
                yield response.follow(data[i]['url'], callback=lambda response, it=data[i]: self.get_product(response, it))
                f = open("filled.json", "a")
                json.dump(data[i], f)
                f.write('\n')
                f.close()
        #response = self.use_browser(response)
        #yield response.follow(response.url, self.get_product)
        #yield {'fin': response.css('.is-current::text').get()}
        #for category in response.css('a.filter-box-label'):
        #    yield {'category': category.css('a.filter-box-label::attr(title)').get()}
        #    yield response.follow(category, self.get_subcategory)

    def test(self, response):
        self.browser.get(response.url)  # load response to the browser
        for i in range(0,9):
            # the element to click to
            button = self.browser.find_element_by_css_selector('button[title="Next"]') # find 
            source = self.browser.page_source # get source of the loaded page
            sel = scrapy.Selector(text=source) # create a Selector object
            for title in sel.css('.item-title'):
                #yield {'title': title.css('::text').get()}
                if  title.css('::text').get() != "Yes":
                    yield response.follow(title, self.get_product)
            button.click() # click
            time.sleep(1) # wait until the page is fully loaded
            