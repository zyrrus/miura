from math import pi, sin, cos, sqrt

import bpy
import numpy as np

from miura.panels.setup import ORI_PT_setup_panel
from miura.ops.gen_domain import ORI_OP_generate_domain
from miura.ops.transform_domain import ORI_OP_transform_domain


# ------------------------------------------------------------------------
#    Properties
# ------------------------------------------------------------------------

class ORI_properties(bpy.types.PropertyGroup):
    paper_theta: bpy.props.FloatProperty(
        name="Theta", 
        description="Size of equilateral triangle sides", 
        soft_min=0, 
        soft_max=2*pi/3, 
        default=pi/3
    )
    x_cell_count: bpy.props.IntProperty(
        name="Horizontal Cell Count", 
        description="Number of cells along the X-axis", 
        soft_min=0,
        default=30
    )
    
    phi_functions: bpy.props.EnumProperty(
        name="Functions",
        items=[
            ('OP1', 'Hyperboloid', ''),
            ('OP2', 'N/A', ''),
        ]
    )  


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = [
    # Properties
    ORI_properties,

    # Panels
    ORI_PT_setup_panel,

    # Operators
    ORI_OP_generate_domain,
    ORI_OP_transform_domain
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
    
    bpy.types.Scene.ori = bpy.props.PointerProperty(type=ORI_properties)
    
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        
    del bpy.types.Scene.ori
