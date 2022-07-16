import grid
import car
import path


if __name__ == "__main__":
  scale = 30
  g = grid.Grid(30)
  c = car.Car()

  (start, end) = path.calc_start_end(scale)
  p = path.shortest_path(g, start, end)
  g.show_traversal(scale, p)
  

