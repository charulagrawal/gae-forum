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

		q1 = Notification.query(action='commented', card = comment.post)
		if q1 == None:
			post = comment.post.get()
			# create notification object
			notification = Notification('commented', 'post', comment.post, 
							comment.author, post.author, comment.timestamp)
			notification.put()
		else:
			size = len(q1.doer)
			if size == 2:
				q1.doer.pop(0)
			q1.doer.append(comment.author)
			q1.timestamp = comment.timestamp
			q1.count += 1
			q1.put()

	def delete(self):
		comment = Comment.query(post=self.get_argument, 
					author=self.get_argument).fetch()
		comment.delete()

