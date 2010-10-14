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
			m.put()
		return m
	
	def authorized(self):
		return users.get_current_user() is not None
	
	def reset(self):
		m = self.getMinefield()
		m.reset()
		m.put()
		return m.render()
	
	def giveup(self):
		m = self.getMinefield()
		m.finished = True
		m.put()
		return m.render()
	
	def render(self):
		m = self.getMinefield()
		return m.render()
	
	def reveal(self, x, y):
		m = self.getMinefield()
		m.reveal(x, y)
		if(m.getState(x,y) == -1):
			m.finished = True
		m.put()
		return m.render()
	
	def mine(self, x, y):
		m = self.getMinefield()
		m.mine(x, y)
		m.put()
		return m.render()

