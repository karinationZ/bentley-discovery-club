"""Painterly look-dev — STRATEGY 'toon_ramp'.
Shader-to-RGB + soft 3-4 band ColorRamp on the diffuse of tripo_mat_83150960 so the surface reads
hand-illustrated / storybook rather than photoreal. NOT a harsh 2-step cel. EEVEE-Next supports
Shader-to-RGB.

Wiring: keep the Color.jpg texture (identity), route a Diffuse BSDF through Shader-to-RGB, remap
tone with a soft multi-band ColorRamp, multiply that banded light term back over the base color,
and feed an Emission so the ramp fully controls the shading (no extra Principled specular).

  blender -b bentley_rig_v1.blend -P lookdev_toon_ramp.py -- <out.png> [normal_str] [bands] [warm]

Non-destructive to geometry; hides mouth_bag/tongue (clean closed mouth). Camera untouched.
"""
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
normal_str = float(argv[1]) if len(argv) > 1 else 0.14
warm = float(argv[3]) if len(argv) > 3 else 1.0

sc = bpy.context.scene

# --- clean closed mouth: hide interior cavity + tongue so no dark seam peeks through
for name in ("mouth_bag", "tongue"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True

mat = bpy.data.materials.get("tripo_mat_83150960")
nt = mat.node_tree
nodes, links = nt.nodes, nt.links
bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")
out_node = next(n for n in nodes if n.type == "OUTPUT_MATERIAL")

# find the base color image texture feeding Base Color (identity texture we must keep)
base_color_socket = None
bc_in = bsdf.inputs["Base Color"]
if bc_in.links:
    base_color_socket = bc_in.links[0].from_socket

# tame normal map so fur reads illustrated, not photoreal (reuse existing normal map node)
nm = next((n for n in nodes if n.type == "NORMAL_MAP"), None)
if nm:
    nm.inputs["Strength"].default_value = normal_str

# --- build the toon chain ---------------------------------------------------
# A lightweight Diffuse BSDF gives us a clean N.L light term to quantize.
diff = nodes.new("ShaderNodeBsdfDiffuse")
diff.location = (bsdf.location.x - 200, bsdf.location.y - 400)
if nm:
    links.new(nm.outputs["Normal"], diff.inputs["Normal"])

s2rgb = nodes.new("ShaderNodeShaderToRGB")   # EEVEE-Next NPR node
s2rgb.location = (bsdf.location.x + 60, bsdf.location.y - 400)
links.new(diff.outputs["BSDF"], s2rgb.inputs["Shader"])

# soft 3-4 band ramp (CONSTANT interpolation = true cel bands, but gentle steps in a narrow value
# window so it reads storybook, not harsh 2-step). Bands sit in the warm mid-to-light range.
ramp = nodes.new("ShaderNodeValToRGB")
ramp.location = (s2rgb.location.x + 220, s2rgb.location.y)
cr = ramp.color_ramp
# EASE = soft plateaus with rounded transitions -> reads painterly/storybook, keeps the multi-band
# tonal *structure* (defined light/mid/shadow) without the hard clay-step edge of CONSTANT.
cr.interpolation = "EASE"
# clear default 2 stops -> build 4 soft bands
while len(cr.elements) > 1:
    cr.elements.remove(cr.elements[-1])
cr.elements[0].position = 0.0
cr.elements[0].color = (0.55, 0.50, 0.46, 1.0)   # soft shadow (warm grey-brown, NOT black)
e1 = cr.elements.new(0.32); e1.color = (0.74, 0.70, 0.64, 1.0)   # mid shadow
e2 = cr.elements.new(0.60); e2.color = (0.90, 0.87, 0.82, 1.0)   # mid light
e3 = cr.elements.new(0.85); e3.color = (1.00, 0.99, 0.96, 1.0)   # highlight
links.new(s2rgb.outputs["Color"], ramp.inputs["Fac"])

# multiply the banded light term over the base color texture -> painterly toon albedo
mix = nodes.new("ShaderNodeMixRGB")
mix.blend_type = "MULTIPLY"
mix.inputs["Fac"].default_value = 1.0
mix.location = (ramp.location.x + 220, ramp.location.y + 120)
if base_color_socket:
    links.new(base_color_socket, mix.inputs["Color1"])
else:
    mix.inputs["Color1"].default_value = (0.80, 0.45, 0.22, 1.0)
links.new(ramp.outputs["Color"], mix.inputs["Color2"])

# slight warm push
warm_mix = nodes.new("ShaderNodeMixRGB")
warm_mix.blend_type = "COLOR"
warm_mix.inputs["Fac"].default_value = 0.10 * warm
warm_mix.location = (mix.location.x + 200, mix.location.y)
links.new(mix.outputs["Color"], warm_mix.inputs["Color1"])
warm_mix.inputs["Color2"].default_value = (1.0, 0.86, 0.66, 1.0)

# emission carries the final flat look (self-lit -> pure ramp control, matte, no gloss)
emit = nodes.new("ShaderNodeEmission")
emit.location = (warm_mix.location.x + 200, warm_mix.location.y)
links.new(warm_mix.outputs["Color"], emit.inputs["Color"])
emit.inputs["Strength"].default_value = 1.0

links.new(emit.outputs["Emission"], out_node.inputs["Surface"])

# --- warm storybook world + softened key/fill/rim (still lights the scene a touch via world) ----
sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.86 * warm, 0.82, 0.74, 1.0)
bg.inputs[1].default_value = 0.55
for name, e in (("Key", 130.0), ("Fill", 95.0), ("Rim", 90.0)):
    l = bpy.data.objects.get(name)
    if l and l.type == "LIGHT":
        l.data.energy = e

# --- render: EEVEE-Next (Shader-to-RGB requires EEVEE), Standard transform for clean storybook color
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
print("LOOKDEV TOON_RAMP DONE", flush=True)
