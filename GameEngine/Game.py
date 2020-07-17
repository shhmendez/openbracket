import sys,os

from collections import namedtuple
from . import Piece, exceptions as Exc
import copy

class ColoredPiece(namedtuple('ColoredPiece',['color','piece'])):
  __slots__ = ()
  WHITE = 1
  BLACK = 0
  def __str__(self):
    n = self.piece.__name__
    if n == '__pawn__': return 'pawn'
    return n
  #temp for testing
  def __repr__(self):
    return self.__str__()
  

EMPTY = lambda: 0

def notation(piecename, x,y, dx,dy):
  file = "abcdefgh"
  return piecename[0].upper()+file[x]+"{}{}{}".format(y,file[dx],dy)


def side(color):
  c = lambda p: ColoredPiece(color,p)
  rook,knight, bishop = Piece.rook, Piece.knight, Piece.bishop
  pawns = [Piece.pawn for _ in range(8)]
  royals = [rook,knight,bishop,Piece.queen,Piece.king,bishop,knight,rook]
  
  return [list(map(c,pawns)),list(map(c,royals))]



def build_board():
  board = side(ColoredPiece.BLACK)[::-1]
  board.extend([[EMPTY() for _ in range(8)] for _ in range(4)])
  board.extend(side((ColoredPiece.WHITE)))
  return board

def interpolate(x,y,x2,y2,stepSize = 1):
  print(x,y,x2,y2)
  stepSize = abs(int(stepSize))
  dx = x2 - x
  dx = 0 if dx == 0 else int(dx/abs(dx))
  dy = y2 - y
  dy = 0 if dy == 0 else int(dy/abs(dy))
  # print("Step Start/End {},{}/{},{}".format(x,y,x2,y2))
  # print("Step Direction {},{}".format(dx,dy))

  # print("{}+{}<{}*{} == {}".format(y,dy,y2,dy, y+dy < y2*dy))
  print("dx: {}, dy: {}".format(dx,dy))
  if dx==0 and dy==0: return
  while (x+dx != x2) or (y+dy != y2):
    x += dx
    y += dy
    yield (x,y,)

def obstructed(board, interpolator, x,y,dx,dy):
  movepath = interpolator(x,y,x+dx,y+dy)
  print("Checking for obstructions")
  for x2,y2 in movepath:
    print("checking {},{}".format(x2,y2))
    if not isempty(board,x2,y2):
      return getspace(board,x2,y2)
  return False


def game():
  board = build_board()

def getspace(board, x,y):
  return board[y][x]

def isempty(board, x,y):
  return getspace(board, x,y) == EMPTY()


def setspace(board, x,y, value):
  board[y][x] = value
  return board

def move(board, x,y,dx,dy, interpolators={Piece.knight: (lambda *args: ())}):
  print('-'*20)
  if dx == 0 and dy == 0: raise Exc.InvalidMove()
  board = copy.deepcopy(board)
  piece = getspace(board, x,y)
  print(piece)
  if not piece:
    raise Exc.InvalidMove()

  occupy = getspace(board,x+dx, y+dy)

  if occupy:
    friendly_collision = occupy.color == piece.color
    collision = not friendly_collision 
  else:
    friendly_collision = False
    collision = False

  new_piece, valid_space = piece.piece(dx,dy*((piece.color)*-2+1), friendly_collision,collision)
  try:
    interpolator = interpolators[piece.piece]
  except:
    interpolator = interpolate

  print(interpolator)
  is_obs = obstructed(board, interpolator, x,y,dx,dy)
  valid_move = False if not valid_space else valid_space and not is_obs
  print("valid move {}, {}".format(valid_move, is_obs))
  print('-'*20)
  if(valid_move):
    board[y][x] = EMPTY()
    p =  ColoredPiece(piece.color, new_piece)
    board[y+dy][x+dx] = p

  return (board, valid_move)


