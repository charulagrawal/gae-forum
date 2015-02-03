
import urllib

from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# /<card_type>/<card_id>/followers
''' create a follower, delete it
	and displays followers for a card'''
class Followers_Handler(webapp2.RequestHandler):

	def post(self):
		follow = Follow()
		follow.author = self.request.get('author')
		follow.timestamp = time.now()	
		follow.card = self.request.get('card', None)
		follow.choices = self.request.get('choices', 'user')	
		follow.put()

		if follow.choices == 'user':
			taskqueue.add(url='/notification', 
			params={'action': 'followed', 'type': 'user', 'card': follow})
			
	def delete(self, user, card):
		follow = Follow.query(user=user, card=card).get()
		follow.delete()

	def get(self, card_type, card_id):
		card_key = ndb.Key(card_type, card_id)
		followers = Follow.query(card=card_key).fetch()
		user_keys = []
		for follower in followers:
			user_keys.append(follower.author)
		# get user entity from user key
		users = ndb.get_multi_async(user_keys)
		