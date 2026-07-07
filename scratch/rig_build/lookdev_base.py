"""Painterly look-dev BASE for the sign-off still (owner milestone 1).
Turns the Tripo photoreal PBR into a matte storybook look, hides the mouth cavity for a clean
closed-mouth pose, warms the light, frames a front-3/4 face-and-chest.

  blender -b bentley_rig_v1.blend -P lookdev_base.py -- <out.png> [normal_str] [rough] [spec] [warm]

Non-destructive: only tweaks the existing material's Principled inputs + hides mouth_bag/tongue.
"""
import bpy, sys, math

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
normal_str = float(argv[1]) if len(argv) > 1 else 0.18
rough = float(argv[2]) if len(argv) > 2 else 0.9
spec = float(argv[3]) if len(argv) > 3 else 0.05
warm = float(argv[4]) if len(argv) > 4 else 1.0

sc = bpy.context.scene

# --- clean closed mouth: hide the interior cavity + tongue so no dark seam peeks through
for name in ("mouth_bag", "tongue"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True

# --- matte-ify the Tripo PBR: keep the color texture (identity), kill the photoreal surface
mat = bpy.data.materials.get("tripo_mat_83150960")
nt = mat.node_tree
bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")

# disconnect roughness + metallic maps -> flat matte
for inp_name, const in (("Roughness", rough), ("Metallic", 0.0)):
    inp = bsdf.inputs[inp_name]
    for link in list(inp.links):
        nt.links.remove(link)
    inp.default_value = const
if "Specular IOR Level" in bsdf.inputs:
    bsdf.inputs["Specular IOR Level"].default_value = spec
elif "Specular" in bsdf.inputs:
    bsdf.inputs["Specular"].default_value = spec

# tame the normal map so fur reads illustrated, not photoreal
nm = next((n for n in nt.nodes if n.type == "NORMAL_MAP"), None)
if nm:
    nm.inputs["Strength"].default_value = normal_str

# --- warm storybook world + softened key/fill/rim
sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.86 * warm, 0.82, 0.74, 1.0)   # warm ambient
bg.inputs[1].default_value = 0.55
for name, e in (("Key", 130.0), ("Fill", 95.0), ("Rim", 90.0)):
    l = bpy.data.objects.get(name)
    if l and l.type == "LIGHT":
        l.data.energy = e

# --- render: EEVEE-Next, filmic-off for clean storybook color, mild AA
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("LOOKDEV BASE DONE", flush=True)
