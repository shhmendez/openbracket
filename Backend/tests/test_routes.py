import unittest
from openbracket.Backend import Server

class Test_Routes(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args,**kwargs)
    self.app = Server.app
    self.client = Server.app.get_local_client()
  
  def test(self):
    
    return self.client.get("/test")

  def test_move(self):
    res = self.client.post("/login",json={"username":"shane","password":"asdad"})
    print(res.data)
    print(self.client.post("/move").data)
class Test_Functions(unittest.TestCase):
  pass
