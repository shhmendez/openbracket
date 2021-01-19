import sys,os

from openbracket.GameEngine import Game, exceptions as Exp
from openbracket.Backend import Models as models
import json

import logging

from clastic import Application, render_basic, render_json, Response, Middleware
from clastic.route import OPTIONS, POST,Route

from openbracket.Backend.Middlewares import *
from types import SimpleNamespace

logger = logging.getLogger('server_logger')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('./logs/server.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

logger.debug("\n\n"+"="*50)
class RouteManager(object):
    def __init__(self):
        self.routes = {}

    def get_entry(self,func):
        
        if not func.__name__ in self.routes: 
            self.routes[func.__name__] = SimpleNamespace(
            route="",function=lambda: None,middlewares=[],method=Route,args=[],kwargs={})
        return self.routes[func.__name__]

    def middlewares(self,*args):
        def inner(func):
            entry = self.get_entry(func)
            entry.middlewares += args
            return func
        return inner

    def route(self,route,Method=Route,Render=None):
        def inner(func):
            entry = self.get_entry(func)
            if Render:
                entry.args.append(Render)
            logger.debug(
                'setting route config\nroute: {}\nfunction:{}\nmethod: {}\nRender:{}'
                .format(route,func,Method,Render))
            entry.route = route
            entry.function = func
            logger.debug(f'{entry}\n')
            return func
        return inner

    def collate(self):
        routes = []
        for entry in self.routes:
            r = self.routes[entry]
            logger.debug(f'Collating: {r}')
            args = [r.route,r.function] + r.args
            kwargs = r.kwargs.copy()
            kwargs['middlewares'] = r.middlewares
            logger.debug(f'{args},{kwargs}')
            # routes.append(r.method(*args,**kwargs))
        return routes

routeman = RouteManager()
board = Game.build_board()
bp = BoardProvider()
up =  UserSession()

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

@routeman.middlewares(up)
@routeman.route("/games/<username>")
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
    logger.debug(cookie.items())
    return "success"

def test(cookie):
  logger.debug("here",cookie.items())


routes = routeman.collate()
logger.debug(routes)
routes.append(("/<path*>",default,render_basic))
app = Application(routes,resources={"board_model": models.Board, "user_model": models.User},middlewares=[Cors(),SignedCookieMiddleware()])

if __name__ == "__main__":
  app.serve()
#request new game
#validate board transition
#request game by id
