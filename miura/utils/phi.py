from math import sqrt, sin, cos, pi, acos

import numpy as np
import mathutils


def identity(x, y):
    return (x, y, 0)


class Hyperboloid:
    def __init__(self, theta):
        self.theta = theta

        self.c0 = cos(theta/2)
        self.s0 = sin(theta/2)
        self.a = 1 / sqrt(1 - (self.s0 * self.s0))

    def domain(self):
        #  Ω = [−s0*, s0*] × [0,2π/α]

        s0_star = sin(0.5 * acos(0.5 / self.c0))
        dimensions = {
            "origin_x": -s0_star,
            "origin_y": 0,
            "width": 2 * s0_star,
            "height": 2 * pi / self.a,
        }

        return dimensions

    # def phi(self, x, y)
    # def phi_x(self, x, y)
    # def phi_y(self, x, y)
    # def phi_normal(self, x, y):
    #     return np.cross(self.phi_x, self.phi_y)

    def calc(self, x, y):
        rho = sqrt((4 * self.c0 * x * x) + 1)
        z = 2 * self.s0 * x

        new_x = rho * cos(self.a * y)
        new_y = rho * sin(self.a * y)
        new_z = z

        return mathutils.Vector([new_x, new_y, new_z])

    def calc_normal(self, x, y):
        epsilon = 0.01

        base_point = self.calc(x, y)

        x_shift = x + epsilon
        y_shift = y
        shifted_point = self.calc(x_shift, y_shift)
        shift_x = shifted_point - base_point

        x_shift = x
        y_shift = y + epsilon
        shifted_point = self.calc(x_shift, y_shift)
        shift_y = shifted_point - base_point

        normal = np.cross(shift_x, shift_y)

        return normal
