from google.appengine.ext import db


class Message(db.Model):
    uid = db.IntegerProperty()
    author = db.StringProperty(multiline=False)
    content = db.StringProperty(multiline=True)
    timestamp = db.IntegerProperty()