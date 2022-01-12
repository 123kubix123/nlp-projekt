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

    def get_product(self, response):
        self.browser.get(response.url)  # load response to the browser
        while 'Are you a human?' in self.browser.page_source:
            time.sleep(.3)
        #tabs = self.browser.find_elements_by_css_selector('div.tab-nav')
        #for tab in tabs:
        #    if 'Reviews' in tab.text:
        
        self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight);var tet = document.getElementsByClassName(\'tab-nav\');for (var i =0; i<tet.length;i++){if(tet[i].firstChild.textContent.includes(\'Reviews\')){tet[i].click();break;}}')
        #        time.sleep(.5)
        #        tab.click() # click
        while True:
            time.sleep(.3)
            if 'class="rating-views"' in self.browser.page_source or 'There are no' in self.browser.page_source:
                break
        
        source = self.browser.page_source # get source of the loaded page
        response = scrapy.http.TextResponse(url=self.browser.current_url, body=source, encoding='utf-8')
        
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
            desc_text = re.sub(r'<br>|<br\/>|<br \/>','\n', desc_text) 
            desc_text = re.sub(r'\s{2,}',' ', desc_text)
            desc_text = re.sub(r'<style>.*<\/style>',' ', desc_text)
            desc_text = re.sub(r'<.*?>',' ', desc_text)

        rating = response.css('.rating-views .rating-views-num::text').get()
        rating_raw = response.css('.rating-views .rating-views-num::text').get()
        if not rating:
            rating = ''
        else:
            rating = re.sub(r' out of 5 eggs','', rating)

        rating_count = response.css('.rating-views .rating-views-count::text').get()
        if not rating_count:
            rating_count = '0'
        else:
            rating_count = re.sub(r'customer ratings','', rating_count)
            rating_count = re.sub(r'\s','', rating_count)

        photos_count = response.css('#product-overview').get()
        if not photos_count:
            photos_count = '0'
        else:
            photos_count =str(photos_count.count('<img'))

        yield   {'title': response.css('.product-title::text').get(),
        'desc': response.css('#product-overview').get(),
        'desc_text': desc_text,
        'photos_count': photos_count,
        'rating': rating,
        'rating_raw': rating_raw,
        'rating_count': rating_count,
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
            for title in response.css('.item-img'):
                #yield {'title': title.css('::text').get()}
                #if  title.css('::text').get() != "Yes":
                products.append(title.css('::attr(href)').get())
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
        f = open("product_urls.json", "a")
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
        with open('categories.json') as json_file:
            data = json.load(json_file)
        
            # Print the type of data variable
            for i in range(0,9):
                yield response.follow(data[i]['href'], self.get_products)
                f = open("got.json", "a")
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
            