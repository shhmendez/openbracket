import sys,os
sys.path.append(os.getcwd())

from collections import namedtuple
import Piece, exceptions as Exc
import copy

class ColoredPiece(namedtuple('ColoredPiece',['color','piece'])):
  __slots__ = ()
  WHITE = 0
  BLACK = 1
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
  
def game():
  board = build_board()
  
def move(board, x,y,dx,dy):
  board = copy.deepcopy(board)
  piece = board[y][x]
  if not piece:
    raise Exc.InvalidPiece()

  occupy = board[y+dy][x+dx]

  if occupy:
    friendly_collision = occupy.color == piece.color
    collision = not friendly_collision 
  else:
    friendly_collision = False
    collision = False

  new_piece, valid_move = piece.piece(dx,dy, friendly_collision,collision)

  if(valid_move):
    board[y][x] = EMPTY()
    p =  ColoredPiece(piece.color, new_piece)
    board[y+dy][x+dx] = p
  return board





