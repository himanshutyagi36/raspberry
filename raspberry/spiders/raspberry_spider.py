import scrapy
import MySQLdb
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from raspberry.items import RaspberryItem


class RaspberryForumsSpider(scrapy.Spider):
    name = "raspberry_main"
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
        # self.db = MySQLdb.connect("localhost","root","1590","raspberry")
        # self.cursor = self.db.cursor()
        # self.cursor.execute("SELECT project_data.project_id,project_link FROM project_data,project_old_links WHERE project_status LIKE '%COMPLETED%' AND project_data.project_id = project_old_links.project_id")
        # self.cursor.execute("SELECT project_data.project_id,project_link FROM project_data,project_link WHERE project_data.project_id = project_link.project_id AND project_status IN ('COMPLETED,','AWARDED,','IN PROGRESS,')")
        # self.cursor.execute("SELECT project_data.project_id,project_link FROM project_data,project_old_links WHERE project_data.project_id = project_old_links.project_id AND project_status IN ('COMPLETED,','AWARDED,','IN PROGRESS,')")

    def __exit__(self):
        print "------------Exiting----------"
        self.browser.quit()


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
            item = RaspberryItem()
            head_list = self.browser.find_elements_by_xpath('//h2')
            for i in range(0,len(head_list)):
                head_forum = head_list[i].text.encode("utf-8")
                head_forum_link = head_list[i].find_element_by_xpath('.//a').get_attribute('href')
                print head_forum
                sub_forum_list = self.browser.find_elements_by_xpath('//ul[@class="topiclist forums"]')
                forum_list = sub_forum_list[i].find_elements_by_xpath('.//li')
                for k in range(0,len(forum_list)):
                    forum_name = forum_list[k].find_element_by_xpath('.//a[@class="forumtitle"]').text.encode("utf-8")
                    forum_link = forum_list[k].find_element_by_xpath('.//a[@class="forumtitle"]').get_attribute('href').encode("utf-8")
                    forum_topics = forum_list[k].find_elements_by_xpath('.//dd')[0].text.encode("utf-8")
                    forum_posts = forum_list[k].find_elements_by_xpath('.//dd')[1].text.encode("utf-8")
                    forum_lp_user = forum_list[k].find_elements_by_xpath('.//dd')[2].find_element_by_xpath('.//a').text
                    forum_lp_user_link = forum_list[k].find_elements_by_xpath('.//dd')[2].find_element_by_xpath('.//a').get_attribute("href")
                    # print forum_name, forum_link, forum_topics, forum_posts, forum_lp_user, forum_lp_user_link
                    
                    key = head_forum+"_"+str(k)
                    item['key'] = key
                    item['head_forum'] = head_forum
                    item['head_forum_link'] = head_forum_link
                    item['forum_name'] = forum_name
                    item['forum_link'] = forum_link
                    item['forum_topics'] = forum_topics
                    item['forum_posts'] = forum_posts
                    item['forum_lp_user'] = forum_lp_user
                    item['forum_lp_user_link'] = forum_lp_user_link
                    yield item

        except NoSuchElementException:
            print "---------Element not found-----------"


        print "------------Exiting----------"
        self.browser.quit()




