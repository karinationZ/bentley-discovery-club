"""Presentable 3s talking-Bentley test: rigged glb + Rhubarb-driven toothless JawOpen, hero framing,
3-point light, subtle head sway, 720p EEVEE. Run:
blender -b --python build_talking_v2.py -- <glb> <vo.mp3> "<transcript>" <rhubarb_bin> <out_dir>
"""
import bpy, math, sys, os, json, subprocess
from mathutils import Vector, Euler

a = sys.argv[sys.argv.index("--") + 1:]
GLB, VO, TRANS, RHUBARB, OUT = a[0], a[1], a[2], a[3], a[4]
FPS = 24
os.makedirs(OUT, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
mlist = [o for o in bpy.data.objects if o.type == "MESH"]
mesh = max(mlist, key=lambda o: len(o.data.vertices))
for o in mlist:
    if o is not mesh:
        bpy.data.objects.remove(o, do_unlink=True)
arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
mw = mesh.matrix_world
co = [mw @ v.co for v in mesh.data.vertices]
xs = [c.x for c in co]; ys = [c.y for c in co]; zs = [c.z for c in co]
xmn, xmx = min(xs), max(xs); ymn, ymx = min(ys), max(ys); zmn, zmx = min(zs), max(zs)

# toothless JawOpen shape key
muzzle = [i for i, c in enumerate(co) if c.x > 0.40 and 0.18 < c.z < 0.62]
mz = [co[i].z for i in muzzle] or [0]
jawcut = min(mz) + 0.50 * (max(mz) - min(mz))
jaw = [i for i in muzzle if co[i].z < jawcut]
mesh.shape_key_add(name="Basis")
sk = mesh.shape_key_add(name="JawOpen")
mwi = mw.inverted(); drop = (zmx - zmn) * 0.09
for i in jaw:
    sk.data[i].co = mwi @ (co[i] + Vector((0.02, 0, -drop)))
sk.value = 0.0

# Rhubarb visemes -> keyframes
wav = os.path.join(OUT, "line.wav"); subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", VO, "-ar", "44100", "-ac", "1", wav], check=True)
tf = os.path.join(OUT, "line.txt"); open(tf, "w").write(TRANS)
cues = json.loads(subprocess.check_output([RHUBARB, "-f", "json", "--dialogFile", tf, wav]).decode())["mouthCues"]
dur = min(3.5, cues[-1]["end"])
sc = bpy.context.scene; sc.render.fps = FPS
OPEN = {"X": 0.0, "A": 0.06, "B": 0.34, "C": 0.64, "D": 0.97, "E": 0.80, "F": 0.44, "G": 0.38, "H": 0.48}
for c in cues:
    sk.value = OPEN.get(c["value"], 0.3)
    sk.keyframe_insert("value", frame=int(round(c["start"] * FPS)) + 1)
endf = int(round(dur * FPS))
sc.frame_start = 1; sc.frame_end = endf

# subtle head sway for life
if arm:
    pb = arm.pose.bones.get("tripo::Head_0")
    if pb:
        pb.rotation_mode = "XYZ"
        for f in range(1, endf + 2, 4):
            t = f / FPS
            pb.rotation_euler = Euler((math.radians(2.2 * math.sin(t * 1.6)), math.radians(1.6 * math.sin(t * 1.15)), math.radians(2.4 * math.sin(t * 0.85))), "XYZ")
            pb.keyframe_insert("rotation_euler", frame=f)

# head-and-shoulders front-3/4 portrait; aim between the eyes and muzzle, pulled back
face = Vector((xmn + 0.62 * (xmx - xmn), (ymn + ymx) / 2, zmn + 0.62 * (zmx - zmn)))
hs = zmx - zmn
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); bpy.context.collection.objects.link(cam); sc.camera = cam
cam.location = face + Vector((hs * 1.85, -hs * 0.55, hs * 0.42))
cam.rotation_euler = (face - cam.location).to_track_quat("-Z", "Y").to_euler()
cam.data.lens = 55

# 3-point light + soft tide-pool world
def area(name, e, size, loc):
    L = bpy.data.objects.new(name, bpy.data.lights.new(name, "AREA")); bpy.context.collection.objects.link(L)
    L.data.energy = e; L.data.size = size; L.location = face + loc
    L.rotation_euler = (face - L.location).to_track_quat("-Z", "Y").to_euler(); return L
area("Key", 500, 2.5, Vector((hs * 1.3, -hs * 1.1, hs * 1.3)))
area("Fill", 150, 4.0, Vector((-hs * 1.1, -hs * 0.9, hs * 0.5)))
area("Rim", 300, 2.0, Vector((-hs * 0.6, hs * 1.2, hs * 1.0)))
w = bpy.data.worlds.new("W"); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.45, 0.68, 0.80, 1); bg.inputs[1].default_value = 0.5

for eng in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "CYCLES"):
    try:
        sc.render.engine = eng; break
    except Exception:
        pass
sc.render.resolution_x = 1280; sc.render.resolution_y = 720
sc.render.film_transparent = True                 # alpha, so we can composite over the tide-pool plate
sc.render.image_settings.color_mode = "RGBA"
sc.render.filepath = os.path.join(OUT, "f_")
print("frames:", endf, "jaw verts:", len(jaw), "engine:", sc.render.engine)
bpy.ops.render.render(animation=True)
print("DONE")
