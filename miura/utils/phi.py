from math import sqrt, sin, cos, pi, acos

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

    def calc(self, x, y):
        rho = sqrt((4 * self.c0 * x * x) + 1)
        z = 2 * self.s0 * x
        
        new_x = rho * cos(self.a * x)
        new_y = rho * sin(self.a * x)
        new_z = z
        
        return (new_x, new_y, new_z)

# def hyperboloid(x, y):
#     # φ(x, y) = (ρ(y)cos(αx), ρ(y)sin(αx), z(y))
    
#     # theta = (0, 2pi/3)
#     theta = pi / 3

#     c0 = cos(theta/2)
#     s0 = sin(theta/2)

#     rho = sqrt((4 * c0 * x * x) + 1)
#     z = 2 * s0 * x
#     a = 1 / sqrt(1 - (s0 * s0))
    
#     new_x = rho * cos(a * x)
#     new_y = rho * sin(a * x)
#     new_z = z
    
#     return (new_x, new_y, new_z)