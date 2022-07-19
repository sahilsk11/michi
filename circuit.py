import matplotlib.pyplot as plt
import math


class Circuit:
    def __init__(self, control_points, track_width):
        self.control_points = control_points
        self.track_width = track_width
        self.construct_boundaries()

    def _get_neighboring_points(self, t, points):
        p1 = int(t) % len(points)
        p2 = (p1 + 1) % len(points)
        p3 = (p2 + 1) % len(points)
        p0 = p1 - 1 if p1 >= 1 else len(points) - 1

        return [points[p0], points[p1], points[p2], points[p3]]

    def _sum_weights(self, axis, points, weights):
        axis_index = 0 if axis == "x" else 1
        if len(points) != len(weights):
            raise Exception("mismatched points and weights")
        out = 0
        for i in range(len(weights)):
            point = points[i][axis_index]
            weight = weights[i]
            out += point * weight
        return out

    def get_spline_point(self, t, points):
        neighboring_points = self._get_neighboring_points(t, points)

        t = t - int(t)
        tt = float(t * t)
        ttt = tt * t

        w0 = -ttt + 2 * tt - t
        w1 = 3 * ttt - 5 * tt + 2
        w2 = -3 * ttt + 4 * tt + t
        w3 = ttt - tt

        weights = [w0, w1, w2, w3]

        tx = 0.5 * self._sum_weights("x", neighboring_points, weights)
        ty = 0.5 * self._sum_weights("y", neighboring_points, weights)

        return (tx, ty)

    def get_spline_gradient(self, t, points):
        neighboring_points = self._get_neighboring_points(t, points)

        t = t - int(t)
        tt = float(t * t)
        w0 = -3 * tt + 4 * t - 1
        w1 = 9 * tt - 10 * t
        w2 = -9 * tt + 8 * t + 1
        w3 = 3 * tt - 2 * t
        weights = [w0, w1, w2, w3]

        tx = 0.5 * self._sum_weights("x", neighboring_points, weights)

        ty = 0.5 * self._sum_weights("y", neighboring_points, weights)

        return (tx, ty)

    def calculate_boundary(self, t):
        control_point = self.get_spline_point(t, self.control_points)
        gradient = self.get_spline_gradient(t, self.control_points)
        gradient_magnitude = math.sqrt(gradient[0] ** 2 + gradient[1] ** 2)

        left_point_x = (
            control_point[0] + self.track_width * -gradient[1] / gradient_magnitude
        )
        left_point_y = (
            control_point[1] + self.track_width * gradient[0] / gradient_magnitude
        )

        right_point_x = (
            control_point[0] - self.track_width * -gradient[1] / gradient_magnitude
        )
        right_point_y = (
            control_point[1] - self.track_width * gradient[0] / gradient_magnitude
        )

        return ((left_point_x, left_point_y), (right_point_x, right_point_y))

    def construct_boundaries(self):
        left = []
        right = []
        for i in range(len(self.control_points)):
            (l, r) = self.calculate_boundary(i)
            left.append(l)
            right.append(r)
        self.left_boundary = self.interpolate_points(left)
        self.right_boundary = self.interpolate_points(right)

    def normalize_vector(self, v):
        mag = math.sqrt(v[0] ** 2 + v[1] ** 2)
        return (v[0] / mag, v[1] / mag)

    def shortest_path(self):
        # https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_RacingLines.cpp#L351
        iterations = 100
        racing_points = [x for x in self.control_points]
        spline_displacement = [0 for _ in self.control_points]

        for _ in range(iterations):
            for i in range(len(self.control_points)):
                prev_point = racing_points[
                    (i + len(racing_points) - 1) % len(racing_points)
                ]
                current_point = racing_points[i]
                next_point = racing_points[(i + 1) % len(racing_points)]

                vector_to_prev = (
                    prev_point[0] - current_point[0],
                    prev_point[1] - current_point[1],
                )
                vector_to_next = (
                    next_point[0] - current_point[0],
                    next_point[1] - current_point[1],
                )

                bisecting_vector = (
                    vector_to_prev[0] + vector_to_next[0],
                    vector_to_prev[1] + vector_to_next[1],
                )
                normalized_bisecting_vector = self.normalize_vector(bisecting_vector)

                normalized_gradient = self.normalize_vector(
                    self.get_spline_gradient(i, self.control_points)
                )
                dot_product = (
                    -normalized_gradient[1] * normalized_bisecting_vector[0]
                    + normalized_gradient[0] * normalized_bisecting_vector[1]
                )

                spline_displacement[i] += dot_product * 0.3

            for i in range(len(self.control_points)):
                if spline_displacement[i] >= self.track_width:
                    spline_displacement[i] = self.track_width
                if spline_displacement[i] <= -self.track_width:
                    spline_displacement[i] = -self.track_width

                normalized_gradient = self.normalize_vector(
                    self.get_spline_gradient(i, self.control_points)
                )

                tx = (
                    self.control_points[i][0]
                    + -normalized_gradient[1] * spline_displacement[i]
                )
                ty = (
                    self.control_points[i][1]
                    + normalized_gradient[0] * spline_displacement[i]
                )

                racing_points[i] = (tx, ty)

        return self.interpolate_points(racing_points)

    def interpolate_points(self, points, increment=0.01):
        t = 0
        increment = 0.01
        interpolated_line = []
        while t < len(points):
            interpolated_line.append(self.get_spline_point(t, points=points))
            t += increment
        return interpolated_line

    def draw_circuit(self):
        plt.figure()
        racing_points = self.shortest_path()
        plt.plot([t[0] for t in self.left_boundary], [t[1] for t in self.left_boundary])
        plt.plot(
            [t[0] for t in self.right_boundary], [t[1] for t in self.right_boundary]
        )
        plt.plot([t[0] for t in racing_points], [t[1] for t in racing_points])

        plt.axis([-10, 260, -50, 280])
        plt.show()
