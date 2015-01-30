import urllib

from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

''' handles creation of post, deletion 
	and displays all the comments in a thread '''
class Post_handler(webapp2.RequestHandler):

	def post(self):
		post = Post()
		post.title = self.request.get('title', None)
		post.author = self.request.get('author', None)
		post.content = self.request.get('content', None)
		post.thread = self.request.get('thread', None)
		post.timestamp = time.now()
		post.upvotes = post.downvotes = 0
		post.put()

	def delete(self, title, author):
		post = Post.query(title = title, author=author).get()
		post.delete()

	def get(self):
		comments = Comment.query(post=self.get_argument).fetch()
		