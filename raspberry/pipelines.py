# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

from raspberry.items import RaspberryItem
class RaspberryPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(user='root', passwd='1590', host='localhost', db='raspberry')
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if (spider.name == "raspberry_main"):
			try:
				
				self.cursor.execute("REPLACE INTO `frontPage` (`key`, `head_forum`, `forum_name`, `forum_link`, `forum_topics`, `forum_posts`,"
					" `forum_lp_user`, `forum_lp_user_link`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
				(item['key'], item['head_forum'], item['forum_name'], item['forum_link'], item['forum_topics'], item['forum_posts'], item['forum_lp_user'],
				item['forum_lp_user_link']))


				#self.cursor.execute("INSERT INTO `raspberry`.`frontPage` ('key', 'head_forum', 'forum_name') VALUES (%s, %s, %s)",(item['key'], item['head_forum'], item['forum_name']))
				self.conn.commit()

			except MySQLdb.Error, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					pass

