import bpy
import numpy as np

from miura.utils.quad import quad_to_miura


class ORI_OP_overlay_ori(bpy.types.Operator):
    bl_idname = "ori.ori"
    bl_label = "Overlay Ori"

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori
        r = ori_props.cell_r
        oriented_up = ori_props.cell_orientation
        should_flip_normals = ori_props.cell_flip_normals

        # Get selected object
        so = bpy.context.active_object

        # Transform vertices
        verts = so.data.vertices
        faces = so.data.polygons


        so.hide_set(True)
        so.select_set(False)
        
        for face in faces:
            vert_indices = face.vertices
            vert_coords = [np.array(verts[v_i].co) for v_i in vert_indices]
            (sw, se, ne, nw) = vert_coords

            normal = np.array(face.normal) * (-1 if should_flip_normals else 1)

            if oriented_up:
                quad_to_miura(nw, ne, se, sw, r, normal)
            else:
                quad_to_miura(ne, se, sw, nw, r, normal)

        # Select first object
        cells = list(filter(lambda obj: 'Cell' in obj.name, bpy.data.objects))
        cells.sort(key=lambda obj: obj.name)
        bpy.context.view_layer.objects.active = cells[0]

        # Mesh clean up
        # bpy.ops.object.join()
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.remove_doubles()
        # bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}
