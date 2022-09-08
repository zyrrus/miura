from math import sin, cos, sqrt

import bpy

from miura.utils.phi import identity, hyperboloid


class ORI_OP_transform_mesh(bpy.types.Operator):
    bl_idname = "ori.phi"
    bl_label = "Phi"

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori

        # Get selected object
        so = bpy.context.active_object

        # Get function
        if ori_props.phi_functions == 'OP1':
            fn = hyperboloid
        else:
            fn = identity

        # Transform vertices
        verts = so.data.vertices
        for vert in verts:
            old = vert.co
            vert.co = fn(old[0], old[1])
        
        return {'FINISHED'}

