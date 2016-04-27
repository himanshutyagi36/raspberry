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
            # for link in self.cursor.fetchall():
            self.browser.get('https://www.raspberrypi.org/forums/viewtopic.php?f=37&t=145727')
            counter = 5
            try:
                ## following if checks if requested topic exists
                if self.browser.find_elements_by_xpath('//h2'):
                    post_head = self.browser.find_elements_by_xpath('//h2')[0].text.encode('utf-8')
                    print post_head
                    
                
                    postbody = self.browser.find_elements_by_xpath('//div[@class="postbody span9"]')
                    # print len(postbody)
                    for i in range(0,len(postbody)):
                        post_author = postbody[i].find_element_by_xpath('.//div[@class="author"]').find_element_by_xpath('.//a').text.encode('utf-8')
                        post_author_link = postbody[i].find_element_by_xpath('.//div[@class="author"]').find_element_by_xpath('.//a').get_attribute('href')
                        post_time = postbody[i].find_element_by_xpath('.//div[@class="author"]').text.encode('utf-8').split('\xbb')[1]
                        post_content = postbody[i].find_element_by_xpath('.//div[@class="content"]').text.encode('utf-8')
                        test_str = self.browser.find_elements_by_xpath('.//dl[@class="postprofile span3"]')[i].find_elements_by_xpath('.//dd')[0].text.encode('utf-8')
                        test_str2 = self.browser.find_elements_by_xpath('.//dl[@class="postprofile span3"]')[i].find_elements_by_xpath('.//dd')[1].text.encode('utf-8')
                        
                        ## If the post is by the forum moderator
                        if 'Forum Moderator' in test_str or 'Raspberry Pi Certified Educator' in test_str:
                            temp_str = self.browser.find_elements_by_xpath('.//dl[@class="postprofile span3"]')[i].find_elements_by_xpath('.//dd')[1].text.encode('utf-8')
                            temp_str2 = self.browser.find_elements_by_xpath('.//dl[@class="postprofile span3"]')[i].find_elements_by_xpath('.//dd')[2].text.encode('utf-8')
                        else:
                            temp_str = test_str
                            temp_str2 = test_str2
                        # print temp_str+','+temp_str2
                        l = temp_str.split(': ')
                        author_postCount = l[1]
                        l2 = temp_str2.split(': ')
                        author_joinDate = l2[1]
                        
                        print post_head+','+post_author

                        item['post_head'] = post_head
                        item['post_author'] = post_author
                        item['post_author_link'] = post_author_link
                        item['post_time'] = post_time
                        item['post_content'] = post_content
                        item['author_postCount'] = author_postCount
                        item['author_joinDate'] = author_joinDate
                        yield item
                        # counter-=1
                else:
                    print "This topic doesn't exist."
                    # continue

            except NoSuchElementException:
                print "---------Element not found-----------"


        except NoSuchElementException:
            print "---------Element not found-----------"


        print "------------Exiting----------"
        self.browser.quit()
        self.cursor.close()
        del self.cursor
        self.db.close()