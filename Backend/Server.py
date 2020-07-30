import sys,os

from openbracket.GameEngine import Game, exceptions as Exp
from openbracket.Backend import Models as models
import json


from clastic import Application, render_basic, render_json, Response, Middleware
from clastic.route import OPTIONS, POST,Route

from openbracket.Backend.Middlewares import *
from collections import namedtuple
class RouteManager(object):
    RouteEntry = namedtuple("Route",("method","args","kwargs"))
    RouteEntry.__new__.func_defaults = (Route,[],{})
    def __init__(self):
        self.routes = {}

    def middlewares(self,*args):
        def inner(func):
            route = self.routes[func.__name__]
            route.kwargs["middlewares"] += args
            return func
        return inner

    def route(self,route,Method=Route,Render=None):
        def inner(func):
            if not func in self.routes: self.routes[func.__name__] = RouteManager.RouteEntry(Method,[route,func],{"middlewares":[]})
            entry = self.routes[func.__name__]
            if Render:
                entry.args.append(Render)
            return func
        return inner
    def collate(self):
        routes = []
        for entry in self.routes:
            r = self.routes[entry]
            routes.append(r.method(*r.args,**r.kwargs))
        return routes

routeman = RouteManager()
board = Game.build_board()
bp = BoardProvider(models.Board)
up =  UserSession(models.User)

@routeman.middlewares(Unpack('username','password'))
@routeman.route("/login", POST,render_raw_json)
def login(username,password,cookie):
    cookie['username'] = username
    return {'success': True, 'username':username}


@routeman.middlewares(Unpack('rank','file','xto','yto','board_id'),bp)
@routeman.route("/move",POST)
def move(board,rank,file,xto,yto):
    rank = int(rank)
    file = int(file)
    dx = int(xto) - rank
    dy = int(yto) - file
    return Game.move(board, rank,file, dx, dy)

def getgames(gameList):
    return {'ids':gameList}

def newgame(user):
    """
    Params
    user: Models.User
    """
    board = Game.build_board()
    models.saveBoard(board,user)
    return sync(board)

@routeman.middlewares(Unpack('board_id'),bp)
@routeman.route("/sync",POST)
def sync(board):
    places = {}
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


routes = routeman.collate()
routes.append(("/<path*>",default,render_basic,{"middlewares":[bp]}))

app = Application(routes,middlewares=[Cors(),SignedCookieMiddleware(),up])

if __name__ == "__main__":
  app.serve()
#request new game
#validate board transition
#request game by id
