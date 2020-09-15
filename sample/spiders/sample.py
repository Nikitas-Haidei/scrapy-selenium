import scrapy
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time 
from scrapy_selenium import SeleniumRequest
from random import randint




class SampleSpider(scrapy.Spider):
    name = 'sample'
    allowed_domains = ['www.linkedin.com'] 
    start_urls = [
        'https://www.linkedin.com'
    ]

    def __init__(self):
        #chrome_options = Options()
        #chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path='./chromedriver.exe') #,options=chrome_options)
        driver.set_window_size(1000, 1000)
        driver.get("https://www.linkedin.com")

        driver.find_element_by_xpath("//a[@class='nav__button-secondary']").click()
        time.sleep(1)
        driver.find_element_by_xpath("//input[@id='username']").send_keys("login") # enter login
        driver.find_element_by_xpath("//input[@id='password']").send_keys("pass") # enter password
        driver.find_element_by_xpath("//button[@class='btn__primary--large from__button--floating']").click()
        time.sleep(2)
        driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections")
        time.sleep(2)

        #last_height = driver.execute_script("return document.body.scrollHeight")

        start = time.time()
        PERIOD_OF_TIME = 1 # seconds
 
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            up = driver.find_element_by_tag_name('html')
            up.send_keys(Keys.PAGE_UP)
            time.sleep(1)

            #new_height = driver.execute_script("return document.body.scrollHeight")
 
            if time.time() > start + PERIOD_OF_TIME:
                break
            #last_height = new_height

        self.html = driver.page_source
        self.cookies = driver.get_cookies()
        #driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        cookies = {}
        for cookie in self.cookies:
            cookies[cookie['name']] = cookie['value']

        
        
        main = resp.xpath("//li[@class='list-style-none']")
        for item in main:
            name = item.xpath("normalize-space(.//span[@class='mn-connection-card__name t-16 t-black t-bold']/text())").get()
            url = response.urljoin(item.xpath(".//a[@data-control-name='connection_profile']/@href").get())
            absolute_url = f"{url}"

            random_int = randint(5, 20) # random time from # to #
            wait = time.sleep(random_int)
            
            yield SeleniumRequest(
                cookies= cookies,
                url= absolute_url,                
                wait_time=wait,
                meta={'name': name,'url': url},
                callback=self.parse_item)
            print('Sleeping for {} seconds'.format(random_int))



    def parse_item(self, response):
        title = response.meta['name']
        links = response.meta['url']
        image_downloading = response.xpath("//div[@class='presence-entity pv-top-card__image presence-entity--size-9 ember-view']/img/@src").get()
        yield {
            'name': title,
            'link': links,
            'image_urls': [image_downloading],
            'image_links': image_downloading
            
        }

        

      
        



    
