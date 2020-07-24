import sys,os
sys.path.append(os.getcwd())

from openbracket.GameEngine import Game



def test_pickle():
  """
  picking is a serialization process, I want to know:
  1. can I pickle a multidimensional array
  2. when unpickling, how are functions resolved

  With regard to 2, do the same function point to the same function in memory, or 2 different instances
  """
  board1 = Game.game()
  board2 = Game.game()


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

  return inner
board = Game.build_board()

def test_move():
  try:
    Game.move(board,0,0,0,3)
  except:
    print("Successfully failed to move")


