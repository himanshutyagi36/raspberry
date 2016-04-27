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
from raspberry.items import ProjectsItem
from raspberry.items import PostItem

class RaspberryPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(user='root', passwd='1590', host='localhost', db='raspberry')
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		if (spider.name == "raspberry_main"):
			try:
				
				self.cursor.execute("REPLACE INTO `frontPage` (`key`, `head_forum`, `head_forum_link`,`forum_name`, `forum_link`, `forum_topics`, `forum_posts`,"
					" `forum_lp_user`, `forum_lp_user_link`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
				(item['key'], item['head_forum'],item['head_forum_link'], item['forum_name'], item['forum_link'], item['forum_topics'], item['forum_posts'], item['forum_lp_user'],
				item['forum_lp_user_link']))


				#self.cursor.execute("INSERT INTO `raspberry`.`frontPage` ('key', 'head_forum', 'forum_name') VALUES (%s, %s, %s)",(item['key'], item['head_forum'], item['forum_name']))
				self.conn.commit()

			except MySQLdb.Error, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					pass
		elif (spider.name == "projects"):
			try:
				self.cursor.execute("REPLACE INTO `projects` (`head_forum`,`topic_name`, `topic_link`, `topic_replies`, `topic_views`, `topic_author`,"
					" `topic_author_link`, `topic_lp_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (item['topic_name'], item['head_forum'],
					item['topic_link'], item['topic_replies'], item['topic_views'], item['topic_author'], item['topic_author_link'], 
					item['topic_lp_time']))
				self.conn.commit()
				
			except MySQLdb.Error, e:
				print "Error %d: %s" % (e.args[0], e.args[1])
				pass
		elif (spider.name == "post"):
			try:
				self.cursor.execute("REPLACE INTO `posts` (`post_head`, `post_author`, `post_author_link`, `post_time`, `post_content`, `author_postCount`,"
					" `author_joinDate`) VALUES (%s, %s, %s, %s, %s, %s, %s)", (item['post_head'], item['post_author'], item['post_author_link'], 
					item['post_time'], item['post_content'], item['author_postCount'], item['author_joinDate']))
				self.conn.commit()
				
			except MySQLdb.Error, e:
				print "Error %d: %s" % (e.args[0], e.args[1])
				pass

