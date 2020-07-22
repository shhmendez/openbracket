import sys,os

from ..GameEngine import Game, exceptions as Exp
from . import UserSession
import json

from clastic import Application, render_basic, render_json, Response, Middleware
from clastic.route import OPTIONS, POST
from clastic.middleware.cookie import SignedCookieMiddleware


def render_raw(context):
    res = Response(context)
    return res
def render_raw_json(context):
    res = Response(json.dumps(context))
    return res
class RenderRawJson(Middleware):
    def request(self,next):
        # res = next()
        return Response()

class Print(Middleware):
    def request(self,next, request):
        res = next()
        global board
        # for rank in board:
        #     print(rank)
        return res



class Unpack(Middleware):
    def __init__(self,*params):
        self.params = params
        self.provides = tuple(self.params)
    def request(self,next,request):
        data = json.loads(request.data.decode("utf-8"))
        #add check for correct data shape
        res = next(**data)
        return res



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

#A cache here could help 
class UserSession(Middleware):
    provides = ('user_session',)
    def __init__(self):
        pass
    def request(self,next, request,cookie): 
        print(f'cookies in request {cookie}')
        response = next({"user_session": {}})
        print(cookie.items(),cook)
        # for (k,v) in cookie.items():
        #     response.set_cookie(k,v)
        
        # print("who: {}".format(cook))
        return response

#this middleware should provide some set of functions that allow 
class GameProvider(Middleware):
    provides = ('boardgames')
def login(username,password,cookie):
    cookie['username'] = username
    return {'success': True, 'username':username}

def move(rank,file,xto,yto):
    try:
        global board
        rank = int(rank)
        file = int(file)
        dx = int(xto) - rank
        dy = int(yto) - file
        print(rank,file,dx, dy)
        new_board,valid = Game.move(board, rank,file, dx, dy)
        board = new_board
        return {'valid':valid}
    except Exp.InvalidMove:
        return {'valid':False}

def getgames(Games):
    return  
def newgame(user_session):
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

def default(request,cookie):
    print(cookie.items())
    return "success"

def test(cookie):
  print("here",cookie.items())

routes = [
        POST('/move', move, render_raw_json, middlewares=[Unpack('rank','file','xto','yto')]),
        POST("/sync",sync),
        POST("/login",login, render_raw_json, middlewares=[Unpack('username','password')]),
        POST("/newgame",newgame),
        POST("/getuser",default,RenderRawJson()),
        POST("/test",test,render_raw),
        ("/<path*>",default,render_basic)
        ]

app = Application(routes,middlewares=[SignedCookieMiddleware(), UserSession(),Cors()])

board = Game.build_board()
if __name__ == "__main__":
  app.serve()
#request new game
#validate board transition
#request game by id
