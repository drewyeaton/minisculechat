from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from views.chat import *


routes = [
        ('/', index),
        ('/message/', message),
        # ('/temp/', temp),
    ]

application = webapp.WSGIApplication(routes, debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()