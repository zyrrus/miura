from math import sqrt

import bpy
import mathutils
import numpy as np

from miura.utils.phi import Hyperboloid


class ORI_OP_generate_domain(bpy.types.Operator):
    bl_idname = 'ori.generate_domain'
    bl_label = 'Generate Domain'

    def execute(self, context):
        # Get props
        ori_props = context.scene.ori
        theta = ori_props.paper_theta
        x_cell_count = ori_props.x_cell_count

        hyperboloid = Hyperboloid(theta)
        domain = hyperboloid.get_domain()
        cell_details = hyperboloid.get_cell_details(x_cell_count)

        gb = GridBuilder(cell_details.x_cell_count, cell_details.y_cell_count, domain.x_origin,
                         domain.y_origin, cell_details.cell_width, cell_details.cell_height)
        gb.generate()

        return {'FINISHED'}


class GridCell:
    def __init__(self, x, y, width, height):
        # (x, y) = origin
        self.x = x
        self.y = y
        self.w = width
        self.h = height

        self.verts = self.get_points()

    def get_points(self):
        v = mathutils.Vector
        tri_length = self.h / 2                # r
        tri_height = tri_length * sqrt(3) / 2  # height of triangle
        half_tri_length = tri_length / 2       # r/2

        up = v((tri_length, 0, 0))
        up_and_over = v((half_tri_length, tri_height, 0))

        se = v((0, 0, 0))
        sw = v((0, self.w, 0))
        ne = v((self.h, 0, 0))
        nw = v((self.h, self.w, 0))
        s = se + up_and_over
        c = s + up
        n = c + up
        e = se + up
        w = sw + up
        #      [ 0   1   2   3  4  5  6  7  8]
        return [sw, se, ne, nw, s, c, n, e, w]

    def build_mesh(self):
        verts = self.verts
        faces = [(0, 4, 8), (8, 5, 4), (8, 5, 3), (3, 5, 6),
                 (6, 5, 2), (2, 7, 5), (5, 7, 4), (4, 7, 1)]

        # Create Mesh Datablock
        mesh = bpy.data.meshes.new('Cell')
        mesh.from_pydata(verts, [], faces)

        # Create Object and link to scene
        self.obj = bpy.data.objects.new("Cell", mesh)
        bpy.context.scene.collection.objects.link(self.obj)

        pos = mathutils.Vector((self.x, self.y, 0))
        self.obj.matrix_basis = mathutils.Matrix.Translation(pos)

    def move_obj_origin(self):
        old_loc = self.obj.location
        new_loc = mathutils.Vector(
            (self.x + (self.h * 3/4), self.y + self.w/2, 0))
        for vert in self.obj.data.vertices:
            vert.co -= new_loc - old_loc
        self.obj.location = new_loc


class GridBuilder:
    def __init__(self, x_cell_count, y_cell_count, x_offset, y_offset, cell_width, cell_height):
        self.x_cell_count = int(x_cell_count)
        self.y_cell_count = int(y_cell_count)
        self.cells = []
        self.origin = (x_offset, y_offset)
        self.cell_width = cell_width
        self.cell_height = cell_height

    def generate(self):
        origin_x = self.origin[0]
        origin_y = self.origin[1]

        for r in range(self.y_cell_count):
            row = []

            for c in range(self.x_cell_count):
                cell = GridCell(origin_x + (self.cell_height * c), origin_y +
                                (self.cell_width * r), self.cell_width, self.cell_height)
                cell.build_mesh()
                cell.move_obj_origin()
                row.append(cell)

            self.cells.append(row)
