"""Publish observed native pose changes with their actual scene cadence."""
from pathlib import Path
import json,html,sys,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];CAP=ROOT/'output/marsh-animation-audit/motion-review';OUT=ROOT/'character/marsh-master-repair-v1/motion-review'
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 primary=json.loads((CAP/'primary-samples.json').read_text());supplement=json.loads((CAP/'samples.json').read_text());assert supplement['samples'][0]['file'].startswith('supplement-')
 records=[s for s in primary['samples'] if s['group']!=0]+supplement['samples'];groups={};seen=set()
 for r in records:
  groups.setdefault(r['title'],[]).append(r)
  seen.update((p['key'],p['slot']) for p in r['poses'])
 states=json.loads((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_text())['states'];missing=[(k,n) for k,s in states.items() for n in range(len(s['files'])) if (k,n) not in seen]
 assert not missing,missing
 summary=[];page='<meta charset="utf-8"><title>Marsh native motion review</title><style>body{background:#192a30;color:#e1e6df;font:16px system-ui;margin:24px}img{max-width:100%;image-rendering:pixelated}a{color:#a0d7d5}</style><h1>Marsh: native motion review</h1><p>All 204 states / 1,058 authored slots observed in advancing native playback. These sequences preserve observed scene timing; screenshots can add capture overhead. Boards show consecutive source-size poses; GIFs show source and station sizes.</p><p><a href="../index.html">Masters and synchronized before/after review</a></p>'
 for index,(title,samples) in enumerate(groups.items()):
  frames=[Image.open(CAP/r['file']).convert('RGB') for r in samples];durations=[max(20,round((samples[n+1]['elapsed']-r['elapsed'])*1000)) if n+1<len(samples) else 150 for n,r in enumerate(samples)]
  name=f'group-{index:02}.gif'
  if '--boards-only' not in sys.argv:frames[0].save(OUT/name,save_all=True,append_images=frames[1:],duration=durations,loop=0)
  chosen=[];signatures=set();previous=None
  for n,r in enumerate(samples):
   sig=tuple((p['key'],p['slot']) for p in r['poses']);seam=previous is not None and any(a[0]==b[0] and a[1]>b[1] for a,b in zip(previous,sig))
   if sig not in signatures or seam or n==len(samples)-1:chosen.append(n)
   signatures.add(sig);previous=sig
  boards=[]
  for start in range(0,len(chosen),8):
   selected=chosen[start:start+8];board=Image.new('RGB',(1280,len(selected)*270),'#293b40');draw=ImageDraw.Draw(board)
   for row,n in enumerate(selected):
    draw.text((8,row*270+4),f'{title} / {samples[n]["elapsed"]:.3f}s',fill='white');board.paste(frames[n].crop((0,32,1280,274)),(0,row*270+24))
   board_name=f'group-{index:02}-board-{start//8:02}.png';board.save(OUT/board_name);boards.append(board_name)
  summary.append({'title':title,'gif':name,'boards':boards,'nativeCaptures':len(samples),'capturedSlots':sorted({(p['key'],p['slot']) for r in samples for p in r['poses']}),'gifTiming':'Observed scene duration rounded to GIF centiseconds; terminal hold 150ms.'})
  page+=f'<details><summary>{html.escape(title)}</summary><img src="{name}" alt="{html.escape(title)} playback">'+''.join(f'<p><img src="{b}" loading="lazy"></p>' for b in boards)+'</details>'
 page=page.replace('<h1>Marsh: native motion review</h1>','<h1>Marsh: native motion review</h1><p>Frame review: no new major body clipping or proportion defects observed. Diagnostics retain a visible tablet and connected grip; cargo turns retain hand/case contact; north shutdown keeps paired legs; injury fluid remains white.</p><p>Each GIF repeats a review sequence. Its final-to-first reset, including shutdown returning to idle or a turn starting again, is a viewer restart. Sequence joins are fixture examples; they do not establish live gameplay handoff or foot-lock correctness. Owner motion acceptance remains pending.</p>')
 report={'states':204,'slots':len(seen),'groups':summary,'missingSlots':missing,'reviewer':'Codex','ownerAcceptance':False,'runtimeContractSha256':hashlib.sha256((ROOT/'character/marsh-consistency-review-v1/runtime-contract.json').read_bytes()).hexdigest(),'visualReview':{'method':'Native advancing playback captured at pose changes; chronological source-size boards for all 30 groups visually inspected, plus initial native source/baseline/station view. GIFs preserve observed cadence for owner review. This is not a claim of continuously watched gameplay.','findings':['No new major clipping or proportion defects observed in reviewed poses.','Diagnostics: visible cyan tablet, coherent grip, canonical head and boots retained.','Cargo and loaded water turns: connected hands/case and coherent directional progression; no obvious new material flashes in consecutive poses.','Run/rest/recovery: readable pose progression; authored sparse frame counts and timing retained.','North ground shutdown: paired legs behind body. White injury fluid retained.'],'limits':['Capture overhead affects observed GIF cadence; GIF centiseconds round timing.','Review-sequence restart is not an authored loop seam or gameplay transition.','World movement, foot sliding and furniture occlusion require live station context; not established by this fixture.']},'profileIsolation':'All invocations explicitly set scratch APPDATA. A fresh before/after real-profile fingerprint was not captured for this review pass; unchanged owner-profile contents are not asserted.','capturePolicy':'Primary 27-group playback plus corrected supplemental travel/aliases. Primary travel images were superseded after supplemental filename collision; supplement uses separate names. Primary terminal queued draw raised an out-of-bounds error after capture completion; bounds guard corrected and supplemental run verified.'}
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');(OUT/'index.html').write_text(page)
 print(len(groups),'native sequences;',len(seen),'observed slots;',sum(len(s['boards']) for s in summary),'pose-change boards')
if __name__=='__main__':main()
