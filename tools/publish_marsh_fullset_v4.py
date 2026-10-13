"""Complete current library viewer with same-phase frozen/current comparisons."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v4';LOGS=ROOT/'output/marsh-animation-audit'
def main():
 current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states'];before=json.loads((BASE/'baseline-contract.json').read_text())['states'];installation=json.loads((BASE/'installation.json').read_text())
 assert '22504 checks, 0 failures' in (LOGS/'fullset-v4-playback.log').read_text()
 assert '1058 source/elapsed checks, 432 captures, 0 failures' in (LOGS/'fullset-v4-native.log').read_text()
 examples=('repair-east','swim-carry-south','cargo-unload-east','sleep-east','run-west','swim-turn-south-east')
 for key in examples:
  frames=[]
  for slot in range(len(current[key]['files'])):
   board=Image.new('RGB',(736,410),'#293b40');draw=ImageDraw.Draw(board)
   for col,states,label in ((0,before,'Before'),(1,current,'Current')):
    s=states[key];im=Image.open(ROOT/s['files'][slot]).convert('RGBA');scale=2
    big=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
    board.paste(big,(col*368+184-round(s['pivot'][0]*scale),385-round(s['pivot'][1]*scale)),big);draw.text((col*368+10,8),label+' / '+key,fill='white')
   frames.append(board)
  frames[0].save(BASE/f'compare-{key}.gif',save_all=True,append_images=frames[1:],duration=current[key]['durations'],loop=0)
 old=(ROOT/'character/marsh-quality-pass-v2/index.html').read_text();script=re.search(r'<script>(.*?)</script>',old,re.S).group(1)
 script=re.sub(r'const DATA=.*?;const images=',lambda m:'const DATA='+json.dumps({'states':current})+';const BEFORE='+json.dumps({'states':before})+';const images=',script,count=1,flags=re.S)
 script=script.replace('Object.values(DATA.states))for(const f','[...Object.values(DATA.states),...Object.values(BEFORE.states)])for(const f')
 script=script.replace("choose.value='tread-north'","choose.value='repair-east'")
 script=script.replace('s=DATA.states[key],duration=',"s=(document.querySelector('#revision').value==='before'?BEFORE:DATA).states[key],duration=")
 html='''<!doctype html><meta charset="utf-8"><title>Marsh / full colour and consistency pass</title>
<style>body{background:#17252a;color:#dce7e8;font:16px system-ui;max-width:1248px;margin:30px auto;padding:18px}p{line-height:1.6}a{color:#b7ddcc}button,select{font:inherit;padding:8px;margin:4px;background:#293b40;color:inherit}canvas,img{max-width:100%;image-rendering:pixelated}details{margin:12px 0}</style>
<h1>Marsh / full colour, detail and consistency pass</h1>
<p>All 204 selected states / 1,058 frame slots reviewed. Calibrated suit brightness in east/west diagnostics, east rest poses and south loaded swimming. Quieted near-black contour pixels in affected cargo, travel, seating and water artwork. 158 clips / 700 frame slots updated.</p>
<p>Authored poses, canvas sizes, registration, alpha silhouettes and timing stay intact. Fixed material settings apply across each affected group; identical poses share the same correction across different clips and canvas padding. Fine detail is retained without resizing, blur or invented texture. Accepted idle/walk/conversation, injury white fluid, ordinary shutdown and welding artwork remain exact. Diagnostic face and planted shin/boot artwork remain fixed.</p>
<h2>Every current animation / same-phase comparison</h2><p>Switch Before/Current while a clip plays to compare the same pose and timing. Station-size reference stays on the right. Nonlooping actions repeat here for review; gameplay holds their final pose.</p>
<select id="state"></select><select id="revision"><option value="current">Current calibration</option><option value="before">Before this pass</option></select><select id="size"><option value="148">Source size</option><option value="65.28">Station size</option><option value="27">Distant view</option></select><select id="speed"><option value="1">Normal speed</option><option value="0.5">Half speed</option><option value="2">Double speed</option></select><button id="pause">Pause</button><button id="restart">Restart</button><canvas id="view" width="1000" height="410"></canvas><p id="caption"></p>
<h2>Selected before / current comparisons</h2>'''
 for key in examples:html+=f'<details><summary>{key}</summary><img src="compare-{key}.gif" alt="{key} before and current"></details>'
 html+='''<h2>Checks and review</h2><p>22,504 game-player checks and 1,058 native source/elapsed checks with 432 captures: zero failures. Four full-set tests verify source hashes, exact alpha/geometry, identical shared poses, protected artwork, selected timings/pivots/calibration and water/furniture metadata. Colour lock: 9,991 paths, zero errors. No canvas edge contacts. Source matrices, ten family overviews and native source/station captures inspected. Measurements support visual review; owner acceptance is pending. Existing short authored pose cadence and intentional foreshortening remain.</p>
<p><a href="../marsh-consistency-review-v1/index.html">All transition chains and fresh native previews</a> | <a href="installation.json">Calibration policy and hashes</a> | <a href="audit.json">All frame measurements</a></p><h2>Complete authored pose boards</h2>'''
 boards=sorted(BASE.glob('*-contact.png'));assert len(boards)==60
 for p in boards:html+=f'<details><summary>{p.stem[:-8]}</summary><img loading="lazy" src="{p.name}" alt="All {p.stem[:-8]} poses"></details>'
 html+='<script>'+script+'</script>';(BASE/'index.html').write_text(html,encoding='utf8');(LOGS/'fullset-v4-review.js').write_text(script,encoding='utf8')
 assert all((BASE/p).exists() for p in re.findall(r'<(?:a|img)[^>]+(?:src|href)="([^"]+)"',html))
 notice=b'<section id="fullset-v4"><h2>Current full-library calibration</h2><p><a href="../marsh-quality-pass-v4/index.html">Open all current animations and same-phase before/current comparisons</a>.</p></section>'
 for name in ('marsh-diagnostics-v7','marsh-consistency-review-v1','marsh-run-carry-review-v1'):
  p=ROOT/'character'/name/'index.html';data=p.read_bytes()
  if b'id="fullset-v4"' not in data:p.write_bytes(data.replace(b'<h1>',notice+b'<h1>',1))
 print('204 selectable before/current clips; 60 matrices; six authored-timing comparisons; links resolve')
if __name__=='__main__':main()
