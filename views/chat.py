from datetime import datetime
from time import mktime
import time

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db

from models.message import Message
import simplejson as json
from settings import *

MAX_RETRIES = 20
POLL_RATE = 1


class index(webapp.RequestHandler):
    def get(self):
        path = os.path.join(TEMPLATE_DIR, 'chat.html')
        self.response.out.write(template.render(path, {}))


class message(webapp.RequestHandler):
    def get(self):        
        s = int(self.request.get('s'))
        uid = int(self.request.get('uid'))
        
        messages = []
        
        for i in range(0, MAX_RETRIES):
            newest_messages = db.GqlQuery('SELECT * FROM Message WHERE timestamp > :1 ORDER BY timestamp DESC LIMIT 10', s)            
            
            if newest_messages.count(1) > 0:
                for m in newest_messages:
                    if m.uid != uid:
                        messages.append({
                                'message': m.content, 
                                'author': m.author, 
                                'timestamp': m.timestamp,
                            })
        
                if len(messages) > 0:
                    break
            
            time.sleep(POLL_RATE)
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(messages))
    
    
    def post(self):
        dt = datetime.now()
        
        message = Message()
        message.uid = int(self.request.get('uid'))
        message.author = self.request.get('author')
        message.content = self.request.get('message')
        message.timestamp = int(mktime(dt.timetuple()) * 1000)
        message.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps({}))

