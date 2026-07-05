"""Import multiview mesh, join, normalize orientation, render head close-ups from N yaw angles.
blender --background --python head_inspect.py -- <fbx> <outdir> [N]"""
import bpy, sys, math
from mathutils import Vector
argv=sys.argv[sys.argv.index("--")+1:]
fbx=argv[0]; outdir=argv[1]; N=int(argv[2]) if len(argv)>2 else 6
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
bpy.ops.import_scene.fbx(filepath=fbx)
ms=[o for o in sc.objects if o.type=='MESH']
# join
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
obj=bpy.context.view_layer.objects.active
# world bbox
pts=[obj.matrix_world @ Vector(c) for c in obj.bound_box]
mn=Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)))
mx=Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
size=mx-mn; H=max(size.x,size.y,size.z)
# "head" = top 35% along the tallest axis (assume z-up after fbx import; check)
up = 2 if size.z>=size.x and size.z>=size.y else (1 if size.y>=size.x else 0)
head_ctr=(mn+mx)/2
# head center: shift toward the top of the up-axis
tp=[getattr(mn,'xyz'[up]),getattr(mx,'xyz'[up])]
hc=Vector(head_ctr); 
setattr(hc,'xyz'[up], mn['xyz'.index('xyz'[up])] if False else (mn[up]+0.82*size[up]))
R=H*0.22  # head is ~ a fifth of body
# camera + lights
tgt=bpy.data.objects.new("T",None); sc.collection.objects.link(tgt); tgt.location=hc
cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo); sc.camera=camo
cam.lens=70
c=camo.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
piv=bpy.data.objects.new("P",None); sc.collection.objects.link(piv); piv.location=hc
camo.parent=piv
camo.location=(0,-H*0.9,0)  # in front, level with head
sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.7,0.7,0.72,1)
sc.world.node_tree.nodes["Background"].inputs[1].default_value=1.0
for loc,e in [((H,-H,H),300),((-H,-H,H*0.5),150)]:
    l=bpy.data.lights.new("L",'AREA'); lo=bpy.data.objects.new("L",l); sc.collection.objects.link(lo)
    lo.location=hc+Vector(loc); l.energy=e; l.size=H
    cc=lo.constraints.new('TRACK_TO'); cc.target=tgt; cc.track_axis='TRACK_NEGATIVE_Z'
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=480; sc.render.resolution_y=480; sc.view_settings.view_transform='Standard'
print(f"BBOX size={tuple(round(v,3) for v in size)} up_axis={'xyz'[up]}")
for i in range(N):
    piv.rotation_euler[up]=math.radians(i*360/N)
    sc.render.filepath=f"{outdir}/head_{i:02d}.png"; bpy.ops.render.render(write_still=True)
print("HEAD RENDERS DONE")
