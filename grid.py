import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np

invalid_space = "."
valid_space = "o"
terminal_space = "^"
visited_space = "x"

def calc_start_end(scale):
  start = (1, int(2*scale+1))
  end = (int(2*math.pi / (1/scale)), int(2*scale+1))
  return (start, end)

def plot_grid(n):
  u = n * (3/2)
  l = n
  w = 1/n

  def upper(x):
    return n*np.cos(w*x)+u

  def lower(x):
    return n*np.cos(w*x)+l

  x_limit = int(2*math.pi / w)
  y_limit = int(n + u)

  x_bounds = (0, x_limit)
  y_bounds = (0, y_limit)

  x_range = range(x_bounds[0], x_bounds[1]+1)
  y_range = range(y_bounds[0], y_bounds[1]+1)

  grid = []
  for y in y_range:
    grid.append([])
    for x in x_range:
      if y >= lower(x) and y <= upper(x):
        grid[y].append(valid_space)
      else:
        grid[y].append(invalid_space)

  return list(reversed(grid))

def print_arr(arr):
  for r in range(len(arr)):
    print("[", end=" ")
    for c in arr[r]:
      print(c, end="  ")
    print("]")

class Grid:
  def __init__(self, scale=None, grid=None):
    if grid is None:
      grid = plot_grid(scale)

    self.grid = self.rotate(grid)
    

  def rotate(self, grid):
    g = []
    for j in range(len(grid[0])):
      g.append([])
      for i in range(len(grid)):
        g[j].append(grid[len(grid)-i-1][j])
    return g

  def list_open_nodes(self):
    out = []
    for i in range(len(self.grid)):
      for j in range(len(self.grid[i])):
        if self.get_position((i, j)) != invalid_space:
          out.append((i, j))
    return out


  def set_terminal(self, pos):
    self.grid[pos[0]][pos[1]] = terminal_space

  def get_position(self, pos):
    if not self.is_valid(pos):
      return invalid_space
    return self.grid[pos[0]][pos[1]]

  def set_position(self, pos, val):
    if not self.is_valid(pos):
      return None
    self.grid[pos[0]][pos[1]] = val

  def is_valid(self, pos):
    if pos[0] < 0 or pos[0] >= len(self.grid):
      return False
    if pos[1] < 0 or pos[1] >= len(self.grid[pos[0]]):
      return False

    return True
  
  def print(self):
    print_arr(self.grid)

  def show_traversal(self, scale, traversed_path):
    u = scale * (3/2)
    l = scale
    w = 1/scale

    def upper(x):
      return scale*np.cos(w*x)+u

    def lower(x):
      return scale*np.cos(w*x)+l


    x_limit = int(2*math.pi / w)

    x_bounds = (0, x_limit)

    x = np.arange(x_bounds[0], x_bounds[1]+1, 0.1)
    y1 = lower(x)
    y2 = upper(x)

    fig, ax3 = plt.subplots(1, 1, sharex=True)

    ax3.plot(x, y1, x, y2, color='black')

    ax3.fill_between(x, y1, y2)
    ax3.set_ylabel('between y1 and y2')
    ax3.set_xlabel('x')

    ax3.plot(data=traversed_path)

    d = np.array(traversed_path)
    x, y = d.T

    ax3.xaxis.set_major_locator(MultipleLocator(1))
    ax3.yaxis.set_major_locator(MultipleLocator(1))

    plt.grid(color='grey', linestyle='-', linewidth=0.3)


    plt.scatter(x, y)

    plt.show()
    