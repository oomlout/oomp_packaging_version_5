"""Render the lightweight dolly GLBs with Blender in background mode."""

from pathlib import Path
import shutil
import subprocess
import sys


def main(**kwargs):
    blender = kwargs.get("blender", "blender")
    from dolly_model import records
    folders = [str(folder / "three_d_model") for folder, part in records(**kwargs)]
    if folders:
        binary = shutil.which(blender)
        if not binary:
            raise RuntimeError("Install Blender or supply blender=<executable>")
        subprocess.run([binary, "-b", "--factory-startup", "--python-exit-code", "1",
                        "-P", str(Path(__file__).resolve()), "--", *folders], check=True)


def render(folder, **kwargs):
    samples = kwargs.get("samples", 20)
    import bpy
    from mathutils import Vector

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = True
    scene.view_settings.view_transform = "Khronos PBR Neutral"
    scene.view_settings.exposure = -0.8
    scene.render.resolution_x = 900
    scene.render.resolution_y = 600
    scene.render.resolution_percentage = 100
    scene.world = bpy.data.worlds.new("Studio")
    scene.world.use_nodes = True
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45
    scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (.82,.86,.90,1)
    bpy.ops.import_scene.gltf(filepath=str(folder / "working.glb"))
    vertices = [obj.matrix_world @ v.co for obj in scene.objects if obj.type == "MESH" for v in obj.data.vertices]
    low = Vector([min(v[i] for v in vertices) for i in range(3)])
    high = Vector([max(v[i] for v in vertices) for i in range(3)])
    centre = (low+high)/2
    span = high.x-low.x
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-.0003))
    floor = bpy.data.materials.new("Studio floor")
    floor.diffuse_color = (.78,.81,.82,1)
    bpy.context.object.data.materials.append(floor)
    for name, offset, power in (("Key", (-1,-2,3), 155), ("Fill", (2,0,2), 90), ("Rim", (-1,2,2), 105)):
        location = Vector(offset)*span
        bpy.ops.object.light_add(type="AREA", location=location)
        lamp = bpy.context.object
        lamp.name = name
        lamp.data.energy = power * span**2
        lamp.data.shape = "DISK"
        lamp.data.size = span*1.6
        lamp.rotation_euler = (centre-location).to_track_quat("-Z","Y").to_euler()
    bpy.ops.object.camera_add(location=centre+Vector((.85,-1.40,.90))*span)
    camera = bpy.context.object
    camera.rotation_euler = (centre-camera.location).to_track_quat("-Z","Y").to_euler()
    camera.data.type = "ORTHO"
    orientation = camera.rotation_euler.to_matrix().inverted()
    visible = [orientation @ (v-centre) for v in vertices]
    width = max(v.x for v in visible)-min(v.x for v in visible)
    height = max(v.y for v in visible)-min(v.y for v in visible)
    camera.data.ortho_scale = max(width, height*1.5)*1.20
    scene.camera = camera
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(folder / "render.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    if "--" in sys.argv:
        for path in sys.argv[sys.argv.index("--")+1:]:
            render(Path(path))
    else:
        main()
