#!/usr/bin/env python
"""
Blender rendering script for MeshMaker example objects.
This script uses Blender's Python API to render 3D objects with proper lighting.
"""

import sys
import os


def render_obj_with_blender(obj_file, output_image, resolution=(1920, 1080), samples=128):
    """
    Render an OBJ file using Blender with proper lighting setup.
    
    Args:
        obj_file: Path to the OBJ file to render
        output_image: Path to save the rendered image
        resolution: Tuple of (width, height) for output image
        samples: Number of render samples for quality
    """
    try:
        import bpy
    except ImportError:
        print("Error: This script must be run with Blender's Python interpreter")
        print("Usage: blender --background --python render_with_blender.py -- <obj_file> <output_image>")
        sys.exit(1)
    
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Import the OBJ file
    print(f"Importing OBJ file: {obj_file}")
    bpy.ops.wm.obj_import(filepath=obj_file)
    
    # Get the imported object
    imported_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    if not imported_objects:
        print("Error: No mesh objects found in OBJ file")
        sys.exit(1)
    
    # Join all imported objects if there are multiple
    if len(imported_objects) > 1:
        bpy.context.view_layer.objects.active = imported_objects[0]
        bpy.ops.object.join()
    
    obj = bpy.context.active_object
    
    # Parse colors from OBJ file comments
    colors_from_obj = parse_obj_colors(obj_file)
    
    # Apply materials with vertex colors
    if colors_from_obj:
        apply_vertex_colors(obj, colors_from_obj)
    
    # Center the object
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.location = (0, 0, 0)
    
    # Calculate object dimensions for camera placement
    dimensions = obj.dimensions
    max_dim = max(dimensions.x, dimensions.y, dimensions.z)
    
    # Set up camera
    bpy.ops.object.camera_add(location=(max_dim * 2, -max_dim * 2, max_dim * 1.5))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)  # Angle the camera nicely
    
    # Point camera at origin
    direction = camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    
    bpy.context.scene.camera = camera
    
    # Set up lighting - three-point lighting setup
    # Key light (main light)
    bpy.ops.object.light_add(type='SUN', location=(max_dim * 3, -max_dim * 2, max_dim * 4))
    key_light = bpy.context.active_object
    key_light.data.energy = 2.0
    key_light.data.angle = 0.5
    
    # Fill light (softer, from opposite side)
    bpy.ops.object.light_add(type='AREA', location=(-max_dim * 2, -max_dim, max_dim * 2))
    fill_light = bpy.context.active_object
    fill_light.data.energy = 150
    fill_light.data.size = max_dim * 2
    
    # Back light (rim light)
    bpy.ops.object.light_add(type='AREA', location=(0, max_dim * 3, max_dim * 2))
    back_light = bpy.context.active_object
    back_light.data.energy = 100
    back_light.data.size = max_dim * 1.5
    
    # Set up world background
    bpy.context.scene.world.use_nodes = True
    bg_node = bpy.context.scene.world.node_tree.nodes['Background']
    bg_node.inputs[0].default_value = (0.05, 0.05, 0.05, 1.0)  # Dark background
    bg_node.inputs[1].default_value = 0.5  # Strength
    
    # Render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = samples
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.context.scene.render.film_transparent = True  # Transparent background
    
    # Set output path
    bpy.context.scene.render.filepath = output_image
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # Render
    print(f"Rendering to: {output_image}")
    bpy.ops.render.render(write_still=True)
    print(f"Render complete: {output_image}")


def parse_obj_colors(obj_file):
    """
    Parse vertex colors from OBJ file comments.
    Returns a list of RGBA tuples.
    """
    colors = []
    with open(obj_file, 'r') as f:
        for line in f:
            if line.startswith('v ') and '# color:' in line:
                # Extract color from comment
                comment_part = line.split('# color:')[1].strip()
                color_values = [float(x) for x in comment_part.split()]
                if len(color_values) >= 3:
                    # Ensure we have RGBA (add alpha if missing)
                    if len(color_values) == 3:
                        color_values.append(1.0)
                    colors.append(tuple(color_values[:4]))
    return colors


def apply_vertex_colors(obj, colors):
    """
    Apply vertex colors to the mesh object.
    """
    import bpy
    
    mesh = obj.data
    
    # Create a new material
    mat = bpy.data.materials.new(name="VertexColorMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add nodes for vertex color shader
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    color_attr_node = nodes.new(type='ShaderNodeAttribute')
    
    # Set attribute name for vertex colors
    color_attr_node.attribute_name = 'Col'
    
    # Connect nodes
    links.new(color_attr_node.outputs['Color'], bsdf_node.inputs['Base Color'])
    links.new(color_attr_node.outputs['Alpha'], bsdf_node.inputs['Alpha'])
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    # Set material properties
    mat.blend_method = 'BLEND'  # Enable transparency
    bsdf_node.inputs['Roughness'].default_value = 0.5
    bsdf_node.inputs['Metallic'].default_value = 0.0
    
    # Assign material to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    
    # Create vertex color layer
    if 'Col' not in mesh.vertex_colors:
        mesh.vertex_colors.new(name='Col')
    
    color_layer = mesh.vertex_colors['Col']
    
    # Apply colors to each loop (vertex instance in a face)
    if len(colors) == len(mesh.vertices):
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                loop = mesh.loops[loop_index]
                vertex_index = loop.vertex_index
                if vertex_index < len(colors):
                    color_layer.data[loop_index].color = colors[vertex_index]


def main():
    """Main entry point for the script."""
    # When run through Blender, arguments after '--' are passed to the script
    import sys
    
    # Find where script arguments start
    try:
        script_args_start = sys.argv.index('--') + 1
        script_args = sys.argv[script_args_start:]
    except ValueError:
        script_args = []
    
    if len(script_args) < 2:
        print("Usage: blender --background --python render_with_blender.py -- <obj_file> <output_image> [width] [height] [samples]")
        print("\nExample:")
        print("  blender --background --python render_with_blender.py -- example_house.obj house_render.png 1920 1080 128")
        sys.exit(1)
    
    obj_file = script_args[0]
    output_image = script_args[1]
    
    # Optional arguments
    width = int(script_args[2]) if len(script_args) > 2 else 1920
    height = int(script_args[3]) if len(script_args) > 3 else 1080
    samples = int(script_args[4]) if len(script_args) > 4 else 128
    
    if not os.path.exists(obj_file):
        print(f"Error: OBJ file not found: {obj_file}")
        sys.exit(1)
    
    render_obj_with_blender(obj_file, output_image, resolution=(width, height), samples=samples)


if __name__ == "__main__":
    main()
