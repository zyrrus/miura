from math import pi, sin, cos, sqrt

import bpy
import numpy as np

from miura.panels.generation import ORI_PT_generation_panel
from miura.panels.transformation import ORI_PT_transformation_panel
from miura.panels.tessellation import ORI_PT_tessellation_panel
from miura.panels.debug import ORI_PT_debug_panel

from miura.ops.gen_grid_mesh import ORI_OP_generate_grid
from miura.ops.transform_mesh import ORI_OP_transform_mesh
from miura.ops.tessellate import ORI_OP_overlay_ori
from miura.ops.debug_cell_point import ORI_OP_debug_cell_point


# Beginner guide
# https://medium.com/geekculture/creating-a-custom-panel-with-blenders-python-api-b9602d890663#:~:text=To%20create%20a%20custom%20panel,this%20class%20in%20the%20bpy.


# ------------------------------------------------------------------------
#    Properties
# ------------------------------------------------------------------------

# Good video about properties
# https://www.youtube.com/watch?v=jZt3MO5D1R8

class ORI_properties(bpy.types.PropertyGroup):
    domain_name: bpy.props.StringProperty(name="Name", default="Omega")
    domain_x_size: bpy.props.FloatProperty(name="X size", soft_min=0, default=2*pi)
    domain_y_size: bpy.props.FloatProperty(name="Y size", soft_min=0, default=2*pi)
    domain_x_cells: bpy.props.IntProperty(name="X cells", soft_min=0, default=10)
    domain_y_cells: bpy.props.IntProperty(name="Y cells", soft_min=0, default=10)

    cell_name: bpy.props.StringProperty(name="Name", default="Guide")
    cell_orientation: bpy.props.BoolProperty(name="Orientated up", description="Facing up = True; Facing right = False.")
    cell_r: bpy.props.FloatProperty(name="r size", description="Size of equilateral triangle sides", soft_min=0, default=1)
    cell_rows: bpy.props.IntProperty(name="Rows", soft_min=0, default=6)
    cell_cols: bpy.props.IntProperty(name="Columns", soft_min=0, default=6)
    cell_flip_normals: bpy.props.BoolProperty(name="Flip normal direction")
    # tessellate_tolerance
    
    phi_functions: bpy.props.EnumProperty(
        name="Functions",
        items=[
            ('OP1', 'Hyperboloid', ''),
            ('OP2', 'N/A', ''),
        ]
    )  

    debug_cell_point: bpy.props.EnumProperty(
        name="Cell point",
        items=[
            ('OP1', 'North', ''),
            ('OP2', 'West', ''),
            ('OP3', 'Center', ''),
            ('OP4', 'East', ''),
            ('OP5', 'South', ''),
            ('OP6', 'N/A', ''),
        ]
    )   



# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = [
    ORI_properties,

    ORI_PT_generation_panel,    
    ORI_PT_transformation_panel,    
    ORI_PT_tessellation_panel,
    ORI_PT_debug_panel,

    ORI_OP_generate_grid,
    ORI_OP_transform_mesh,
    ORI_OP_overlay_ori,
    ORI_OP_debug_cell_point,
]

bl_info = {
    "name" : "Miura Ori",
    "author" : "Zeke Abshire",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D > right-side panel > Miura",
    "warning" : "",
    "category" : "Object"
}


def register():
    for c in classes:
        bpy.utils.register_class(c)
    
    # for k, v in props.items():
    #     setattr(bpy.types.Scene, k, v)
    
    bpy.types.Scene.ori = bpy.props.PointerProperty(type=ORI_properties)
    
def unregister():
    # for k in props.keys():
    #     delattr(bpy.types.Scene, k)
        
    for c in classes:
        bpy.utils.unregister_class(c)
        
    del bpy.types.Scene.ori
