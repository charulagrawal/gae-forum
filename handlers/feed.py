import urllib

from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# /users/<user_id>/feed
# diplay feed for a user
class Feed_Handler(webapp2.RequestHandler):
	def get(self):
		follows = Follow.query(user=user_id, choices='thread')
		thread_keys = []
		for follow in follows:
			thread_keys.append(follow.card)

		threads = get_multi_async(thread_keys)

		feed = []
		for thread in threads:
			feed.append(Post.query(thread=thread))

		