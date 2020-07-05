import sys,os
sys.path.append(os.getcwd())
import Game
import json
import exceptions as Exp
from clastic import Application, render_basic, render_json, Response, Middleware
from clastic.route import OPTIONS, POST
from collections import Sized
def Post(func):
    def inner(request):
        # args = func.__code__.co_varnames[func.__code__]
        # print(args)
        # kwargs = {k: request.values[k] for k in args} 
        data = json.loads(request.data.decode("utf-8"))
        return func(**data)
    return inner

board = Game.build_board()


class Cors(Middleware):
    def request(self, next):
        res = next()
        if(type(res) != Response):
            try:
                res = json.dumps(res)
            except:
                pass
            res = Response(res)
        res.headers['Access-Control-Allow-Origin'] = "*"
        res.headers['Access-Control-Allow-Headers'] = "*"
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

class Print(Middleware):
    def request(self,next, request):
        res = next()
        global board
        for rank in board:
            print(rank)
        return res

def move(rank,file,xto,yto):
    try:
        global board
        rank = int(rank)
        file = int(file)
        dx = int(xto) - rank
        dy = int(yto) - file
        print(rank,file,dx, dy)
        board,valid = Game.move(board, rank,file, dx, dy)
        context = {'valid':valid}
    except Exp.InvalidMove:
        context =  {'valid':False}
    finally:
        return Response(json.dumps(context), content_type='application/json') 

def newgame():
    global board
    board = Game.build_board()
    return {"success":True}
def sync():
    places = [[],[]]
    global board
    for i,rank in enumerate(board):
        for j,piece in enumerate(rank):
            if(piece == 0):
                continue
            places[piece.color].append((str(piece), i, j))

    return {'black': places[0], 'white':places[1]}

def default(request):
    return "success"

routes = [
        POST('/move', Post(move)),
        POST("/sync",sync),
        POST("/newgame",newgame),
        ("/<path*>",default,render_basic)
        ]

app = Application(routes,middlewares=[Cors(),Print()])




app.serve()
#request new game
#validate board transition
#request game by id
