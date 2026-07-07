"""Dump the blend's structure: objects, materials/nodes/images, shape keys, bones, constraints.
Run: blender -b <blend> -P inspect_scene.py"""
import bpy

sc = bpy.context.scene
print("=== OBJECTS ===")
for o in sc.objects:
    print(f"{o.name:24} type={o.type:8} loc={tuple(round(v, 3) for v in o.location)} "
          f"scale={tuple(round(v, 3) for v in o.scale)} parent={o.parent.name if o.parent else '-'}")
    if o.type == "MESH":
        me = o.data
        print(f"    verts={len(me.vertices)} mats={[m.name if m else None for m in me.materials]}")
        if me.shape_keys:
            for kb in me.shape_keys.key_blocks:
                print(f"    shapekey {kb.name!r} value={kb.value:.3f}")
    if o.type == "ARMATURE":
        for b in o.pose.bones:
            print(f"    bone {b.name!r} rot={tuple(round(v, 3) for v in b.rotation_euler)}")

print("=== MATERIALS ===")
for m in bpy.data.materials:
    print(f"mat {m.name!r} use_nodes={m.use_nodes}")
    if m.use_nodes:
        for n in m.node_tree.nodes:
            extra = ""
            if n.type == "TEX_IMAGE" and n.image:
                extra = f" image={n.image.name!r} file={n.image.filepath!r} size={tuple(n.image.size)}"
            if n.type == "BSDF_PRINCIPLED":
                ins = {k: (round(n.inputs[k].default_value, 3)
                           if isinstance(n.inputs[k].default_value, float) else "…")
                       for k in ("Roughness", "Metallic") if k in n.inputs}
                extra = f" {ins}"
            print(f"    node {n.type:20} {n.name!r}{extra}")

print("=== WORLD/RENDER ===")
print("engine:", sc.render.engine, "res:", sc.render.resolution_x, sc.render.resolution_y)
print("camera:", sc.camera.name if sc.camera else None)
for o in sc.objects:
    if o.type == "LIGHT":
        print(f"light {o.name!r} kind={o.data.type} energy={o.data.energy} loc={tuple(round(v,2) for v in o.location)}")
print("INSPECT DONE", flush=True)
