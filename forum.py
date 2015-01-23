import os
import urllib

from models import User, Forum, Post

import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		
		template = JINJA_ENVIRONMENT.get_template('templates/home.html')
		self.response.write(template.render({}))
      

class Register(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/register.html')
		self.response.write(template.render({}))

	def post(self):  
		user = User()
		user.username = self.request.get('username')
		user.email = self.request.get('email')
		user.password = self.request.get('password')
		user.put()

		template_values = {
			'user': user
		}
		template = JINJA_ENVIRONMENT.get_template('templates/user.html')
		self.response.write(template.render(template_values))

		
class Forum(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/create_forum.html')
		self.response.write(template.render({}))

	def post(self):  
		forum = Forum()
		forum.title = self.request.get('title')
		forum.posts = []
		forum.put()

		template_values = {
			'forum': forum
		}
		template = JINJA_ENVIRONMENT.get_template('templates/forum.html')
		self.response.write(template.render(template_values))


class Post(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('templates/create_post.html')
		self.response.write(template.render({}))

	def post(self):
		post = Post()
		post.title = self.request.get('title')
		post.content = self.request.get('content')
		post.put()

application = webapp2.WSGIApplication([
   	('/', MainPage),
   	('/register', Register),
   	('/forum', Forum),
   	('/post', Post)
], debug=True)