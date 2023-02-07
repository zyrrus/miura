from math import sqrt

import bpy
import numpy as np

# import bpy
# from bpy import context
import mathutils
# from mathutils import Matrix
# import math

def track_to_point( obj, point ):
    normal = obj.data.polygons[0].normal.xyz
    mat_obj = obj.matrix_basis
    mat_scale = mathutils.Matrix.Scale(1, 4, mat_obj.to_scale() )
    trans = mat_obj.to_translation()
    mat_trans = mathutils.Matrix.Translation(trans)
    print( "mat_scale\n" + str(mat_obj.to_scale()))
    point_trans = point - trans
    q = normal.rotation_difference( point_trans )
    mat_rot = q.to_matrix()
    mat_rot.resize_4x4()

    mat_obj = mat_trans * mat_rot * mat_scale    
    obj.matrix_basis = mat_obj


class ORI_OP_transform_domain(bpy.types.Operator):
    bl_idname = 'ori.transform_domain'
    bl_label = 'Transform Domain'

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori


        cell_objs = [obj for obj in bpy.data.objects if obj.name.startswith("Cell")]
        for cell in cell_objs:
            track_to_point(cell, mathutils.Vector([0, 0, 0]))


        return {'FINISHED'}