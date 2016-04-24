import scrapy
import MySQLdb
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from raspberry.items import PostItem


class PostSpider(scrapy.Spider):
    name = "post"
    allowed_domains = ["raspberrypi.org"]
    start_urls = [
        "https://www.raspberrypi.org/forums/"
    ]

    def __init__(self, *args, **kwargs):
        # print "3"
        ## Initiate firefox
        self.browser=webdriver.Firefox()
        ## Open the forums link
        self.browser.get('https://www.raspberrypi.org/forums/')
        ## Get the login button path. Find element with title "Login", encode it to utf-8 and then click on the same to go to login page.
        login_path = self.browser.find_element_by_xpath('//a[@title="Login"]')
        # login_path.get_attribute('href').encode("utf-8")
        login_path.click()
        
        ## Get the username input field and populate it with the username.
        username_id = self.browser.find_element_by_xpath('//input[@id="username"]')
        username_id.send_keys("####")

        password_id = self.browser.find_element_by_xpath('//input[@id="password"]')
        password_id.send_keys("####")

        login_button = self.browser.find_element_by_xpath('//input[@name="login"]')
        login_button.click()
        time.sleep(5)
        self.db = MySQLdb.connect("localhost","root","####","raspberry")
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT projects.topic_link FROM projects")
        
    def __exit__(self):
        print "------------Exiting----------"
        self.browser.quit()
        self.cursor.close()
        del self.cursor
        self.db.close()


    def parse(self, response):
        
        try:
            item = PostItem()
            for link in self.cursor.fetchall():
                self.browser.get(link)
                try:
                    
                    postbody = self.browser.find_elements_by_xpath('//div[@class="postbody span9"]')
                    for i in range(0,len(postbody)):
                        post_author = postbody[i].find_element_by_xpath('.//a').text.encode('utf-8')
                        post_author_link = postbody[i].find_element_by_xpath('.//a').get_attribute('href').encode('utf-8')
                        post_time = postbody[i].find_element_by_xpath('.//div[@class="author"]').text.encode('utf-8').split('\xbb')[1]
                        post_content = postbody[i].find_element_by_xpath('.//div[@class="content"]').text.encode('utf-8')
                        author_postCount = self.browser.find_elements_by_xpath('.//dl[@class="postprofile span3"]')[i].find_elements_by_xpath('.//dd')[0].text.encode('utf-8')
                        author_joinDate = self.browser.find_elements_by_xpath('.//dl[@class="postprofile span3"]')[i].find_elements_by_xpath('.//dd')[1].text.encode('utf-8')
                        
                        item['post_author'] = post_author
                        item['post_author_link'] = post_author_link
                        item['post_time'] = post_time
                        item['post_content'] = post_content
                        item['author_postCount'] = author_postCount
                        item['author_joinDate'] = author_joinDate
                        yield item

                except NoSuchElementException:
                    print "---------Element not found-----------"


        except NoSuchElementException:
            print "---------Element not found-----------"


        print "------------Exiting----------"
        self.browser.quit()
        self.cursor.close()
        del self.cursor
        self.db.close()