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

class Notification_Handler(webapp2.RequestHandler):
	def post(self):
		action = self.request.get('action')
		card = self.request.get('card')
		type = self.request.get('type')
		card_key = card.key()

		q1 = Notification.query(action=action, card = card_key)

		if q1 == None:
			if action=='commented':
				post = card.card.get()
				recepient = post.author
			if action=='followed':
				recepient = card.card
			# create notification object
			notification = Notification(action, type, card.card, 
							card.author, 0, recepient, card.timestamp)
			notification.put()
		else:
			size = len(q1.doer)
			if size == 2:
				q1.doer.pop(0)
			q1.doer.append(card.author)
			q1.timestamp = card.timestamp
			q1.count += 1
			q1.put()
