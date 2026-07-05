"""Jaw-open shape key driven by the Rhubarb openness curve -> talking render. Proven camera."""
import bpy, sys, math, json
from mathutils import Vector, Matrix
argv=sys.argv[sys.argv.index("--")+1:]; fbx,outdir,curvef=argv[0],argv[1],argv[2]
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene
bpy.ops.import_scene.fbx(filepath=fbx)
ms=[o for o in sc.objects if o.type=='MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active=ms[0]
if len(ms)>1: bpy.ops.object.join()
obj=bpy.context.view_layer.objects.active; me=obj.data; W=obj.matrix_world
co=[W@v.co for v in me.vertices]
mn=Vector((min(p.x for p in co),min(p.y for p in co),min(p.z for p in co)))
mx=Vector((max(p.x for p in co),max(p.y for p in co),max(p.z for p in co))); size=mx-mn; H=max(size)
allc=sum(co,Vector())/len(co)
hz=mn.z+0.68*size.z; head=[i for i,p in enumerate(co) if p.z>hz]
hc=sum((co[i] for i in head),Vector())/len(head)
axis=Vector((1,0,0)) if size.x>=size.y else Vector((0,1,0)); fwd=axis*(1 if (hc-allc).dot(axis)>0 else -1)
nose=max((co[i] for i in head), key=lambda p:p.dot(fwd)); muzlen=(nose-Vector((hc.x,hc.y,nose.z))).dot(fwd) or size.x*0.3
hinge=nose-fwd*muzlen*1.05; hinge.z=nose.z+size.z*0.015
sideax=fwd.cross(Vector((0,0,1))).normalized(); mouth_z=nose.z-size.z*0.01
jaw=[i for i in head if (co[i]-hinge).dot(fwd)>muzlen*0.12 and co[i].z<mouth_z+size.z*0.045]
base_yaw=math.degrees(math.atan2(fwd.y,fwd.x)-math.atan2(-1,0))
# shape keys
kb=obj.shape_key_add(name="Basis"); ko=obj.shape_key_add(name="jaw_open")
ang=math.radians(30)
for i in jaw:
    pw=co[i]; d=(pw-hinge).dot(fwd); f=min(1.0,d/muzlen); R=Matrix.Rotation(ang*f,4,sideax)
    ko.data[i].co=W.inverted()@(hinge+R@(pw-hinge))
# cavity inside mouth, parented, scale driven by openness
cc=nose-fwd*muzlen*0.42; cc.z=mouth_z-size.z*0.015
bpy.ops.mesh.primitive_uv_sphere_add(radius=muzlen*0.44, location=tuple(cc))
cav=bpy.context.active_object; dm=bpy.data.materials.new("D"); dm.use_nodes=False; dm.diffuse_color=(0.02,0.01,0.015,1); cav.data.materials.append(dm)
cav.parent=obj; cav.matrix_parent_inverse=obj.matrix_world.inverted()
# animate from curve
cur=json.loads(open(curvef).read()); fps=cur["fps"]; op=cur["open"]; N=len(op)
sc.render.fps=fps; sc.frame_start=1; sc.frame_end=N
for fr,val in enumerate(op, start=1):
    ko.value=val; ko.keyframe_insert("value",frame=fr)
    s=max(0.001, val); cav.scale=(1,1,0.62); cav.scale=(s, s, s*0.62); cav.keyframe_insert("scale",frame=fr)
# proven camera + lights, front (base_yaw)
hc2=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z+0.82*size.z))
tgt=bpy.data.objects.new("T",None); sc.collection.objects.link(tgt); tgt.location=hc2
cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo); sc.camera=camo; cam.lens=75
c=camo.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
piv=bpy.data.objects.new("P",None); sc.collection.objects.link(piv); piv.location=hc2; camo.parent=piv; camo.location=(0,-H*1.25,H*0.10); piv.rotation_euler[2]=math.radians(base_yaw+6)
sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.72,0.73,0.76,1); sc.world.node_tree.nodes["Background"].inputs[1].default_value=1.0
for loc,e in [((H,-H,H),150),((-H,-H,H*0.5),75),((0,H,H*1.2),60)]:
    l=bpy.data.lights.new("L",'AREA'); lo=bpy.data.objects.new("L",l); sc.collection.objects.link(lo); lo.location=hc2+Vector(loc); l.energy=e; l.size=H
    cc2=lo.constraints.new('TRACK_TO'); cc2.target=tgt; cc2.track_axis='TRACK_NEGATIVE_Z'
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=480; sc.render.resolution_y=480; sc.view_settings.view_transform='Standard'
sc.render.image_settings.file_format='PNG'; sc.render.filepath=f"{outdir}/f_"
bpy.ops.render.render(animation=True)
print("TALK RENDER DONE",flush=True)
