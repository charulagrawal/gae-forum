from google.appengine.ext import ndb


class User(ndb.Model):
	username = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)

class Thread(ndb.Model):
	title = ndb.StringProperty(required=True)
	# for now, each thread is associated with one tag
	tag = ndb.KeyProperty(kind=Tag)

class Tag(ndb.Model):
	name = ndb.StringProperty(required=True)

class Post(ndb.Model):
	title = ndb.StringProperty(required=True)
	author = ndb.KeyProperty(kind=User)
	date = ndb.DateTimeProperty(auto_now_add=True)
	content = ndb.TextProperty(required=True)
	upvotes = ndb.IntegerProperty()
	thread = ndb.KeyProperty(kind=Thread)

class Comment(ndb.Model):
	post = ndb.KeyProperty(kind=Post)
	date = ndb.DateTimeProperty(auto_now_add=True)
	content = ndb.TextProperty(required=True)
	author = ndb.KeyProperty(kind=User)
	