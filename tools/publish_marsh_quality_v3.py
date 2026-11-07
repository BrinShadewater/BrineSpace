"""Publish current complete motion review and source-preserving diagnostic correction."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v3'
def main():
 current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states'];before=json.loads((BASE/'baseline-contract.json').read_text())['states']
 audit=json.loads((BASE/'audit.json').read_text());assert len(current)==audit['states']==204
 native=(ROOT/'output/marsh-animation-audit/quality-v3-native.log').read_text();assert '1058 source/elapsed checks, 432 captures, 0 failures' in native
 playback=(ROOT/'output/marsh-animation-audit/quality-v3-playback.log').read_text();assert '22504 checks, 0 failures' in playback
 for d in ('south','north','east','west'):
  frames=[];durations=[]
  for action in ('kneel','repair','stand'):
   key=action+'-'+d
   for i,ms in enumerate(current[key]['durations']):
    tile=Image.new('RGB',(736,410),'#293b40');draw=ImageDraw.Draw(tile)
    for col,states,title in [(0,before,'Before'),(1,current,'Corrected')]:
     im=Image.open(ROOT/states[key]['files'][i]).convert('RGBA').resize((368,368),Image.Resampling.NEAREST);tile.paste(im,(col*368,30),im);draw.text((col*368+10,8),title+' / '+key,fill='white')
    frames.append(tile);durations.append(ms)
  frames[0].save(BASE/f'diagnostic-chain-{d}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
 old=(ROOT/'character/marsh-quality-pass-v2/index.html').read_text();script=re.search(r'<script>(.*?)</script>',old,re.S).group(1)
 script=re.sub(r'const DATA=.*?;const images=',lambda m:'const DATA='+json.dumps({'states':current})+';const images=',script,count=1,flags=re.S).replace("choose.value='tread-north'","choose.value='interact-east'")
 html='''<!doctype html><meta charset="utf-8"><title>Marsh / complete consistency pass 3</title>
<style>body{background:#17252a;color:#dce7e8;font:16px system-ui;max-width:1248px;margin:30px auto;padding:18px}p{line-height:1.6;max-width:1000px}a{color:#b7ddcc}button,select{font:inherit;padding:8px;margin:4px;background:#293b40;color:inherit;border:1px solid #647c80}canvas,img{max-width:100%;image-rendering:pixelated}details{margin:12px 0}</style>
<h1>Marsh / complete consistency pass 3</h1>
<p>Current selection: 204 states, 1,058 frame slots, all four directions and 27 transition chains. Reviewed standing scale, changing posture, perspective, anatomy, source density, material consistency, loop seams and action joins. Accepted crew conversation revision 2 remains selected.</p>
<h2>Corrected diagnostic body changes</h2><p>24 states / 120 slots: interact, repair, inspect, salvage and their entry/exit poses. The previous working figures changed his head, neck, torso and legs. They now retain the exact approved idle pixels outside documented complete-arm/tool regions. Existing authored gestures and tools remain; face and stance no longer switch to a broader figure. Entry/repair/exit joins match exactly. Original art, timings and frozen source hashes are preserved. No new generation, global palette change or resampling.</p>
<p>Before and corrected below use the original action timing.</p>'''
 for d in ('south','north','east','west'):html+=f'<details><summary>{d.title()} diagnostic chain: before / corrected</summary><img src="diagnostic-chain-{d}.gif" alt="{d} diagnostic correction"></details>'
 html+='''<h2>Every current animation</h2><p>Select a clip and compare source, station and distant size. Nonlooping clips repeat here for review; gameplay still holds their last pose. Travel uses distance cadence in game. Timed frame playback and sparse authored pose cadence are distinct: close zoom can still show the short run/swimming pose count.</p>
<select id="state"></select><select id="size"><option value="148">Source size</option><option value="65.28">Station size</option><option value="27">Distant view</option></select><select id="speed"><option value="1">Normal speed</option><option value="0.5">Half speed</option><option value="2">Double speed</option></select><button id="pause">Pause</button><button id="restart">Restart</button><canvas id="view" width="1000" height="410"></canvas><p id="caption"></p>
<h2>Checks and visual evidence</h2><p>22,504 actual-player continuous playback, gait phase, pause/Continue and registration checks: zero failures and no warnings. Fresh native review: all 204 states / 1,058 source/elapsed checks / 432 captures / zero failures. Three anatomy/provenance/transition tests pass. All current standing calibrations remain 148 source pixels per 65.28 world units. No source frame touches its canvas edges. Loop seam changes are within the range of ordinary pose changes; metrics flag review rather than certify subjective motion quality.</p>
<p>The authoring matrices and native phase samples were inspected. Their perspective includes intended foreshortening in swimming, floor work, seating and prone poses; these poses are not stretched to standing height. Complete-pose boards now fit artwork below the pivot, fixing cropped previews. Owner acceptance of the new diagnostic correction is pending.</p>
<p><a href="../marsh-consistency-review-v1/index.html">Current chains and 27 native phase previews</a> | <a href="../marsh-crew-chat-v2/index.html">Accepted crew interaction</a> | <a href="audit.json">All per-state measurements</a> | <a href="installation.json">Correction provenance</a></p>
<h2>All 60 complete pose boards</h2>'''
 boards=[p for p in sorted(BASE.glob('*-contact.png')) if not p.name.startswith('corrected-')];assert len(boards)==60
 for p in boards:html+=f'<details><summary>{p.stem[:-8]}</summary><img loading="lazy" src="{p.name}" alt="All authored {p.stem[:-8]} poses"></details>'
 html+='<script>'+script+'</script>';(BASE/'index.html').write_text(html,encoding='utf8')
 (ROOT/'output/marsh-animation-audit/quality-v3-review.js').write_text(script,encoding='utf8')
 assert all((BASE/p).exists() for p in re.findall(r'<(?:a|img)[^>]+(?:src|href)="([^"]+)"',html))
 section=b'<h2>Current complete consistency pass</h2><p>All 204 states reviewed; diagnostic body switches corrected. <a href="../marsh-quality-pass-v3/index.html">Open the current complete motion review</a>.</p>'
 for name in ('marsh-consistency-review-v1','marsh-run-carry-review-v1','marsh-gameplay-review-v1','marsh-quality-pass-v2'):
  p=ROOT/'character'/name/'index.html';data=p.read_bytes()
  if b'<h2>Current complete consistency pass</h2>' not in data:p.write_bytes(data.replace(b'<h1>',section+b'<h1>',1))
 print('204 timed clips / 60 full pose boards / four before-after chains; links resolve')
if __name__=='__main__':main()
