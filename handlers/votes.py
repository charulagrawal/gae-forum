'''handles creation of upvote, its deletion 
	and fetches all the votes of a card'''
class Votes_Handler():

	def post(self):
		vote = Vote()
		vote.card=self.request.get('card', None)
		vote.user=self.request.get('user', None)
		vote.choices=self.request.get('choice', 'Post')
		vote.vote_type = self.request.get('vote_type', 'upvote')
		vote.timestamp = time.now()

		q = Vote.query(card=vote.card, 
					user=vote.user).get()
		# if there is already some vote on that card
		if q != None:
			# user wants to again do the same vote
			if vote.vote_type == q.vote_type:
				return "you are not allowed to " + q.vote_type + ' again'
			else:
				# upvote to downvote
				if vote.vote_type == 'downvote':
					q.vote_type = vote.vote_type
					ent = q.get()
					ent.decrement_upvotes_counter()
					ent.increment_downvotes_counter()
					ent.put()
				else:
					# downvotes to upvote
					q.vote_type = vote.vote_type
					ent = q.get()
					ent.decrement_downvotes_counter()
					ent.increment_upvotes_counter()
					ent.put()
					# notify when changed from downvote to upvote
					q1 = Notification.query(action='upvoted', card = vote.card)
					# check if there is already a notification for this activity
					if q1 == None:
						notification = Notification('upvoted', vote.choices, 
								vote.card, vote.user,
								ent.author, vote.timestamp)
						notification.put()
					else:
						# limiting the size of doer list to 2
						size = len(q1.doer)
						if size == 2:
							q1.doer.pop(0)
						q1.doer.append(vote.user)
						q1.count += 1
						q1.timestamp = vote.timestamp
						q1.put()

		# if there is no vote on that card
		else:
			vote.put()
			card_entity = vote.card.get()

			if vote.vote_type == 'upvote':
				card_entity.increment_upvotes_counter()
				card_entity.put()
				# check if the upvote activity is already done on that card
				q1 = Notification.query(action='upvoted', card = vote.card)
				if q1 == None:
					notification = Notification('upvote', vote.choices, 
								vote.card, vote.user,
								card_entity.author, vote.timestamp)
					notification.put()
				else:
						size = len(q1.doer)
						if size == 2:
							q1.doer.pop(0)
						q1.doer.append(vote.user)
						q1.count += 1
						q1.timestamp = vote.timestamp
						q1.put()

			elif vote.vote_type == 'downvote':
				card_entity.increment_downvotes_counter()
				card_entity.put()


	def delete(self):
		vote = Vote.query(card=self.get_argument, 
					user=self.get_argument).get()
		if vote.vote_type == 'upvote':
			card_entity = vote.card.get()
			card_entity.decrement_upvotes_counter()

		elif vote.vote_type == 'downvote':
			card_entity = vote.card.get()
			card_entity.decrement_downvotes_counter()
		vote.delete()

	# fetch all the votes of a card
	def get(self):
		votes = Up_Vote.query(card=self.get_argument).fetch()
		user_keys = []
		for vote in votes:
			user_keys.append(vote.user)
		# get user entity from user key
		users = ndb.get_multi_async(user_keys)
		template_values = {
            'users': users,
        }

        template = JINJA_ENVIRONMENT.get_template('users.html')
        self.response.write(template.render(template_values))
