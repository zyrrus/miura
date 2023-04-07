from math import sqrt, atan2

import bpy
import mathutils
import numpy as np

from miura.utils.phi import Hyperboloid, get_rotation_matrix
from miura.utils.visualize import debug_vector, debug_orientation


def reorient_obj(obj, orientation, new_pos):
    rotation_matrix = get_rotation_matrix(
        orientation.x, orientation.y, orientation.normal).to_4x4().transposed()
    translation_matrix = mathutils.Matrix.Translation(new_pos)
    transformation_matrix = translation_matrix @ rotation_matrix
    obj.matrix_world = transformation_matrix


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
            reorient_obj(cell, orientation, new_pos)

        return {'FINISHED'}
