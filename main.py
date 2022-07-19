import numpy as np
import matplotlib.pyplot as plt
import math

class Circuit:
    def __init__(self, control_points, track_width):
        self.control_points = control_points
        self.track_width = track_width
        self.construct_boundaries()

    def _get_neighboring_points(self, t):
        p1 = int(t) % len(self.control_points)
        p2 = (p1 + 1) % len(self.control_points)
        p3 = (p2 + 1) % len(self.control_points)
        p0 = p1 - 1 if p1 >= 1 else len(self.control_points) - 1

        return [p0, p1, p2, p3]

    def _sum_weights(self, axis, points, weights):
        axis_index = 0 if axis == "x" else 1
        if len(points) != len(weights):
            raise Exception("mismatched points and weights")
        out = 0
        for i in range(len(weights)):
            point = points[i]
            weight = weights[i]
            out += self.control_points[point][axis_index] * weight
        return out

    def get_spline_point(self, t):
        points = self._get_neighboring_points(t)

        t = t - int(t)
        tt = float(t * t)
        ttt = tt * t

        w0 = -ttt + 2 * tt - t
        w1 = 3 * ttt - 5 * tt + 2
        w2 = -3 * ttt + 4 * tt + t
        w3 = ttt - tt

        weights = [w0, w1, w2, w3]

        tx = 0.5 * self._sum_weights("x", points, weights)
        ty = 0.5 * self._sum_weights("y", points, weights)

        return (tx, ty)

    def get_spline_gradient(self, t):
        points = self._get_neighboring_points(t)

        t = t - int(t)
        tt = float(t * t)
        w0 = -3 * tt + 4 * t - 1
        w1 = 9 * tt - 10 * t
        w2 = -9 * tt + 8 * t + 1
        w3 = 3 * tt - 2 * t
        weights = [w0, w1, w2, w3]

        tx = 0.5 * self._sum_weights("x", points, weights)
        
        ty = 0.5 * self._sum_weights("y", points, weights)

        return (tx, ty)


    def calculate_boundary(self, t):
        control_point = self.get_spline_point(t)
        gradient = self.get_spline_gradient(t)
        gradient_magnitude = math.sqrt(gradient[0] ** 2 + gradient[1] ** 2)

        left_point_x = control_point[0] + self.track_width * -gradient[1] / gradient_magnitude
        left_point_y = control_point[1] + self.track_width * gradient[0] / gradient_magnitude

        right_point_x = control_point[0] - self.track_width * -gradient[1] / gradient_magnitude
        right_point_y = control_point[1] - self.track_width * gradient[0] / gradient_magnitude

        return ((left_point_x, left_point_y), (right_point_x, right_point_y))
    
    def construct_boundaries(self):
        increment = 0.01
        t = 0
        self.left_boundary = []
        self.right_boundary = []
        while t < float(len(self.control_points)):
            (left, right) = self.calculate_boundary(t)
            self.left_boundary.append(left)
            self.right_boundary.append(right)
            t += increment

    def draw_circuit(self):
        plt.figure()
        plt.plot([t[0] for t in self.left_boundary], [t[1] for t in self.left_boundary])
        plt.plot([t[0] for t in self.right_boundary], [t[1] for t in self.right_boundary])

        plt.axis([-10, 260, -50, 280])
        plt.show()



control_points = [
    (81.8, 196.0),
    (108.0, 210.0),
    (152.0, 216.0),
    (182.0, 185.6),
    (190.0, 159.0),
    (198.0, 122.0),
    (226.0, 93.0),
    (224.0, 41.0),
    (204.0, 15.0),
    (158.0, 24.0),
    (146.0, 52.0),
    (157.0, 93.0),
    (124.0, 129.0),
    (83.0, 104.0),
    (77.0, 62.0),
    (40.0, 57.0),
    (21.0, 83.0),
    (33.0, 145.0),
    (30.0, 198.0),
    (48.0, 210.0),
]

c = Circuit(control_points=control_points, track_width=10)
c.draw_circuit()


# plt.plot([t[0] for t in path], [t[1] for t in path])
# plt.plot([t[0] for t in track_self.control_points], [t[1] for t in track_self.control_points], "x")

