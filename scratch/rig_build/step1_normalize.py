"""Import Tripo FBX -> join -> normalize (feet z=0, centered, height=2, faces -Y) -> save .blend
-> render 4 canonical views with SUN lights. blender -b -P step1_normalize.py -- <fbx> <outdir>"""
import bpy, sys, math
from mathutils import Vector, Matrix
argv=sys.argv[sys.argv.index("--")+1:]; fbx=argv[0]; outdir=argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
bpy.ops.import_scene.fbx(filepath=fbx)
ms=[o for o in sc.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
obj=bpy.context.view_layer.objects.active
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
me=obj.data
co=[v.co.copy() for v in me.vertices]
mn=Vector((min(p.x for p in co),min(p.y for p in co),min(p.z for p in co)))
mx=Vector((max(p.x for p in co),max(p.y for p in co),max(p.z for p in co))); size=mx-mn
# forward = dir from head centroid to avg of 30 farthest-horizontal head verts
hz=mn.z+0.62*size.z; head=[p for p in co if p.z>hz]
hc=sum(head,Vector())/len(head); hc.z=0
def hdist(p): q=Vector((p.x,p.y,0)); return (q-hc).length
far=sorted(head,key=hdist,reverse=True)[:40]
fwd=Vector((0,0,0))
for p in far: fwd+=Vector((p.x-hc.x,p.y-hc.y,0))
fwd.normalize()
# rotate about Z so fwd -> (0,-1,0)
ang=math.atan2(-1,0)-math.atan2(fwd.y,fwd.x)
Rz=Matrix.Rotation(ang,4,'Z')
for v in me.vertices: v.co=Rz@v.co
me.update()
# recompute bbox, drop feet to 0, center xy, scale height->2
co=[v.co for v in me.vertices]
mn=Vector((min(p.x for p in co),min(p.y for p in co),min(p.z for p in co)))
mx=Vector((max(p.x for p in co),max(p.y for p in co),max(p.z for p in co))); size=mx-mn
s=2.0/size.z; cx=(mn.x+mx.x)/2; cy=(mn.y+mx.y)/2
for v in me.vertices: v.co=Vector(((v.co.x-cx)*s,(v.co.y-cy)*s,(v.co.z-mn.z)*s))
me.update()
bpy.ops.wm.save_as_mainfile(filepath=f"{outdir}/bentley_norm.blend")
print("NORMALIZED height=2, faces -Y, saved bentley_norm.blend",flush=True)
# render 4 views with SUN
sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
bg=sc.world.node_tree.nodes["Background"]; bg.inputs[0].default_value=(0.8,0.8,0.82,1); bg.inputs[1].default_value=0.9
for d,e in [((0,-1,-0.3),3.0),((-1,-0.6,-0.2),1.2),((0.5,1,-0.4),1.0)]:
    l=bpy.data.lights.new("S",'SUN'); lo=bpy.data.objects.new("S",l); sc.collection.objects.link(lo)
    l.energy=e; dirv=Vector(d).normalized(); lo.rotation_euler=dirv.to_track_quat('-Z','Y').to_euler()
cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo); sc.camera=camo; cam.lens=50
tgt=bpy.data.objects.new("T",None); sc.collection.objects.link(tgt); tgt.location=(0,0,1.0)
c=camo.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Z'
piv=bpy.data.objects.new("P",None); sc.collection.objects.link(piv); piv.location=(0,0,1.0); camo.parent=piv
camo.location=(0,-5,0.4)
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=420; sc.render.resolution_y=420; sc.view_settings.view_transform='Standard'
for i,tag in [(0,"front"),(90,"right"),(180,"back"),(270,"left")]:
    piv.rotation_euler[2]=math.radians(i); sc.render.filepath=f"{outdir}/norm_{tag}.png"; bpy.ops.render.render(write_still=True)
print("DIAG DONE",flush=True)
