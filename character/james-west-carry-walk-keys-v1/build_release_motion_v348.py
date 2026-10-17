import json,hashlib
from pathlib import Path
from PIL import Image
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';o=p/'release-motion-review-v348';old=p/'selected-family-audit-v333'
current=json.loads((o/'selected-inventory.json').read_text());previous=json.loads((old/'selected-inventory.json').read_text());provenance=json.loads((old/'pixel-provenance.json').read_text());assert current['failures']==0
families=['idle','walk','inspect','repair','weld','carry','unload','sit-down','sit-idle','sit-rise','lie-down','sleep','get-up','swim','swim-distress','recover-air','death-ground','death-water']
groups={};protected=0
for gear in ['bare','diving-helmet']:
    bank={row['key']:row for row in current['gears'][gear]};origin={row['key']:row for row in provenance['gears'][gear]}
    for row in previous['gears'][gear]:
        assert bank[row['key']]==row,(gear,row['key']);protected+=row['frameCount']
    for family in families:
        for direction in ['west','east','north','south']:
            key=family+'-'+direction
            if key not in origin:continue
            row=bank[key];paths=[]
            for i,matches in enumerate(origin[key]['sourceMatches']):
                file=r/matches[0];image=Image.open(file).convert('RGBA');assert hashlib.sha256(image.tobytes()).hexdigest()==row['pixelHashes'][i]
                paths.append('/'+file.relative_to(r).as_posix())
            groups.setdefault(family,[]).append({'gear':gear,'direction':direction,'paths':paths,'meta':row['metadata'],'clocks':row['durationsMs'],'loop':row['loop']})
    for direction in ['west','east','north','south']:
        for target in ['west','east','north','south']:
            if direction==target:continue
            key='carry-turn-'+direction+'-'+target
            if key not in origin:continue
            row=bank[key]
            for index,matches in enumerate(origin[key]['sourceMatches']):
                assert hashlib.sha256(Image.open(r/matches[0]).convert('RGBA').tobytes()).hexdigest()==row['pixelHashes'][index],(gear,key,index)
            groups.setdefault('turn-'+direction,[]).append({'gear':gear,'direction':target,'paths':['/'+Path(matches[0]).as_posix().replace('\\','/') for matches in origin[key]['sourceMatches']],'meta':row['metadata'],'clocks':row['durationsMs'],'loop':row['loop']})
(o/'playback.json').write_text(json.dumps(groups))
(o/'index.html').write_text('''<!doctype html><html><meta charset="utf-8"><title>James release motion review</title><style>body{background:#303b40;color:#eee;font:16px system-ui;margin:18px}button,select{font:inherit;margin:5px;padding:5px}canvas{width:1024px;max-width:100%;image-rendering:pixelated}p{max-width:1000px}#status{white-space:pre-wrap}</style><h2>James — selected animation playback</h2><label>Animation <select id="family"></select></label><button id="replay">Replay</button><button id="pause">Pause</button><label>Standing height <select id="scale"><option>82</option><option>148</option><option>54</option><option>27</option></select> px</label><p>All directions, bare above and helmet below. Original source pixels, fixed foot anchors and selected clocks. Finite actions hold their endpoint. This is source playback, not station collision or furniture acceptance.</p><canvas id="board" width="1024" height="660"></canvas><p id="status">Loading selected sources…</p><script>
let groups,rows=[],started=0,paused=false,held=0,loaded=false;const canvas=document.querySelector('canvas'),ctx=canvas.getContext('2d'),family=document.querySelector('#family'),status=document.querySelector('#status'),cache=new Map();
async function select(){loaded=false;status.textContent='Loading…';rows=groups[family.value];for(const row of rows){row.images=await Promise.all(row.paths.map(path=>{if(cache.has(path))return cache.get(path);const result=new Promise((resolve,reject)=>{const img=new Image;img.onload=()=>resolve(img);img.onerror=reject;img.src=path});cache.set(path,result);return result}))}loaded=true;started=performance.now();held=0;paused=false;document.querySelector('#pause').textContent='Pause'}
fetch('playback.json').then(r=>r.json()).then(data=>{groups=data;for(const name of Object.keys(data)){const op=document.createElement('option');op.value=op.textContent=name;family.append(op)}select()});family.onchange=select;document.querySelector('#replay').onclick=select;document.querySelector('#pause').onclick=()=>{if(!paused)held=performance.now()-started;else started=performance.now()-held;paused=!paused;document.querySelector('#pause').textContent=paused?'Play':'Pause'};
function draw(){ctx.fillStyle='#303b40';ctx.fillRect(0,0,1024,660);if(loaded){let elapsed=paused?held:performance.now()-started;const scale=Number(document.querySelector('#scale').value)/148;let trace=[];for(const row of rows){const total=row.clocks.reduce((a,b)=>a+b,0);let cursor=row.loop?elapsed%total:Math.min(elapsed,total-.001);let index=0;while(index<row.clocks.length-1&&cursor>=row.clocks[index])cursor-=row.clocks[index++];const x=128+256*['west','east','north','south'].indexOf(row.direction),y=row.gear==='bare'?220:540,m=row.meta[index],im=row.images[index];ctx.imageSmoothingEnabled=false;ctx.drawImage(im,x-m.pivot[0]*scale,y-m.pivot[1]*scale,im.width*scale,im.height*scale);ctx.fillStyle='#fff';ctx.font='14px system-ui';ctx.fillText(row.gear+' '+row.direction+' · '+index,x-110,y+88);trace.push(row.gear+'/'+row.direction+':'+index)}status.textContent=(paused?'Paused':'Playing')+' · '+Math.round(elapsed)+' ms · '+trace.join(' | ')}requestAnimationFrame(draw)}requestAnimationFrame(draw);
</script></html>''')
(o/'playback-binding.json').write_text(json.dumps({'protectedOriginalSlots':protected,'groups':len(groups),'rows':sum(map(len,groups.values())),'newWaterRows':sum(len(current['gears'][g])-len(previous['gears'][g]) for g in current['gears']),'scope':'Fresh normal loader inventory compared with V333: all original row pixels/metadata/clocks exact; source playback paths verified. New installed water rows counted separately.'},indent=2))
html=o/'index.html';text=html.read_text();text=text.replace('rows=groups[family.value];for(const row of rows)','const selected=groups[family.value];for(const row of selected)').replace('loaded=true;started=performance.now()','if(groups[family.value]!==selected)return;rows=selected;loaded=true;started=performance.now()');html.write_text(text.replace('height="660"','height="500"').replace('1024,660','1024,500').replace("?220:540","?180:390").replace('y+88','y+75').replace('—','-').replace('…','...').replace('·','/'),encoding='utf8')
print(f'V348 protected {protected} original selected slots; playback {len(groups)} groups')
