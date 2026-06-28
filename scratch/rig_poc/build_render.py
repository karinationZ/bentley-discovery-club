"""Headless Blender: load the Tripo-rigged Bentley glb and render turntable angles in EEVEE.
Proves the rigged asset is pipeline-ready in our OWN free renderer (zero per-shot AI cost).
Run: /opt/homebrew/bin/blender --background --python build_render.py -- <glb> <out_dir>
"""
import bpy, math, sys, os
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
GLB, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
meshes = [o for o in bpy.data.objects if o.type == "MESH"]


def world_bbox(objs):
    cos = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    mn = Vector((min(c.x for c in cos), min(c.y for c in cos), min(c.z for c in cos)))
    mx = Vector((max(c.x for c in cos), max(c.y for c in cos), max(c.z for c in cos)))
    return mn, mx


mn, mx = world_bbox(meshes)
center = (mn + mx) / 2
size = mx - mn
r = max(size.x, size.y, size.z)

# light + world
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
bpy.context.collection.objects.link(sun)
sun.data.energy = 4.0
sun.rotation_euler = (math.radians(55), 0, math.radians(35))
w = bpy.data.worlds.new("W"); bpy.context.scene.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.92, 0.93, 0.97, 1); bg.inputs[1].default_value = 1.2

# camera
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

sc = bpy.context.scene
for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
    try:
        sc.render.engine = eng; break
    except Exception:
        continue
sc.render.resolution_x = sc.render.resolution_y = 512
print("engine:", sc.render.engine, "| bbox r=", round(r, 3), "| bones:",
      sum(len(o.data.bones) for o in bpy.data.objects if o.type == "ARMATURE"))

for i, az in enumerate((0, 90, 180, 270)):
    a, el, dist = math.radians(az), math.radians(10), r * 2.7
    cam.location = center + Vector((math.sin(a) * dist, -math.cos(a) * dist, math.sin(el) * dist + size.z * 0.15))
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.render.filepath = os.path.join(OUT, f"angle_{i}.png")
    bpy.ops.render.render(write_still=True)
print("rendered 4 angles ->", OUT)
