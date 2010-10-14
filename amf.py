from google.appengine.api import users

import pyamf
from pyamf.remoting.gateway.google import WebAppGateway

from model import Minefield

class Handler(WebAppGateway):
	def __init__(self, *args, **kwargs):
		WebAppGateway.__init__(self, *args, **kwargs)
		
		self.addService(self, name='minesweeper')
	
	def getMinefield(self):
		user = users.get_current_user()
		m = Minefield.gql("WHERE author = :1", user).get()
		if not(m):
			m = Minefield(
				author = user,
				width = 10,
				height = 10,
			)
		return m
	
	def render(self):
		import logging; logging.info('rendering')
		m = self.getMinefield()
		return m.render()
	
	def reveal(self, x, y):
		import logging; logging.info((x,y))
		m = self.getMinefield()
		m.reveal(x, y)
		return m.render()
	
	def mine(self, x, y):
		import logging; logging.debug((x,y))
		m = self.getMinefield()
		m.mine(x, y)
		return m.render()

