# queries written

# queries all the users
q = User.query()


# queries post created by a author after a particular date
q = Post.query(ndb.AND(author.id = some_id, date > some_date))


# queries all the comments made by a particular user for a post
q = Comment.query(ndb.AND(post.id = id, author.id = some_id))




# list of common people followed by two users
q = Follow.query(ndb.AND(user = some_key, choices='User'))
q2 = Follow.query(user=key2, choices='User')
q = q.filter(Follow.card = )