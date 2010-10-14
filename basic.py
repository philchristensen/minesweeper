from google.appengine.api import users
from google.appengine.ext import webapp

from model import Minefield

class LoginHandler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if(user):
			self.redirect('/flex/bin-debug/MinesweeperClient.html')
		else:
			self.redirect(users.create_login_url(self.request.uri))

class Handler(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		
		if(user):
			m = Minefield.gql("WHERE author = :1", user).get()
			if not(m):
				m = Minefield(
					author = user,
				)
			
			for point in self.request.get_all('mine'):
				x,y = [int(x) for x in point.split(',')]
				m.mine(x, y)
			
			for point in self.request.get_all('reveal'):
				x,y = [int(x) for x in point.split(',')]
				m.reveal(x, y)
				if(m.getState(x,y) == -1):
					m.finished = True
			
			for point in self.request.get_all('hide'):
				x,y = [int(x) for x in point.split(',')]
				m.hide(x, y)
			
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
