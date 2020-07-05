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
    def render(self, next, context, request, _route):
        res = render_basic(context,request,_route)
        res.headers['Access-Control-Allow-Origin'] = "*"
        res.headers['Access-Control-Allow-Headers'] = "*"
        return res
def move(rank,file,xto,yto):
    try:
        global board
        rank = int(rank)
        file = int(file)
        xto = int(xto)
        yto = int(yto)
        board,valid = Game.move(board, rank,file, xto-rank, yto-file)
        return valid
    except Exp.InvalidMove:
        return False
    finally:
        for rank in board:
            print(rank)

def default(request):
    return "success"
routes = [
        POST('/move', Post(move), render_basic),
        ("/<path*>",default,render_basic)
        ]

app = Application(routes,middlewares=[Cors()])




app.serve()
#request new game
#validate board transition
#request game by id
