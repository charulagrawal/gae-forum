from handlers import feed, comment, follower, post, thread, user, vote


routes = [
	webapp2.Route('/thread/<thread_id>', thread.Thread_Handler),
	webapp2.Route('/users', user.All_Users_Handler),
	webapp2.Route('/users/<user_id>', user.User_Handler),
	webapp2.Route('/users/<user_id>/feed', feed.Feed_Handler),
	webapp2.Route('/users/<user_id>/votes', user.User_Votes_Handler), 
	webapp2.Route('/users/<user_id>/notifications', user.User_Notifications_Handler)
	webapp2.Route('/posts/<post_id>', post.Post_Handler), 
	webapp2.Route('/<card_type>/<card_id>/followers', follower.Followers_Handler)
	webapp2.Route('/<card_type>/<card_id>/votes', vote.Votes_Handler)
	]