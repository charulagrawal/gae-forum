import os
import urllib

from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

''' handles creation of a comment and its deletion'''
class Comment_Handler(self):
	def post(self):
		# create comment object
		comment = Comment()
		comment.post = self.request.get('post', None)
		comment.timestamp = time.now()
		comment.content = self.request.get('content', None)
		comment.author = self.request.get('author', None)
		comment.put()

		# create notification object
		notification = Notification()
		notification.action = 'commented'
		notification.type = 'post'
		notification.card = comment.post
		notification.doer = comment.author
		post = comment.post.get()
		notification.recepient = post.author
		notification.timestamp = comment.timestamp
		notification.put()



	def delete(self):
		comment = Comment.query(post=self.get_argument, 
					author=self.get_argument).fetch()
		comment.delete()

