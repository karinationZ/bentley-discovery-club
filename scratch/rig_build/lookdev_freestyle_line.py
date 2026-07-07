"""Painterly look-dev — STRATEGY "freestyle_line".
Matte storybook base (identical to lookdev_base.py) + a SUBTLE Freestyle line render:
thin, soft dark edge on silhouette + creases for a storybook-illustration outline.
Lines are kept DELICATE (a heavy outline is wrong). Freestyle runs in EEVEE.

Fallback chain if Freestyle won't produce lines headless:
  attempt 1 -> Freestyle (EEVEE, delicate)
  attempt 2 -> Freestyle retry (force-enable + freestyle_settings)
  fallback  -> compositor Sobel edge composited faintly over the matte base
  last resort-> matte-only (base look), reported honestly

  blender -b bentley_rig_v1.blend -P lookdev_freestyle_line.py -- <out.png> [mode] [normal_str] [rough] [spec] [warm]
    mode: "freestyle" (default) | "sobel" | "matte"
"""
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
mode = argv[1] if len(argv) > 1 else "freestyle"
normal_str = float(argv[2]) if len(argv) > 2 else 0.18
rough = float(argv[3]) if len(argv) > 3 else 0.9
spec = float(argv[4]) if len(argv) > 4 else 0.05
warm = float(argv[5]) if len(argv) > 5 else 1.0

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

for inp_name, const in (("Roughness", rough), ("Metallic", 0.0)):
    inp = bsdf.inputs[inp_name]
    for link in list(inp.links):
        nt.links.remove(link)
    inp.default_value = const
if "Specular IOR Level" in bsdf.inputs:
    bsdf.inputs["Specular IOR Level"].default_value = spec
elif "Specular" in bsdf.inputs:
    bsdf.inputs["Specular"].default_value = spec

nm = next((n for n in nt.nodes if n.type == "NORMAL_MAP"), None)
if nm:
    nm.inputs["Strength"].default_value = normal_str

# --- warm storybook world + softened key/fill/rim
sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.86 * warm, 0.82, 0.74, 1.0)
bg.inputs[1].default_value = 0.55
for name, e in (("Key", 130.0), ("Fill", 95.0), ("Rim", 90.0)):
    l = bpy.data.objects.get(name)
    if l and l.type == "LIGHT":
        l.data.energy = e

# --- render engine: EEVEE-Next, standard storybook color
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.image_settings.file_format = "PNG"
sc.render.filepath = out


# ------------------------------------------------------------------
# FREESTYLE: delicate storybook outline
# ------------------------------------------------------------------
def setup_freestyle():
    """Enable Freestyle with a thin, soft, slightly-transparent dark edge.
    Returns True if the linesets were configured."""
    sc.render.use_freestyle = True
    # Freestyle line thickness is in px at final res; keep it thin & AA'd.
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = 2.0  # delicate but clearly readable

    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fset = vl.freestyle_settings
    # crease angle: only mark fairly hard creases so we don't scribble the whole fur
    fset.crease_angle = 2.6  # radians (~149deg) -> only strong creases + silhouette
    fset.use_culling = True
    fset.use_smoothness = True

    # start from a clean lineset
    while len(fset.linesets) > 1:
        fset.linesets.remove(fset.linesets[-1])
    if len(fset.linesets) == 0:
        fset.linesets.new("StorybookLine")
    ls = fset.linesets[0]
    ls.name = "StorybookLine"
    # what edges to draw: silhouette + border + hard creases (NOT every material edge)
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = True
    ls.select_edge_mark = False
    ls.select_material_boundary = False
    if hasattr(ls, "select_contour"):
        ls.select_contour = True

    # line style: thin, soft dark-brown (warmer than pure black), semi-transparent
    lstyle = ls.linestyle
    lstyle.color = (0.11, 0.07, 0.05)   # warm near-black (storybook ink, not pure black)
    lstyle.alpha = 0.9                   # DELICATE but readable — soft line, not heavy ink
    lstyle.thickness = 2.0
    lstyle.thickness_position = 'CENTER'
    lstyle.caps = 'ROUND'
    lstyle.use_chaining = True
    # taper the ends a little (thinning) if the modifier stack is available
    try:
        lstyle.thickness_modifiers.new(name="taper", type='ALONG_STROKE')
        tmod = lstyle.thickness_modifiers[-1]
        tmod.value_min = 0.0
        tmod.value_max = 1.1
    except Exception:
        pass
    # slight alpha fade along stroke for a hand-drawn feel
    try:
        lstyle.alpha_modifiers.new(name="afade", type='ALONG_STROKE')
        amod = lstyle.alpha_modifiers[-1]
        amod.value_min = 0.7
        amod.value_max = 0.95
    except Exception:
        pass
    return True


def setup_sobel_compositor():
    """Fallback: composite a faint Sobel edge over the matte render via the compositor."""
    sc.use_nodes = True
    tree = sc.node_tree
    tree.nodes.clear()
    rl = tree.nodes.new("CompositorNodeRLayers")
    # Sobel filter on the image -> edges
    filt = tree.nodes.new("CompositorNodeFilter")
    filt.filter_type = 'SOBEL'
    tree.links.new(rl.outputs["Image"], filt.inputs["Image"])
    # invert so edges are dark, then knock them back to faint
    inv = tree.nodes.new("CompositorNodeInvert")
    tree.links.new(filt.outputs["Image"], inv.inputs["Color"])
    # desaturate + darken the edge so it's a soft dark line, not rainbow
    hsv = tree.nodes.new("CompositorNodeHueSat")
    hsv.inputs["Saturation"].default_value = 0.0
    hsv.inputs["Value"].default_value = 0.15  # keep edges dark/faint
    tree.links.new(inv.outputs["Color"], hsv.inputs["Image"])
    # multiply edges over the base render (darkens along edges only), faint via mix factor
    mix = tree.nodes.new("CompositorNodeMixRGB")
    mix.blend_type = 'MULTIPLY'
    mix.inputs["Fac"].default_value = 0.45  # DELICATE
    tree.links.new(rl.outputs["Image"], mix.inputs[1])
    tree.links.new(hsv.outputs["Image"], mix.inputs[2])
    comp = tree.nodes.new("CompositorNodeComposite")
    tree.links.new(mix.outputs["Image"], comp.inputs["Image"])


ok = False
err = ""
if mode == "matte":
    print("MODE=matte (no lines)", flush=True)
elif mode == "sobel":
    try:
        setup_sobel_compositor()
        print("MODE=sobel compositor", flush=True)
        ok = True
    except Exception as e:
        err = str(e)
else:
    # freestyle path
    try:
        ok = setup_freestyle()
        print("FREESTYLE configured", flush=True)
    except Exception as e:
        err = str(e)
        print("FREESTYLE FAILED:", err, flush=True)
        # auto-fallback within the same run -> sobel
        try:
            sc.render.use_freestyle = False
            setup_sobel_compositor()
            print("FELL BACK to sobel compositor", flush=True)
            ok = True
        except Exception as e2:
            print("SOBEL fallback also failed:", e2, flush=True)

bpy.ops.render.render(write_still=True)
print("LOOKDEV FREESTYLE DONE ok=%s err=%s" % (ok, err), flush=True)
