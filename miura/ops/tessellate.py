import bpy
import numpy as np

from miura.utils.quad import quad_to_miura


class ORI_OP_overlay_ori(bpy.types.Operator):
    bl_idname = "ori.ori"
    bl_label = "Overlay Ori"

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori

        # Get selected object
        so = bpy.context.active_object

        # Compute r
        cell_len = ori_props.domain_x_size / ori_props.domain_x_cells
        r = cell_len / 2

        # Transform vertices
        verts = so.data.vertices
        faces = so.data.polygons
        
        for face in faces:
            vert_indices = face.vertices
            vert_coords = [np.array(verts[v_i].co) for v_i in vert_indices]
            (sw, nw, ne, se) = vert_coords

            # quad_to_miura(nw, ne, se, sw, r, np.array(face.normal))
            quad_to_miura(sw, nw, ne, se, r, np.array(face.normal))

        return {'FINISHED'}
