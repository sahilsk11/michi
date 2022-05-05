import math
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import numpy as np

invalid_space = "#"
valid_space = "o"
terminal_space = "^"
visited_space = "x"

# def upper(x):
#   return (-(1/4)*(x-4)**2) + 4

# def lower(x):
#   return (-(1/3)*(x-4)**2) + 2

def upper(x):
  return 10*np.cos(0.2*x)+17

def lower(x):
  return 10*np.cos(0.2*x)+10

def plot_grid():
  x_range = range(0, 18)
  y_range = range(0, 8)

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
    for c in arr[r]:
      print(c, end="  ")
    print()

class Grid:
  def __init__(self):
    self.grid = plot_grid()

  def set_terminal(self, pos):
    self.grid[len(self.grid)-pos[1]-1][pos[0]] = terminal_space

  def get_position(self, pos):
    if not self.is_valid(pos):
      return None
    return self.grid[len(self.grid)-pos[1]-1][pos[0]]

  def is_valid(self, pos):
    if pos[1] < 0 or pos[1] >= len(self.grid):
      return False
    if pos[0] < 0 or pos[0] >= len(self.grid[pos[1]]):
      return False
    return self.grid[len(self.grid)-pos[1]-1][pos[0]] != invalid_space
  
  def print(self):
    print_arr(self.grid)

  def show_traversal(self, start, traversed_path):
    traversed_path.insert(0, start)

    x = np.arange(10.0, 20, 0.1)
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
    