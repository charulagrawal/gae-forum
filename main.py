import os
import urllib

from models import *

import jinja2
import webapp2
import random
from google.appengine.ext.db import GqlQuery

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Followers_Handler(webapp2.RequestHandler):
	def get(self):
		action = self.request.get('action', None)
		u1 = self.request.get('u1', None)
		u2 = self.request.get('u2', None)
		if action == 'common':
			self.common(u1, u2)
		if action == 'create':
			self.create()
		if action == 'delete':
			self.delete()
		if action == 'show':
			self.show()

	def create(self):
		for i in range(30):
			follower = Followers()
			follower.x = random.randint(1, 30)
			follower.y = random.randint(1, 30)
			follower.put()
		self.response.write('created 30 entities')

	def delete(self):
		ndb.delete_multi(Followers.query().fetch(keys_only=True))

	'''@ndb.tasklet
	def get_users(user):
		q1 = yield Followers.query(Followers.x==user).fetch_async()
		list1 = [item.y for item in q1]
		raise ndb.Return(list1)
	'''
	def show(self):
		q1 = Followers.query().fetch_async()
		u1 = q1.get_result()
		self.response.write(u1)

	def common(self, u1, u2):
		u = int(u1)
		v = int(u2)
		q1 = Followers.query(Followers.x==u).fetch_async()	
		q2 = Followers.query(Followers.x==v).fetch_async()
		u1 = q1.get_result()
		u2 = q2.get_result()
		list1 = [item.y for item in u1]
		list2 = [item.y for item in u2]
		self.response.write("followers of user " + str(u) + " are " + str(list1))
		self.response.write("followers of user " + str(v) + " are " + str(list2))
		self.response.write("common followers of both users " + str(set(list1)& set(list2)))
		
		#output1 = get_users(u)
		#output2 = get_users(v)
		#self.response.write(list(set(output1)& set(output2)))


application = webapp2.WSGIApplication([
    ('/followers', Followers_Handler),
], debug=True)
