import sys,os

from ..GameEngine import Game, exceptions as Exp
import json

from clastic import Application, render_basic, render_json, Response, Middleware
from clastic.route import OPTIONS, POST
from clastic.middleware.cookie import SignedCookieMiddleware



class Print(Middleware):
    def request(self,next, request):
        res = next()
        global board
        # for rank in board:
        #     print(rank)
        return res


def Post(func):
    def inner(request):
        # args = func.__code__.co_varnames[func.__code__]
        # print(args)
        # kwargs = {k: request.values[k] for k in args} 
        data = json.loads(request.data.decode("utf-8"))
        return func(**data)
    return inner

board = Game.build_board()

def render_raw(context):
    res = Response(context)
    return res

def render_raw_json(context):
    res = json.dumps(context)
    return Response(res)
class Cors(Middleware):
    def request(self, next, request):
        res = next()
        if(type(res) != Response):
            try:
                res = json.dumps(res)
            except:
                pass
            res = Response(res)
        

        #find more specific implementation 
        base_url = request.origin
        res.headers['Access-Control-Allow-Origin'] = base_url
        res.headers['Access-Control-Allow-Headers'] = "content-type"
        res.headers['Access-Control-Allow-Credentials'] = 'true'
        return res

class OnlineGame(Middleware):
    provides = ('session',)
    def __init__(self,cookie_name='user_id', secret_key=None):
        self.cookie_name = cookie_name
        self.secret_key = secret_key or os.urandom(20)
    def request(self,next, request):
        session = load_cookie(request, self.cookie_name, self.secret_key)
        response = next(session=session)
        session.save_cookie(response, key=self.cookie_name)
        return response

class VerifyUser(Middleware):
    def __init__(self,cookie_name='user_id', secret_key=None):
        self.cookie_name = cookie_name
        self.secret_key = secret_key or os.urandom(20)
    def request(self,next, request,cookie):
        response = next()
        cook = cookie.pop("user",None)
        print(cook)
        return response
def move(rank,file,xto,yto):
    try:
        global board
        rank = int(rank)
        file = int(file)
        dx = int(xto) - rank
        dy = int(yto) - file
        print(rank,file,dx, dy)
        board,valid = Game.move(board, rank,file, dx, dy)
        return {'valid':valid}
    except Exp.InvalidMove:
        return {'valid':False}

def newgame():
    global board
    board = Game.build_board()
    return {"success":True}

def sync():
    places = {}
    global board
    for i,rank in enumerate(board):
        for j,piece in enumerate(rank):
            if(piece == 0):
                continue
            places[str((i,j))] = {'name':str(piece), 'color': piece.color}
    return places

def getuser(cookie):
    cookie['user'] = '123456'
    return {"success":True}

def default(request):
    return "success"

def test(cookie):
  print("here",cookie)
routes = [
        POST('/move', Post(move), render_raw_json),
        POST("/sync",sync),
        POST("/newgame",newgame),
        POST("/getuser",getuser,render_raw_json),
        POST("/test",test,render_raw),
        ("/<path*>",default,render_basic)
        ]

app = Application(routes,middlewares=[Cors(),SignedCookieMiddleware(), VerifyUser()])


if __name__ == "__main__":
  app.serve()
#request new game
#validate board transition
#request game by id
