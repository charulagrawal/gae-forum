''' handles creation of post, deletion 
	and displays all the comments in a thread '''
class Post_handler(webapp2.RequestHandler):

	def post(self):
		post = Post()
		post.title = self.request.get('title')
		post.content = self.request.get('content', None)
		post.put()

	def delete(self, title, author):
		post = Post.query(title = title, author=author).get()
		post.delete()

	def get(self):
		comments = Comment.query(post=self.get_argument).fetch()

		template_values = {
            'comments': comments,
        }

		template = JINJA_ENVIRONMENT.get_template('templates/comments.html')
		self.response.write(template.render({template_values}))
