"""Blender product portrait. Pot and removable lid use their exported geometry."""

import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

folder = Path(sys.argv[-1])
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 32
scene.cycles.use_denoising = True
try:
    devices = bpy.context.preferences.addons["cycles"].preferences
    devices.compute_device_type = "OPTIX"
    devices.refresh_devices()
    if any(d.type == "OPTIX" for d in devices.devices):
        for d in devices.devices:
            d.use = d.type == "OPTIX"
        scene.cycles.device = "GPU"
except (RuntimeError, TypeError):
    pass
scene.world = bpy.data.worlds.new("Softbox studio")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.72, 0.78, 0.82, 1)
bg.inputs[1].default_value = 0.55


def material(name, color, roughness):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    shader = m.node_tree.nodes.get("Principled BSDF")
    shader.inputs["Base Color"].default_value = (*color, 1)
    shader.inputs["Roughness"].default_value = roughness
    return m, shader


pp, bs = material("Natural clear polypropylene", (0.96, 0.99, 0.99), 0.13)
bs.inputs["Transmission Weight"].default_value = 0.93
bs.inputs["IOR"].default_value = 1.49
floor, _ = material("Mineral blue studio", (0.11, 0.19, 0.22), 0.43)


def load(name):
    bpy.ops.wm.stl_import(filepath=str(folder / (name + ".stl")))
    obj = bpy.context.object
    obj.data.materials.append(pp)
    bevel = obj.modifiers.new("Mould edge glints", "BEVEL")
    bevel.width = 0.11
    bevel.segments = 3
    obj.modifiers.new("Face normals", "WEIGHTED_NORMAL")
    return obj


body = load("body")
lid = load("lid")
w, l, h = body.dimensions
scale = max(w, l)
# Lift the lid clear of its seating and move it back to expose the interior.
lid.location = (w * 0.46, l * 0.32, h * 0.86)
bpy.ops.mesh.primitive_plane_add(size=scale * 140, location=(0, 0, -0.1))
bpy.context.object.data.materials.append(floor)
target = Vector((w * 0.2, l * 0.16, h * 0.8))
for xyz, power, size in [((-1, -1, 2), 45, 1.35), ((1.4, 0.8, 1.2), 90, 0.8), ((-0.9, 1.8, 0.85), 65, 0.55)]:
    bpy.ops.object.light_add(type="AREA", location=target + Vector(xyz) * scale)
    o = bpy.context.object
    o.rotation_euler = (target - o.location).to_track_quat("-Z", "Y").to_euler()
    o.data.energy = power * scale**2
    o.data.shape = "DISK"
    o.data.size = size * scale
bpy.ops.object.camera_add(location=target + Vector((1.5, -1.15, 0.99)) * scale * 2)
cam = bpy.context.object
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.type = "ORTHO"
cam.data.ortho_scale = scale * 1.85
cam.data.clip_end = scale * 12
scene.camera = cam
scene.render.resolution_x = 1300
scene.render.resolution_y = 950
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(folder / "presentation.png")
bpy.ops.render.render(write_still=True)

# The seated portrait uses the same two meshes and their native assembly coordinates.
lid.location=(0,0,0)
target=Vector((0,0,h*.48))
cam.location=target+Vector((1.50,-1.15,.83))*scale*2
cam.rotation_euler=(target-cam.location).to_track_quat("-Z","Y").to_euler()
cam.data.ortho_scale=scale*1.55
scene.render.filepath=str(folder/"assembled.png")
bpy.ops.render.render(write_still=True)

# glTF uses metres. Bake the studio bevel into two separately selectable meshes.
bpy.ops.object.select_all(action="DESELECT")
depsgraph=bpy.context.evaluated_depsgraph_get()
for source,name in [(body,"Open pot"),(lid,"Removable lid")]:
    mesh=bpy.data.meshes.new_from_object(source.evaluated_get(depsgraph))
    mesh.transform(Matrix.Scale(.001,4))
    obj=bpy.data.objects.new(name,mesh)
    scene.collection.objects.link(obj)
    obj.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(folder/"systempak.glb"),export_format="GLB",use_selection=True,
                          export_yup=True,export_animations=False)
