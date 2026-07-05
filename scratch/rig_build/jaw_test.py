"""Decisive test: can we open this closed mouth? Detect muzzle, select lower-jaw verts,
(a) highlight them, (b) rotate open + dark cavity. blender --background --python jaw_test.py -- <fbx> <outdir>"""
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
me=obj.data
W=obj.matrix_world
co=[W@v.co for v in me.vertices]
mn=Vector((min(p.x for p in co),min(p.y for p in co),min(p.z for p in co)))
mx=Vector((max(p.x for p in co),max(p.y for p in co),max(p.z for p in co)))
size=mx-mn
# head verts = top 32%
hz=mn.z+0.68*size.z
head=[i for i,p in enumerate(co) if p.z>hz]
hc=sum((co[i] for i in head),Vector())/len(head)
# nose = head vert max horizontal dist from head-center
nose=max((co[i] for i in head), key=lambda p:(p.x-hc.x)**2+(p.y-hc.y)**2)
fwd=Vector((nose.x-hc.x,nose.y-hc.y,0)); fwd.normalize()
muzlen=(Vector((nose.x,nose.y,0))-Vector((hc.x,hc.y,0))).length
# hinge: behind nose along -fwd, at ~ nose height
hinge=Vector((nose.x,nose.y,nose.z))-fwd*muzlen*1.1; hinge.z=nose.z+size.z*0.02
side=fwd.cross(Vector((0,0,1))).normalized()  # jaw rotation axis (horizontal, across face)
# lower jaw verts: forward of hinge AND below mouth line (mouth ~ nose.z - a bit)
mouth_z=nose.z - size.z*0.015
jaw=[]
for i in head:
    p=co[i]; d=(p-hinge).dot(fwd)
    if d>muzlen*0.15 and p.z < mouth_z + size.z*0.05:
        jaw.append(i)
print(f"size={tuple(round(v,2) for v in size)} nose={tuple(round(v,2) for v in nose)} fwd={tuple(round(v,2) for v in fwd)} jaw_verts={len(jaw)}",flush=True)

# --- render helper (face-on + 3/4) ---
def setup_cam_lights():
    tgt=bpy.data.objects.new("T",None); sc.collection.objects.link(tgt)
    mouth_ctr=Vector((nose.x,nose.y,mouth_z))-fwd*muzlen*0.1; tgt.location=mouth_ctr
    cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo); sc.camera=camo; cam.lens=80
    c=camo.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Y'
    piv=bpy.data.objects.new("P",None); sc.collection.objects.link(piv); piv.location=mouth_ctr; camo.parent=piv
    camo.location=fwd_off
    sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value=(0.7,0.7,0.72,1); sc.world.node_tree.nodes["Background"].inputs[1].default_value=1.0
    for loc,e in [((size.z,-size.z,size.z),200),((-size.z,-size.z,size.z*0.4),90)]:
        l=bpy.data.lights.new("L",'AREA'); lo=bpy.data.objects.new("L",l); sc.collection.objects.link(lo); lo.location=mouth_ctr+Vector(loc); l.energy=e; l.size=size.z
        cc=lo.constraints.new('TRACK_TO'); cc.target=tgt; cc.track_axis='TRACK_NEGATIVE_Z'
    return piv
fwd_off=Vector((fwd.x,fwd.y,0))*size.z*0.75 + Vector((0,0,size.z*0.03))
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=480; sc.render.resolution_y=480; sc.view_settings.view_transform='Standard'
piv=setup_cam_lights()

# (a) highlight jaw verts red
redmat=bpy.data.materials.new("RED"); redmat.diffuse_color=(1,0,0,1); redmat.use_nodes=False
obj.data.materials.append(redmat); ridx=len(obj.data.materials)-1
jawset=set(jaw)
for poly in me.polygons:
    if any(v in jawset for v in poly.vertices): poly.material_index=ridx
for yaw,tag in [(0,"front"),(35,"3q")]:
    piv.rotation_euler[2]=math.radians(yaw); sc.render.filepath=f"{outdir}/sel_{tag}.png"; bpy.ops.render.render(write_still=True)

# (b) open the jaw: rotate jaw verts about hinge around 'side' axis, falloff by forward dist
ang=math.radians(24)
for i in jaw:
    p=me.vertices[i].co  # local == world (identity-ish); use world then back
    pw=co[i]; d=(pw-hinge).dot(fwd); f=min(1.0, d/(muzlen*1.0))
    R=Matrix.Rotation(ang*f, 4, side)
    npw=hinge + R@(pw-hinge)
    me.vertices[i].co = W.inverted()@npw
me.update()
# dark cavity sphere just behind the mouth
bpy.ops.mesh.primitive_uv_sphere_add(radius=muzlen*0.5, location=(nose - fwd*muzlen*0.5 - Vector((0,0,size.z*0.02))))
cav=bpy.context.active_object; darkm=bpy.data.materials.new("DARK"); darkm.diffuse_color=(0.02,0.01,0.01,1); darkm.use_nodes=False
cav.data.materials.append(darkm)
for yaw,tag in [(0,"front"),(35,"3q")]:
    piv.rotation_euler[2]=math.radians(yaw); sc.render.filepath=f"{outdir}/open_{tag}.png"; bpy.ops.render.render(write_still=True)
print("JAW TEST DONE",flush=True)
