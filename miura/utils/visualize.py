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
    