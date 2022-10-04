import bpy

from miura.panels.root import ORI_PT_main_panel


# Panel docs
# https://docs.blender.org/api/current/bpy.types.Panel.html?#bpy.types.Panel.bl_space_type

class ORI_PT_debug_panel(ORI_PT_main_panel, bpy.types.Panel):
    bl_category = "Miura"
    bl_label = "Debug"
    # bl_description
    bl_idname = "ORI_PT_debug_panel"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self, context):
        return True
    
    def draw(self, context):
        ori_props = context.scene.ori
        
        col = self.layout.column()
        col.label("View spheres around cell point:")
        col.prop(ori_props, "debug_cell_point")
        col.operator(ORI_OP_debug_cell_point.bl_idname, text="View Spheres")
        
        