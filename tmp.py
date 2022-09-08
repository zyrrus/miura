from math import sqrt, sin, cos, pi
import bpy 

def gen():
    # Settings 
    name = 'Omega' 
    dim = 10
    rows = dim
    columns = dim
    size = (2 * pi)/(dim - 1)

    # Utility functions 
    def vert(column, row): 
        """ Create a single vert """ 
        return ((column * size) - pi, (row * size) - pi, 0) 

    def face(column, row): 
        """ Create a single face """ 
        return (column * rows + row, (column + 1) * rows + row, (column + 1) * rows + 1 + row, column * rows + 1 + row) 

    # Looping to create the grid 
    verts = [vert(x, y) for x in range(columns) for y in range(rows)] 
    faces = [face(x, y) for x in range(columns - 1) for y in range(rows - 1)] 

    # Create Mesh Datablock 
    mesh = bpy.data.meshes.new(name) 
    mesh.from_pydata(verts, [], faces) 

    # Create Object and link to scene 
    obj = bpy.data.objects.new(name, mesh) 
    bpy.context.scene.collection.objects.link(obj) 

    # Select the object 
    bpy.context.view_layer.objects.active = obj

###

def mod():
    def hyperboloid(x, y):
        # φ(x, y) = (ρ(y)cos(αx), ρ(y)sin(αx), z(y))
        
        rho = sqrt(1 + (y * y))
        
        new_x = rho * cos(x)
        new_y = rho * sin(x)
        new_z = y
        
        return (new_x, new_y, new_z)

    so = bpy.context.active_object

    verts = so.data.vertices

    for vert in verts:
        old = vert.co
        vert.co = hyperboloid(old[0], old[1])
    
mod()