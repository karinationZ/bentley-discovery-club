"""Reuse the PROVEN head_inspect camera; add jaw-open. Render face yaws closed vs open."""
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
obj=bpy.context.view_layer.objects.active; me=obj.data; W=obj.matrix_world
co=[W@v.co for v in me.vertices]
mn=Vector((min(p.x for p in co),min(p.y for p in co),min(p.z for p in co)))
mx=Vector((max(p.x for p in co),max(p.y for p in co),max(p.z for p in co))); size=mx-mn; H=max(size)
up=2
# jaw detection (forward = nose dir)
hz=mn.z+0.68*size.z; head=[i for i,p in enumerate(co) if p.z>hz]
hc=sum((co[i] for i in head),Vector())/len(head)
nose=max((co[i] for i in head), key=lambda p:(p.x-hc.x)**2+(p.y-hc.y)**2)
fwd=Vector((nose.x-hc.x,nose.y-hc.y,0)); fwd.normalize(); muzlen=(Vector((nose.x,nose.y,0))-Vector((hc.x,hc.y,0))).length
hinge=Vector((nose.x,nose.y,nose.z))-fwd*muzlen*1.1; hinge.z=nose.z+size.z*0.02
sideax=fwd.cross(Vector((0,0,1))).normalized(); mouth_z=nose.z-size.z*0.015
jaw=[i for i in head if (co[i]-hinge).dot(fwd)>muzlen*0.15 and co[i].z<mouth_z+size.z*0.05]

# --- PROVEN head_inspect camera/lights ---
hc2=Vector(((mn.x+mx.x)/2,(mn.y+mx.y)/2,mn.z+0.82*size.z))
tgt=bpy.data.objects.new("T",None); sc.collection.objects.link(tgt); tgt.location=hc2
cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo); sc.camera=camo; cam.lens=70
c=camo.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
piv=bpy.data.objects.new("P",None); sc.collection.objects.link(piv); piv.location=hc2; camo.parent=piv; camo.location=(0,-H*0.9,0)
sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.7,0.7,0.72,1); sc.world.node_tree.nodes["Background"].inputs[1].default_value=1.0
for loc,e in [((H,-H,H),300),((-H,-H,H*0.5),150)]:
    l=bpy.data.lights.new("L",'AREA'); lo=bpy.data.objects.new("L",l); sc.collection.objects.link(lo); lo.location=hc2+Vector(loc); l.energy=e; l.size=H
    cc=lo.constraints.new('TRACK_TO'); cc.target=tgt; cc.track_axis='TRACK_NEGATIVE_Z'
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=460; sc.render.resolution_y=460; sc.view_settings.view_transform='Standard'
def render(tag):
    for y in (90,120,150):
        piv.rotation_euler[up]=math.radians(y); sc.render.filepath=f"{outdir}/{tag}_{y}.png"; bpy.ops.render.render(write_still=True)
render("closed")
# open jaw + dark cavity
ang=math.radians(26)
for i in jaw:
    pw=co[i]; d=(pw-hinge).dot(fwd); f=min(1.0,d/muzlen); R=Matrix.Rotation(ang*f,4,sideax)
    me.vertices[i].co=W.inverted()@(hinge+R@(pw-hinge))
me.update()
bpy.ops.mesh.primitive_uv_sphere_add(radius=muzlen*0.5, location=tuple(nose-fwd*muzlen*0.5-Vector((0,0,size.z*0.01))))
cav=bpy.context.active_object; dm=bpy.data.materials.new("D"); dm.use_nodes=False; dm.diffuse_color=(0.03,0.015,0.02,1); cav.data.materials.append(dm)
render("open")
print(f"jaw={len(jaw)} DONE3",flush=True)
