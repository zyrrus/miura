import bpy
import numpy as np
from numpy import sqrt, dot, cross                       
from numpy.linalg import norm


def quad_to_miura(nw, ne, se, sw, r, normal):
    '''
    If the cell is 'pointed' upwards:
        NW /\ NE
          |  |
          |/\|
        SW    SE
    '''

    r_root3 = r * sqrt(3)

    try:
        # c = get_intersection_point(normal, True,  nw, ne, sw, r, r, r_root3)
        # n = get_intersection_point(normal, True, nw, ne, c, r, r, r)
        # e = get_intersection_point(normal, True,  ne, se, c, r, r, r)
        # s = get_intersection_point(normal, False, sw, se, c, r, r, r)
        # w = get_intersection_point(normal, True,  sw, nw, c, r, r, r)

        c = get_intersection_point(normal, True, sw, se, ne, r_root3, r_root3, r, debug=False)
        n = get_intersection_point(normal, True, nw, ne, c, r, r, r, debug=False)
        s = get_intersection_point(normal, True, sw, se, c, r, r, r, debug=False)
        w = get_intersection_point(normal, True, nw, sw, n, r, r, r_root3, debug=False)
        e = get_intersection_point(normal, True, ne, se, n, r, r, r_root3, debug=False)

        build_cell_mesh(nw, ne, se, sw, n, e, s, w, c)
    except:
        pass


def get_intersection_point(normal_dir, want_normal_side, c1, c2, c3, r1, r2, r3, debug=False):
    # Get both intersection points
    p1, p2 = intersect_spheres(c1, c2, c3, r1, r2, r3)

    # Debug spheres
    if debug:
        bpy.ops.mesh.primitive_ico_sphere_add(location=c1, radius=r1, subdivisions=4)
        bpy.ops.mesh.primitive_ico_sphere_add(location=c2, radius=r2, subdivisions=4)
        bpy.ops.mesh.primitive_ico_sphere_add(location=c3, radius=r3, subdivisions=4)

    # Find which is pointing in the normal direction
    p1_is_normal = dot(normal_dir, p1) > 0

    if want_normal_side:
        return p1 if p1_is_normal else p2

    return p2 if p1_is_normal else p1


def intersect_spheres(c1, c2, c3, r1, r2, r3):
    # Pseudocode:
    # intersect(sphere1, sphere2) => circle1
    # circle1.getplane() => plane1
    # intersect(plane1, sphere3) => circle2
    # intersect(circle1, circle2) => (point1, point2)

    temp1 = c2-c1                                        
    e_x = temp1/norm(temp1)                              
    temp2 = c3-c1                                        
    i = dot(e_x,temp2)                                   
    temp3 = temp2 - i*e_x                                
    e_y = temp3/norm(temp3)                              
    e_z = cross(e_x,e_y)                                 
    d = norm(c2-c1)                                      
    j = dot(e_y,temp2)                                   
    x = (r1*r1 - r2*r2 + d*d) / (2*d)                    
    y = (r1*r1 - r3*r3 -2*i*x + i*i + j*j) / (2*j)       
    temp4 = r1*r1 - x*x - y*y                            
    if temp4 < 0:
        raise Exception("The three spheres do not intersect!\n" + \
            f"{c1}, {r1} \n{c2}, {r2} \n{c3}, {r3}");
    z = sqrt(abs(temp4))                                     
    p_12_a = c1 + x*e_x + y*e_y + z*e_z                  
    p_12_b = c1 + x*e_x + y*e_y - z*e_z                  
    return p_12_a, p_12_b    


def build_cell_mesh(nw, ne, se, sw, n, e, s, w, c):
    #       [ 0   1   2   3  4  5  6  7  8]
    verts = [nw, ne, se, sw, n, e, s, w, c]
    faces = [
        # (0, 4, 8), 
        # (0, 8, 7), 
        # (1, 8, 4),
        # (1, 5, 8),
        # (3, 7, 6),
        # (7, 8, 6),
        # (2, 6, 5),
        # (6, 8, 5)
        (0, 4, 8, 7),
        (4, 1, 5, 8),
        (8, 5, 2, 6),
        (8, 6, 3, 7),
    ]
    
    # Put mesh in Blender
    name = "Cell"
    mesh = bpy.data.meshes.new(name) 
    mesh.from_pydata(verts, [], faces) 
    obj = bpy.data.objects.new(name, mesh) 
    bpy.context.scene.collection.objects.link(obj)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    