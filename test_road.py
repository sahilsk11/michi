from path import *
import grid

def test_calculate_angle():
  positions = [(0, 0), (1, 0), (2, 0)]
  assert calculate_angle(positions) == 180, "no change in angle"

  positions = [(0, 0), (1, 0), (1, 1)]
  assert calculate_angle(positions) == 90, "270 brought to 90 deg angle change"

  positions = [(0, 1), (1, 1), (1, 2)]
  assert calculate_angle(positions) == 90, "90 deg angle change"

  positions = [(1, 6), (2, 5), (2, 4)]
  assert calculate_angle(positions) == 135, "135 deg angle change"

def test_valid_moves():
  (x, o, t) = (grid.invalid_space, grid.valid_space, grid.terminal_space)
  g = grid.Grid(grid=[
    [o, x, x],
    [x, o, x],
    [x, x, t]
  ])
  assert valid_moves((0, 2), g) == [(1, 1)], "simple traversal"

  g = grid.Grid(grid=[
    [o, o, x, x],
    [x, o, o, o],
  ])
  # starting 
  assert valid_moves((1, 1), g, [(0, 1)]) == [(3, 0)], "no sharp turns"

if __name__ == "__main__":
    test_calculate_angle()
    test_valid_moves()
    print("Everything passed")