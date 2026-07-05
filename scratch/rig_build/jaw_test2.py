"""Clean re-test: flat world light, proper face-on framing. Closed vs open jaw."""
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
mx=Vector((max(p.x for p in co),max(p.y for p in co),max(p.z for p in co))); size=mx-mn
hz=mn.z+0.68*size.z; head=[i for i,p in enumerate(co) if p.z>hz]
hc=sum((co[i] for i in head),Vector())/len(head)
nose=max((co[i] for i in head), key=lambda p:(p.x-hc.x)**2+(p.y-hc.y)**2)
fwd=Vector((nose.x-hc.x,nose.y-hc.y,0)); fwd.normalize()
muzlen=(Vector((nose.x,nose.y,0))-Vector((hc.x,hc.y,0))).length
hinge=Vector((nose.x,nose.y,nose.z))-fwd*muzlen*1.1; hinge.z=nose.z+size.z*0.02
sideax=fwd.cross(Vector((0,0,1))).normalized()
mouth_z=nose.z-size.z*0.015
jaw=[i for i in head if (co[i]-hinge).dot(fwd)>muzlen*0.15 and co[i].z<mouth_z+size.z*0.05]
mouth_ctr=Vector((nose.x,nose.y,mouth_z))-fwd*muzlen*0.1

# FLAT world lighting only — no area lamps (kills blowout)
sc.world=bpy.data.worlds.new("W"); sc.world.use_nodes=True
bg=sc.world.node_tree.nodes["Background"]; bg.inputs[0].default_value=(0.85,0.85,0.87,1); bg.inputs[1].default_value=1.6
try: sc.render.engine='BLENDER_EEVEE_NEXT'
except: sc.render.engine='BLENDER_EEVEE'
sc.render.resolution_x=460; sc.render.resolution_y=460; sc.view_settings.view_transform='Standard'
# camera face-on: place along +fwd from mouth, slightly above, look at mouth
cam=bpy.data.cameras.new("C"); camo=bpy.data.objects.new("C",cam); sc.collection.objects.link(camo); sc.camera=camo; cam.lens=85
tgt=bpy.data.objects.new("T",None); sc.collection.objects.link(tgt); tgt.location=mouth_ctr
c=camo.constraints.new('TRACK_TO'); c.target=tgt; c.track_axis='TRACK_NEGATIVE_Z'; c.up_axis='UP_Z'
piv=bpy.data.objects.new("P",None); sc.collection.objects.link(piv); piv.location=mouth_ctr; camo.parent=piv
camo.location=(fwd*size.z*0.62 + Vector((0,0,size.z*0.06)))
def render(tag):
    for yaw,t in [(0,"front"),(38,"3q")]:
        piv.rotation_euler[2]=math.radians(yaw); sc.render.filepath=f"{outdir}/{tag}_{t}.png"; bpy.ops.render.render(write_still=True)
render("closed")
# open jaw
ang=math.radians(26)
for i in jaw:
    pw=co[i]; d=(pw-hinge).dot(fwd); f=min(1.0,d/muzlen); R=Matrix.Rotation(ang*f,4,sideax)
    me.vertices[i].co=W.inverted()@(hinge+R@(pw-hinge))
me.update()
bpy.ops.mesh.primitive_uv_sphere_add(radius=muzlen*0.55, location=tuple(nose-fwd*muzlen*0.55-Vector((0,0,size.z*0.015))))
cav=bpy.context.active_object; dm=bpy.data.materials.new("D"); dm.use_nodes=False; dm.diffuse_color=(0.03,0.015,0.02,1); cav.data.materials.append(dm)
render("open")
print("DONE2",flush=True)
