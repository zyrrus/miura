from math import sqrt

import bpy
import numpy as np


class Cell: 
    tri_side = 0        # r
    tri_height = 0      # r * sqrt(3)/2 
    orientation = ''    # 'up' | 'left'
    mesh_name = ''

    def __init__(self, row, col):
        long_side, short_side = Cell.tri_side * 2, Cell.tri_height * 2
        x_len, y_len = (short_side, long_side) if Cell.orientation == 'up' else (long_side, short_side)
        left, up = np.array([x_len, 0, 0]), np.array([0, y_len, 0])

        # Gen verts
        self.sw = (col * left) + (row * up)
        self.se = self.sw + left
        self.nw = self.sw + up
        self.ne = self.se + up
        self.verts = [self.sw, self.se, self.ne, self.nw]

        # Gen faces
        self.face = [(0, 1, 2, 3)]

        self.gen_mesh(self.verts, self.face)


    def gen_mesh(self, verts, faces):
        # Create Mesh Datablock 
        mesh = bpy.data.meshes.new(Cell.mesh_name) 
        mesh.from_pydata(verts, [], faces) 

        # Create Object and link to scene 
        obj = bpy.data.objects.new(Cell.mesh_name, mesh) 
        bpy.context.scene.collection.objects.link(obj) 

        # Select the object 
        bpy.context.view_layer.objects.active = obj



class ORI_OP_generate_grid(bpy.types.Operator):
    bl_idname = 'ori.generate_grid'
    bl_label = 'Generate Grid'

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori

        name = ori_props.cell_name
        oriented_up = ori_props.cell_orientation
        orientation = "up" if oriented_up else "left"
        r = ori_props.cell_r
        r3 = r * sqrt(3)/2
        rows = ori_props.cell_rows
        cols = ori_props.cell_cols
        
        # Generate verts
        long_side, short_side = r * 2, r3 * 2
        x_len, y_len = (short_side, long_side) if oriented_up else (long_side, short_side)
        num_row_verts, num_col_verts = cols + 1, rows + 1
        left, up = np.array([x_len, 0, 0]), np.array([0, y_len, 0])
        half_x, half_y = (x_len * cols) / 2, (y_len * rows) / 2
        

        x_values =  [(i * x_len) - half_x for i in range(0, num_row_verts)]
        y_values =  [(i * y_len) - half_y for i in range(0, num_col_verts)]
        
        def face(x, y):
            sw = (num_col_verts * x) + y
            nw = sw + 1
            ne = nw + num_col_verts
            se = ne - 1 
            return (sw, se, ne, nw)
        
        verts = [(x, y, 0) for x in x_values for y in y_values]
        edges = []
        faces = [face(x, y) for x in range(0, cols) for y in range(0, rows)]
        
        # Create Mesh Datablock 
        mesh = bpy.data.meshes.new(name) 
        mesh.from_pydata(verts, edges, faces) 

        # Create Object and link to scene 
        obj = bpy.data.objects.new(name, mesh) 
        bpy.context.scene.collection.objects.link(obj) 

        # Select the object 
        bpy.context.view_layer.objects.active = obj





        # Clean up mesh
        # - select all objects
        # - join cell meshes
        # - merge verts
        # bpy.ops.object.select_all(action='SELECT')
        # bpy.ops.object.join()
        # bpy.ops.object.mode_set(mode='EDIT')
        # bpy.ops.mesh.remove_doubles()
        # bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}