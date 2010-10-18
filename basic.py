"""
Basic HTTP Handler
"""

from google.appengine.api import users
from google.appengine.ext import webapp

from model import Minefield

class Handler(webapp.RequestHandler):
	"""
	Basic ASCII game page for initial testing.
	"""
	def get(self):
		"""
		Processes events, renders minefield. Redirects for login, when necessary.
		"""
		user = users.get_current_user()
		
		if(user):
			m = Minefield.gql("WHERE author = :1", user).get()
			if not(m):
				m = Minefield(
					author = user,
				)
			
			# place any requested mines
			for point in self.request.get_all('mine'):
				x,y = [int(x) for x in point.split(',')]
				m.mine(x, y)
			
			# reveal any requested coordinates
			#  support multiple args for testing
			for point in self.request.get_all('reveal'):
				x,y = [int(x) for x in point.split(',')]
				m.reveal(x, y)
				if(m.getState(x,y) == -1):
					m.finished = True
			
			# hide any requested coordinates
			#  support multiple args for testing
			for point in self.request.get_all('hide'):
				x,y = [int(x) for x in point.split(',')]
				m.hide(x, y)
			
			# toggle 'finished' flag
			finish_req = self.request.get('finished')
			if(finish_req):
				m.finished = bool(int(finish_req))
			
			m.put()
			
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Hello, %s\n' % user.nickname())
			
			sep = ''.join(['='] * m.width) + '\n'
			
			self.response.out.write(sep)
			self.response.out.write(m.render())
			self.response.out.write(sep)
		else:
			self.redirect(users.create_login_url(self.request.uri))
