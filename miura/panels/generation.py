import bpy

from miura.panels.root import ORI_PT_main_panel
from miura.ops.gen_grid_mesh import ORI_OP_generate_grid


# Panel docs
# https://docs.blender.org/api/current/bpy.types.Panel.html?#bpy.types.Panel.bl_space_type

class ORI_PT_generation_panel(ORI_PT_main_panel, bpy.types.Panel):
    bl_category = "Miura"
    bl_label = "Mesh Generation"
    # bl_description
    bl_idname = "ORI_PT_generation_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    
    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        ori_props = context.scene.ori
        
        col = self.layout.column()
        col.label(text="Mesh Generation:")
        col.prop(ori_props, "cell_name")
        col.prop(ori_props, "cell_orientation")
        col.prop(ori_props, "cell_r")
        col.prop(ori_props, "cell_rows")
        col.prop(ori_props, "cell_cols")
        col.operator(ORI_OP_generate_grid.bl_idname, text="Generate Grid")
        
        