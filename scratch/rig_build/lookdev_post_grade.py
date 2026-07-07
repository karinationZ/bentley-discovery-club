"""STRATEGY "post_grade": Post-grade painterly (cheap).

Cheapest path to the EP4 storybook look: render a matte base in Blender (no NPR), then
run a pure post-process grade in PIL/numpy toward the LOCKED EP4 look:
  - warm tone curve (lift shadows warm, roll off highlights)
  - slight desaturate-then-warm (kills the plasticky orange, adds storybook warmth)
  - gentle bloom / soft-light self-blend (matte glow, softens the 3D CG crispness)
  - subtle paper/paint grain (breaks the clean render surface)

No Blender NPR nodes are used, so nothing can fail headless — the matte base always renders,
and the grade is deterministic numpy. This establishes how far a $0 post-only treatment gets
vs the heavier NPR strategies.

Two-stage:
  STAGE A (in Blender): render the matte base -> <base_png>   (reuses lookdev_base logic)
  STAGE B (in python3): grade <base_png> -> <out_png>

Run STAGE A headless via blender, then STAGE B is invoked by this same file when run under
plain python3 (no bpy). A driver at the bottom picks the mode by whether bpy imports.
"""
import sys

# ---------------------------------------------------------------------------
# STAGE B — post grade (pure python3 + PIL/numpy). Defined first so both modes see it.
# ---------------------------------------------------------------------------
def grade(base_png, out_png):
    import numpy as np
    from PIL import Image, ImageFilter

    im = Image.open(base_png).convert("RGB")
    W, H = im.size
    a = np.asarray(im).astype(np.float32) / 255.0  # HxWx3 in 0..1

    luma0 = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]

    # --- 1. warm tone curve. GOAL: EP4 is warm+RICH, not pale. So NO big shadow lift
    #        (keeps the black mask black), a midtone S for depth, mild highlight rolloff. ---
    def curve(x, lift, gamma, gain):
        x = np.clip(x, 0.0, 1.0)
        x = lift + (1.0 - lift) * x        # tiny floor lift only (storybook, not crushed)
        x = np.power(x, gamma)             # <1 brightens mids, >1 deepens
        x = 1.0 - np.power(1.0 - x, gain)  # soft highlight shoulder
        return x

    # deepen shadows a touch (gamma>1 low-end via contrast S below), warm channel split
    a[..., 0] = curve(a[..., 0], lift=0.010, gamma=0.90, gain=1.15)   # R brighter/warmer
    a[..., 1] = curve(a[..., 1], lift=0.006, gamma=0.98, gain=1.12)   # G near-neutral
    a[..., 2] = curve(a[..., 2], lift=0.004, gamma=1.10, gain=1.06)   # B deepened/cooled-dark

    # --- 1b. gentle S-contrast on luma to restore depth the base lacks (mask reads darker) ---
    lm = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    s = 0.5 + 0.5 * np.tanh((lm - 0.5) * 2.3) / np.tanh(1.15)   # smooth S around mid
    scont = 0.30
    a = a * (1.0 - scont) + (a / np.clip(lm, 1e-4, None)) * s * scont  # push luma S, keep hue

    # --- 2. saturation: DON'T grey it out. EP4 is a saturated amber-brown. Boost chroma
    #        slightly and rotate hue a hair toward red-amber (away from plasticky orange). ---
    lm2 = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    sat = 1.14  # +14% chroma -> richer fawn
    a = lm2 + (a - lm2) * sat
    a = np.clip(a, 0.0, 1.0)

    # --- 3. warm color-grade: warm white balance + golden shadow wash (EP4 amber ambient) ---
    warm_mul = np.array([1.050, 1.000, 0.930], dtype=np.float32)
    a = a * warm_mul
    lm3 = (0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2])[..., None]
    shadow_mask = np.clip(1.0 - lm3, 0.0, 1.0) ** 1.8
    warm_wash = np.array([0.030, 0.016, 0.002], dtype=np.float32)   # gold into darks
    a = a + shadow_mask * warm_wash
    # warm the neutral grey backdrop toward the EP4 cream/paper tone
    a = np.clip(a, 0.0, 1.0)
    luma = lm3

    # --- 4. gentle bloom / soft-light: blur a bright-pass and screen it back ---
    graded = Image.fromarray((a * 255).astype(np.uint8), "RGB")
    # bright pass = pixels above threshold, softened wide -> matte glow
    b = a.copy()
    thr = 0.62
    bright = np.clip((b - thr) / (1.0 - thr), 0.0, 1.0) * b
    bright_img = Image.fromarray((np.clip(bright, 0, 1) * 255).astype(np.uint8), "RGB")
    bloom = bright_img.filter(ImageFilter.GaussianBlur(radius=max(W, H) * 0.009))
    bloom_a = np.asarray(bloom).astype(np.float32) / 255.0
    # screen blend the bloom (soft, ~18%) -> airy storybook highlights, not blown out
    a = 1.0 - (1.0 - a) * (1.0 - bloom_a * 0.18)

    # --- 4b. overall soft-light self-blend: blur the whole frame & soft-light it back
    # this is what melts the crisp CG edges into a matte-painting surface
    blur_full = graded.filter(ImageFilter.GaussianBlur(radius=max(W, H) * 0.006))
    blur_a = np.asarray(blur_full).astype(np.float32) / 255.0
    def soft_light(base, blend):
        # W3C soft-light
        return np.where(
            blend <= 0.5,
            base - (1 - 2 * blend) * base * (1 - base),
            base + (2 * blend - 1) * (np.where(base <= 0.25,
                                               ((16 * base - 12) * base + 4) * base,
                                               np.sqrt(np.clip(base, 0, 1))) - base),
        )
    sl = soft_light(a, blur_a)
    soft_amt = 0.13   # lighter melt -> keeps depth, still softens CG crispness
    a = a * (1.0 - soft_amt) + sl * soft_amt
    a = np.clip(a, 0.0, 1.0)

    # --- 5. subtle paper / paint grain (deterministic) ---
    rng = np.random.default_rng(42)
    grain = rng.normal(0.0, 1.0, size=(H, W, 1)).astype(np.float32)
    # luminance-aware grain: a bit stronger in midtones, gentle in highlights
    mid = 1.0 - np.abs(luma - 0.5) * 2.0
    grain_amt = 0.012
    a = a + grain * grain_amt * (0.5 + 0.5 * mid)

    # --- 6. very gentle warm vignette (storybook framing) ---
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W / 2.0, H * 0.46
    r = np.sqrt(((xx - cx) / (W * 0.62)) ** 2 + ((yy - cy) / (H * 0.62)) ** 2)
    vig = np.clip(1.0 - (r ** 2) * 0.16, 0.0, 1.0)[..., None]
    a = a * (0.90 + 0.10 * vig)

    a = np.clip(a, 0.0, 1.0)
    out = Image.fromarray((a * 255).astype(np.uint8), "RGB")
    out.save(out_png)
    print("POST-GRADE DONE ->", out_png, flush=True)


# ---------------------------------------------------------------------------
# Mode dispatch
# ---------------------------------------------------------------------------
try:
    import bpy
    IN_BLENDER = True
except Exception:
    IN_BLENDER = False


if IN_BLENDER:
    # ============ STAGE A: matte base render (mirrors lookdev_base.py) ============
    import math
    argv = sys.argv[sys.argv.index("--") + 1:]
    base_out = argv[0]                                   # where to write matte base
    normal_str = float(argv[1]) if len(argv) > 1 else 0.18
    rough = float(argv[2]) if len(argv) > 2 else 0.9
    spec = float(argv[3]) if len(argv) > 3 else 0.05
    warm = float(argv[4]) if len(argv) > 4 else 1.0

    sc = bpy.context.scene

    # clean closed mouth: hide interior cavity + tongue (no dark seam peeking through)
    for name in ("mouth_bag", "tongue"):
        o = bpy.data.objects.get(name)
        if o:
            o.hide_render = True

    # matte-ify the Tripo PBR: keep color texture (identity), kill photoreal surface
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

    # warm storybook world + softened key/fill/rim (camera untouched)
    sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.86 * warm, 0.82, 0.74, 1.0)
    bg.inputs[1].default_value = 0.55
    for name, e in (("Key", 130.0), ("Fill", 95.0), ("Rim", 90.0)):
        l = bpy.data.objects.get(name)
        if l and l.type == "LIGHT":
            l.data.energy = e

    try:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    except Exception:
        sc.render.engine = "BLENDER_EEVEE"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.resolution_x = sc.render.resolution_y = 900
    sc.render.image_settings.file_format = "PNG"
    sc.render.filepath = base_out
    bpy.ops.render.render(write_still=True)
    print("LOOKDEV MATTE BASE DONE ->", base_out, flush=True)

else:
    # ============ STAGE B invoked directly: grade base -> out ============
    # usage: python3 lookdev_post_grade.py <base_png> <out_png>
    base_png, out_png = sys.argv[1], sys.argv[2]
    grade(base_png, out_png)
