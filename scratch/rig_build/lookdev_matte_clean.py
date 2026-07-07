"""STRATEGY 'matte_clean' — Matte clean (tuned).

Keeps the base approach (flat matte Principled, clean closed mouth, warm world) but SWEEPS the
matte parameters to find the softest, most illustrated storybook surface WITHOUT any painterly post.
This is the FLOOR every other strategy must beat.

Renders N named variants in ONE Blender launch (camera fixed, mouth cavity hidden), so they are
directly comparable. Each variant tunes:
  - normal-map strength (fur relief; lower = more illustrated/matte)
  - roughness (higher = more diffuse/chalky, kills any waxy sheen)
  - specular IOR level (0 = fully non-glossy)
  - key/fill/rim light energy + a soft warm rim
  - world warmth + ambient level (soft storybook bounce, no crushed blacks)

  blender -b bentley_rig_v1.blend -P lookdev_matte_clean.py -- <out_dir> <final_out.png>

Non-destructive per-variant: we re-apply the Principled inputs + light energies before each render.
"""
import bpy, sys, os

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir = argv[0] if len(argv) > 0 else "."
final_out = argv[1] if len(argv) > 1 else os.path.join(out_dir, "lookdev_matte_clean.png")
os.makedirs(out_dir, exist_ok=True)

sc = bpy.context.scene

# --- clean closed mouth: hide the interior cavity + tongue so no dark seam peeks through
for name in ("mouth_bag", "tongue"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True

mat = bpy.data.materials.get("tripo_mat_83150960")
nt = mat.node_tree
bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
nm = next((n for n in nt.nodes if n.type == "NORMAL_MAP"), None)


def matte_ify(normal_str, rough, spec, sheen=0.0):
    """Re-apply flat-matte Principled inputs (idempotent — safe to call per variant)."""
    # disconnect roughness + metallic maps -> flat matte constants
    for inp_name, const in (("Roughness", rough), ("Metallic", 0.0)):
        inp = bsdf.inputs[inp_name]
        for link in list(inp.links):
            nt.links.remove(link)
        inp.default_value = const
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = spec
    elif "Specular" in bsdf.inputs:
        bsdf.inputs["Specular"].default_value = spec
    # a whisper of sheen gives cloth-like fur softness at grazing angles (storybook rim on fur)
    if "Sheen Weight" in bsdf.inputs:
        bsdf.inputs["Sheen Weight"].default_value = sheen
        if "Sheen Roughness" in bsdf.inputs:
            bsdf.inputs["Sheen Roughness"].default_value = 0.5
    # tame the normal map so fur reads illustrated, not photoreal
    if nm:
        nm.inputs["Strength"].default_value = normal_str


def set_world(warm, strength):
    sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    # warm, high ambient bounce = soft storybook fill, no crushed shadow (matte read)
    bg.inputs[0].default_value = (0.88 * warm, 0.84, 0.78, 1.0)
    bg.inputs[1].default_value = strength


def set_lights(key, fill, rim, warmth_key=(1.0, 0.96, 0.90), warmth_rim=(1.0, 0.90, 0.78)):
    for name, e, col in (("Key", key, warmth_key),
                         ("Fill", fill, (0.94, 0.96, 1.0)),
                         ("Rim", rim, warmth_rim)):
        l = bpy.data.objects.get(name)
        if l and l.type == "LIGHT":
            l.data.energy = e
            try:
                l.data.color = col
            except Exception:
                pass


# --- render config: EEVEE-Next, Standard transform (clean storybook color), no filmic
try:
    sc.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    sc.render.engine = "BLENDER_EEVEE"
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
# nudge exposure/contrast toward the soft matte read (slightly lifted, gentle contrast)
sc.view_settings.exposure = 0.15
sc.view_settings.gamma = 1.0
sc.render.resolution_x = sc.render.resolution_y = 900
sc.render.image_settings.file_format = "PNG"

# --- the sweep: 3 tuned variants around the matte-storybook sweet spot -------------------
# base render used normal=0.18, rough=0.9, spec=0.05, warm=1.0, key/fill/rim=130/95/90.
# The base reads slightly waxy + warm-blown. We push softer: lower normal relief, higher
# roughness, spec->~0, higher ambient fill, gentle warm rim, a touch of sheen for fur softness.
variants = [
    # name          normal rough spec sheen  world_warm world_str  key   fill  rim
    ("v1_soft",     0.10,  0.95, 0.02, 0.06,  1.02,      0.70,      120,  105,  70),
    ("v2_softest",  0.06,  1.00, 0.00, 0.10,  1.04,      0.80,      105,  110,  60),
    ("v3_warm",     0.12,  0.92, 0.03, 0.05,  1.08,      0.62,      130,  100,  85),
    # v4 = v1's softness, but lower ambient + warmer stronger key so the black MASK stays dark
    # (protects the already-weak mask defect instead of lifting it toward grey) and form holds.
    ("v4_final",    0.09,  0.96, 0.01, 0.07,  1.03,      0.52,      140,   88,  72),
]

rendered = []
for name, nstr, rough, spec, sheen, wwarm, wstr, key, fill, rim in variants:
    matte_ify(nstr, rough, spec, sheen)
    set_world(wwarm, wstr)
    set_lights(key, fill, rim)
    path = os.path.join(out_dir, f"matte_{name}.png")
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    rendered.append(path)
    print(f"VARIANT DONE {name} -> {path}", flush=True)

print("MATTE_CLEAN SWEEP DONE", flush=True)
print("RENDERED:", ",".join(rendered), flush=True)
