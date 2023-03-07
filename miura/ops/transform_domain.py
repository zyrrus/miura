from math import sqrt, atan2

import bpy
import mathutils
import numpy as np

from miura.utils.phi import Hyperboloid, get_rotation_matrix
from miura.utils.visualize import debug_vector, debug_orientation

one_flag = True

def face_normal(obj, orientation, new_pos):
    global one_flag

    rotation_matrix = get_rotation_matrix(orientation.x, orientation.y, orientation.normal).to_4x4().transposed()
    translation_matrix = mathutils.Matrix.Translation(new_pos)
    transformation_matrix = translation_matrix @ rotation_matrix
    obj.matrix_world =  transformation_matrix
    
    # if one_flag: 
    #     origin = new_pos
    #     debug_vector(origin, mathutils.Vector(orientation.normal), name="Normal")
    #     debug_vector(origin, mathutils.Vector(orientation.x), name="Dx")
    #     debug_vector(origin, mathutils.Vector(orientation.y), name="Dy")
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
            # debug_orientation(orientation.x, orientation.y, orientation.normal, new_pos)

            face_normal(cell, orientation, new_pos)
            # cell.location = new_pos

        return {'FINISHED'}