from mongoengine import *
import pymongo
connect('openbracket')

class User(Document):
  username = StringField(required=True, max_length=200, primary_key=True)
  ciphertext = StringField(required=True, max_length=200)
  game_id_list = ListField(StringField,required=False)
class Board(Document):
  serial = BinaryField(required=True)  
  owner = ListField(LazyReferenceField(User),required=True)

def verifyUser(username,ciphertext):
  user = User.objects(username=username)
  if not user or user[0].ciphertext != ciphertext: return None
  return user

