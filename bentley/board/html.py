"""Render episodes/<ep>/board.html — a self-contained, browser-viewable production canvas.

The board.json is inlined as a JS object and rendered client-side, so the file opens directly in any
browser (file://) with no server. Regenerate anytime: `python -m bentley.board render <ep>` (also writes
BOARD.md) or `python -m bentley.board html <ep>`. Dark "mission-control" dashboard; fully offline (system
fonts, no CDN)."""
import json

_TEMPLATE = r"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ — Production Board</title>
<style>
  :root{
    --bg:#0a0e1a; --bg2:#0e1424; --card:rgba(255,255,255,.028); --card2:rgba(255,255,255,.05);
    --line:rgba(255,255,255,.08); --line2:rgba(255,255,255,.14);
    --tx:#e8ecf6; --tx2:#9aa6be; --tx3:#66708a;
    --lock:#34d399; --pend:#fbbf24; --rest:#fb7185; --key:#38bdf8; --todo:#7c89a6; --rev:#a78bfa;
    --accent:#22d3ee; --accent2:#a78bfa;
    --mono:"SF Mono","JetBrains Mono",ui-monospace,"Cascadia Code",Menlo,Consolas,monospace;
    --sans:-apple-system,"SF Pro Display",Inter,"Segoe UI",system-ui,sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;font-family:var(--sans);color:var(--tx);
    background:
      radial-gradient(1200px 600px at 80% -10%, rgba(167,139,250,.10), transparent 60%),
      radial-gradient(1000px 500px at -10% 10%, rgba(34,211,238,.08), transparent 55%),
      var(--bg);
    -webkit-font-smoothing:antialiased;line-height:1.5;min-height:100vh}
  .wrap{max-width:1220px;margin:0 auto;padding:34px 26px 80px}
  .mono{font-family:var(--mono)}
  a{color:var(--accent)}
  .h{color:var(--tx3);font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin:0 0 12px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px}
  .grid{display:grid;gap:14px}

  /* header */
  header{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap;margin-bottom:8px}
  .brand{font-size:13px;letter-spacing:.34em;text-transform:uppercase;color:var(--tx3);font-weight:600}
  h1{margin:6px 0 0;font-size:30px;font-weight:650;letter-spacing:-.01em;
    background:linear-gradient(92deg,#fff, #b8c6ff 60%, var(--accent));-webkit-background-clip:text;background-clip:text;color:transparent}
  .sub{color:var(--tx2);font-size:14px;margin-top:5px}
  .stagepill{display:inline-flex;align-items:center;gap:9px;padding:9px 16px;border-radius:100px;
    background:linear-gradient(100deg,rgba(34,211,238,.16),rgba(167,139,250,.16));
    border:1px solid rgba(167,139,250,.32);font-weight:600;font-size:14px;color:#e7ecff}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px rgba(34,211,238,.18);animation:pulse 2.4s infinite}
  @keyframes pulse{0%,100%{opacity:1}50%{opacity:.45}}

  /* next-action banner */
  .next{margin:20px 0;display:flex;gap:16px;align-items:center;
    background:linear-gradient(100deg,rgba(251,191,36,.10),rgba(251,191,36,.03));
    border:1px solid rgba(251,191,36,.28);border-radius:16px;padding:16px 20px}
  .next .k{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--pend);font-weight:700}
  .next .v{font-size:16px;color:#fde6bf;font-weight:550;margin-top:2px}

  /* stats */
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:12px;margin:18px 0 24px}
  .stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;text-align:left}
  .stat .n{font-size:26px;font-weight:650;line-height:1}
  .stat .l{font-size:11px;color:var(--tx2);margin-top:6px;text-transform:capitalize;letter-spacing:.02em}

  /* stage rail */
  .rail{display:flex;gap:6px;margin:2px 0 26px;flex-wrap:wrap}
  .step{flex:1;min-width:96px;padding:11px 10px 10px;border-radius:11px;border:1px solid var(--line);
    background:var(--card);font-size:12.5px;color:var(--tx3);position:relative;text-transform:capitalize}
  .step .idx{font-family:var(--mono);font-size:10px;color:var(--tx3);display:block;margin-bottom:3px}
  .step.done{color:var(--tx2)} .step.done .idx{color:var(--lock)}
  .step.now{border-color:rgba(34,211,238,.5);background:linear-gradient(120deg,rgba(34,211,238,.12),rgba(167,139,250,.10));color:#eaf6ff;font-weight:600}
  .step.now .idx{color:var(--accent)}

  /* manifest */
  .man{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}
  .chip{display:inline-block;font-family:var(--mono);font-size:11px;color:var(--tx2);
    background:rgba(255,255,255,.05);border:1px solid var(--line);border-radius:7px;padding:2px 7px;margin:3px 4px 0 0}
  .manrow b{font-weight:600;font-size:13.5px}

  /* shot board */
  .board{display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:14px}
  .shot{background:var(--card);border:1px solid var(--line);border-left-width:3px;border-radius:14px;
    padding:15px 16px;transition:transform .12s,border-color .12s,background .12s}
  .shot:hover{transform:translateY(-2px);background:var(--card2);border-color:var(--line2)}
  .shot .top{display:flex;justify-content:space-between;align-items:center;gap:8px}
  .shot .id{font-family:var(--mono);font-size:16px;font-weight:600;letter-spacing:-.01em}
  .shot .beat{color:var(--tx3);font-size:12px;margin:1px 0 12px;text-transform:capitalize}
  .badge{font-size:11px;font-weight:700;letter-spacing:.03em;padding:4px 10px;border-radius:100px;white-space:nowrap}
  .lockicon{margin-left:5px}
  .row{display:flex;gap:8px;font-size:12.5px;margin:5px 0;align-items:baseline}
  .row .rk{color:var(--tx3);min-width:52px;font-size:11px;text-transform:uppercase;letter-spacing:.04em}
  .row .rv{color:var(--tx);flex:1}
  .row .rv.q{color:#cdd6ea;font-style:italic}
  .path{font-family:var(--mono);font-size:11px;color:var(--tx2);word-break:break-all}
  .rr{display:inline-flex;gap:4px;align-items:center}
  .rr i{width:7px;height:7px;border-radius:50%;background:var(--line2);display:inline-block}
  .rr i.on{background:var(--pend)}
  .flag{margin-top:9px;font-size:11.5px;font-weight:600;color:var(--rest);
    background:rgba(251,113,133,.10);border:1px solid rgba(251,113,133,.3);border-radius:9px;padding:6px 9px}
  .flag.cos{color:var(--tx2);background:rgba(255,255,255,.04);border-color:var(--line)}

  /* two col */
  .cols{display:grid;grid-template-columns:1.15fr .85fr;gap:16px;margin-top:24px}
  @media(max-width:820px){.cols{grid-template-columns:1fr}}
  .dec{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--line)}
  .dec:last-child{border-bottom:0}
  .dec .d{font-family:var(--mono);font-size:11px;color:var(--tx3);min-width:44px;padding-top:2px}
  .dec .scope{font-family:var(--mono);font-size:10px;color:var(--accent2);background:rgba(167,139,250,.1);border-radius:5px;padding:1px 6px}
  .dec .cost{font-family:var(--mono);font-size:11px;color:var(--pend);float:right}
  .proto{counter-reset:p}
  .proto li{list-style:none;font-size:13px;color:var(--tx);margin:9px 0;padding-left:30px;position:relative}
  .proto li:before{counter-increment:p;content:counter(p);position:absolute;left:0;top:-1px;
    width:20px;height:20px;border-radius:6px;background:rgba(34,211,238,.12);border:1px solid rgba(34,211,238,.3);
    color:var(--accent);font-family:var(--mono);font-size:11px;display:flex;align-items:center;justify-content:center}
  .foot{margin-top:30px;color:var(--tx3);font-size:11.5px;text-align:center}
  .glow{box-shadow:0 0 26px -8px var(--gc,transparent)}
  .sechead{display:flex;align-items:center;gap:11px;margin:26px 2px 13px;font-size:15px;font-weight:600;color:var(--tx2)}
  .sechead.cur{color:#eaf6ff;border-left:3px solid var(--accent);padding-left:11px}
  .secn{font-family:var(--mono);font-size:11px;color:var(--accent);background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.28);border-radius:6px;padding:2px 8px}
  .secb{font-size:11px;font-weight:600;padding:3px 11px;border-radius:100px;margin-left:auto}
  .secb.rev{color:var(--lock);background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.3)}
  .secb.rdy{color:var(--pend);background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.3)}
  .secb.wip{color:var(--tx3);background:rgba(255,255,255,.04);border:1px solid var(--line)}
  .curtag{font-size:11px;color:var(--accent);font-weight:600}
  a.flink{color:var(--accent);text-decoration:none;cursor:pointer;border-bottom:1px dashed rgba(34,211,238,.35)}
  a.flink:hover{color:#67e8f9;border-bottom-color:var(--accent)}
  .chip a.flink{color:var(--tx2)}
  .chip a.flink:hover{color:#67e8f9}
</style>
</head>
<body>
<div class="wrap" id="app"></div>
<script>
const INLINE = __BOARD_JSON__;
let BOARD = INLINE, LIVE = false, __last = JSON.stringify(INLINE);
const S = {
  locked:      {l:'locked',      c:'var(--lock)', bg:'rgba(52,211,153,.14)'},
  owner_review:{l:'owner review',c:'var(--rev)',  bg:'rgba(167,139,250,.14)'},
  qc:          {l:'qc',          c:'var(--pend)', bg:'rgba(251,191,36,.14)'},
  rendered:    {l:'rendered',    c:'var(--pend)', bg:'rgba(251,191,36,.14)'},
  kf_approved: {l:'keyframe ✓',  c:'var(--key)',  bg:'rgba(56,189,248,.14)'},
  keyframe:    {l:'keyframe',    c:'var(--key)',  bg:'rgba(56,189,248,.14)'},
  todo:        {l:'todo',        c:'var(--todo)', bg:'rgba(124,137,166,.14)'},
};
const STAGES=['premise','vo','animatic','keyframes','renders','assemble','mix_grade','qa','release'];
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const el=(h)=>{const d=document.createElement('div');d.innerHTML=h.trim();return d.firstChild;};

function voStr(s){return (s.vo||[]).map(v=>typeof v==='object'?v.label:v).join(' · ')||'—';}
function voText(s){for(const v of (s.vo||[])){if(typeof v==='object'&&v.text)return v.text;}return '';}
function currentSection(b){for(const s of (b.sections||[]))if(!s.reviewed)return s;return null;}
function shotsInSec(b,id){return (b.shots||[]).filter(s=>s.section===id);}
function nextShot(b){const c=currentSection(b);if(!c)return null;for(const s of (b.shots||[]))if(s.section===c.id&&!s.locked)return s;return null;}
function shotHint(s){if(s.must_restage)return 'restage as a natural ACTION per its VO, then render';const st=s.state;if(st==='kf_approved')return 'render (keyframe locked)';if(['rendered','qc','owner_review'].includes(st))return 'QC → present → owner approve';return 'keyframe → owner pick → render';}
function computeNext(b){if(!(b.sections||[]).length)return b.next_action||'';const c=currentSection(b);if(!c)return 'ALL portions reviewed → assemble the full episode (mix · grade · QA)';const ns=nextShot(b);if(ns)return (ns.sid||ns.id)+' — '+shotHint(ns)+'  ·  section '+c.id+': '+(c.title||'');return "section "+c.id+" ('"+(c.title||'')+"') renders COMPLETE → assemble it with VO + owner review before the next portion";}
// a repo-relative path -> a clickable link that reveals the file in Finder (served) or opens it (file://).
function fileLink(p, text){ if(!p) return esc(text||'—'); return `<a href="../../${esc(p)}" class="flink" data-p="${esc(p)}" title="click to reveal in Finder">${esc(text!=null?text:p)}</a>`; }

function render(){
  const b=BOARD, app=document.getElementById('app');
  const counts={}; (b.shots||[]).forEach(s=>counts[s.state]=(counts[s.state]||0)+1);
  const locked=(b.shots||[]).filter(s=>s.locked).length, total=(b.shots||[]).length;

  // header
  let h=`<header>
    <div><div class="brand">Bentley&nbsp;·&nbsp;Discovery&nbsp;Club</div>
      <h1>${esc(b.episode)} · ${esc(b.title||'')}</h1>
      <div class="sub">guest: ${esc(b.guest||'—')} &nbsp;·&nbsp; ${total} shots &nbsp;·&nbsp; production board</div></div>
    <div class="stagepill"><span class="dot"></span> stage: ${esc(b.stage||'—')}</div>
  </header>`;

  const nextTxt=computeNext(b);
  if(nextTxt) h+=`<div class="next"><div><div class="k">next action · in order</div>
     <div class="v">${esc(nextTxt)}</div></div></div>`;

  // stats
  const order=['locked','owner_review','qc','rendered','kf_approved','keyframe','todo'];
  h+=`<div class="stats">
    <div class="stat"><div class="n" style="color:var(--lock)">${locked}</div><div class="l">locked</div></div>`;
  order.filter(k=>k!=='locked'&&counts[k]).forEach(k=>{const st=S[k];
    h+=`<div class="stat"><div class="n" style="color:${st.c}">${counts[k]}</div><div class="l">${st.l}</div></div>`;});
  const cr=b.credits||{}; if(cr.balance!=null)
    h+=`<div class="stat"><div class="n" style="color:var(--accent)">${Number(cr.balance).toLocaleString()}</div><div class="l">credits</div></div>`;
  h+=`</div>`;

  // stage rail
  const curi=STAGES.indexOf(b.stage);
  h+=`<div class="rail">`+STAGES.map((s,i)=>{
    const cl=i<curi?'done':(i===curi?'now':'');
    return `<div class="step ${cl}"><span class="idx">${String(i+1).padStart(2,'0')}</span>${s.replace('_',' · ')}</div>`;
  }).join('')+`</div>`;

  // manifest
  const cn=b.canon||{};
  h+=`<div class="card" style="margin-bottom:16px"><div class="h">locked asset manifest · the canon</div><div class="man">`;
  if(cn.style_anchor) h+=`<div class="manrow"><b>style</b><br><span class="chip">${fileLink(cn.style_anchor, cn.style_anchor.split('/').pop())}</span><span class="chip">painterly VOID</span></div>`;
  for(const [nm,c] of Object.entries(cn.characters||{})){
    h+=`<div class="manrow"><b>${esc(nm)}</b><br>`+Object.entries(c).map(([k,v])=>{
      const val=String(v); const inner = val.includes('/') ? fileLink(val, val.split('/').pop()) : esc(val);
      return `<span class="chip">${esc(k)}: ${inner}</span>`;}).join('')+`</div>`;}
  if(cn.environments&&Object.keys(cn.environments).length)
    h+=`<div class="manrow"><b>plates</b><br>`+Object.entries(cn.environments).map(([k,v])=>`<span class="chip">${fileLink(String(v), k)}</span>`).join('')+`</div>`;
  if(cn.models_LOCKED)
    h+=`<div class="manrow"><b>models · locked</b><br>`+Object.values(cn.models_LOCKED).map(v=>`<span class="chip">${esc(v)}</span>`).join('')+`</div>`;
  h+=`</div></div>`;

  // shot board — grouped by section (in-order portions)
  const shotCard=(s)=>{
    const st=S[s.state]||S.todo;
    const rr=[0,1].map(i=>`<i class="${i<(s.rerolls||0)?'on':''}"></i>`).join('');
    const vt=voText(s);
    return `<div class="shot glow" style="border-left-color:${st.c};--gc:${st.bg}">
      <div class="top"><span class="id">${esc(s.sid||s.id)}</span>
        <span class="badge" style="color:${st.c};background:${st.bg}">${st.l}${s.locked?'<span class="lockicon">🔒</span>':''}</span></div>
      <div class="beat">${esc(s.beat||'')}</div>
      ${s.purpose?`<div class="row"><span class="rk">feel</span><span class="rv">${esc(s.purpose)}</span></div>`:''}
      <div class="row"><span class="rk">vo</span><span class="rv">${esc(voStr(s))}</span></div>
      ${vt?`<div class="row"><span class="rk"></span><span class="rv q">"${esc(vt)}"</span></div>`:''}
      ${s.action?`<div class="row"><span class="rk">action</span><span class="rv">${esc(s.action)}</span></div>`:''}
      <div class="row"><span class="rk">reroll</span><span class="rv"><span class="rr">${rr}</span> <span style="color:var(--tx3);font-size:11px">${s.rerolls||0}/2</span></span></div>
      ${s.keyframe?`<div class="row"><span class="rk">keyframe</span><span class="rv path">${fileLink(s.keyframe)}</span></div>`:''}
      ${s.deliverable?`<div class="row"><span class="rk">clip ▸</span><span class="rv path">${fileLink(s.deliverable)}</span></div>`:''}
      ${s.must_restage?`<div class="flag">⚠ reroll cap hit → RESTAGE (new staged action, no reroll #3)</div>`:''}
      ${s.cosmetic_defer?`<div class="flag cos">cosmetic defect → deferred to assembly (never gates approval)</div>`:''}
    </div>`;
  };
  h+=`<div class="h" style="margin-top:26px">shot board · ${total} shots · ${(b.sections||[]).length||1} portions · produced IN ORDER</div>`;
  const curSec=currentSection(b);
  const secs=(b.sections||[]).length?b.sections:[{id:null,title:''}];
  secs.forEach(sec=>{
    const list=sec.id==null?(b.shots||[]):shotsInSec(b,sec.id);
    if(!list.length)return;
    const heroes=list.filter(s=>s.plan==='kling');
    const done=heroes.length>0&&heroes.every(s=>s.locked);
    const badge=sec.reviewed?`<span class="secb rev">reviewed ✓</span>`
      :(done?`<span class="secb rdy">renders done · assemble + VO-review</span>`:`<span class="secb wip">in progress</span>`);
    const isCur=curSec&&curSec.id===sec.id;
    if(sec.id!=null) h+=`<div class="sechead${isCur?' cur':''}"><span class="secn">section ${sec.id}</span> <span>${esc(sec.title||'')}</span> ${badge}${sec.cut?` <span class="chip">${fileLink(sec.cut,'▸ section cut')}</span>`:''}${isCur?`<span class="curtag">◀ current portion</span>`:''}</div>`;
    h+=`<div class="board">`+list.map(shotCard).join('')+`</div>`;
  });

  // decisions + protocol
  const proto=[
    'Read the board FIRST, every session — the single source of truth.',
    'Act only on next_action — one shot / one wave at a time.',
    'Update the board after every step; an action not on the board didn\'t happen.',
    'Never touch a LOCKED shot — QC is a pre-approval gate only.',
    'A shot advances state only by passing its gate.',
    'Reroll ≤2 → RESTAGE → trim → flag; the board refuses reroll #3.',
    'Cosmetic ≠ blocking — it never gates an owner approval.'];
  h+=`<div class="cols">
    <div class="card"><div class="h">decisions log · structured</div>`+
    (b.decisions||[]).map(d=>`<div class="dec"><div class="d">${esc(d.date||'')}</div>
       <div style="flex:1"><span class="scope">${esc(d.scope||'')}</span>
       ${d.cost!=null?`<span class="cost">${esc(d.cost)}cr</span>`:''}
       <div style="margin-top:4px;color:var(--tx);font-size:13px">${esc(d.decision||'')}</div></div></div>`).join('')
    +`</div>
    <div class="card"><div class="h">agent protocol · the rails</div><ol class="proto">`+
    proto.map(p=>`<li>${esc(p)}</li>`).join('')+`</ol></div>
  </div>`;

  const liveTxt = LIVE
    ? '<span style="color:var(--lock)">● live</span> · updates automatically'
    : '<span style="color:var(--tx3)">○ static snapshot</span> · refresh (⌘R) after changes, or run <span class="mono">make board-serve</span> for live';
  h+=`<div class="foot">${liveTxt} · from <span class="mono">episodes/${esc(b.episode)}/board.json</span></div>`;

  app.innerHTML=h;
}
render();

// CLICKABLE PATHS: reveal the file in Finder when served (/__open); else open it in the browser (file://).
document.addEventListener('click', function(e){
  const a = e.target.closest('a.flink'); if(!a) return;
  e.preventDefault();
  const p = a.getAttribute('data-p');
  fetch('/__open?path=' + encodeURIComponent(p)).then(function(r){
    if(r.ok){ const o=a.style.color; a.style.color='var(--lock)'; setTimeout(function(){a.style.color=o;}, 700); }
    else { window.open(a.getAttribute('href')); }
  }).catch(function(){ window.open(a.getAttribute('href')); });
});

// LIVE MODE: when served over http, poll board.json and auto-re-render on change (no refresh needed).
// Over file:// the fetch fails silently and the page stays a static snapshot.
async function poll(){
  try{
    const r = await fetch('board.json', {cache:'no-store'});
    if(!r.ok) return;
    const t = await r.text();
    let changed = false;
    if(t !== __last){ __last = t; BOARD = JSON.parse(t); changed = true; }
    if(!LIVE){ LIVE = true; changed = true; }
    if(changed) render();
  }catch(e){ /* file:// or no server — remain static */ }
}
poll();
setInterval(poll, 2000);
</script>
</body>
</html>"""


def render_html(board):
    data = json.dumps(board, ensure_ascii=False).replace("</", "<\\/")
    return _TEMPLATE.replace("__BOARD_JSON__", data).replace("__TITLE__", str(board.get("episode", "board")))
