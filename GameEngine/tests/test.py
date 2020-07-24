import sys,os
sys.path.append(os.getcwd())

from .. import Game

def printb(board):
  for p in board:
    print(p)
def moveboard(board):
  def inner(x,y,dx,dy):
    nonlocal board
    y = len(board) - y - 1
    dy = -dy
    board = Game.move(board,x,y,dx,dy)
    printb(board)
    print('-'*30)

  return inner
board = Game.build_board()

try:
  Game.move(board,0,0,0,3)
except:
  print("Successfully failed to move")


