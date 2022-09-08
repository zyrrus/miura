import bpy


class ORI_OP_generate_grid(bpy.types.Operator):
    bl_idname = "ori.generate_grid"
    bl_label = "Generate Grid"

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori
        name = ori_props.domain_name
        x_size, y_size = ori_props.domain_x_size, ori_props.domain_y_size
        x_cells, y_cells = ori_props.domain_x_cells, ori_props.domain_y_cells
        
        # Generate verts
        vx, vy = x_cells + 1, y_cells + 1
        half_x, half_y = x_size/2, y_size/2
        x_values =  [(i * x_size/x_cells) - half_x for i in range(0, vx)]
        y_values =  [(i * y_size/y_cells) - half_y for i in range(0, vy)]
        
        def face(x, y):
            bl = (vy * x) + y
            tl = bl + 1
            tr = tl + vy
            br = tr - 1 
            return (bl, tl, tr, br)
        
        verts = [(x, y, 0) for x in x_values for y in y_values]
        edges = []
        faces = [face(x, y) for x in range(0, x_cells) for y in range(0, y_cells)]
        
        # Create Mesh Datablock 
        mesh = bpy.data.meshes.new(name) 
        mesh.from_pydata(verts, edges, faces) 

        # Create Object and link to scene 
        obj = bpy.data.objects.new(name, mesh) 
        bpy.context.scene.collection.objects.link(obj) 

        # Select the object 
        bpy.context.view_layer.objects.active = obj
        
        return {'FINISHED'}