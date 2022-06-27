from operator import itemgetter
from grid import *
import sys

def valid_moves(pos, grid, previous_positions=[]):
  out = []

  rows = [pos[0], pos[0]+1, pos[0]+2]
  cols = [pos[1]-1, pos[1], pos[1]+1]

  for r in rows:
    for c in cols:
      if grid.get_position((r, c)) != invalid_space and (r != pos[0] or c != pos[1]):
        path = previous_positions.copy()
        path.append(pos)
        path.append((r, c))
        if calculate_angle(path) > 135:
          out.append((r, c))

  return out

def calculate_angle(positions):
  if len(positions) < 3:
    return 180 #assume it's on the same path
  (a, b, c) = (positions[-3], positions[-2], positions[-1])
  ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])) # law of cosines
  if ang < 0:
    ang += 360
  if ang > 180:
    ang = 360 - ang
  return ang
  

def dist(a, b):
  if a is None or b is None:
    return None
  return math.sqrt((b[1]-a[1])**2 + (b[0]-a[0])**2)

def traverse(pos, grid, visited={}):
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
  previous_node_map = {}

  unvisited_nodes = grid.list_open_nodes()
  for node in unvisited_nodes:
    shortest_path[node] = sys.maxsize
  shortest_path[start] = 0

  while unvisited_nodes:
    # select closest node. the first time this runs,
    # it should pick the start node
    closest_node = unvisited_nodes[0]
    for node in unvisited_nodes[1:]:
      if shortest_path[node] < shortest_path[closest_node]:
        closest_node = node
    node = closest_node

    moves = valid_moves(node, grid, get_prev_traversal(previous_node_map, node))
    for potential_move in moves:
      d = shortest_path[node] + dist(node, potential_move)
      # if path from node to potential_move is shorter
      # than the current shortest path to potential_move, update
      if d < shortest_path[potential_move]:
        shortest_path[potential_move] = d
        previous_node_map[potential_move] = node

    unvisited_nodes.remove(node)

  return previous_node_map, shortest_path

def get_prev_traversal(prev_nodes, node):
  path = []
  
  while node in prev_nodes:
    path.append(prev_nodes[node])
    node = prev_nodes[node]

  return path

if __name__ == "__main__":
  scale = 3
  grid = Grid(scale)

  (start, end) = calc_start_end(scale)
  # end = (2, 5)
  print(start, end)
  grid.set_terminal(end)

  path = []
  prev_nodes, distances = dijkstra(start, grid)
  if end not in distances or distances[end] >= sys.maxsize:
    print("no path found")
    path.append(start)
  else:
    path = get_prev_traversal(prev_nodes, end)
    print(path)

    path.append(end)
  grid.show_traversal(scale, path)

