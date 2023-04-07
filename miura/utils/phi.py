import abc
from dataclasses import dataclass
from math import sqrt, sin, cos, pi, acos

import numpy as np
from mathutils import Vector, Matrix


def get_rotation_matrix(x, y, n):
    # Normalize the input vectors
    X = x.normalized()
    Y = y.normalized()
    N = n.normalized()

    # Construct the rotation matrix
    M = Matrix((X, Y, N))

    # Ensure that the determinant of M is +1
    det = X.dot(Y.cross(N))
    if det < 0:
        M[0] *= -1

    return M


@dataclass
class Dimension:
    x_origin: float
    y_origin: float
    width: float
    height: float


@dataclass
class Orientation:
    x: Vector
    y: Vector
    normal: Vector


@dataclass
class CellDetails:
    x_cell_count: int
    y_cell_count: int
    cell_width: float
    cell_height: float


class AbstractPhi(abc.ABC):
    @abc.abstractmethod
    def get_domain(self) -> Dimension:
        pass

    @abc.abstractmethod
    def phi(self, x, y) -> Vector:
        pass

    @abc.abstractmethod
    def phi_x(self, x, y) -> Vector:
        pass

    @abc.abstractmethod
    def phi_y(self, x, y) -> Vector:
        pass

    @abc.abstractclassmethod
    def get_cell_details(self, cell_count) -> CellDetails:
        pass

    def get_orientation(self, x, y) -> Orientation:
        phi_x = self.phi_x(x, y)
        phi_y = self.phi_y(x, y)
        normal = phi_x.cross(phi_y)
        return Orientation(phi_x.normalized(), phi_y.normalized(), normal.normalized())


class Hyperboloid(AbstractPhi):
    def __init__(self, theta):
        self.theta = theta

        self.c0 = cos(theta/2)
        self.s0 = sin(theta/2)
        self.a = 1 / sqrt(1 - (self.s0 * self.s0))
        self.s0_star = sin(0.5 * acos(0.5 / self.c0))

    def get_domain(self):
        #  Ω = [−s0*, s0*] × [0,2π/α]

        dimensions = Dimension(
            x_origin=-self.s0_star,
            y_origin=0,
            width=2 * self.s0_star,
            height=2 * pi / self.a,
        )

        return dimensions

    def phi(self, x, y):
        rho = self.__rho(x)
        new_x = rho * cos(self.a * y)
        new_y = rho * sin(self.a * y)
        new_z = 2 * self.s0 * x

        return Vector([new_x, new_y, new_z])

    def phi_x(self, x, y):
        rho_prime = self.__rho_prime(x)
        new_x = rho_prime * cos(self.a * y)
        new_y = rho_prime * sin(self.a * y)
        new_z = 2 * self.s0

        return Vector([new_x, new_y, new_z])

    def phi_y(self, x, y):
        rho = self.__rho(x)
        new_x = -self.a * rho * sin(self.a * y)
        new_y = self.a * rho * cos(self.a * y)
        new_z = 0

        return Vector([new_x, new_y, new_z])

    def __rho(self, x):
        return sqrt((4 * self.c0 * x * x) + 1)

    def __rho_prime(self, x):
        return 4 * self.c0 * x / sqrt((4 * self.c0 * x * x) + 1)

    def get_cell_details(self, cell_count):
        domain = self.get_domain()

        max_circumference = self.__rho(self.s0_star) * 2 * pi
        cell_width = max_circumference / cell_count
        r = cell_width / sqrt(3)
        cell_height = r * 2
        x_cell_count = domain.width // cell_height

        # Cells point up in the end
        # cell_height = domain.width / cell_count
        # r = cell_height / 2
        # cell_width = r * sqrt(3)
        # y_cell_count = domain.height // cell_width

        # Cells point sideways in the end
        # cell_width = domain.width / cell_count
        # r = cell_width / sqrt(3)
        # cell_height = 2 * r
        # y_cell_count = domain.height // cell_height

        cell_details = CellDetails(
            x_cell_count=x_cell_count,
            y_cell_count=cell_count,
            cell_width=cell_width,
            cell_height=cell_height
        )

        return cell_details
