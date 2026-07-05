# BENTLEY RIG STUDIO — Build Plan (team output, 2026-07-02)

*Owner directive: build our own 3D-rig lip-sync system. Four-specialist team output, preserved verbatim.*
*Status: P0 (live Blender bridge) EXECUTED same day — addon vendored at tools/blender_mcp/, MCP registered user-scope, bridge on localhost:9876. MCP tools available from the NEXT Claude session.*

---

# REPORT 1 — Pipeline Engineer: Blender MCP wiring
# Blender MCP wiring runbook (macOS, verified on this machine 2026-07-02)

## 0. Preflight — ALL ALREADY SATISFIED (verified live)
- `uv/uvx` 0.10.4 at `/home/user/.local/bin/uvx` ✓
- Blender 5.1.2 at `/opt/homebrew/bin/blender` (cask wrapper → `/Applications/Blender.app`) ✓
- Claude Code 2.1.198 at `/home/user/.local/bin/claude` ✓
- `uvx blender-mcp` smoke-tested: resolves from PyPI, installed 37 pkgs, logs "BlenderMCP server starting up"; the startup "Could not connect to Blender [Errno 61]" is a NON-FATAL warning (it retries per tool call). uv cache is now warm.
- Blender 5.1.2 headless still exposes legacy add-on ops (`bpy.ops.preferences.addon_install/addon_enable` both present; addons dir = `~/Library/Application Support/Blender/5.1/scripts/addons`). The addon is legacy `bl_info` style (min Blender 3.0, version (1,2)) — works on 5.x (community-confirmed on 4.5/5.0).

## 1. KEY FINDING — the addon AUTO-STARTS; no GUI "Connect" click needed
I read the current `addon.py` source directly (2813 lines). Facts that older docs get wrong:
- `register()` (lines ~2758-2771) **auto-starts the socket server** when the addon loads: Scene prop `blendermcp_auto_start_server` defaults `True`; during startup registration `bpy.context` is restricted → falls back to defaults (port 9876, auto_start True) and calls `BlenderMCPServer.start()`. So once the addon is enabled + userprefs saved, EVERY GUI Blender launch listens on `localhost:9876` with zero clicks. The sidebar "Connect to Claude" button (`bl_idname = "blendermcp.start_server"`; stop = `"blendermcp.stop_server"`) is only a manual fallback.
- **Headless is a hard no for this addon**: `start()` explicitly refuses `bpy.app.background` ("commands would never execute") because commands are marshaled to the main thread via `bpy.app.timers.register(...)`, which needs the GUI event loop. macOS has no xvfb — a real GUI window must stay open.
- Server object lives on `bpy.types.blendermcp_server` (not the scene) — it survives opening/loading .blend files within the session.
- `execute_code` runs `exec(code, {"bpy": bpy})` with stdout captured via `redirect_stdout` and returned — `print()` output comes back to Claude. **Namespace is a fresh dict per call** (no state persistence — see gotchas for the workaround).
- Telemetry defaults **ON on both sides**: addon `AddonPreferences.telemetry_consent` default `True` ("prompts, code snippets, and screenshots"); MCP-server side disabled by `DISABLE_TELEMETRY=true`. The runbook disables both.

## 2. Install runbook (execute verbatim; ~5 min; zero owner clicks)

**Step 1 — vendor the addon into the repo** (convention matches vendored `tools/rhubarb/`):
```bash
mkdir -p /project/tools/blender_mcp
curl -fsSL -o /project/tools/blender_mcp/blender_mcp_addon.py \
  https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py
```
(Renaming `addon.py` → `blender_mcp_addon.py` is safe — the addon uses `bl_idname = __name__` throughout — and gives a sane module name instead of `addon`. Commit the file to pin the version: bl_info (1,2).)

**Step 2 — install + enable the addon headless, kill telemetry, persist prefs** (background mode is fine for INSTALL; only the socket server refuses background):
```bash
/opt/homebrew/bin/blender --background --python-expr "import bpy; bpy.ops.preferences.addon_install(overwrite=True, filepath='/project/tools/blender_mcp/blender_mcp_addon.py'); bpy.ops.preferences.addon_enable(module='blender_mcp_addon'); bpy.context.preferences.addons['blender_mcp_addon'].preferences.telemetry_consent=False; bpy.ops.wm.save_userpref()"
```
Expected output includes `BlenderMCP: cannot start server in background mode` (harmless — proves register() ran) and `BlenderMCP addon registered`.

**Step 3 — register the MCP server with Claude Code** (user scope; absolute uvx path because GUI-launched Claude Code does not inherit `~/.local/bin` on PATH):
```bash
claude mcp add --scope user blender -e DISABLE_TELEMETRY=true -- /home/user/.local/bin/uvx blender-mcp
claude mcp list   # expect: blender ... ✓ (the stdio server health-checks OK even with Blender closed)
```
Scope semantics (from the installed CLI 2.1.198, `claude mcp add --help`):
- syntax: `claude mcp add [options] <name> <commandOrUrl> [args...]`, options: `-s/--scope local|user|project` (default **local**), `-e KEY=VAL`, `-t stdio` (default), `--` separates the spawned command.
- `local` (default): stored in `~/.claude.json` under THIS project path's entry — does NOT follow git worktrees (we use EnterWorktree, so local is a trap here).
- `user`: `~/.claude.json` top-level — all projects/worktrees for this user. **Use this.**
- `project`: writes `.mcp.json` in repo root (committable; each user must approve on first use).
- **Takes effect at the next Claude Code session launch** — a running session does not pick up a newly added server; restart the session (check with `/mcp` inside a session, `claude mcp list` outside). Each session start spawns `uvx blender-mcp` fresh (fast — cache is warm).

**Step 4 — launch the persistent GUI Blender (the "render node")**:
```bash
open -a Blender          # or: open -a Blender /path/to/bentley_rig.blend
sleep 15 && nc -z localhost 9876 && echo BRIDGE_UP
```
Auto-starts the socket server on 9876 (Step 1 finding). After any reboot, just `open -a Blender` again. Optional: add Blender to Login Items.

**Step 5 — smoke test in a NEW Claude Code session**: call `mcp__blender__get_scene_info`, then `mcp__blender__execute_blender_code` with `print(len(bpy.data.objects))`, then `mcp__blender__get_viewport_screenshot`. Known quirk (README): "sometimes the first command won't go through but after that it starts working" — retry once.

## 3. What needs the OWNER's one-time manual action
**Strictly: nothing.** Every step above is CLI-only. Two soft items:
1. If macOS's application firewall pops "Do you want Blender to accept incoming network connections?" → click **Allow** (bind is loopback-only `localhost:9876`, so the dialog usually doesn't even appear).
2. A Blender GUI window will live on the desktop during rig sessions — the owner must not quit it mid-session (quitting kills the bridge; display sleep is fine, app quit is not). Bonus: she can watch the rig work live in the viewport.

## 4. Tools the MCP exposes (tool names → `mcp__blender__*`)
Core (always on): `get_scene_info`, `get_object_info(name)`, `get_viewport_screenshot(max_size=800)` (saves temp PNG via context-overridden viewport screenshot, returns as Image to Claude), `execute_blender_code(code)` (arbitrary Python, stdout returned). Plus one MCP prompt: `asset_creation_strategy`.
Asset integrations (per-scene checkboxes, all default OFF — leave them off, we have our own Tripo mesh and they bloat the tool list): PolyHaven (categories/search/download/set_texture), Hyper3D Rodin, Sketchfab, Hunyuan3D (each with status/search/generate/poll/import tools that no-op unless enabled).

## 5. Gotchas (each verified in source)
- **GUI mandatory** — `blender -b` refused by design (timers never fire). No xvfb on macOS.
- **180s socket timeout** on the MCP client side; error text confirms it. Long bakes/renders must be fire-and-forget: kick off with `execute_blender_code` writing results to disk, poll a status file in later calls. Our render calls should write to `scratch/rig_build/` and return immediately.
- **No state between `execute_blender_code` calls** (fresh `{"bpy": bpy}` namespace). Workaround: stash state in `sys.modules` — first call does `import sys, types; m=types.ModuleType('rigstate'); sys.modules['rigstate']=m` then later calls `import rigstate`. Or keep state on `bpy` data (custom props). Or write a helper module into the .blend's text datablock and import it.
- **Timer-context execution**: code runs on the main thread via a timer, with no active window/area context — context-dependent `bpy.ops` (mode switches, some sculpt/edit ops) can fail. Prefer the data API (`bpy.data`, `obj.vertex_groups`, `mesh.shape_keys`) — which is exactly the discipline our proven headless scripts already use. This dodges the "sculpting blind via ops" failure from before.
- **One MCP client at a time** (README): don't also register blender-mcp in Claude Desktop/Cursor.
- **Port conflicts**: 9876 hardcoded default; change via the sidebar Port field + `-e BLENDER_PORT=<n>` on `claude mcp add` (server reads `BLENDER_HOST`/`BLENDER_PORT`).
- **Save before risky ops** — `execute_blender_code` is arbitrary code in the live session; make "save .blend to a versioned path" the first and last step of every rig work block.
- **Addon/server version skew**: after a `uvx` package update, re-download `addon.py` (upstream guidance). Pinning our vendored copy + uv's cached wheel keeps them in sync until we deliberately upgrade.
- FYI: Blender Foundation has an official experimental MCP effort (projects.blender.org/lab/blender_mcp); page 403'd for me — worth a look later, not load-bearing now.

## 6. Fallback: our own bridge, zero new deps (repo-controlled)
Two variants — B2 is the sleeper pick because it matches our proven headless pipeline:

**B1 — GUI bridge addon (parity clone of blender-mcp's transport):** ~200-line `tools/blender_bridge/bridge_addon.py`: daemon thread accepts on `127.0.0.1:9877`, queues JSON commands, `bpy.app.timers.register(executor)` runs them on the main thread (copy blender-mcp's exact pattern — we've read the source), returns `{ok, stdout, error(traceback)}` with length-prefixed framing. Client `tools/blender_bridge/bb.py` (stdlib socket): `python3 bb.py "<code>"` / `-f script.py` — Claude Code drives it via plain Bash, **no MCP registration, no session restart, works in any worktree**. Screenshots = command writes PNG to scratchpad, Claude Reads the file (Read renders images — equivalent to the MCP screenshot tool). Improvements over blender-mcp for free: persistent exec namespace (state across calls), no 180s cap, no telemetry, custom high-level commands (batch viseme keyframes, turntable render, save/checkpoint). Launch: `open -a Blender --args --python /abs/path/bridge_addon.py` (no install needed) or install+enable like Step 2. Same GUI requirement as blender-mcp (timers need the event loop). Effort: ~half a day incl. hardening.

**B2 — headless persistent worker (fully dodges the GUI constraint):** `blender -b --python worker.py` where `worker.py` itself runs the blocking socket accept/exec loop **on the main thread** — no timers needed, so the background-mode limitation disappears entirely. No viewport, so "screenshots" become camera EEVEE/Workbench renders to PNG (works headless on macOS Metal; our `scratch/rig_build/*.py` turntable/normalize/jaw scripts already prove this). Survives SSH, launchd-able, invisible to the owner. Downside: no live viewport for the owner to watch; renders are slower than viewport grabs.

**Effort/capability verdict:** blender-mcp = 5 minutes, maintained, viewport screenshots, MCP-native — **do it first (it's Step 1-5 above)**. Build B1/B2 only if we hit real friction (180s timeout on bakes, non-persistent namespace, MCP-registration pain in worktrees); B2 additionally unlocks unattended overnight rig/render loops that blender-mcp structurally cannot do. The two aren't exclusive — same Blender process can run blender-mcp on 9876 and our bridge on 9877.

## Files
- Verified addon source copy: `/private/tmp/claude-501/-Users-xxxxxxxxxxxxxxxxxx-src-bentley-discovery-club/e62d0454-ffb8-4f17-9dd0-a2d49a9817f9/scratchpad/addon.py` (scratch only; runbook Step 1 vendors it properly to `/project/tools/blender_mcp/blender_mcp_addon.py`)
- Blender addons dir: `/home/user/Library/Application Support/Blender/5.1/scripts/addons`
- Claude Code MCP config lands in: `/home/user/.claude.json` (user scope)

---

# REPORT 2 — Rigging Engineer: the rig build plan
# Bentley 3D Rig — Technical Build Plan (Rigging Engineer)

## 0. Ground truth (verified on disk, this session)

Mesh audit of `/project/scratch/rig_build/bentley_mv.fbx` (headless Blender 5.1.2):

- ONE mesh object `tripo_node_83150960`: 9,298 verts / 9,298 faces, **9,296 quads + 2 tris, 0 ngons** — clean retopo, ideal weight/sculpt density.
- **Only 2 boundary edges → the mesh is effectively watertight. The mouth is 100% sealed geometry** (the "mouth" is only painted texture). This is the root constraint of the whole plan.
- No armature, no vertex groups, no shape keys. Scale 1.0, dims 0.64 x 0.39 x 1.0 (1 Blender unit tall). 1 UV layer, 1 material, 4x 2048px textures (Tripo PBR set).
- Failure evidence reviewed: `/project/scratch/rig_build/jaw/open_F.png` vs `closed_F.png` — the entire muzzle (nose included) rotated down and swelled; **no mouth opening appears at all**.

## 1. Why raw-vertex rotation ballooned (and why a weighted jaw bone fixes it)

From `jaw_test4.py` / `step2_talk.py`:

1. **Selection by height heuristic, not topology.** `jaw = verts where z < mouth_z + 4.5% of body height AND forward of hinge` — on a sealed mesh there is no topological "lower jaw", so this band captured the nose underside, upper flews, and lower muzzle as one slab. Rotating it moved the nose (visible in `open_F.png`: the nose ball drops between the eyes).
2. **The skin is continuous across the (nonexistent) mouth line.** Every selected vertex is edge-connected to unselected neighbors above it; rotating the selection stretches those quads outward, which reads as inflation/ballooning. Opening a sealed surface without a seam can only bulge it — there is nothing to separate.
3. **Falloff along the wrong axis.** `f = d_forward / muzlen` fades the rotation front-to-back, but there is no falloff across the mouth corners or vertically across the lip line — a hard shading crease forms at the selection boundary.
4. **No interior.** Nothing exists behind the skin; the dark ellipsoid stuffed in afterward intersects the skin and shades as a blister, not a mouth cavity.
5. **Hinge too far forward.** `hinge = nose - fwd*muzlen*1.05` sits just behind the mouth corner. A real (and cartoon) jaw pivot is the TMJ: below the ear canal, ~2.2–2.5 muzzle-lengths behind the nose tip. A far-forward pivot turns rotation into near-pure downward translation of the chin — hatch-flap motion.

A **weighted jaw bone** fixes each cause by construction: the deform region is defined by painted weights bounded by a real cut seam (topology, not a z-threshold); weights blend 1.0→0.0 smoothly across the mouth corners (normalized skinning = no crease); the pivot is an authored bone head at the anatomical hinge; and the cut + mouth-bag gives the opening somewhere to open INTO.

## 2. Armature layout (muzzle quadruped, v1 talking-head scope)

Rig object `Bentley_RIG`, mesh renamed `Bentley_body`. Character normalized to face **-Y** (Blender convention), origin at floor. Bone chain (deform bones marked D):

```
root                    (origin, non-deform, master control)
 └─ spine              (D, single bone v1 — keeps chest/collar stable)
     └─ neck           (D)
         └─ head       (D, from neck top to skull crown)
             ├─ jaw    (D) — HEAD of bone at the jaw hinge, TAIL at chin tip
             │   └─ tongue_01 → tongue_02   (D, for tongue-out acting + L support)
             ├─ ear_L / ear_R  (D, optional v1.1 — floppy-ear secondary motion)
             └─ eye_L / eye_R  (D, optional v1.1 — pupils; blink = shape key)
```

**Jaw pivot placement (the critical number):** in side orthographic view, place the jaw bone head at the front edge of the ear base — vertically at/just below the mouth-corner line, horizontally ~2.2x muzzle length back from the nose tip (for this mesh: muzlen was computed at import; place interactively and confirm visually). Bone tail at the chin tip so the bone's rest axis runs along the mandible; rotation axis = local X (side axis). Cartoon-open max: **25 degrees** (step2's 30 deg * 0.92 openness peaked near 27.6 and looked over-cranked).

Why a single jaw bone (not jaw+lip bones): the 9-viseme taxonomy is scalar-per-shape; lip micro-shapes are cleaner as sculpted shape keys (section 4). Lip bones are a v2 upgrade only if a shape proves unsculptable.

Concrete bpy (scriptable parts):
```python
bpy.ops.object.armature_add(); arm = bpy.context.object; arm.name = "Bentley_RIG"
# in EDIT mode: create/parent edit_bones, set head/tail from measured landmarks
eb = arm.data.edit_bones; jaw = eb.new("jaw"); jaw.head = HINGE; jaw.tail = CHIN
jaw.parent = eb["head"]; ...
arm.data.bones["root"].use_deform = False   # after object mode
```
Bone placement itself should be done/verified **in the live viewport** (the whole point of the interactive session).

## 3. The sealed mouth: cut strategy

Evaluated:

**(a) Seam cut along the painted mouth line + bridged inner lips — PRIMARY.**
Keeps ONE manifold mesh → automatic weights solve correctly (post-cut, the lower-lip skin connects to the upper head only via the mouth corners, which is exactly the geodesic separation bone-heat needs), shape keys stay coherent, no gap management. Procedure (inherently interactive — do in the live session):
1. Edit Mode, side + front ortho views. Try `Alt+Click` edge-loop select along the lip crease first — Tripo retopo often flows a loop along strong texture creases. If no clean loop exists, use **Knife Project**: draw a Bezier curve tracing the painted mouth line in the front/side view, `bpy.ops.mesh.knife_project(cut_through=False)` per side, giving a clean new edge loop exactly on the paint line.
2. Select the seam loop → `bpy.ops.mesh.edge_split(type='EDGE')` (or rip `V`) → lips separated, two open boundaries.
3. Build the mouth bag by bridging inward: select upper boundary → `E`(extrude)+`S`(scale) 3–4 steps backward/inward to form the palate; same from the lower boundary for the mouth floor; `bpy.ops.mesh.bridge_edge_loops()` / grid-fill to close the back of the bag. Target ~300–600 new quads.
4. Add a simple tongue (squashed rounded cube, ~80 faces) merged into the mouth-floor region of the same object; give it its own vertex group `tongue`.
5. New faces get dedicated untextured materials: `M_mouth_interior` (dark warm near-black, diffuse ~(0.08, 0.02, 0.02), low spec) and `M_tongue` (soft pink (0.8, 0.35, 0.4)). **Toothless by construction — no tooth geometry exists, satisfying the owner-locked policy at the mesh level.**

**(b) Rip + separate modeled mouth-bag insert — FALLBACK.** Same seam rip, but the interior is a separate pouch+tongue object parented to `head` (bag) with its front-lower region weighted to `jaw`. Faster if bridging fights the AI topology, at the cost of possible gap glints at max open and a shading discontinuity at the lip edge. Use only if (a)'s bridge produces unmanageable shading.

**(c) Shrinkwrap/lattice — REJECTED.** Deformers cannot create an opening in a closed surface; a lattice jaw reproduces exactly the balloon we already have photographic proof of.

## 4. Weighting strategy

1. After the cut: select mesh then armature, `bpy.ops.object.parent_set(type='ARMATURE_AUTO')` (automatic weights). The seam makes bone-heat put the lower lip on `jaw` and the upper muzzle on `head` naturally.
2. **Known AI-mesh failure mode:** "Bone Heat Weighting failed" on overlapping shells — the collar and gold tag are the suspects. Fix: manually assign collar/tag verts 1.0 to `neck`/`head` (`Select Linked` + vertex-group assign), rerun auto weights on the body only, or accept envelope weights for those islands.
3. Corrective weight painting (interactive, X-mirror ON): `jaw` = 1.0 on chin/lower lip/mouth floor/lower flews; smooth gradient over ~6–10 edge rows at the mouth corners and under-cheek; exactly 0.0 on nose, upper flews, skull. `tongue_01/02` on tongue verts. Finish with Normalize All + Limit Total. **Paint with the jaw posed at 20–25 deg** so errors are visible live — this is the viewport-feedback step that headless scripting could never do.
4. Residual volume loss/shear at big opens is fixed in Step R4 by a **driven corrective shape key**, not more weights.

## 5. Bone-driven vs shape-key-driven: the split for the 9 visemes

Standard split, applied to our taxonomy (`/project/bentley/lipsync/visemes.py`): **jaw open = bone; lip shaping = keys; a viseme = (jaw angle) + (key weight vector)**. Only 6 sculpted keys + 1 corrective are needed for all 9 visemes:

| Project viseme | jaw (deg) | shape keys (value) |
|---|---|---|
| REST_CLOSED | 0 | none (basis) |
| MBP | 0 | lips_pressed 1.0 (flews pressed, lips rolled slightly in) |
| CONS | 8–10 | none (relaxed parted) |
| AI | 22–25 | mouth_wide 1.0 (corners drawn back) |
| E | 10–12 | mouth_wide 0.6 |
| O | 14–16 | lips_round 1.0 (corners forward, oval) |
| U | 6–8 | lips_pucker 1.0 |
| FV | 3–4 | lowerlip_tuck 1.0 (lower lip rolls in/up behind upper flew — dog-safe F/V) |
| L | 12–14 | tongue_up 1.0 (tongue tip to palate) |

Plus: `crv_jaw_open` — corrective key sculpted at jaw=25 deg, with a **driver** on the jaw bone's X rotation (`clamp(rot_x/radians(25),0,1)`) to restore flew volume and kill corner shear automatically at any opening. Extra acting keys (non-viseme): `blink`, `tongue_out` (canon happiness). Shape keys evaluate before the armature modifier in the stack, so keys sculpted at rest are correctly carried along by the jaw rotation — sculpt all lip keys at jaw=0 with the armature modifier visible in Sculpt Mode to preview the combined result. Since Rhubarb `D` maps to AI in v1 (per `RHUBARB_MAP`), AI's jaw value is the loudest shape; an `OPEN_JAW` variant later is just a table row (jaw 25, mouth_wide 0.4), zero new sculpting.

## 6. Ordered build plan with acceptance tests

Save an incremental .blend at every gate (`bentley_rig_s<N>.blend` in `/project/scratch/rig_build/`). Reuse the proven camera/light block from `step2_talk.py` for all acceptance renders.

- **R0 — Normalize (scripted).** Import FBX, rename, `transform_apply(rotation=True, scale=True)`, rotate so face = -Y, origin to floor center. ACCEPT: front ortho screenshot — Bentley faces camera at -Y, upright, collar level.
- **R1 — Mouth seam cut + bag (interactive).** Section 3(a). ACCEPT: (i) closed front render pixel-comparable to pre-cut `closed_F.png` (seam invisible at rest); (ii) side view with clipping/wireframe shows separated lips and a closed dark interior bag + tongue; (iii) `select_non_manifold` inside the bag region only — no stray open boundary on the visible skin.
- **R2 — Armature (scripted skeleton + interactive pivot placement).** Section 2. ACCEPT: side-view screenshot — jaw bone head sits at the ear-base line below/behind the eye, tail at chin tip; rotating jaw 25 deg in Pose Mode (pre-skinning) sweeps an arc whose chin travel looks like a dog opening its mouth, not a hatch.
- **R3 — Skinning (auto + interactive paint).** Section 4. ACCEPT: pose jaw 25 deg → screenshot must show mouth opening along the cut seam, dark interior + tongue visible, **nose and upper muzzle pixel-static vs closed**, smooth mouth-corner blend, zero spikes on collar/tag; head-bone 15 deg yaw carries ears+jaw, body static.
- **R4 — Corrective key (interactive sculpt + scripted driver).** `crv_jaw_open` @ jaw 25. ACCEPT: jaw-25 screenshot overlaid on closed — upper-head silhouette identical; flews keep volume; no shear crease at corners.
- **R5 — Viseme keys (interactive sculpt, scripted contact sheet).** Sculpt the 6 keys; encode the table in `bentley/lipsync/viseme_rig_table.json`. ACCEPT: scripted 3x3 contact sheet rendering all 9 visemes — every shape distinct, matches taxonomy intent, REST_CLOSED and MBP fully closed, **no teeth anywhere**, FV reads as lower-lip tuck not a bite.
- **R6 — Baker (scripted).** `rig_bake.py`: load our cue JSON → per cue, set jaw rotation + key values from the table, keyframe at `cue.start` with a 0.05–0.08 s ease-in from the previous pose (keyframe the previous viseme at `start - ramp`), hold to `cue.end`. ACCEPT: render the existing test line `/project/scratch/rig_build/rh/B_strong.{wav,json}` muxed with audio — lips fully close on M/B/P, wide on AI, tongue on L; plus automated check: sampled jaw curve at each cue midpoint equals table value ±5%.
- **R7 — Master lock + pipeline hook.** Save `bentley_rig_v1.blend` as the production master; headless `build_talk_shot.py` (blend + audio + transcript → adapter → baker → EEVEE render) slots into the existing cue-sheet→ffmpeg flow. ACCEPT: one full VO line rendered headless end-to-end at 24 fps with zero interactive steps.

## 7. blender_rhubarb_lipsync_ng vs our JSON — verified comparison and recommendation

Verified via WebFetch of github.com/Premik/blender_rhubarb_lipsync_ng (README): current release **1.8.1**; supports Blender 3.2+, **tested through 5.1.0** (our 5.1.2 fine); Blender 4.2+ installs as a native **extension zip** (drag into window), older as legacy addon; **bundles its own rhubarb binary**; workflow = UI capture (audio → cues) → map each cue A–H,X to an **Action** (single-frame pose Actions; works for bone poses or shape-key-value Actions; "action sheets" allow multiple cues in one Action) → **bake as NLA strips** (2 interleaving tracks for 3D with blending, 1 track for 2D). Two hard caveats found: **(1) baking shape-key NLA tracks needs the extra third-party "Bake Shape Keys" addon** (Blender can't natively bake shape-key NLA); **(2) no documented headless/Python API — capture and mapping are UI-button workflows.**

**RECOMMENDATION: skip NG for production; drive the rig directly from our cue JSON.** Decisive reasons:
1. **Headless is the product.** Our pipeline runs `blender --background`; NG's capture/mapping is UI-only. NG would make the ONLY non-scriptable link in an otherwise fully scripted chain.
2. **We already own the timing layer.** `bentley/lipsync/rhubarb_adapter.py` + `visemes.py` (18 tests) emit a validated project-viseme timeline and enforce the hard policy Rhubarb-B→CONS-never-closed, `--dialogFile` real transcripts, `--extendedShapes GHX`, pinned vendored rhubarb 1.14.0 at `tools/rhubarb/`. NG re-runs rhubarb with its own bundled binary (version skew risk) and its per-cue mapping is manual UI state that does not carry our tested policy.
3. **The baker is trivial next to what NG replaces.** Keyframing 1 bone channel + ≤6 key values per cue (~40 lines of bpy, Step R6) vs NG's Action-per-cue authoring + NLA strips + a second addon just to bake shape-key tracks.
4. **One pose model.** Our table drives bone AND keys in one `apply_viseme()`; NG splits bone-Actions and shape-key-Actions across separate mapped objects/tracks.

NG remains a legitimate **interactive preview aid** during R5 (scrub cues against poses in the viewport) — but even that is covered by rendering the R6 contact sheet/test line, so the lean call is: don't install it; keep `tools/rhubarb/` as the single rhubarb source of truth.

## Key paths
- Mesh: `/project/scratch/rig_build/bentley_mv.fbx` (also `bentley_norm.blend`, normalized)
- Failure evidence: `/project/scratch/rig_build/jaw/{closed_F,open_F}.png`, `jaw_test4.py`, `step2_talk.py`
- Timing layer to integrate: `/project/bentley/lipsync/{rhubarb_adapter,visemes}.py`; vendored binary `tools/rhubarb/Rhubarb-Lip-Sync-1.14.0-macOS/rhubarb`
- Ready-made baker test fixture: `/project/scratch/rig_build/rh/B_strong.{wav,txt,json}`
- Blender: `/opt/homebrew/bin/blender` (5.1.2)

---

# REPORT 3 — Asset Scout: pre-rigged base candidates
# Asset Scout — Pre-rigged cartoon-dog / quadruped Blender rigs (Plan B for Bentley lip-sync)

Scouted: Blender Studio character library + DOGWALK, BlendSwap, Sketchfab, Quaternius/poly.pizza, TurboSquid/CGTrader free sections. License verdicts verified against the actual pages (studio.blender.org pages fetched directly; Sketchfab license JSON extracted from page source).

## RANKED CANDIDATES

### 1. Blender Studio "Dog" — Wing It! (2023) — BEST FACE RIG, version-pinned, paywalled download
- Link: https://studio.blender.org/characters/dog/v1/
- License: **CC-BY** — page states: "The character is free to use, provided that you respect the CC-BY license and include the credit: Dog Rig (CC-BY) Blender Foundation | studio.blender.org". CC-BY permits commercial use → **SAFE for a monetized kids' YouTube channel** (credit in video description).
- Access gotcha: "Login to Download" — per the page's own comment thread (answered by rig author Demeter Dzadik), the cat and dog rigs "require some level of subscription" (Blender Studio, ~EUR 11.50/mo, cancel anytime). License rights survive after download.
- Rig features: full film-production **CloudRig face rig** — big cartoon smile, **GeoNode-driven inner mouth** (a Surface-Deform reimplementation, per the author), tongue, full facial controls. This is exactly the "mouth interior" tech we're missing. Caveat: it has cartoon TEETH (canon = toothless → hide/scale-out the teeth objects).
- Version pin: **requires exactly Blender 3.6 LTS** — "may break on lower or higher versions", explicitly NOT maintained (author confirmed Oct 2025). On our Blender 5.1.2 it will likely break; you'd keep a side-by-side 3.6 install for this rig.
- Format: .blend. Style match: cartoony lanky dog with a big smile — the closest stylistic cousin to cartoony-Pixar in this list; Boxer-puppy conform = shorten muzzle + jowls + floppy ears + docked stub = moderate-to-heavy sculpt with jaw-pivot re-placement and mouth-weight repaint.

### 2. Spring "Autumn" (2019) — FREE direct download, real quadruped dog-creature, BlenRig face
- Link: https://studio.blender.org/characters/autumn/v1/
- License: **CC-BY**, **free direct download (61.2 MB, no subscription)**. (Note: the page's credit line says "Einar Rig (c) Blender Foundation" — an obvious copy/paste slip on their page; credit it as Autumn Rig CC-BY Blender Foundation | studio.blender.org.)
- Rig features: **BlenRig 5** rig — BlenRig ships one of the most advanced facial systems in free Blender rigs, including **jaw-rotation controls and a tongue**; Autumn is a genuine quadruped dog-like companion (fluffy, game-of-catch personality). Requires the BlenRig add-on; built for Blender 2.80+ (old-generation rig; expect add-on/version friction on 5.1.2; fur is particle-hair, disabled by default).
- Style match: semi-stylized fluffy creature — further from Pixar-cartoony than the Wing It Dog; fur look would be replaced by our short-coat shading. Muzzle is dog-like; conform feasible but the fluffy proportions bleed through.

### 3. DOGWALK "Chocomel" (2025) — FREE, CC-BY, MODERN Blender 4.5, but a GAME rig with minimal face
- Links: https://www.blender.org/download/demo-files/ (entry "Blender 4.5 LTS – DOGWALK, by Blender Studio, 383MB – CC-BY"), project https://studio.blender.org/projects/dogwalk/, rigging write-up https://studio.blender.org/blog/character-rigging-for-project-dogwalk/, GitHub mirror https://github.com/nikitalita/DOGWALK
- License: **CC-BY**, fully free (blender.org demo file + free asset library via Steam/itch).
- Rig features (from the rigging article by Hjalti Hjalmarsson): production rig but built for Godot export — **no bendy bones, strict direct deform-bone hierarchy**; the article's fancy mouth system is for PINDA (the kid; camera-facing papercraft billboard mouth), NOT the dog. The game is dialogue-free → Chocomel has body/ears/jaw-level articulation but **no viseme-grade facial rig**.
- Version: Blender 4.5 LTS — the only candidate near our 5.1.2. Style: papercraft (hand-painted paper textures) — farthest from Pixar look.
- Real value: a clean, modern, license-safe **quadruped skeleton + weight-paint reference** to dissect, not a conform base.

### 4. (REJECT — license trap) BlendSwap "Rigged Dog" #2970
- Link: https://blendswap.com/blend/2970 — tagged CC-BY, "rigged, shape keys, basic expressions library".
- Reject because: author's own description says **"Based off 'Pluto'"** — a Disney character likeness. CC-BY tag cannot clear third-party IP; on a monetized kids' channel this is a real takedown/claim risk. Also ancient (Blender 2.4x/2.6-era, ~2012) and comments indicate the rig is partial ("when you said rigged I expected a full rig").

### 5. (REJECT — license trap) Sketchfab "Cartoon Dog Rigged" (ScaryCartoonCatAndDog) and kin
- Link: https://sketchfab.com/3d-models/cartoon-dog-rigged-2408c57500c04617a2e9be7f78ba2315 — page source confirms CC Attribution 4.0, free.
- Reject because: "Cartoon Dog" is **Trevor Henderson's copyrighted creepypasta character**; a fan upload can't license the underlying IP — and it's a horror meme, double-wrong for a kids' brand. General Sketchfab pattern found in this scout: most CC-tagged "cartoon dog rigs" are fan-IP uploads; additionally Sketchfab serves converted glTF (morph targets survive, but Blender control rigs/constraints do NOT) unless the author attached the source .blend. No clean, original, face-rigged dog surfaced worth ranking.

### 6. (REJECT for this purpose) Quaternius / poly.pizza
- Links: https://quaternius.com/packs/ultimateanimatedanimals.html, https://poly.pizza/
- Genuinely **CC0** (best license on the board) with rigged + animated animals incl. dogs, BUT low-poly game style with **no facial rigs, no shape keys, no mouth interior** — useless for lip-sync. Keep as CC0 body-animation reference only.

Also noted: Wing It! "Cat" rig (same CC-BY family/tech as the Dog) exists if a feline guest character ever needs the same treatment. TurboSquid/CGTrader free sections: no free cartoon-dog with a real facial rig in Blender format surfaced — the face-rigged ones there are paid and mostly Maya.

## HONEST ASSESSMENT — conform-a-base vs rig-our-own-mesh

**What conforming buys us:** the exact things that failed in scratch/rig_build (jaw-open via raw vertex rotation ballooned because there are no weights, no jaw pivot, no mouth interior) come pre-solved in candidate #1: tested weight paint, a correct jaw pivot, an inner-mouth system, a tongue, eyelid controls.

**What conforming costs:**
1. **Identity risk (the #1 project blocker).** Bentley's likeness is owner-validated on the Tripo mesh (/project/scratch/rig_build/bentley_mv.fbx). Sculpting the Wing It Dog into a short-muzzled Boxer puppy is a heavy re-proportioning: muzzle shortening moves the jaw pivot and invalidates mouth/jowl weights (repaint), ear/tail changes are easy, but the base's proportions tend to bleed through → "cousin of Bentley" risk, the same class of drift the owner keeps rejecting.
2. **Texture projection is the easy part** — projecting the black mask / grey chin / white blaze / teal collar from Bentley_MASTER_pixar.png + turnaround onto EITHER mesh is comparable work.
3. **Version pinning.** The best rig (Wing It Dog) is frozen at Blender 3.6 with GeoNodes that likely break on 5.1.2 — a permanent side-by-side 3.6 install and a caged pipeline. Autumn needs BlenRig-era add-on archaeology. Only Chocomel is modern, and it lacks the face.
4. **Money/friction:** #1 needs a one-month Blender Studio subscription (~EUR 11.50) — trivial vs KIE spend, but not "free".

**Effort estimate:** Wing It Dog → Bentley conform ≈ several focused days (subscription, 3.6 setup, proportion sculpt, weight repaint around the new muzzle, retexture, de-teeth) and the output is version-pinned. Rigging our own Tripo mesh ≈ comparable time for v1 (jaw bone + weights + mouth-interior patch + tongue + the 8 viseme shape keys mapped to our existing Rhubarb layer in /project/bentley/lipsync/) — the earlier failure was doing deformation without an armature/weights, not evidence that rigging the mesh is infeasible.

**Recommendation:** don't conform-first. Use the rigs as **dissection references, not bases**: grab Autumn (free, today) and the DOGWALK library (free, modern 4.5) immediately to copy the jaw-bone placement, mouth-interior construction, and quadruped weight-paint patterns onto OUR mesh; optionally spend one subscription month to open the Wing It Dog and clone its GeoNode inner-mouth/tongue setup. That keeps the owner-validated likeness (non-negotiable per the consistency-blocker history) and a modern Blender 5.x pipeline. **Plan B trigger:** if our-own-rig v1 (jaw + visemes) isn't presentable after the first real attempt, fall back to conforming the Wing It Dog in a pinned 3.6 environment — license-wise it is fully cleared (CC-BY + description credit).

Sources:
- [Dog - Character Rig - Blender Studio](https://studio.blender.org/characters/dog/v1/)
- [Characters - Blender Studio](https://studio.blender.org/characters/)
- [Autumn - Character Rig - Blender Studio](https://studio.blender.org/characters/autumn/v1/)
- [Character Rigging for Project DogWalk - Blender Studio](https://studio.blender.org/blog/character-rigging-for-project-dogwalk/)
- [DOGWALK Official Release - Blender Studio](https://studio.blender.org/blog/dogwalk-official-release/)
- [Blender Demo Files (DOGWALK 4.5 LTS, CC-BY)](https://www.blender.org/download/demo-files/)
- [DOGWALK GitHub mirror](https://github.com/nikitalita/DOGWALK)
- [BlendSwap Rigged Dog #2970](https://blendswap.com/blend/2970)
- [Sketchfab Cartoon Dog Rigged (CC-BY, fan-IP)](https://sketchfab.com/3d-models/cartoon-dog-rigged-2408c57500c04617a2e9be7f78ba2315)
- [Quaternius Ultimate Animated Animal Pack (CC0)](https://quaternius.com/packs/ultimateanimatedanimals.html)
- [Advanced Rigging (BlenRig) - Blender Studio](https://studio.blender.org/training/blenrig/)
- [Rigged Cartoon Dog - TurboSquid](https://www.turbosquid.com/3d-model/rigged/cartoon-dog)
- [Dog 3D models - CGTrader](https://www.cgtrader.com/3d-models/dog-rig)

---

# REPORT 4 — Skill Writer
DRAFTED AND WRITTEN TO DISK: /project/.claude/skills/lipsync-pro/SKILL.md

Sources read before drafting: docs/guides/LIPSYNC_PRO_RESEARCH_2026-07.md, HIGH_QUALITY_LIPSYNC_SYSTEM_PLAN.md, LIPSYNC_SYSTEM_RUNBOOK.md, TALKING_LIPSYNC_METHOD.md, bentley/lipsync/*.py docstrings (rhubarb_adapter, visemes, pipeline, characters, plates, qa_sweep, calibrate), youtube_vault/Production/Lip-Sync Rig System.md, episode-production SKILL §0.3/§5/§5a, plus the memory laws (bentley-lipsync-pro-research.md — OmniHuman Bentley ban + wrong-speaker root cause + KIE hosting/taskId gotchas; bentley-3d-rig-build.md — rig status, Blender commands, camera/forward-axis techniques) and the working scripts scratch/omni_ep3/gen_line.py, qa_line.py, scratch/rig_build/step1_normalize.py, step2_talk.py.

The full SKILL.md text follows (exactly as written to disk):

---
name: lipsync-pro
description: >-
  Use when ANY character must speak on screen in "Bentley's Big Adventures" — planning, generating,
  rendering, fixing, or QA-ing a talking shot, dialogue plate, lip-sync pass, Avatar/OmniHuman call,
  Rhubarb/viseme timing, or the Blender rig. Also use when a mouth flaps 

(Full skill lives at .claude/skills/lipsync-pro/SKILL.md — registered and live.)
