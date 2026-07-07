"""Painterly look-dev — STRATEGY 'kuwahara'  (Blender 5.1.2).

Renders the matte base (same non-destructive PBR->matte tweaks as lookdev_base.py), then applies a
PAINTERLY pass to reach the matte-storybook EP4 surface:

  PASS A (in-Blender): compositor Kuwahara node, variation=ANISOTROPIC, size ~8px, softened sharpness
                       -> directional 'brush stroke' storybook smoothing on the render result.
  PASS B (PIL post):   run SEPARATELY by lookdev_kuwahara_post.py on system python (Blender's bundled
                       python has no PIL). Gentle edge-preserving smooth + warm sat + soft bloom.

Blender 5.x moved the compositor to scene.compositing_node_group (a NodeTree datablock); the old
CompositorNodeComposite output is gone -> we use a NodeGroupOutput with an interface OUTPUT socket.
If the Kuwahara wiring fails, we still write the plain render so a real image is always produced.

  blender -b bentley_rig_v1.blend -P lookdev_kuwahara.py -- <prePIL.png> [normal_str] [rough] [spec] [warm] [kuwahara_px]

Camera (RigCam) untouched. mouth_bag + tongue hidden (clean closed mouth).
"""
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]                                        # this script writes the PRE-PIL render here
normal_str = float(argv[1]) if len(argv) > 1 else 0.18
rough      = float(argv[2]) if len(argv) > 2 else 0.9
spec       = float(argv[3]) if len(argv) > 3 else 0.05
warm       = float(argv[4]) if len(argv) > 4 else 1.0
kuwahara_px = float(argv[5]) if len(argv) > 5 else 8.0

sc = bpy.context.scene

# --- clean closed mouth: hide interior cavity + tongue so no dark seam peeks through -------------
for name in ("mouth_bag", "tongue"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True

# --- matte-ify the Tripo PBR: keep color texture (identity), kill photoreal surface --------------
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

# --- CANON PUSH (shading-only): mildly deepen the weak black mask via a gamma on Base Color -------
# Can't paint markings that aren't in the texture, but a small gamma pulls the darkest muzzle range
# darker so the greyish mask reads a touch closer to the master's crisp black. Kept mild.
try:
    base_col_input = bsdf.inputs["Base Color"]
    if base_col_input.links:
        from_socket = base_col_input.links[0].from_socket
        gamma = nt.nodes.new("ShaderNodeGamma")
        gamma.inputs["Gamma"].default_value = 1.12
        nt.links.new(from_socket, gamma.inputs["Color"])
        nt.links.new(gamma.outputs["Color"], base_col_input)
        print("canon-push: mask gamma applied", flush=True)
except Exception as e:
    print("canon-push skipped:", e, flush=True)

# --- warm storybook world + softened key/fill/rim ------------------------------------------------
if not sc.world:
    sc.world = bpy.data.worlds.new("W")
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.86 * warm, 0.82, 0.74, 1.0)
bg.inputs[1].default_value = 0.55
for name, e in (("Key", 130.0), ("Fill", 95.0), ("Rim", 90.0)):
    l = bpy.data.objects.get(name)
    if l and l.type == "LIGHT":
        l.data.energy = e

# --- render settings: EEVEE-Next, standard view-transform, 900px --------------------------------
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.image_settings.file_format = "PNG"

# --- PASS A: compositor Kuwahara (anisotropic painterly) — Blender 5.x node-group API ------------
kuwahara_ok = False
try:
    ng = bpy.data.node_groups.new("BentleyComp", "CompositorNodeTree")
    sc.compositing_node_group = ng

    rl  = ng.nodes.new("CompositorNodeRLayers")
    kuw = ng.nodes.new("CompositorNodeKuwahara")
    go  = None

    # anisotropic 'brush stroke' look; softer sharpness = more painterly melt
    try:
        kuw.inputs["Type"].default_value = "Anisotropic"
    except Exception as e:
        print("kuwahara Type set skipped:", e, flush=True)
    kuw.inputs["Size"].default_value = kuwahara_px
    if "Sharpness" in kuw.inputs:
        kuw.inputs["Sharpness"].default_value = 0.5   # 0=very smooth, 1=crisp; 0.5 keeps eyes
    if "Uniformity" in kuw.inputs:
        kuw.inputs["Uniformity"].default_value = 4
    if "Eccentricity" in kuw.inputs:
        kuw.inputs["Eccentricity"].default_value = 1.2

    # group output socket (replaces the removed Composite node)
    ng.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    go = ng.nodes.new("NodeGroupOutput")

    ng.links.new(rl.outputs["Image"], kuw.inputs["Image"])
    ng.links.new(kuw.outputs["Image"], go.inputs["Image"])
    kuwahara_ok = True
    print("KUWAHARA node wired (Anisotropic, size=%.1f)" % kuwahara_px, flush=True)
except Exception as e:
    print("KUWAHARA wiring FAILED (rendering plain matte instead):", e, flush=True)
    if hasattr(sc, "compositing_node_group"):
        sc.compositing_node_group = None

sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("LOOKDEV KUWAHARA RENDER DONE (kuwahara_node=%s) -> %s" % (kuwahara_ok, out), flush=True)
