from clastic import Application, render_basic
import sys,os
sys.path.append(os.getcwd())
import Game


def Post(func):
    def inner(request):
        args = func.func_code.co_varnames
        kwargs = {k: request.values[k] for k in args}
        return func(**kwargs)
    return inner

board = Game.build_board()

@Post
def move(rank,file,xto,yto):
    global board
    rank = int(rank)
    file = int(file)
    xto = int(xto)
    yto = int(yto)
    board = Game.move(board, rank,file, xto-rank, yto-file)
    return not not board

routes = [('/move', move, render_basic)]

app = Application(routes)
app.serve()
#request new game
#validate board transition
#request game by id
