import bpy

from miura.panels.root import ORI_PT_main_panel
from miura.ops.transform_mesh import ORI_OP_transform_mesh


# Panel docs
# https://docs.blender.org/api/current/bpy.types.Panel.html?#bpy.types.Panel.bl_space_type

class ORI_PT_transformation_panel(ORI_PT_main_panel, bpy.types.Panel):
    bl_category = "Miura"
    bl_label = "Mesh Transformation"
    # bl_description
    bl_idname = "ORI_PT_transformation_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        ori_props = context.scene.ori
        
        col = self.layout.column()
        col = self.layout.column()
        col.label(text="Transform Mesh:")
        col.prop(ori_props, "phi_functions")
        col.operator(ORI_OP_transform_mesh.bl_idname, text="Transform Mesh")
        
        