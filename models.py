from google.appengine.ext import ndb


class User(ndb.Model):
	username = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)

class Thread(ndb.Model):
	title = ndb.StringProperty(required=True)
	# for now, each thread is associated with one tag
	tag = ndb.KeyProperty(kind=Tag)
	timestamp = ndb.KeyProperty(auto_now_add=True)

	# count for followers
	followers = ndb.IntegerProperty(0)

	def increment_counter(self):
		self.followers += 1

	def decrement.counter(self):
		self.followers -= 1

class Tag(ndb.Model):
	name = ndb.StringProperty(required=True)

class Post(ndb.Model):
	title = ndb.StringProperty(required=True)
	author = ndb.KeyProperty(kind=User)
	date = ndb.DateTimeProperty(auto_now_add=True)
	content = ndb.TextProperty(required=True)	
	thread = ndb.KeyProperty(kind=Thread)
	timestamp = ndb.KeyProperty(auto_now_add=True)

	# counter to store upvote count 
	upvotes = ndb.IntegerProperty(0)
	downvotes = ndb.IntegerProperty(0)
	
	def increment_counter(self):
		self.upvotes += 1

	def decrement_counter(self):
		self.downvotes += 1

	def total_votes(self):

		if upvotes > downvotes:
			return upvotes - downvotes

		else:
			return 0

class Comment(ndb.Model):
	post = ndb.KeyProperty(kind=Post)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
	content = ndb.TextProperty(required=True)
	author = ndb.KeyProperty(kind=User)

	# counter to store upvote count 
	upvotes = ndb.IntegerProperty(0)
	downvotes = ndb.IntegerProperty(0)
	
	def increment_counter(self):
		self.upvotes += 1

	def decrement_counter(self):
		self.downvotes += 1

	def total_votes(self):

		if upvotes > downvotes:
			return upvotes - downvotes

		else:
			return 0
	
class Follow(ndb.Model):
	user = ndb.KeyProperty(kind=User)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
	card = ndb.KeyProperty()

class Vote(ndb.Model):
	user = ndb.KeyProperty(kind=User)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
	card = ndb.KeyProperty()
