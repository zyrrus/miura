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

        # Cells point up in the end
        cell_height = domain.width / x_cell_count
        r = cell_height / 2
        cell_width = cell_height * sqrt(3) / 2
        y_cell_count = domain.height // cell_width

        # Cells point sideways in the end
        # cell_width = domain.width / x_cell_count
        # r = cell_width / sqrt(3)
        # cell_height = 2 * r
        # y_cell_count = domain.height // cell_height

        gb = GridBuilder(domain.width, domain.height, x_cell_count,
                         y_cell_count, domain.x_origin, domain.y_origin)
        gb.generate()

        return {'FINISHED'}


class GridCell:
    def __init__(self, x, y, width, height):
        # (x, y) = bottom left corner
        self.x = x
        self.y = y
        self.w = width
        self.h = height

        self.get_points()

    def get_points(self):
        self.sw = (0, 0, 0)
        self.se = (self.w, 0, 0)
        self.ne = (self.w, self.h, 0)
        self.nw = (0, self.h, 0)

    def build_mesh(self):
        verts = [self.sw, self.se, self.ne, self.nw]
        faces = [(0, 1, 2, 3)]

        # Create Mesh Datablock
        mesh = bpy.data.meshes.new('Cell')
        mesh.from_pydata(verts, [], faces)

        # Create Object and link to scene
        obj = bpy.data.objects.new("Cell", mesh)
        bpy.context.scene.collection.objects.link(obj)

        pos = mathutils.Vector((self.x, self.y, 0))
        obj.matrix_basis = mathutils.Matrix.Translation(pos)


class GridBuilder:
    def __init__(self, width, height, x_cell_count, y_cell_count, x_offset, y_offset):
        self.width = width
        self.height = height
        self.x_cell_count = int(x_cell_count)
        self.y_cell_count = int(y_cell_count)
        self.cells = []
        self.origin = (x_offset, y_offset)

    def generate(self):
        cell_width = self.width / self.x_cell_count
        cell_height = self.height / self.y_cell_count

        origin_x = self.origin[0]
        origin_y = self.origin[1]

        for r in range(self.y_cell_count):
            row = []

            for c in range(self.x_cell_count):
                cell = GridCell(origin_x + (cell_width * c), origin_y +
                                (cell_height * r), cell_width, cell_height)
                cell.build_mesh()
                row.append(cell)

            self.cells.append(row)
