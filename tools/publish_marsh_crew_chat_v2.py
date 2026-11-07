"""Publish corrected near-arm animation using current native paired captures."""
from pathlib import Path
import json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-crew-chat-v2';CAP=ROOT/'output/marsh-animation-audit/chat-native'
def main():
 log=(CAP.parent/'chat-native.log').read_text();assert '36 native captures, 0 failures' in log
 checks=re.search(r'MARSH CREW CHAT: (\d+) checks',log).group(1)
 durations=json.loads((BASE/'manifest.json').read_text())['states'][0]['frameDurationsMs']
 html='''<!doctype html><meta charset="utf-8"><title>Marsh / corrected crew gesture</title>
<style>body{background:#17252a;color:#dce7e8;font:17px system-ui;max-width:1200px;margin:30px auto;padding:18px}p{line-height:1.6}a{color:#b7ddcc}img{max-width:100%;image-rendering:pixelated}.pair{display:flex;gap:18px;flex-wrap:wrap;align-items:center}.pair img:first-child{width:600px}.pair img:last-child{width:368px}</style>
<h1>Marsh / corrected crew gesture</h1><p>Revision 2 replaces the complete moving arm, including its old hanging glove, so the side views have a single connected shoulder/elbow/wrist. His original head and neck remain stationary. All pixels outside the documented arm polygons remain exact selected idle pixels. Four independent generated source strips retain their prompts; the first sheet remake was rejected for retaining duplicate arms.</p>
<p>The compact gesture raises, opens, holds and lowers the hand. It starts and finishes on exact idle. Timing remains 1.1 seconds, performed once in his existing speaking turn. Conversation behavior and save format are unchanged.</p>
<p>Current native paired playback: __CHECKS__ checks, 36 room captures, zero failures, including all 32 slots, four disk restores and pause. Two source/provenance tests protect fixed anatomy and frozen exports. These mechanical checks are separate from owner visual acceptance.</p>
<p><a href="../marsh-consistency-review-v1/index.html">Current complete source playback review</a> | <a href="installation.json">Registration and source hashes</a></p>'''.replace('__CHECKS__',checks)
 for d in ('south','north','east','west'):
  frames=[Image.open(CAP/f'{d}-{i:02}.png').convert('RGB').crop((290,115,890,570)) for i in range(8)]
  frames[0].save(BASE/f'native-{d}.gif',save_all=True,append_images=frames[1:],duration=durations,loop=0)
  html+=f'<h2>{d.title()}</h2><div class="pair"><img src="native-{d}.gif" alt="Native {d} conversation"><img src="crew-chat-{d}.gif" alt="Enlarged {d} gesture"></div>'
 html+='<h2>All corrected poses</h2><img src="contact.png" alt="All corrected conversation poses">'
 (BASE/'index.html').write_text(html,encoding='utf8')
 assert all((BASE/p).exists() for p in re.findall(r'<(?:a|img)[^>]+(?:href|src)="([^"]+)"',html))
 section=b'<h2>Marsh crew interaction</h2><p>Corrected complete-arm gesture, with stationary head and no duplicate hanging arm. <a href="../marsh-crew-chat-v2/index.html">Open the revised crew interaction review</a>.</p>'
 for name in ('marsh-run-carry-review-v1','marsh-consistency-review-v1','marsh-quality-pass-v2','marsh-gameplay-review-v1'):
  p=ROOT/'character'/name/'index.html';data=p.read_bytes()
  data=re.sub(rb'<h2>Marsh crew interaction</h2><p>.*?</p>',lambda m:section,data,count=1,flags=re.S) if b'<h2>Marsh crew interaction</h2>' in data else data.replace(b'<h1>',section+b'<h1>',1)
  p.write_bytes(data)
 print('Four corrected native/source previews; all review links resolve')
if __name__=='__main__':main()
