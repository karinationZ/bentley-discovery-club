"""Deterministic talking-line renderer for the Bentley rig.

Drives the jaw BONE from a Rhubarb-derived openness curve (0..1 per frame) and renders a
tight front-3/4 face CU. No generation, no drift, $0/line.

  blender -b <rig.blend> -P render_talk.py -- <openness.json> <outdir> [max_deg]

Then mux with the line's mp3 in ffmpeg. Reusable for any line / any future episode.
"""
import bpy, sys, math, json
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
curvef, outdir = argv[0], argv[1]
MAX_DEG = float(argv[2]) if len(argv) > 2 else 8.5

sc  = bpy.context.scene
arm = bpy.data.objects["Bentley_RIG"]
pb  = arm.pose.bones["jaw"]
pb.rotation_mode = 'XYZ'

# --- drive the jaw from the openness curve ---
cur = json.loads(open(curvef).read())
fps, op = cur["fps"], cur["open"]
N = len(op)
sc.render.fps = fps
sc.frame_start, sc.frame_end = 1, N
# bezier by default so any interpolation reads as speech, not a strobe (5.x-safe: no fcurve API)
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'BEZIER'
for fr, val in enumerate(op, start=1):
    pb.rotation_euler = (-math.radians(MAX_DEG * val), 0, 0)
    pb.keyframe_insert("rotation_euler", frame=fr)

# --- subtle procedural idle on the HEAD bone so she breathes (sway + head-tilt + duck on emphasis) ---
head = arm.pose.bones.get("head")
if head:
    head.rotation_mode = 'XYZ'
    A_nod, A_yaw, A_roll = 1.2, 1.6, 1.0          # degrees — kept small on purpose
    f_nod, f_yaw, f_roll = 0.28, 0.22, 0.16       # Hz — slow drift, not a wobble
    for fr, val in enumerate(op, start=1):
        t = (fr - 1) / fps
        nod  = A_nod * math.sin(2*math.pi*f_nod*t + 0.5) - 0.8 * val   # duck slightly on loud syllables
        roll = A_roll * math.sin(2*math.pi*f_roll*t + 1.0)             # gentle head-tilt
        yaw  = A_yaw * math.sin(2*math.pi*f_yaw*t)
        head.rotation_euler = (math.radians(nod), math.radians(roll), math.radians(yaw))
        head.keyframe_insert("rotation_euler", frame=fr)

# --- use the rig's saved talking-CU camera; add a subtle push-in along its lens axis ---
cam = bpy.data.objects["RigCam"]
sc.camera = cam
base = cam.location.copy()
fwd = (cam.matrix_world.to_3x3() @ Vector((0, 0, -1))).normalized()  # camera looks down local -Z
push = 0.09  # world units of dolly-in across the whole line = "alive" shot
for fr in range(1, N + 1):
    t = (fr - 1) / max(1, N - 1)
    cam.location = base + fwd * (push * t)
    cam.keyframe_insert("location", frame=fr)

# (world + lights + materials come from the saved look-dev in the .blend — do not override)

# --- render ---
try: sc.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception: sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = 640
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = f"{outdir}/f_"
bpy.ops.render.render(animation=True)
print("TALK RENDER DONE", flush=True)
