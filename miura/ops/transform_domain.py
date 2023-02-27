from math import sqrt, atan2

import bpy
import mathutils
import numpy as np

from miura.utils.phi import Hyperboloid, get_rotation_matrix
from miura.utils.visualize import debug_vector

one_flag = True

def face_normal(obj, orientation, new_pos):
    # current_normal = obj.data.polygons[0].normal
    # rotation_matrix = get_rotation_matrix(orientation.x, orientation.y, orientation.normal)
    # euler = rotation_matrix.to_euler()
    # obj.rotation_euler = euler
    
    
    global one_flag
    
    new_normal = orientation.normal
    current_normal = obj.data.polygons[0].normal
    rot_matrix = current_normal.rotation_difference(new_normal)
    z_axis = mathutils.Vector((0, 0, 1))
    align_matrix = z_axis.rotation_difference(obj.data.polygons[0].normal)
    final_matrix = rot_matrix @ align_matrix
    obj.rotation_euler = final_matrix.to_euler()

    if one_flag: 
        origin = new_pos
        debug_vector(origin, mathutils.Vector(orientation.normal).normalized(), name="Normal")
        debug_vector(origin, mathutils.Vector(orientation.x).normalized(), name="Dx")
        debug_vector(origin, mathutils.Vector(orientation.y).normalized(), name="Dy")
        # one_flag = False

class ORI_OP_transform_domain(bpy.types.Operator):
    bl_idname = 'ori.transform_domain'
    bl_label = 'Transform Domain'

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori
        theta = ori_props.paper_theta

        cell_objs = [
            obj for obj in bpy.data.objects if obj.name.startswith("Cell")
        ]

        hyperboloid = Hyperboloid(theta)

        for cell in cell_objs:
            pos = cell.location
            new_pos = hyperboloid.phi(pos.x, pos.y)
            orientation = hyperboloid.get_orientation(pos.x, pos.y)
            face_normal(cell, orientation, new_pos)
            cell.location = new_pos

        return {'FINISHED'}
