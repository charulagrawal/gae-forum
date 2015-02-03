import urllib

from models import *

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# /<card_type>/<card_id>/votes
'''handles creation of upvote, its deletion 
	and fetches all the votes of a card'''
class Votes_Handler(webapp2.RequestHandler):

	def post(self):
		vote = Vote()
		vote.card=self.request.get('card', None)
		vote.author=self.request.get('author', None)
		vote.choices=self.request.get('choice', 'post')
		vote.vote_type = self.request.get('vote_type', 'upvote')
		vote.timestamp = time.now()

		q = Vote.query(card=vote.card, 
					author=vote.author).get()
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
					taskqueue.add(url='/notification', 
						params={'action': 'upvoted', 'type': vote.choices, 'card': vote})

		# if there is no vote on that card
		else:
			vote.put()
			card_entity = vote.card.get()

			if vote.vote_type == 'upvote':
				card_entity.increment_upvotes_counter()
				card_entity.put()
				taskqueue.add(url='/notification', 
						params={'action': 'upvoted', 'type': vote.choices, 'card': vote})


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
	def get(self, card_type, card_id):
		card_key = ndb.Key(card_type, card_id)
		votes = Up_Vote.query(card=card_key).fetch()
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
