"""Painterly look-dev — STRATEGY "mask_seam_repair".

Attacks the two worst IDENTITY defects of the base render WITHOUT any new AI, purely in-Blender:
  (a) strengthen the canon BLACK FACE MASK — a procedural, object-space + forward-facing mask
      multiplies the muzzle / around-eyes region toward crisp black over the weak greyish base color.
  (b) reduce the harsh baked MOUTH SEAM — a soft coat-colored band is mixed OVER the base color at
      the seam's Z height to bury the dark jagged lip line under coat tone, and roughness is kept flat
      there so no specular edge re-reveals it.

Everything sits on top of the matte base look (mouth cavity hidden, PBR flattened, warm world).
Object-space Texture-Coordinate + Geometry Normal are used (robust headless — no image-editor ops).

  blender -b bentley_rig_v1.blend -P lookdev_mask_seam_repair.py -- <out.png>
          [normal_str] [rough] [spec] [warm] [mask_strength] [seam_strength]
"""
import bpy, sys, math

argv = sys.argv[sys.argv.index("--") + 1:]
out = argv[0]
normal_str    = float(argv[1]) if len(argv) > 1 else 0.07   # low: kills the fur-normal smear at the mask edge
rough         = float(argv[2]) if len(argv) > 2 else 0.92
spec          = float(argv[3]) if len(argv) > 3 else 0.04
warm          = float(argv[4]) if len(argv) > 4 else 1.0
# mask_strength ~0.58 is the sweet spot: a believable EVEN dark muzzle mask that reads
# symmetrically on the 3/4-turned head. Higher (>0.8) exposes the turned-head asymmetry as a
# one-eyed black patch + a mesh-ridge streak; lower barely reads. seam kept gentle.
mask_strength = float(argv[5]) if len(argv) > 5 else 0.58   # how dark the mask gets (0..1)
seam_strength = float(argv[6]) if len(argv) > 6 else 0.50   # how hard the seam line is softened (0..1)

sc = bpy.context.scene

# --- clean closed mouth: hide the interior cavity + tongue so no dark seam peeks through
for name in ("mouth_bag", "tongue"):
    o = bpy.data.objects.get(name)
    if o:
        o.hide_render = True

mat = bpy.data.materials.get("tripo_mat_83150960")
nt = mat.node_tree
nodes, links = nt.nodes, nt.links
bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")

# --- matte-ify the Tripo PBR: keep the color texture (identity), kill the photoreal surface
for inp_name, const in (("Roughness", rough), ("Metallic", 0.0)):
    inp = bsdf.inputs[inp_name]
    for link in list(inp.links):
        links.remove(link)
    inp.default_value = const
if "Specular IOR Level" in bsdf.inputs:
    bsdf.inputs["Specular IOR Level"].default_value = spec
elif "Specular" in bsdf.inputs:
    bsdf.inputs["Specular"].default_value = spec

# tame the normal map so fur reads illustrated, not photoreal
nm = next((n for n in nodes if n.type == "NORMAL_MAP"), None)
if nm:
    nm.inputs["Strength"].default_value = normal_str

# ---------------------------------------------------------------------------
# Find the base-color image node (feeds Base Color) — we splice our mask BETWEEN
# that texture and the BSDF Base Color input.
# ---------------------------------------------------------------------------
basecol_link = bsdf.inputs["Base Color"].links[0]
basecol_src  = basecol_link.from_socket          # the texture's Color output
basecol_node = basecol_link.from_node

# Object-space coordinates of the surface (stable, headless-safe)
# CALIBRATED from a coordinate-debug render (debug_coords / _2). The head is turned/offset:
#   face front sits at X ~ +0.02..+0.32 (centred ~+0.19), Y forward <= -0.40 (nose reaches -0.54),
#   Z: chin ~1.60, muzzle ~1.72, eyes ~1.78, forehead ~1.80. Seam is a tight band Z ~1.655..1.700.
texco = nodes.new("ShaderNodeTexCoord")
texco.location = (-1400, 400)
sep = nodes.new("ShaderNodeSeparateXYZ")
sep.location = (-1200, 400)
links.new(texco.outputs["Object"], sep.inputs["Vector"])
X_CENTER = 0.19   # face is offset in +X in this pose

# Forward-facing weight: geometry normal .y negative => faces the camera front (muzzle/mask side)
geo = nodes.new("ShaderNodeNewGeometry")
geo.location = (-1400, 100)
nsep = nodes.new("ShaderNodeSeparateXYZ")
nsep.location = (-1200, 100)
links.new(geo.outputs["Normal"], nsep.inputs["Vector"])
neg_ny = nodes.new("ShaderNodeMath"); neg_ny.operation = "MULTIPLY"
neg_ny.location = (-1000, 100); neg_ny.inputs[1].default_value = -1.0
links.new(nsep.outputs["Y"], neg_ny.inputs[0])
front = nodes.new("ShaderNodeMapRange")     # remap -N.y -> 0.35..1 (soft; never fully kills facing side)
front.location = (-820, 100)
front.inputs["From Min"].default_value = -0.05
front.inputs["From Max"].default_value = 0.45
front.inputs["To Min"].default_value = 0.35   # floor: receding-but-front surfaces still get mask
front.inputs["To Max"].default_value = 1.0
front.clamp = True
links.new(neg_ny.outputs[0], front.inputs["Value"])

# ---------------------------------------------------------------------------
# (a) BLACK MASK region — 3D ELLIPSOIDAL distance falloff (robust, organic wrap;
#     no horizontal banding). Centre on the muzzle/nose bridge; radii let it cover
#     nose -> whole muzzle -> up around the eyes, and taper off toward the cheeks
#     and the back of the head. Gated by the FRONT weight so only the facing side
#     gets the mask (the ellipsoid also reaches the far side otherwise).
#
#     Calibrated centres/radii from the coord-debug samples:
#       nose ~ (0.16,-0.53,1.72) · eyes ~ (0.20,-0.43,1.78) · chin ~ (0.19,-0.52,1.63)
#     Ellipsoid centre C, per-axis radius R -> d = |(P-C)/R| ; mask = 1 - smoothstep(d).
# ---------------------------------------------------------------------------
CX, CY, CZ = 0.17, -0.49, 1.70      # mask centre (muzzle/nose bridge), nudged to catch both eyes
RX, RY, RZ = 0.205, 0.17, 0.150     # ellipsoid radii (wider X for both eyes, taller Z to nose+brow)

def norm_axis(sock, c, r, loc):
    s = nodes.new("ShaderNodeMath"); s.operation="SUBTRACT"; s.location=(loc[0],loc[1]); s.inputs[1].default_value=c
    links.new(sock, s.inputs[0])
    d = nodes.new("ShaderNodeMath"); d.operation="DIVIDE"; d.location=(loc[0]+160,loc[1]); d.inputs[1].default_value=r
    links.new(s.outputs[0], d.inputs[0])
    return d.outputs[0]

nx = norm_axis(sep.outputs["X"], CX, RX, (-1160, 640))
ny = norm_axis(sep.outputs["Y"], CY, RY, (-1160, 500))
nz = norm_axis(sep.outputs["Z"], CZ, RZ, (-1160, 360))
# d^2 = nx^2 + ny^2 + nz^2
def sq(sock, loc):
    m=nodes.new("ShaderNodeMath"); m.operation="MULTIPLY"; m.location=loc; links.new(sock,m.inputs[0]); links.new(sock,m.inputs[1]); return m.outputs[0]
sx2=sq(nx,(-820,640)); sy2=sq(ny,(-820,500)); sz2=sq(nz,(-820,360))
a1=nodes.new("ShaderNodeMath"); a1.operation="ADD"; a1.location=(-640,560); links.new(sx2,a1.inputs[0]); links.new(sy2,a1.inputs[1])
d2=nodes.new("ShaderNodeMath"); d2.operation="ADD"; d2.location=(-480,560); links.new(a1.outputs[0],d2.inputs[0]); links.new(sz2,d2.inputs[1])
# mask = 1 inside (d2<0.8), fade to 0 by d2~1.6 (soft ellipsoid edge)
maskR=nodes.new("ShaderNodeMapRange"); maskR.location=(-320,560)
maskR.inputs["From Min"].default_value=1.7; maskR.inputs["From Max"].default_value=0.55; maskR.clamp=True
links.new(d2.outputs[0], maskR.inputs["Value"])
# lateral cutoff: kill any spill onto the EARS (|X-CX| beyond the muzzle sides)
ex=nodes.new("ShaderNodeMath"); ex.operation="SUBTRACT"; ex.location=(-560,360); ex.inputs[1].default_value=CX; links.new(sep.outputs["X"],ex.inputs[0])
eax=nodes.new("ShaderNodeMath"); eax.operation="ABSOLUTE"; eax.location=(-420,360); links.new(ex.outputs[0],eax.inputs[0])
ecut=nodes.new("ShaderNodeMapRange"); ecut.location=(-280,360)
ecut.inputs["From Min"].default_value=0.235; ecut.inputs["From Max"].default_value=0.195; ecut.clamp=True  # 1 inside, 0 past the muzzle side (tighter -> no ear spill)
links.new(eax.outputs[0], ecut.inputs["Value"])
mc=nodes.new("ShaderNodeMath"); mc.operation="MULTIPLY"; mc.location=(-200,470)
links.new(maskR.outputs["Result"],mc.inputs[0]); links.new(ecut.outputs["Result"],mc.inputs[1])
# gate by front-facing
mg=nodes.new("ShaderNodeMath"); mg.operation="MULTIPLY"; mg.location=(-140,560)
links.new(mc.outputs[0],mg.inputs[0]); links.new(front.outputs["Result"],mg.inputs[1])
# user strength
maskw=nodes.new("ShaderNodeMath"); maskw.operation="MULTIPLY"; maskw.location=(20,560)
links.new(mg.outputs[0],maskw.inputs[0]); maskw.inputs[1].default_value=mask_strength

# black-mask colour: WARM near-black (canon black mask reads warm, not cold). Kept very
# dark so under the flat storybook light it still reads as a real dark mask.
black=nodes.new("ShaderNodeRGB"); black.location=(20,760)
black.outputs[0].default_value=(0.020, 0.016, 0.014, 1.0)

mix_mask=nodes.new("ShaderNodeMixRGB"); mix_mask.blend_type="MIX"; mix_mask.location=(240,620)
links.new(maskw.outputs[0], mix_mask.inputs["Fac"])
links.new(basecol_src, mix_mask.inputs["Color1"])
links.new(black.outputs[0], mix_mask.inputs["Color2"])

# ---------------------------------------------------------------------------
# (b) MOUTH SEAM softening. NOTE (measured): the base-color texture has NO sharp
#     dark line at any Z across the muzzle — it is a uniform mid-brown. The harsh
#     seam is a MESH/NORMAL crease catching shadow, not a paintable colour line.
#     So we do NOT paint a wide coat band (that just washed the muzzle). Instead
#     the black mask above already swallows the upper seam, and we additionally
#     lift the base color TOWARD the mask/coat in a THIN band right at the seam so
#     the residual crease reads softer, not a hard grey line. Kept narrow.
# ---------------------------------------------------------------------------
def thin_band(sock, lo, hi, feather, loc):
    up=nodes.new("ShaderNodeMapRange"); up.location=(loc[0],loc[1]+120)
    up.inputs["From Min"].default_value=lo-feather; up.inputs["From Max"].default_value=lo+feather; up.clamp=True
    links.new(sock,up.inputs["Value"])
    dn=nodes.new("ShaderNodeMapRange"); dn.location=(loc[0],loc[1]-120)
    dn.inputs["From Min"].default_value=hi+feather; dn.inputs["From Max"].default_value=hi-feather; dn.clamp=True
    links.new(sock,dn.inputs["Value"])
    mn=nodes.new("ShaderNodeMath"); mn.operation="MINIMUM"; mn.location=loc
    links.new(up.outputs["Result"],mn.inputs[0]); links.new(dn.outputs["Result"],mn.inputs[1]); return mn.outputs[0]

# reuse X-centred abs for the seam width limit
xshift=nodes.new("ShaderNodeMath"); xshift.operation="SUBTRACT"; xshift.location=(-1160,-160); xshift.inputs[1].default_value=X_CENTER
links.new(sep.outputs["X"], xshift.inputs[0])
absx=nodes.new("ShaderNodeMath"); absx.operation="ABSOLUTE"; absx.location=(-1000,-160); links.new(xshift.outputs[0],absx.inputs[0])

seam_z=thin_band(sep.outputs["Z"], 1.630, 1.660, 0.018, (-820,-40))   # thin, at the lip line
sxb=nodes.new("ShaderNodeMapRange"); sxb.location=(-820,-260)
sxb.inputs["From Min"].default_value=0.22; sxb.inputs["From Max"].default_value=0.08; sxb.clamp=True
links.new(absx.outputs[0], sxb.inputs["Value"])
syb=nodes.new("ShaderNodeMapRange"); syb.location=(-820,-460)
syb.inputs["From Min"].default_value=-0.34; syb.inputs["From Max"].default_value=-0.46; syb.clamp=True
links.new(sep.outputs["Y"], syb.inputs["Value"])
s1=nodes.new("ShaderNodeMath"); s1.operation="MULTIPLY"; s1.location=(-560,-120); links.new(seam_z,s1.inputs[0]); links.new(sxb.outputs["Result"],s1.inputs[1])
s2=nodes.new("ShaderNodeMath"); s2.operation="MULTIPLY"; s2.location=(-380,-120); links.new(s1.outputs[0],s2.inputs[0]); links.new(syb.outputs["Result"],s2.inputs[1])
s3=nodes.new("ShaderNodeMath"); s3.operation="MULTIPLY"; s3.location=(-200,-120); links.new(s2.outputs[0],s3.inputs[0]); links.new(front.outputs["Result"],s3.inputs[1])
seamw=nodes.new("ShaderNodeMath"); seamw.operation="MULTIPLY"; seamw.location=(-40,-120); links.new(s3.outputs[0],seamw.inputs[0]); seamw.inputs[1].default_value=seam_strength*0.6

# coat tone to lift the thin seam line toward surrounding muzzle
coat=nodes.new("ShaderNodeRGB"); coat.location=(-40,-320)
coat.outputs[0].default_value=(0.24, 0.185, 0.155, 1.0)
mix_seam=nodes.new("ShaderNodeMixRGB"); mix_seam.blend_type="MIX"; mix_seam.location=(460,420)
links.new(seamw.outputs[0], mix_seam.inputs["Fac"])
links.new(mix_mask.outputs["Color"], mix_seam.inputs["Color1"])
links.new(coat.outputs[0], mix_seam.inputs["Color2"])

# final -> Base Color
links.new(mix_seam.outputs["Color"], bsdf.inputs["Base Color"])

# ---------------------------------------------------------------------------
# Also nudge the eyes a touch warmer/darker IF an eye material exists (best-effort,
# harmless if absent). Shading can't enlarge them, but warmer iris reads closer to canon.
# ---------------------------------------------------------------------------
for m in bpy.data.materials:
    ln = m.name.lower()
    if any(k in ln for k in ("eye", "iris", "cornea")) and m.use_nodes:
        eb = next((n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
        if eb and not eb.inputs["Base Color"].links:
            eb.inputs["Base Color"].default_value = (0.14, 0.07, 0.03, 1.0)  # warm brown iris

# --- warm storybook world + softened key/fill/rim
sc.world = bpy.data.worlds.new("W") if not sc.world else sc.world
sc.world.use_nodes = True
bg = sc.world.node_tree.nodes["Background"]
# EVEN, FLAT storybook lighting: high fill + soft key so the mask reads SYMMETRICALLY on
# both sides (a directional key made the mask look like a one-eyed patch). Soft = painterly.
bg.inputs[0].default_value = (0.86 * warm, 0.82, 0.74, 1.0)
bg.inputs[1].default_value = 0.62   # generous ambient -> flat, soft, storybook
for name, e in (("Key", 78.0), ("Fill", 105.0), ("Rim", 60.0)):
    l = bpy.data.objects.get(name)
    if l and l.type == "LIGHT":
        l.data.energy = e
        # soften shadows: enlarge area/spot size if possible
        if hasattr(l.data, "shadow_soft_size"):
            l.data.shadow_soft_size = 2.5

# --- render: EEVEE-Next, standard transform for clean storybook color
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
print("LOOKDEV MASK_SEAM_REPAIR DONE", flush=True)
