
from types import SimpleNamespace

#I'm doing everything in my power to avoid classes

def wrapper():
  funcs = {}
  def namespace(func):
    nonlocal funcs
    funcs[func.__name__] = func
    return func
  
  @namespace
  def getuser(username, password):
    return username


  @namespace
  def getgames(userid):
    pass

  return SimpleNamespace(**funcs)


usersession = wrapper()

