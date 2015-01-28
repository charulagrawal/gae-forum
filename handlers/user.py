'''handles creation of user, its deletion 
	and fetches posts created by user'''
class User_Handler(webapp2.RequestHandler):

	def post(self):
		user = User()
		user.username = self.request.get('username', None)
		user.email = self.request.get('email', None)
		user.password = self.request.get('password', None)
		user.put()

	def delete(self, username, email):
		user = User.query(username = username, 
			email = email).get()
		user.delete()

	# fetch all the posts	 made by a user
	def get(self):
		action = self.request.get('action', None)
		if action == 'votes':
			self.votes()
		if action == 'notification':
			self.notification()

		posts = Post.query(author=self.get_argument).fetch()

		template_values = {
            'posts': posts,
        }

        template = JINJA_ENVIRONMENT.get_template('posts.html')
        self.response.write(template.render(template_values))

    def votes(self):
    	# queries all the posts voted by user
		upvotes= Vote.query(ndb.AND(user=some_key, 
			choices='Post', vote_type='upvote')).fetch()
		post_keys=[]
		for upvote in upvotes:
			post_keys.append(upvote.card)

		posts = ndb.get_multi_async(post_keys)

		template_values = {
            'posts': posts,
        }

        template = JINJA_ENVIRONMENT.get_template('posts.html')
        self.response.write(template.render(template_values))

    def notification(self):
    	notifications = Notification.query(recepient=some_key)
    						.order(-timestamp).fetch()
    	for notification in notifications:
    		user1 = notification.doer[-1].get()
            user2 = notification.doer[0].get()
    		size = len(notification.doer)
    		card = notification.card.get()
    		
    		if notification.action == 'upvoted' or notification.action == 'followed':
    			if size > 1:
    				self.response.write(user1+','+user2+' and '+size+' more people have '+notification.action+' your '
    					+notification.type+card.content)
    			else:
    				self.response.write(user+' has '+notification.action+' your '
    					+notification.type+card.content)
    		
    		elif notification.action == 'commented':
    			if size > 1:
    				self.response.write(user1+','+user2+' and '+size+' more people have '+notification.action+' on your '
    					+notification.type+card.content))
				else:
    				self.response.write(user+' has '+notification.action+' on your '
    					+notification.type+card.content)
			



    						


