
''' create a follower, delete it
	and displays followers for a card'''
class Followers_Handler(webapp2.RequestHandler):

	def post(self):
		follow = Follow()
		follow.user = self.request.get('user')
		follow.choices = self.request.get('choices', 'User')
		follow.card = self.request.get('card', None)
		follow.timestamp = time.now()
		follow.put()

		if follow.choices == 'User':
			q1 = Notification.query(action='followed', card = comment.post)
			if q1 == None:
				# create notification object
				notification = Notification('followed', 'user', 
								follow.card, follow.user,
								follow.card, follow.timestamp)
				notification.put()
			else:
				size = len(q1.doer)
				if size == 2:
					q1.doer.pop(0)
				q1.doer.append(Follow.user)
				q1.timestamp = comment.timestamp
				q1.count += 1
				q1.put()

	def delete(self, user, card):
		follow = Follow.query(user=user, card=card).get()
		follow.delete()

	def get(self):
		followers = Follow.query(card=self.get_argument).fetch()
		user_keys = []
		for vote in votes:
			user_keys.append(followers.user)
		# get user entity from user key
		users = ndb.get_multi_async(user_keys)
		
		template_values = {
			'users' = users,
		}

		template = JINJA_ENVIRONMENT.get_template('templates/followers.html')
		self.response.write(template.render({template_values}))