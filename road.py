from operator import itemgetter
from grid import *

def valid_moves(pos, grid):
  moves = []
  # left and right
  if grid.is_valid((pos[0]-1, pos[1])):
    moves.append((pos[0]-1, pos[1]))
  if grid.is_valid((pos[0]+1, pos[1])):
    moves.append((pos[0]+1, pos[1]))

  # forward and back
  if grid.is_valid((pos[0], pos[1]-1)):
    moves.append((pos[0], pos[1]-1))
  if grid.is_valid((pos[0], pos[1]+1)):
    moves.append((pos[0], pos[1]+1))

  # diagonals
  if grid.is_valid((pos[0]-1, pos[1]-1)):
    moves.append((pos[0]-1, pos[1]-1))
  if grid.is_valid((pos[0]-1, pos[1]+1)):
    moves.append((pos[0]-1, pos[1]+1))
  if grid.is_valid((pos[0]+1, pos[1]+1)):
    moves.append((pos[0]+1, pos[1]+1))
  if grid.is_valid((pos[0]+1, pos[1]-1)):
    moves.append((pos[0]+1, pos[1]-1))

  return moves

def dist(a, b):
  if a is None or b is None:
    return None
  return math.sqrt((b[1]-a[1])**2 + (b[0]-a[0])**2)

def traverse(pos, grid, visited={}):
  print(pos)
  if pos in visited.keys() and visited[pos][0] is not None:
    return visited[pos]
  if pos in visited.keys() and visited[pos][0] is None:
    return (None, None)

  if grid.get_position(pos) == terminal_space:
    return (0, [])

  visited[pos] = (None, None)
  
  moves = valid_moves(pos, grid)
  (shortest_len, shortest_path, next_move) = (None, None, None)
  for m in moves:
    l, path = traverse(m, grid, visited)
    print("option", pos, m, l, path)
    if l != None:
      l += dist(pos, m)
      if shortest_len is None or l < shortest_len:
        shortest_len = l
        shortest_path = path.copy()
        next_move = m
  print("picked", pos, next_move, shortest_len, shortest_path)
  
  if shortest_path is None:
    return (None, None)

  shortest_path.insert(0, next_move)

  visited[pos] = (shortest_len, shortest_path)
  return (shortest_len, shortest_path)

if __name__ == "__main__":
  grid = Grid()

  start = (13, 7)
  grid.set_terminal((17, 7))
  print()
  l, traversal = traverse(start, grid)
  print(l)
  grid.show_traversal(start, traversal)

