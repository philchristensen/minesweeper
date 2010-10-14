from google.appengine.ext import webapp

import basic, amf

application = webapp.WSGIApplication([('/', basic.Handler), ('/login', basic.LoginHandler), ('/amf', amf.Handler)], debug=True)

def main():
	from google.appengine.ext.webapp.util import run_wsgi_app
	run_wsgi_app(application)

if __name__ == "__main__":
	main()