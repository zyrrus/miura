from math import sqrt, atan2

import bpy
import mathutils
import numpy as np

from miura.utils.phi import Hyperboloid


def face_normal(obj, normal):
    # current_normal = obj.data.polygons[0].normal
    # rot_matrix = current_normal.rotation_difference(normal)
    # obj.rotation_euler = rot_matrix.to_euler()

    # Get the current normal vector of the quad
    current_normal = obj.data.polygons[0].normal

    # Get the rotation matrix that rotates the current normal to the new normal
    rot_matrix = current_normal.rotation_difference(normal)

    # Align the short side of the quad with the Z axis
    z_axis = mathutils.Vector((0, 0, 1))
    align_matrix = z_axis.rotation_difference(obj.data.polygons[0].normal)

    # Combine the two matrices to get the final rotation matrix
    final_matrix = rot_matrix @ align_matrix

    # Rotate the quad using the final rotation matrix
    obj.rotation_euler = final_matrix.to_euler()


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
            new_pos = hyperboloid.calc(pos.x, pos.y)
            normal = hyperboloid.calc_normal(pos.x, pos.y)
            # normal = mathutils.Vector([1, 0, 0])
            face_normal(cell, normal)
            cell.location = new_pos

        return {'FINISHED'}
