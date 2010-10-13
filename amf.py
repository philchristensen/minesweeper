from google.appengine.api import users

import pyamf
from pyamf.remoting.gateway.google import WebAppGateway

from model import Minefield

class Handler(WebAppGateway):
	def __init__(self, *args, **kwargs):
		WebAppGateway.__init__(self, *args, **kwargs)
		
		self.addService(self, name='minesweeper')
	
	def render(self):
		user = users.User('blueradical@gmail.com') #users.get_current_user()
		m = Minefield.gql("WHERE author = :1", user).get()
		if not(m):
			m = Minefield(
				author = user,
				width = 10,
				height = 10,
			)
		return m.render()

