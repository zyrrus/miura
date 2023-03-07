import bpy
from mathutils import Vector

def debug_vector(position, direction, length=0.2, name="Debug Cone"):
    # create the cone mesh
    bpy.ops.mesh.primitive_cone_add(radius1=0.01, depth=length)
    obj = bpy.context.active_object
    
    # set the rotation of the cone to point in the direction of the vector
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_mode = 'QUATERNION'
    obj.rotation_quaternion = rot_quat
    
    obj.location = position

    # set the name of the cone object
    obj.name = name
    
def debug_orientation(x, y, z, pos, name="Debug Cube"):
    # Create a new mesh object
    mesh = bpy.data.meshes.new(name)

    x = x * 0.1
    y = y * 0.1
    z = z * 0.1

    # Define the vertices of the rectangular prism
    vertices = [Vector((0, 0, 0)), y, x + y, x, z, y + z, x + y + z, x + z]

    # Define the faces of the rectangular prism
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7)
    ]

    # Create the mesh
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    # Create a new object and link it to the scene
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)

    # Set the position of the object
    obj.location = pos

    # Return the new object
    return obj
