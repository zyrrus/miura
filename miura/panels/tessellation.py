import bpy

from miura.panels.root import ORI_PT_main_panel
from miura.ops.tessellate import ORI_OP_overlay_ori

# Panel docs
# https://docs.blender.org/api/current/bpy.types.Panel.html?#bpy.types.Panel.bl_space_type

class ORI_PT_tessellation_panel(ORI_PT_main_panel, bpy.types.Panel):
    bl_category = "Miura"
    bl_label = "Tessellation"
    # bl_description
    bl_idname = "ORI_PT_tessellation_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        ori_props = context.scene.ori
        
        col = self.layout.column()
        col.label(text="Overlay Tessellation:")
        col.prop(ori_props, "cell_flip_normals")
        col.operator(ORI_OP_overlay_ori.bl_idname, text="Tessellate")
        
        