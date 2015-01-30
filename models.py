from google.appengine.ext import ndb

class User(ndb.Model):
	username = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)


class Tag(ndb.Model):
	name = ndb.StringProperty(required=True)


class Thread(ndb.Model):
	title = ndb.StringProperty(required=True)
	# for now, each thread is associated with one tag
	tag = ndb.KeyProperty(kind=Tag)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

	# count for followers
	followers = ndb.IntegerProperty()

	def increment_counter(self):
		self.followers += 1

	def decrement_counter(self):
		self.followers -= 1


class Post(ndb.Model):
	title = ndb.StringProperty(required=True)
	author = ndb.KeyProperty(kind=User)
	content = ndb.TextProperty(required=True)	
	thread = ndb.KeyProperty(kind=Thread)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

	# counter to store upvote count 
	upvotes = ndb.IntegerProperty()
	downvotes = ndb.IntegerProperty()
	
	def increment_upvotes_counter(self):
		self.upvotes += 1

	def decrement_upvotes_counter(self):
		self.upvotes -= 1

	def increment_downvotes_counter(self):
		self.upvotes += 1

	def decrement_downvotes_counter(self):
		self.downvotes -= 1

	def total_score(self):
		if upvotes > downvotes:
			return upvotes - downvotes

		else:
			return 0

	def total_votes(self):
		return upvotes + downvotes


class Comment(ndb.Model):
	post = ndb.KeyProperty(kind=Post)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
	content = ndb.TextProperty(required=True)
	author = ndb.KeyProperty(kind=User)

	# counter to store upvote count 
	upvotes = ndb.IntegerProperty()
	downvotes = ndb.IntegerProperty()
	
	def increment_upvotes_counter(self):
		self.upvotes += 1
		
	def decrement_upvotes_counter(self):
		self.upvotes -= 1

	def increment_downvotes_counter(self):
		self.upvotes += 1

	def decrement_downvotes_counter(self):
		self.downvotes -= 1

	def total_votes(self):
		if upvotes > downvotes:
			return upvotes - downvotes

		else:
			return 0
	

class Follow(ndb.Model):
	user = ndb.KeyProperty(kind=User)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
	choices = ndb.StringProperty(choices=['user', 'thread'])
	card = ndb.KeyProperty()


class Vote(ndb.Model): 
	user = ndb.KeyProperty(kind=User)
	timestamp = ndb.DateTimeProperty(auto_now_add=True)
	vote_type =  ndb.StringProperty(choices=['upvote', 'downvote'])
	choices = ndb.StringProperty(choices=['Post', 'Comment'])
	card = ndb.KeyProperty()


class Notification(ndb.Model):
	''' action can be upvote, comment, follow '''
	action = ndb.StringProperty(choices=['upvoted', 'commented', 'followed'])
	''' type can be upvote -> comment or post,
		comment -> post, follow -> user '''
	type = ndb.StringProperty(choices=['comment', 'post', 'user'])
	card = ndb.KeyProperty()
	doer = ndb.KeyProperty(kind=User, repeated=True)
	count = ndb.IntegerProperty()
	recepient = ndb.KeyProperty(kind=User)
	timestamp = ndb.DateTimeProperty()
