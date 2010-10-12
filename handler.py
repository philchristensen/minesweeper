import logging

from google.appengine.api import users

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app

import pyamf
from pyamf.remoting.gateway.google import WebAppGateway

adjacent = lambda x, y: [
	(x-1, y-1),
	(x,	  y-1),
	(x+1, y-1),
	(x-1, y),
	(x+1, y),
	(x-1, y+1),
	(x,	  y+1),
	(x+1, y+1),
]

class Minefield(db.Model):
	author = db.UserProperty(required=True)
	width = db.IntegerProperty(required=True)
	height = db.IntegerProperty(required=True)
	mines = db.StringListProperty(default=[])
	exposures = db.StringListProperty(default=[])
	finished = db.BooleanProperty(default=False)
	
	def mine(self, x, y):
		mine = '%s,%s' % (x,y)
		if(mine in self.mines):
			return
		self.mines.append(mine)
	
	def expose(self, x, y):
		position = '%s,%s' % (x,y)
		if(position in self.exposures):
			return
		self.exposures.append(position)
	
	def hide(self, x, y):
		position = '%s,%s' % (x,y)
		if(position not in self.exposures):
			return
		self.exposures.remove(position)
	
	def getState(self, x, y):
		position = '%s,%s' % (x,y)
		if(position in self.mines):
			return -1
		
		state = 0
		for point in adjacent(x,y):
			if not(-1 < point[0] < self.width):
				continue
			elif not(-1 < point[1] < self.height):
				continue
			elif('%s,%s' % point in self.mines):
				state += 1
		
		return state
	
	def isExposed(self, x, y):
		if(self.finished):
			return True
		return '%s,%s' % (x,y) in self.exposures
	
	def render(self):
		output = '======================\n'
		for row in range(self.height):
			for col in range(self.width):
				if(self.isExposed(row, col)):
					state = self.getState(row, col)
					if(state == -1):
						output += '*'
					elif(state == 0):
						output += ' '
					else:
						output += str(state)
				else:
					output += '#'
			output += '\n'
		output += '======================\n'
		return output

class AMFHandler(WebAppGateway):
	def __init__(self, *args, **kwargs):
		WebAppGateway.__init__(self, *args, **kwargs)
		
		self.addService(self, name='minesweeper')
	
	def render(self):
		user = users.get_current_user()
		m = Minefield.gql("WHERE author = :1", user).get()
		if not(m):
			m = Minefield(
				author = user,
				width = 10,
				height = 10,
			)
		return m.render()

class MainPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		
		if(user):
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Hello, %s\n' % user.nickname())
			
			m = Minefield.gql("WHERE author = :1", user).get()
			if not(m):
				m = Minefield(
					author = user,
					width = 10,
					height = 10,
				)
			
			for point in self.request.get_all('mine'):
				x,y = [int(x) for x in point.split(',')]
				m.mine(x, y)
			
			for point in self.request.get_all('expose'):
				x,y = [int(x) for x in point.split(',')]
				m.expose(x, y)
				if(m.getState(x,y) == -1):
					m.finished = True
			
			for point in self.request.get_all('hide'):
				x,y = [int(x) for x in point.split(',')]
				m.hide(x, y)
			
			finish_req = self.request.get('finished')
			if(finish_req):
				m.finished = bool(int(finish_req))
			
			m.put()
			
			self.response.out.write(m.render())
		else:
			self.redirect(users.create_login_url(self.request.uri))

application = webapp.WSGIApplication([('/', MainPage), ('/amf', AMFHandler)], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()