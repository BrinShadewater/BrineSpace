"""Record door provenance, refresh card references and build the owner review."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pack=ROOT/'assets/door-polish-v1'
out=ROOT/'output/door-polish-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'prompt':p.name.replace('-source.png','.prompt.txt')} for p in [pack/'low-source.png',pack/'riser-source.png']]
cards=json.loads((pack/'cards/runtime.json').read_text())
for name in ['scripts/room_card_art.gd','scripts/grid_canvas.gd']:
    p=ROOT/name;s=p.read_text()
    for row in cards:
        rid=row['room'];target='res://assets/door-polish-v1/cards/'+rid+'.png'
        pattern=r'("'+re.escape(rid)+r'":\s*\[?")res://[^"\n]+\.png(")'
        s,n=re.subn(pattern,lambda m:m[1]+target+m[2],s)
        assert n in ([1] if name.endswith('room_card_art.gd') else [1,2]),(name,rid,n)
    p.write_text(s)
manifest={'sources':sources,'finishes':['bio','life-support','engineering','generic','brine'],'geometry':['low front','low side','raised north','BRINE default sockets','airlock inner/outer'],'aperture_world':72,'source_pixels':'Unmodified; runtime rectangular UV registration excludes backgrounds.','review':{'materials':'Native review complete, owner acceptance pending','dry_frames':150,'wet_frames':40,'native_integration':'output/door-polish-v1/integration.log','physics':'output/door-polish-v1/physics.log','coverage':'Shared live door renderers and 44 furnished-room cards; corridor card silhouettes retained.'}}
(pack/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
records=json.loads((out/'manifest.json').read_text())
html='''<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Door artwork and flooding review</title><style>
body{margin:0;background:#14272c;color:#d6e3dd;font:16px system-ui}main{max-width:1320px;margin:40px auto;padding:0 24px}h1{font-weight:550}p{max-width:850px;line-height:1.6}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px}article{background:#22363a;border:1px solid #3d585a;border-radius:10px;padding:14px}img{width:100%;image-rendering:auto}input{width:100%}button{padding:8px 16px;color:#d6e3dd;background:#345652;border:1px solid #668d85;border-radius:5px}textarea{box-sizing:border-box;width:100%;min-height:64px;background:#172b30;color:#d6e3dd;border:1px solid #587174;padding:10px;margin-top:10px}.room{max-width:460px}small{color:#b0c6be}</style><main>
<h1>Door artwork &amp; flooded closing</h1><p>Detailed latches, service plates, seals and status indicators across the door set. The wet sequence adds amber closure lights, narrowing foam and pressure ripples. Flow stops when the door seals. Existing water simulation and crew clearance are preserved.</p>
<p>Drag any slider to inspect a frame. The two flooding studies play automatically. Notes stay in this browser; use Export notes to save them.</p><button id="export">Export notes</button><h2>Flooded closing</h2><section class="grid" id="wet"></section><h2>Five finishes, three views</h2><section class="grid" id="dry"></section><h2>In BRINE</h2><img class="room" src="../../assets/door-polish-v1/cards/brine_core.png"><details><summary>Live station closing check</summary><img src="station-closing-2.png"></details><p><small>Review frames are enlarged for inspection. Native station, pause, aperture, airlock and water checks pass. Some older fixtures report resource cleanup warnings at exit. Owner visual acceptance is pending.</small></p></main><script>
const records=RECORDS;let notes=JSON.parse(localStorage.getItem('door-polish-notes')||'{}');
for(const r of records){const wet=r.variant==='flooding',id=r.variant+'-'+r.kind;const c=document.createElement('article');c.innerHTML=`<h3>${r.variant} · ${r.kind}</h3><img alt="${id}"><input type="range" min="0" max="${r.frames.length-1}" value="0" aria-label="${id} animation frame"><button>Play</button><textarea aria-label="Notes for ${id}" placeholder="Notes or fixes…"></textarea>`;let frame=0,playing=wet;const img=c.querySelector('img'),slider=c.querySelector('input'),button=c.querySelector('button'),note=c.querySelector('textarea');const show=()=>{img.src=r.frames[frame];slider.value=frame};button.textContent=playing?'Pause':'Play';button.onclick=()=>{playing=!playing;button.textContent=playing?'Pause':'Play'};slider.oninput=()=>{playing=false;button.textContent='Play';frame=+slider.value;show()};note.value=notes[id]||'';note.oninput=()=>{notes[id]=note.value;localStorage.setItem('door-polish-notes',JSON.stringify(notes))};setInterval(()=>{if(playing){frame=(frame+1)%r.frames.length;show()}},wet?110:170);show();document.getElementById(wet?'wet':'dry').append(c)}
document.getElementById('export').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(notes,null,2)],{type:'application/json'}));a.download='door-polish-notes.json';a.click();URL.revokeObjectURL(a.href)};
</script></html>'''.replace('RECORDS',json.dumps(records))
(out/'index.html').write_text(html,encoding='utf-8')
print(f'{len(cards)} card references updated; {len(records)} review sequences; 2 source hashes recorded')
