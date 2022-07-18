import numpy as np
import matplotlib.pyplot as plt

def get_spline_point(t, points):
  p1 = int(t)
  p2 = (p1 + 1) % len(points)
  p3 = (p2 + 1) % len(points)
  p0 = p1 - 1 if p1 >= 1 else len(points) - 1

  t = t - int(t)
  tt = float(t * t)
  ttt = tt * t

  q1 = -ttt + 2*tt - t
  q2 = 3*ttt - 5*tt + 2
  q3 = -3*ttt + 4*tt + t
  q4 = ttt - tt

  tx = 0.5 * (points[p0][0] * q1 + points[p1][0] * q2 + points[p2][0] * q3 + points[p3][0] * q4)
  ty = 0.5 * (points[p0][1] * q1 + points[p1][1] * q2 + points[p2][1] * q3 + points[p3][1] * q4)

  return (tx, ty)

t = np.arange(0, 4, 0.1) # the increments to try

track_points = [
  (0, 0), (0, 1), (1, 1), (1, 0)
]

increment = 0.001
t = 0
path = []
while t < float(len(track_points)):
  path.append(get_spline_point(t, track_points))
  t += increment

plt.figure()
plt.plot([t[0] for t in path], [t[1] for t in path])
plt.plot([t[0] for t in track_points], [t[1] for t in track_points], 'x')
plt.axis([-1.05, 4, -1.05, 4])
plt.show()