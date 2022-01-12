import scrapy
from selenium import webdriver
import time

class FooSpider(scrapy.Spider):
    name = 'foo'
    allow_domains = 'www.newegg.com'
    start_urls = ['https://www.newegg.com/LED-TV/SubCategory/ID-798?Tid=167585&Order=5']

    def __init__(self):
       # super(FooSpider, self).__init__(*args, **kwargs)
        self.download_delay = 0.25
        self.browser = webdriver.Chrome('C:\\Users\\kubix\\Documents\\GitHub\\srcap nlp\\chromedriver.exe')
        self.browser.implicitly_wait(60)

    def testing(self, response):
        #temp_browser = webdriver.Chrome('C:\\Users\\kubix\\Documents\\GitHub\\srcap nlp\\chromedriver.exe')
        #temp_browser.implicitly_wait(60)
        #temp_browser.get(response.url)
        #source = temp_browser.page_source # get source of the loaded page
        #sel = scrapy.Selector(text=source) # create a Selector object
        #for title in response.css('.product-title'):
        yield {'title': response.css('.product-title::text').get()}
        yield {'desc': response.css('#product-overview').get()}
        yield {'rating': response.css('.rating.is-large::attr(title)').get()}

    def parse(self, response):
        self.browser.get(response.url)  # load response to the browser
        for i in range(0,2):
            # the element to click to
            button = self.browser.find_element_by_css_selector('button[title="Next"]') # find 
            source = self.browser.page_source # get source of the loaded page
            sel = scrapy.Selector(text=source) # create a Selector object
            for title in sel.css('.item-title'):
                #yield {'title': title.css('::text').get()}
                if  title.css('::text').get() != "Yes":
                    yield response.follow(title, self.testing)
            button.click() # click
            time.sleep(1) # wait until the page is fully loaded
            