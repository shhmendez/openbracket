import sys,os
sys.path.append(os.getcwd())

import Game
import __init__ as server

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
printb(board)
print(Game.side('black'))
print('-'*30)
try:
  Game.move(board,3,3,1,1)
except:
  print("Successful failure")

move = moveboard(board)

