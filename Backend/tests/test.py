import unittest

from .. import UserSession as us
import pymongo
from ...GameEngine import Game

class Tests(unittest.TestCase):
  def test_user(self):
    user = us.User(name="shane")
    user.save()
    print(us.User.objects.count())

  def test_pickle(self):
    """
    picking is a serialization process, I want to know:
    1. can I pickle a multidimensional array
    2. when unpickling, how are functions resolved

    With regard to 2, do the same function point to the same function in memory, or 2 different instances
    """
    board1 = Game.game()
    board2 = Game.game()

