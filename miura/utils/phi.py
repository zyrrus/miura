from math import sqrt, sin, cos


def identity(x, y):
    return (x, y, 0)

def hyperboloid(x, y):
    # φ(x, y) = (ρ(y)cos(αx), ρ(y)sin(αx), z(y))
    rho = sqrt(1 + (y * y))
    new_x = rho * cos(x)
    new_y = rho * sin(x)
    new_z = y
    return (new_x, new_y, new_z)