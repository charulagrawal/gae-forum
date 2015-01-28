''' handles creation of thread, its deletion
	and displays all the posts in a thread '''
class Thread_handler(webapp2.RequestHandler):

	def post(self):  
		thread = Thread()
		thread.title = self.request.get('title')
		thread.tag = self.request.get('tag', None)
		thread.timestamp = time.now()
		thread.put()

	def delete(self, title):
		thread = Thread.query(title = title).get()
		thread.delete()

	def get(self):
		posts = Post.query(thread=self.get_argument).fetch()

		template_values = {
            'posts': posts,
        }

        template = JINJA_ENVIRONMENT.get_template('posts.html')
        self.response.write(template.render(template_values))
