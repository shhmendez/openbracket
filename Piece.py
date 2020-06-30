

def rook(dx,dy,friendly_collision,collision):
  valid = dx * dy == 0 and not friendly_collision
  return (rook, valid)

def bishop(dx,dy,friendly_collision,collision):
  valid = abs(dx) == abs(dy) and not friendly_collision
  return (bishop,valid)

def queen(*args):
  return (queen, rook(*args)[1] or bishop(*args)[1])

def king(dx,dy,friendly_collision,collision):
  return abs(dx) >= 1 and abs(dy) >= 1 and not friendly_collision

def knight(dx,dy,friendly_collision,collision):
  L = sorted(map(lambda i: abs(i), [dx,dy]))
  return (knight, L[0] == 1 and L[1] == 2 and not friendly_collision)

def __pawn__(dx,dy, friendly_collision, collision):
  def inner():
    if friendly_collision: return False
    elif collision:
      if dx == 0: return False
      if abs(dx) == 1 and dy == 1: return True
    else:
      return dx == 0 and dy == 1

  return (pawn,inner())

def pawn(dx,dy,friendly_collision,collision):
  
  
  if dx == 0 and dy == 2 and not friendly_collision and not collision: 
    return (__pawn__, True)
  else:
    return __pawn__(dx,dy,friendly_collision,collision)

