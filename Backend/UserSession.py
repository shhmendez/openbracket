from mongoengine import *

connect('openbracket')

class User(Document):
  name = StringField(required=True, max_length=200)
  password = StringField(required=True, max_length=200)

class Board(Document):
  def __init__(self):
    pass


def verifyuser(Users,username, password):
  return username
def adduser(Users,username, password):
  return username

def getgames(Games,userid):
  pass

def addgame(Games,userid):
  pass

def removegame(Games,userid, boardid):
  pass

