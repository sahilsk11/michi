from operator import itemgetter
from grid import *
import sys

def valid_moves(pos, grid):
  out = []

  rows = [pos[0], pos[0]+1]
  cols = [pos[1]-1, pos[1], pos[1]+1]
  for r in rows:
    for c in cols:
      if grid.get_position((r, c)) != invalid_space and grid.get_position((r, c)) != None:
        out.append((r, c))

  return out

def dist(a, b):
  if a is None or b is None:
    return None
  return math.sqrt((b[1]-a[1])**2 + (b[0]-a[0])**2)

def traverse(pos, grid, visited={}):
  print(pos)
  if pos in visited.keys():
    return visited[pos]

  if grid.get_position(pos) == terminal_space:
    return (0, [])

  visited[pos] = (None, None)
  
  moves = valid_moves(pos, grid)
  (shortest_len, shortest_path, next_move) = (None, None, None)
  for m in moves:
    l, path = traverse(m, grid, visited)
    if l != None:
      l += dist(pos, m)
      if shortest_len is None or l < shortest_len:
        shortest_len = l
        shortest_path = path.copy()
        next_move = m
  
  if shortest_path is None:
    return (None, None)

  shortest_path.insert(0, next_move)

  visited[pos] = (shortest_len, shortest_path)
  return (shortest_len, shortest_path)

def find_terminal(start, grid, path=[]):
  q = [(start, 0)]
  for e in q:
    print(e[0], grid.get_position(e[0]))
    if grid.get_position(e[0]) == terminal_space:
      return e[1]

    moves = valid_moves(e[0], grid)
    for m in moves:
      if grid.get_position(m) != invalid_space:
        q.append((m, e[1]+1))
        grid.set_position(e[0], invalid_space)

  return None

def dijkstra(start, grid):
  shortest_path = {}
  previous_nodes = {}

  unvisited_nodes = grid.list_nodes()
  for node in unvisited_nodes:
    shortest_path[node] = sys.maxsize
  shortest_path[start] = 0

  while unvisited_nodes:
    min_node = None
    for node in unvisited_nodes:
      if min_node == None or shortest_path[node] < shortest_path[min_node]:
        min_node = node
    
    moves = valid_moves(min_node, grid)
    for m in moves:
      d = shortest_path[min_node] + dist(min_node, m)
      if d < shortest_path[m]:
        shortest_path[m] = d
        previous_nodes[m] = min_node

    unvisited_nodes.remove(min_node)

  return previous_nodes, shortest_path

def get_traversal(prev_nodes, start, end):
  path = []
  node = end
  
  while node != start:
    path.append(node)
    node = prev_nodes[node]

  # Add the start node manually
  path.append(start)
  return path

if __name__ == "__main__":
  grid = Grid()

  start = (1, 220)
  end = (270, 160)
  grid.set_terminal(end)
  # print()
  prev_nodes, distances = dijkstra(start, grid)
  if end not in distances or distances[end] >= sys.maxsize:
    print("what")
  else:
    path = get_traversal(prev_nodes, start, end)
    print(distances[end])
    grid.show_traversal(path)

