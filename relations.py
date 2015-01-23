class Commentable(object):

	def after_adding_comment(self):
		# implement

	def after_deleting_comment(self):
		# implement

	def after_editing_comment(self, comment_key, content):
			comment = comment_key.get()

			comment.content = content
			comment.put()

class Upvotable(object):

	def after_upvoting_card(self, card_key):
		card = card_key.get()

		card.increment_counter()

	def after_downvote_card(self, card_key):
		card = card_key.get()

		card.decrement_counter()

class Followable(object):

	def after_following_card(self, card_key):
		card = card_key.get()

		card.increment_counter()
	
	def after_unfollowing_card(self, card_key):
		card = card_key.get()

		card.decrement_counter()

		



