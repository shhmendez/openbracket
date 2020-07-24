import unittest
import sys
from Backend import UserSession as us
import pymongo


class Tests(unittest.TestCase):
  def test_user(self):
    user = us.User(name="shane")
    user.save()
    print(us.User.objects.count())



