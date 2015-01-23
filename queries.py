# queries written

# queries all the users
q = User.query()

# queries post created by a author
q = Post.query(author.id = some_id)

# queries post created by a author after a particular date
q = Post.query(ndb.AND(author.id = some_id, date > some_date))

# queries all the comments for a post
q = Comment.query(post.id = some_id)

# queries all the comments made by a particular user for a post
q = Comment.query(ndb.AND(post.id = id, author.id = some_id))

# queries all the post of a thread
q = Post.query(thread.id = id)



