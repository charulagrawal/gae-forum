import urllib

from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

''' handles creation of thread, its deletion
	and displays all the posts in a thread '''
class Thread_handler(webapp2.RequestHandler):

	def post(self):  
		thread = Thread()
		thread.title = self.request.get('title')
		thread.tag = self.request.get('tag', None)
		thread.timestamp = time.now()
		thread.followers = 0
		thread.put()

	def delete(self, title):
		thread = Thread.query(title = title).get()
		thread.delete()

	def get(self):
		posts = Post.query(thread=self.get_argument).fetch()
		