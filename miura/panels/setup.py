import bpy

from miura.panels.root import ORI_PT_root_panel
from miura.ops.gen_domain import ORI_OP_generate_domain
from miura.ops.transform_domain import ORI_OP_transform_domain

class ORI_PT_setup_panel(ORI_PT_root_panel, bpy.types.Panel):
    bl_category = "Miura"
    bl_label = "Setup"
    bl_idname = "ORI_PT_setup_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    
    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        ori_props = context.scene.ori
        
        col = self.layout.column()
        col.label(text="Initialize Parameters:")
        col.prop(ori_props, "paper_theta")
        col.prop(ori_props, "x_cell_count")

        col.label(text="Operations:")
        col.operator(ORI_OP_generate_domain.bl_idname, text="Generate Domain")
        col.operator(ORI_OP_transform_domain.bl_idname, text="Transform Domain")
        
