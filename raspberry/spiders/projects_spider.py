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
        
        time.sleep(5)
        self.db = MySQLdb.connect("localhost","root","####","raspberry")
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
                head_forum = self.browser.find_elements_by_xpath('//h2')[0].text.encode('utf-8')
                total_count = self.browser.find_elements_by_xpath('//div[@class="paging span6 text-right"]')[0].text.encode('utf-8').split()
                total_count_len = len(total_count)
                n = total_count[total_count_len - 1]
                counter = 0
                for i in range(0,int(n)):
                    i+=1
                    url = link[0]+'&start='+str(counter)
                    # print url
                    # print "i="+str(i)
                    counter+=25
                    self.browser.get(url)
                    try:
                        item = ProjectsItem()
                        topic_list = self.browser.find_elements_by_xpath('//ul[@class="topiclist topics"]')
                        sub_topic_list = topic_list[1].find_elements_by_xpath('.//li') 
                        # print len(sub_topic_list)
                        # # print topic_list[0].text, topic_list[1].text
                        for i in range(0,len(sub_topic_list)):
                            topic_name = sub_topic_list[i].find_element_by_xpath('.//a[@class="topictitle"]').text.encode("utf-8")
                            topic_link = sub_topic_list[i].find_element_by_xpath('.//a[@class="topictitle"]').get_attribute('href')
                            topic_replies = sub_topic_list[i].find_elements_by_xpath('.//dd')[0].text.encode("utf-8")
                            topic_views = sub_topic_list[i].find_elements_by_xpath('.//dd')[1].text.encode("utf-8")
                            topic_author = sub_topic_list[i].find_elements_by_xpath('.//dd')[2].find_element_by_xpath('.//a').text
                            topic_author_link  = sub_topic_list[i].find_elements_by_xpath('.//dd')[2].find_element_by_xpath('.//a').get_attribute('href')
                            topic_lp_time = sub_topic_list[i].find_elements_by_xpath('.//dd')[3].find_element_by_xpath('.//time').text.encode("utf-8")
                            print "*****************************************************"
                            print head_forum+','+topic_name
                            
                            item['head_forum'] = head_forum
                            item['topic_name'] = topic_name
                            item['topic_link'] = topic_link
                            item['topic_replies'] = topic_replies
                            item['topic_views'] = topic_views
                            item['topic_author'] = topic_author
                            item['topic_author_link'] = topic_author_link
                            item['topic_lp_time'] = topic_lp_time
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