"""Headless Blender turntable: blender --background --python turntable.py -- <glb> <outdir> [nframes]
Renders N angles of the model on a neutral studio set → PNGs. EEVEE, fast."""
import bpy, sys, math
from mathutils import Vector
argv=sys.argv[sys.argv.index("--")+1:]
glb=argv[0]; outdir=argv[1]; N=int(argv[2]) if len(argv)>2 else 8

bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene
ext=glb.lower().rsplit(".",1)[-1]
try:
    if ext=="fbx": bpy.ops.import_scene.fbx(filepath=glb)
    else: bpy.ops.import_scene.gltf(filepath=glb)
except Exception as e: print("IMPORT ERROR",e); sys.exit(1)

meshes=[o for o in sc.objects if o.type=='MESH']
if not meshes: print("NO MESH IMPORTED"); sys.exit(1)
# bbox in world space
import itertools
pts=[o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
mn=Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)))
mx=Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
ctr=(mn+mx)/2; size=(mx-mn); R=max(size.x,size.y,size.z)

# pivot empty at center; parent meshes so we rotate the whole model
piv=bpy.data.objects.new("PIV",None); sc.collection.objects.link(piv); piv.location=ctr
for o in meshes:
    o.parent=piv; o.matrix_parent_inverse=piv.matrix_world.inverted()

# camera looking at center, slightly above
cam_d=R*2.2
cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo)
camo.location=ctr+Vector((0,-cam_d,R*0.15))
tt=camo.constraints.new('TRACK_TO'); 
tgt=bpy.data.objects.new("TGT",None); sc.collection.objects.link(tgt); tgt.location=ctr
tt.target=tgt; tt.track_axis='TRACK_NEGATIVE_Z'; tt.up_axis='UP_Y'
sc.camera=camo

# world + lights
sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.72,0.72,0.74,1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value=1.0
def light(name,loc,energy,typ='AREA',size=None):
    l=bpy.data.lights.new(name,typ); o=bpy.data.objects.new(name,l); sc.collection.objects.link(o)
    o.location=ctr+Vector(loc); l.energy=energy
    if size and typ=='AREA': l.size=size
    c=o.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'
    return o
light("key",(R*1.5,-R*1.5,R*2),450,'AREA',R*2.5)
light("fill",(-R*2,-R*1.2,R*0.6),180,'AREA',R*3.5)
light("rim",(0,R*2,R*1.5),120,'AREA',R*2)

# render settings — EEVEE fast
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=640; sc.render.resolution_y=640
sc.render.film_transparent=False
sc.view_settings.view_transform='Standard'
for i in range(N):
    piv.rotation_euler[2]=math.radians(i*360/N)
    sc.render.filepath=f"{outdir}/ang_{i:02d}.png"
    bpy.ops.render.render(write_still=True)
print(f"RENDERED {N} angles -> {outdir}")
