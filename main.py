import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

t = np.arange(0, 4, 0.1) # the increments to try

track_points = [
  (0, 0), (1, 1), (2, 2), (3, 3), (3, 0), (0, 0) # regular points
]

(x, y) = ([t[0] for t in track_points], [t[1] for t in track_points])

# tck,u = interpolate.splprep([x,y], s=0)
# unew = np.arange(0, 1.01, 0.01)
# out = interpolate.splev(unew, tck)
# print(out)

plt.figure()
plt.plot(x, y, 'x', x[0], y[1])
plt.axis([-1.05, 4, -1.05, 4])
plt.title('Spline of parametrically-defined curve')
plt.show()