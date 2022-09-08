import bpy

from miura.ops.transform_mesh import ORI_OP_transform_mesh
from miura.ops.gen_grid_mesh import ORI_OP_generate_grid


# Panel docs
# https://docs.blender.org/api/current/bpy.types.Panel.html?#bpy.types.Panel.bl_space_type

class ORI_PT_main_panel(bpy.types.Panel):
    bl_category = "Miura"
    bl_label = "Miura Ori"
    bl_idname = "ORI_PT_main_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    
        
        