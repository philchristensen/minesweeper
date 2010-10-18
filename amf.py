"""
Server-side AMF Support
"""

from google.appengine.api import users
from google.appengine.ext import webapp

import pyamf
from pyamf.remoting.gateway.google import WebAppGateway

from model import Minefield

class LoginHandler(webapp.RequestHandler):
	"""
	Login support hook.
	"""
	def get(self):
		"""
		Redirect to login or game page, as appropriate.
		"""
		user = users.get_current_user()
		if(user):
			self.redirect('/flex/bin-debug/MinesweeperClient.html')
		else:
			self.redirect(users.create_login_url(self.request.uri))

class Handler(WebAppGateway):
	"""
	WSGI-Compatible AMF gateway.
	"""
	def __init__(self, *args, **kwargs):
		"""
		Implement 'minesweeper.*' commands
		"""
		WebAppGateway.__init__(self, *args, **kwargs)
		self.addService(self, name='minesweeper')
	
	def getMinefield(self):
		"""
		Fetch the minefield for the current user.
		"""
		user = users.get_current_user()
		m = Minefield.gql("WHERE author = :1", user).get()
		if not(m):
			m = Minefield(
				author = user,
			)
			m.put()
		return m
	
	def authorized(self):
		"""
		Is the current session authenticated?
		"""
		return users.get_current_user() is not None
	
	def reset(self):
		"""
		Reset the user's minefield
		"""
		m = self.getMinefield()
		m.reset()
		m.put()
		return m.render()
	
	def clear(self):
		"""
		Clear the user's minefield.
		"""
		m = self.getMinefield()
		m.clear()
		m.put()
		return m.render()
	
	def giveup(self):
		"""
		Give up and expose the user's minefield.
		"""
		m = self.getMinefield()
		m.finished = True
		m.put()
		return m.render()
	
	def render(self):
		"""
		Return an ASCII-based layout of mines and squares
		"""
		m = self.getMinefield()
		return m.render()
	
	def reveal(self, x, y):
		"""
		Register a 'click' at particular coordinates.
		"""
		m = self.getMinefield()
		m.reveal(x, y)
		if(m.getState(x,y) == -1):
			m.finished = True
		m.put()
		return m.render()
	
	def mine(self, x, y):
		"""
		Place a mine at particular coordinates.
		"""
		m = self.getMinefield()
		m.mine(x, y)
		m.put()
		return m.render()

