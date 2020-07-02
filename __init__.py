from clastic import Application, render_basic, render_json, Response,POST
import sys,os
sys.path.append(os.getcwd())
import Game
import exceptions as Exp
from collections import Sized
def Post(func):
    def inner(request):
        # args = func.__code__.co_varnames[func.__code__]
        # print(args)
        # kwargs = {k: request.values[k] for k in args}
        print(request.values)
        print(request.headers)
        return func(**request.values)
    return inner

board = Game.build_board()

def Cors(context, request, _route):
    res = render_basic(context,request, _route)
    res.headers['Access-Control-Allow-Origin'] = "*"
    res.headers['Access-Control-Allow-Headers'] = "*"
    # print(res.headers)
    return res
def move(rank,file,xto,yto):
    try:
        global board
        rank = int(rank)
        file = int(file)
        xto = int(xto)
        yto = int(yto)
        board,valid = Game.move(board, rank,file, xto-rank, yto-file)
        for rank in board:
            print(rank)
        return valid
    except Exp.InvalidMove:
        return False

def default(request):
    return "success"

routes = [POST('/move', Post(move), Cors),
        ("/test",default,Cors)
        ]

app = Application(routes)
app.serve()
#request new game
#validate board transition
#request game by id
