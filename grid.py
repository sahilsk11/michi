import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np

invalid_space = "#"
valid_space = "o"
terminal_space = "^"
visited_space = "x"

x_bounds = (0, 270)
y_bounds = (0, 250)

# def upper(x):
#   return (-(1/4)*(x-4)**2) + 4

# def lower(x):
#   return (-(1/3)*(x-4)**2) + 2

def upper(x):
  return 100*np.cos(0.05*x)+130

def lower(x):
  return 100*np.cos(0.05*x)+100

def plot_grid():
  x_range = range(x_bounds[0], x_bounds[1]+1)
  y_range = range(y_bounds[0], y_bounds[1]+1)

  grid = []
  for y in y_range:
    grid.append([])
    for x in x_range:
      u = upper(x)
      l = lower(x)
      if y >= l and y <= u:
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
  def __init__(self):
    # v = valid_space
    # x = invalid_space
    # t = terminal_space
    # g = [
    #   [v, x, x, x],
    #   [x, v, x, x],
    #   [t, x, t, x]
    # ]
    

    g = plot_grid()

    self.grid = self.rotate(g)


  def rotate(self, grid):
    g = []
    for j in range(len(grid[0])):
      g.append([])
      for i in range(len(grid)):
        g[j].append(grid[len(grid)-i-1][j])
    return g

  def list_nodes(self):
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
      return None
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

  def show_traversal(self, traversed_path):
    x = np.arange(x_bounds[0], x_bounds[1], 0.1)
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

    print(len(traversed_path))
    