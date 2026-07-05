"""Render ONE on-model keyframe from the rig for the hybrid pipeline (bright front-3/4 face CU).
  blender -b <rig.blend> -P render_keyframe.py -- <out.png> [jaw_deg nod yaw roll]
Optional pose lets you author expression/gaze per shot; default = neutral mouth-closed (ideal Avatar input)."""
import bpy, sys, math
argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
jaw = float(argv[1]) if len(argv) > 1 else 0.0
nod = float(argv[2]) if len(argv) > 2 else 0.0
yaw = float(argv[3]) if len(argv) > 3 else 0.0
roll = float(argv[4]) if len(argv) > 4 else 0.0
sc = bpy.context.scene
arm = bpy.data.objects["Bentley_RIG"]
arm.pose.bones["jaw"].rotation_euler = (-math.radians(jaw), 0, 0)
if "head" in arm.pose.bones:
    arm.pose.bones["head"].rotation_euler = (math.radians(nod), math.radians(roll), math.radians(yaw))
bpy.context.view_layer.update()
try: sc.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception: sc.render.engine = 'BLENDER_EEVEE'
sc.render.resolution_x = sc.render.resolution_y = 768
sc.view_settings.view_transform = 'Standard'
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("KEYFRAME DONE", flush=True)
