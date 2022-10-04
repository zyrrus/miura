from math import sqrt 

import bpy


class ORI_OP_debug_cell_point(bpy.types.Operator):
    bl_idname = "ori.debug_cell_point"
    bl_label = "Cell Point"

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori

        r = ori_props.cell_r
        r_root3 = r * sqrt(3)

        # Get selected object
        so = bpy.context.active_object

        # Change spheres depending on selected points
        if ori_props.debug_cell_point == 'OP1':
            c1, c2, c3 = nw, ne, c
            r1, r2, r3 = r, r, r
        elif ori_props.debug_cell_point == 'OP2':
            c1, c2, c3 = nw, sw, n
            r1, r2, r3 = r, r, r_root3
        elif ori_props.debug_cell_point == 'OP3':
            c1, c2, c3 = sw, se, ne
            r1, r2, r3 = r_root3, r_root3, r
        elif ori_props.debug_cell_point == 'OP4':
            c1, c2, c3 = ne, se, n
            r1, r2, r3 = r, r, r_root3
        elif ori_props.debug_cell_point == 'OP5':
            c1, c2, c3 = sw, se, c
            r1, r2, r3 = r, r, r
        else:
            return {'FINISHED'}

        # Draw spheres
        bpy.ops.mesh.primitive_ico_sphere_add(location=c1, radius=r1, subdivisions=4)
        bpy.ops.mesh.primitive_ico_sphere_add(location=c2, radius=r2, subdivisions=4)
        bpy.ops.mesh.primitive_ico_sphere_add(location=c3, radius=r3, subdivisions=4)
        
        return {'FINISHED'}

