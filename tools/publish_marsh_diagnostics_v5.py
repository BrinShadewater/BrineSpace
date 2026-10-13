"""Publish corrected diagnostic chains and the complete current timed clip viewer."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-diagnostics-v5'
def main():
 current=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states']
 assert len(current)==204
 logs=ROOT/'output/marsh-animation-audit'
 assert '22504 checks, 0 failures' in (logs/'diagnostics-v5-playback.log').read_text()
 assert '1058 source/elapsed checks, 432 captures, 0 failures' in (logs/'diagnostics-v5-native.log').read_text()
 for d in ('south','north','east','west'):
  frames=[];durations=[]
  for action in ('kneel','repair','stand'):
   key=action+'-'+d
   for i,ms in enumerate(current[key]['durations']):
    tile=Image.new('RGB',(736,410),'#293b40');draw=ImageDraw.Draw(tile)
    for col,path,title in [(0,ROOT/f'character/marsh-diagnostics-v4/frames/{key}/{i:03}.png','Previous / arm overlays'),(1,ROOT/current[key]['files'][i],'Replacement / complete poses')]:
     im=Image.open(path).convert('RGBA').resize((368,368),Image.Resampling.NEAREST);tile.paste(im,(col*368,30),im);draw.text((col*368+8,8),title,fill='white')
    frames.append(tile);durations.append(ms)
  frames[0].save(BASE/f'diagnostic-chain-{d}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
 old=(ROOT/'character/marsh-quality-pass-v3/index.html').read_text()
 script=re.search(r'<script>(.*?)</script>',old,re.S).group(1)
 script=re.sub(r'const DATA=.*?;const images=',lambda m:'const DATA='+json.dumps({'states':current})+';const images=',script,count=1,flags=re.S).replace("choose.value='interact-east'","choose.value='repair-east'")
 html='''<!doctype html><meta charset="utf-8"><title>Marsh / coherent diagnostics 5</title>
<style>body{background:#17252a;color:#dce7e8;font:16px system-ui;max-width:1248px;margin:30px auto;padding:18px}p{line-height:1.6}a{color:#b7ddcc}button,select{font:inherit;padding:8px;margin:4px;background:#293b40;color:inherit}canvas,img{max-width:100%;image-rendering:pixelated}details{margin:12px 0}</style>
<h1>Marsh / coherent diagnostics 5</h1>
<p>Replaced the defective arm overlays with complete authored diagnostic figures. A broad cyan tablet is supported by one hand while the other taps its screen; its edge remains visible from behind. Twelve full working poses cover four directions, packaged into 24 diagnostic states / 120 slots. Original timings, canvas, pivot, palette and calibration remain. Exact idle endpoints and work entry/exit joins are retained.</p>
<h2>Diagnostic entry, work and exit</h2><p>Previous on the left, corrected on the right. These comparisons use the authored action timing.</p>'''
 for d in ('south','north','east','west'):html+=f'<details open><summary>{d.title()}</summary><img src="diagnostic-chain-{d}.gif" alt="{d} diagnostic repair"></details>'
 html+='''<h2>All 204 current clips</h2><p>Compare source and station size at normal or slow speed. Nonlooping actions repeat for review; gameplay holds the final pose. Crew conversation revision 2 remains selected.</p>
<select id="state"></select><select id="size"><option value="148">Source size</option><option value="65.28">Station size</option><option value="27">Distant view</option></select><select id="speed"><option value="1">Normal speed</option><option value="0.5">Half speed</option><option value="2">Double speed</option></select><button id="pause">Pause</button><button id="restart">Restart</button><canvas id="view" width="1000" height="410"></canvas><p id="caption"></p>
<h2>Verification</h2><p>22,504 game animation-player checks: zero failures. Native playback: 1,058 source/elapsed checks and 432 phase captures, zero failures. Tablet visibility, provenance, idle endpoints, work joins and unchanged unrelated states pass. Whole figures are registered at the feet with one fixed scale per direction; no arm/body splice is used. The rear screen is mostly occluded naturally, with its outer edge visible. Twelve authored working poses provide a restrained tapping gesture; repeated frame slots are holds, not additional drawings. Owner visual acceptance is pending.</p>
<p><a href="../marsh-consistency-review-v1/index.html">Current transition chains and native phase previews</a> | <a href="audit.json">Full set measurements</a> | <a href="installation.json">Diagnostic provenance</a></p><h2>Complete authored pose boards</h2>'''
 boards=sorted(BASE.glob('*-contact.png'));assert len(boards)==60
 for p in boards:html+=f'<details><summary>{p.stem[:-8]}</summary><img loading="lazy" src="{p.name}" alt="{p.stem[:-8]} poses"></details>'
 html+='<script>'+script+'</script>';(BASE/'index.html').write_text(html,encoding='utf8');(logs/'diagnostics-v5-review.js').write_text(script,encoding='utf8')
 assert all((BASE/p).exists() for p in re.findall(r'<(?:a|img)[^>]+(?:src|href)="([^"]+)"',html))
 notice=b'<section id="diagnostic-v5"><h2>Complete diagnostic replacement</h2><p>The owner rejected the previous arm overlays. <a href="../marsh-diagnostics-v5/index.html">Open the current complete diagnostic poses</a>.</p></section>'
 for name in ('marsh-quality-pass-v3','marsh-diagnostics-v4','marsh-consistency-review-v1','marsh-run-carry-review-v1'):
  p=ROOT/'character'/name/'index.html';data=p.read_bytes()
  if b'id="diagnostic-v5"' not in data:p.write_bytes(data.replace(b'<h1>',notice+b'<h1>',1))
 print('Published 204 timed clips, 60 boards, four diagnostic comparisons; links resolve')
if __name__=='__main__':main()
