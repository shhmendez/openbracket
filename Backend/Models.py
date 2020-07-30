from mongoengine import *
import pymongo
import pickle
connect('openbracket')

class User(Document):
  username = StringField(required=True, max_length=200, primary_key=True)
  ciphertext = StringField(required=True, max_length=200)
  game_id_list = ListField(StringField(max_length=200),required=False)

class Board(Document):
  serial = BinaryField(required=True)  
  players = ListField(StringField(max_length=200),required=True)

def verifyUser(username,ciphertext):
  user = User.objects(username=username)
  if not user or user[0].ciphertext != ciphertext: return None
  return user

def saveBoard(board,user):
  model = Board(serial=pickle.dumps(board),players=[user])
  model.save()