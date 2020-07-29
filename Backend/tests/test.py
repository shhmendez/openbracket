import unittest
import sys
from Backend import UserSession as us
import pickle
import pymongo
import sys
# from mongoengine import *
from mongoengine.pymongo_support import count_documents
from openbracket.GameEngine import Game

class Tests(unittest.TestCase):
  def setUp(self):
    user = us.User(username="shane",ciphertext="abc")
    self.user = user
    user2 = us.User(username="collin",ciphertext="dvx")
    self.board = single_board_write(user,user2)
    user2.save()
    user.save()
  def test_user(self):
    user = self.user
    valid_user = us.verifyUser(user.username,user.ciphertext)
    assert valid_user
    invalid_user = us.verifyUser('doesntexist','12341234')
    assert invalid_user == None
           
  def test_board_read(self):
    board = pickle.loads(self.board.serial)
    assert board[0][0] == Game.build_board()[0][0]

    board2,valid = Game.move(board,0,1,0,1)
    valid == True

  def tearDown(self):
    us.User.objects().delete()
    us.Board.objects().delete()

def single_board_write(user,user2):
  board = Game.build_board()
  pickled = pickle.dumps(board)
  boardRecord = us.Board(serial=pickled,owner=[user,user2])
  boardRecord.save()
  return boardRecord       

# print(sys.getsizeof(board))
# print(sys.getsizeof(self.board.serial))