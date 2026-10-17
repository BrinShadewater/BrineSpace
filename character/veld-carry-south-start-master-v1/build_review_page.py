from pathlib import Path
import json
P=Path(__file__).resolve().parent
clips={}
for gear in ['bare','helmet']:
 data=json.loads((P/f'{gear}-manifest.json').read_text(encoding="utf-8"))
 clips[gear]={s['id'].split('-')[1]:{'frames':['/'+x.removeprefix('res://') for x in s['frameFiles']],'durations':s['frameDurationsMs']} for s in data['states'] if s['id'] in ['carry-start-south','carry-stop-south']}
page='''<!doctype html><meta charset="utf-8"><title>Veld South master carry start and stop</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:28px}img{max-width:100%}.motion{width:512px;image-rendering:pixelated}.stage{position:relative;width:512px;height:512px}.stage img{position:absolute;inset:0;width:512px;height:512px}button,select{font:inherit;padding:7px;margin:4px}output{margin:12px}</style><h1>Veld South - first carrying step</h1><p>Whole-body first steps with exact planted and stride endpoints. Travel coordination and gameplay transitions remain under review.</p><label>Action <select id="action"><option value="start">Start</option><option value="stop">Stop</option></select></label><label>Equipment <select id="gear"><option value="bare">Bare</option><option value="helmet">Helmet</option></select></label><label>Speed <select id="speed"><option value="1">Normal</option><option value="0.25">Slow review</option></select></label><div><button id="play">Play</button><button id="replay">Replay</button><button id="previous">Previous pose</button><button id="next">Next pose</button><output id="phase">Pose 1 / 4</output></div><div class="stage"><img id="pose" class="motion"></div><p>Slow review changes this preview only. Game timing stays unchanged.</p><h2>All poses</h2><img src="paired-start-stop.png"><script>
const clips=__CLIPS__,action=document.getElementById('action'),gear=document.getElementById('gear'),speed=document.getElementById('speed'),pose=document.getElementById('pose'),phase=document.getElementById('phase'),play=document.getElementById('play');
let elapsed=0,index=0,playing=false,last=performance.now();
function clip(){return clips[gear.value][action.value]}
function total(){return clip().durations.reduce((a,b)=>a+b,0)}
function show(){let cursor=elapsed;index=clip().frames.length-1;for(let i=0;i<clip().frames.length;i++){cursor-=clip().durations[i];if(cursor<0){index=i;break}}pose.src=clip().frames[index];phase.textContent='Pose '+(index+1)+' / '+clip().frames.length+(elapsed>=total()?' - complete':'');phase.dataset.phase=index;phase.dataset.elapsed=elapsed.toFixed(1);phase.dataset.action=action.value;phase.dataset.gear=gear.value;play.textContent=playing?'Pause':'Play'}
function reset(){elapsed=0;playing=false;last=performance.now();show()}
action.onchange=reset;gear.onchange=reset;speed.onchange=()=>{last=performance.now()};
play.onclick=()=>{if(elapsed>=total())elapsed=0;playing=!playing;last=performance.now();show()};
document.getElementById('replay').onclick=()=>{elapsed=0;playing=true;last=performance.now();show()};
function step(delta){playing=false;index=Math.max(0,Math.min(clip().frames.length-1,index+delta));elapsed=clip().durations.slice(0,index).reduce((a,b)=>a+b,0);show()}
document.getElementById('next').onclick=()=>step(1);document.getElementById('previous').onclick=()=>step(-1);
function tick(t){if(playing){elapsed=Math.min(total(),elapsed+Math.max(0,t-last)*Number(speed.value));if(elapsed>=total())playing=false;show()}last=t;requestAnimationFrame(tick)}
Object.values(clips).forEach(bank=>Object.values(bank).forEach(c=>c.frames.forEach(src=>{const im=new Image();im.src=src})));reset();requestAnimationFrame(tick);
</script>'''
gallery=''
if (P/'native-review-evidence.json').exists():
 gallery='<h2>Engine comparisons</h2><p>Recorded sprite-player views: staged master stride above, transition candidate below at three display sizes. These repeating previews cover 400 milliseconds; the game actions remain finite at 320 milliseconds.</p>'
 for gear in ['bare','helmet']:
  for action in ['start','stop']:gallery+=f'<h3>{gear.title()} {action}</h3><img src="{gear}-{action}-native-review.apng">'
(P/'index.html').write_text(page.replace('__CLIPS__',json.dumps(clips)).replace('<script>',gallery+'<script>'),encoding='utf-8')
print('Finite source review uses exact ordered manifest frames and holds; normal/quarter speed, both gears and actions.')
