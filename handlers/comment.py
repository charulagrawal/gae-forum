import os
import urllib

from google.appengine.api import taskqueue
from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

''' handles creation of a comment and its deletion'''
class Comment_Handler(webapp2.RequestHandler):
	def post(self):
		# create comment object
		comment = Comment()
		comment.author = self.request.get('author', None)
		comment.timestamp = time.now()
		comment.card = self.request.get('card', None)
		comment.content = self.request.get('content', None)	
		comment.upvotes = comment.downvotes = 0
		comment.put()

		taskqueue.add(url='/notification', 
			params={'action': 'commented', 'type': 'post', 'card': comment})


	def delete(self):
		comment = Comment.query(card=self.get_argument, 
					author=self.get_argument).fetch()
		comment.delete()

