import scrapy
import MySQLdb
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from raspberry.items import ProjectsItem


class ProjectsSpider(scrapy.Spider):
    name = "projects"
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
        username_id.send_keys("tortuga90")

        password_id = self.browser.find_element_by_xpath('//input[@id="password"]')
        password_id.send_keys("Admin098")

        login_button = self.browser.find_element_by_xpath('//input[@name="login"]')
        login_button.click()
        time.sleep(5)
        self.db = MySQLdb.connect("localhost","root","1590","raspberry")
        self.cursor = self.db.cursor()
        self.cursor.execute("SELECT frontPage.forum_link FROM frontPage WHERE head_forum='Projects'")
        
    def __exit__(self):
        print "------------Exiting----------"
        self.browser.quit()
        self.cursor.close()
        del self.cursor
        self.db.close()


    def parse(self, response):
        # print "1"
        # try:
        #     run_test = WebDriverWait(self.browser, 15).until(EC.presence_of_element_located((By.XPATH, '//h2')))
        #     except NoSuchElementException:
        #         print "---------------------------Element Not Found ----------------------- "
        #         continue;
        #     except TimeoutException:
        #         timeout_counter = timeout_counter+1
        #         if timeout_counter>5:
        #             print "Link = " + link[1]
        #             print "counter : " + str(c)
        #             break
        #         continue;
        #     except:
        #         print "counter : " + str(c)
        #         break;
        #     c = c+1
        #     print "counter : " + str(c)

        try:
            item = ProjectsItem()
            for link in self.cursor.fetchall():
                self.browser.get(link)
                try:
                    item = ProjectsItem()
                    topic_list = self.browser.find_elements_by_xpath('//ul[@class="topiclist topics"]') 
                    for i in range(0,len(topic_list)):
                        topic_name = topic_list[i].find_element_by_xpath('.//a[@class="topictitle"]').text.encode("utf-8")
                        topic_link = topic_list[i].find_element_by_xpath('.//a[@class="topictitle"]').get_attribute('href')
                        topic_replies = topic_list[i].find_elements_by_xpath('.//dd')[0].text.encode("utf-8")
                        topic_views = topic_list[i].find_elements_by_xpath('.//dd')[1].text.encode("utf-8")
                        topic_author = topic_list[i].find_elements_by_xpath('.//dd')[2].find_element_by_xpath('.//a').text
                        topic_author_link  = topic_list[i].find_elements_by_xpath('.//dd')[2].find_element_by_xpath('.//a').get_attribute('href')
                        print "*****************************************************"
                        print topic_name, topic_author
                        print "*****************************************************"
                        item['topic_name'] = topic_name
                        item['topic_link'] = topic_link
                        item['topic_replies'] = topic_replies
                        item['topic_views'] = topic_views
                        item['topic_author'] = topic_author
                        item['topic_author_link'] = topic_author_link
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