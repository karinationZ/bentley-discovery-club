"""Headless Blender capstone: make the rigged Bentley TALK a line, driven by Rhubarb visemes.
Adds a rough toothless JawOpen shape key (no teeth — pure jaw drop), keyframes it from Rhubarb mouth
cues, and renders a head close-up. Proves the full free pipeline: rig + Rhubarb -> talking, $0/shot.
Run: blender -b --python build_talking.py -- <glb> <vo.mp3> "<transcript>" <rhubarb_bin> <out_dir>
"""
import bpy, math, sys, os, json, subprocess
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
GLB, VO, TRANS, RHUBARB, OUT = a[0], a[1], a[2], a[3], a[4]
FPS = 24
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
mlist = [o for o in bpy.data.objects if o.type == "MESH"]
mesh = max(mlist, key=lambda o: len(o.data.vertices))   # the real 231k-vert mesh, not the stray Icosphere
for o in mlist:
    if o is not mesh:
        bpy.data.objects.remove(o, do_unlink=True)
mw = mesh.matrix_world
co = [mw @ v.co for v in mesh.data.vertices]          # world-space verts
xs = [c.x for c in co]; ys = [c.y for c in co]; zs = [c.z for c in co]
xmn, xmx = min(xs), max(xs); zmn, zmx = min(zs), max(zs)
hz = zmn + 0.52 * (zmx - zmn)   # head height (used for camera framing)

# Bentley faces +X; head bone ~ (0.09, 0, 0.47). Muzzle = forward (+X) of the head, at head height.
muzzle = [i for i, c in enumerate(co) if c.x > 0.40 and 0.18 < c.z < 0.62]
mz = [co[i].z for i in muzzle] or [0]
jawcut = min(mz) + 0.50 * (max(mz) - min(mz))
jaw = [i for i in muzzle if co[i].z < jawcut]          # lower muzzle = the jaw
print("muzzle verts:", len(muzzle), "jaw verts:", len(jaw))

# toothless JawOpen shape key: drop the jaw verts straight down (world -Z), no teeth involved
mesh.shape_key_add(name="Basis")
sk = mesh.shape_key_add(name="JawOpen")
mwi = mw.inverted()
drop = (zmx - zmn) * 0.07
for i in jaw:
    sk.data[i].co = mwi @ (co[i] + Vector((0, 0, -drop)))
sk.value = 0.0

# Rhubarb visemes -> open amount
wav = os.path.join(OUT, "line.wav")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-ar", "44100", "-ac", "1", wav], check=True)
tf = os.path.join(OUT, "line.txt"); open(tf, "w").write(TRANS)
cues = json.loads(subprocess.check_output([RHUBARB, "-f", "json", "--dialogFile", tf, wav]).decode())["mouthCues"]
dur = cues[-1]["end"]
OPEN = {"X": 0.0, "A": 0.05, "B": 0.30, "C": 0.60, "D": 0.95, "E": 0.75, "F": 0.40, "G": 0.35, "H": 0.45}
sc = bpy.context.scene; sc.render.fps = FPS
for c in cues:
    sk.value = OPEN.get(c["value"], 0.3)
    sk.keyframe_insert("value", frame=int(round(c["start"] * FPS)) + 1)
sc.frame_start = 1; sc.frame_end = int(round(dur * FPS)) + 2

# head close-up camera (front, +X)
hc = Vector((xmx - (xmx - xmn) * 0.10, (min(ys) + max(ys)) / 2, hz + (zmx - hz) * 0.45))
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); bpy.context.collection.objects.link(cam); sc.camera = cam
cam.location = hc + Vector(((xmx - xmn) * 1.15, -(xmx - xmn) * 0.45, (zmx - zmn) * 0.12))
cam.rotation_euler = (hc - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.lens = 50

sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")); bpy.context.collection.objects.link(sun)
sun.data.energy = 4.0; sun.rotation_euler = (math.radians(55), 0, math.radians(30))
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.9, 0.92, 0.97, 1); bg.inputs[1].default_value = 1.3
for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
    try:
        sc.render.engine = eng; break
    except Exception:
        pass
sc.render.resolution_x = sc.render.resolution_y = 480
sc.render.filepath = os.path.join(OUT, "f_")
print("engine:", sc.render.engine, "frames:", sc.frame_end)
bpy.ops.render.render(animation=True)
print("DONE")
