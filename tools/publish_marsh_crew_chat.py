"""Review the installed conversation gesture beside an actual crew partner."""
from pathlib import Path
import json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-crew-chat-v1';CAP=ROOT/'output/marsh-animation-audit/chat-native'
def main():
    log=(CAP.parent/'chat-native.log').read_text();assert '36 native captures, 0 failures' in log
    checks=re.search(r'MARSH CREW CHAT: (\d+) checks',log).group(1)
    manifest=json.loads((BASE/'manifest.json').read_text());duration=manifest['states'][0]['frameDurationsMs']
    for d in ('south','north','east','west'):
        frames=[Image.open(CAP/f'{d}-{i:02}.png').convert('RGB').crop((290,115,890,570)) for i in range(8)]
        frames[0].save(BASE/f'native-{d}.gif',save_all=True,append_images=frames[1:],duration=duration,loop=0)
    html='''<!doctype html><meta charset="utf-8"><title>Marsh / crew conversation</title>
<style>body{background:#17252a;color:#dce7e8;font:17px system-ui;max-width:1200px;margin:30px auto;padding:18px}p{line-height:1.6;max-width:1000px}a{color:#b7ddcc}img{max-width:100%;image-rendering:pixelated}.pair{display:flex;gap:18px;flex-wrap:wrap;align-items:center}.pair img:first-child{width:600px}.pair img:last-child{width:368px}</style>
<h1>Marsh / crew conversation</h1><p>A brief open-hand response with a restrained nod, authored in all four directions. The gesture starts and finishes on his exact current idle, with fixed boots, torso and canonical face. Generated forearms use his locked palette; the head nod translates the selected head without resampling it.</p>
<p>Installed in the existing off-duty conversation system. Marsh uses this gesture once during his speaking turn, then holds idle for the rest of that turn; his partner listens. The gesture lasts 1.1 seconds inside the existing three-second speaking window. Injury or a charging return takes priority. Conversation duration, curiosity reward and cooldown remain the existing rules.</p>
<p>Actual Crew Lounge captures below show Marsh speaking to Bill in each facing. These are real paired conversations, rather than a pasted character composite. Native checks cover all 32 authored slots, reciprocal pairing, facing, completed release, four disk Continue restores and pause: __CHECKS__ checks, 36 captures, zero failures. Existing crew social regression and two source/provenance tests also pass. The complete current player review has 204 states and 1,058 frame slots.</p>
<p><a href="../marsh-consistency-review-v1/index.html">Current complete animation review</a> | <a href="installation.json">Source and registration record</a></p>'''
    for d in ('south','north','east','west'):
        html+=f'<h2>{d.title()}</h2><div class="pair"><img src="native-{d}.gif" alt="Native {d} conversation with Bill"><img src="crew-chat-{d}.gif" alt="Enlarged {d} gesture"></div>'
    html+='<h2>All selected poses</h2><img src="contact.png" alt="All four conversation directions">'
    html=html.replace('__CHECKS__',checks)
    (BASE/'index.html').write_text(html,encoding='utf8')
    assert all((BASE/x).exists() for x in re.findall(r'<(?:a|img)[^>]+(?:href|src)="([^"]+)"',html))
    section=b'<h2>Marsh crew interaction</h2><p>A new four-direction open-hand conversation gesture is installed. <a href="../marsh-crew-chat-v1/index.html">Open the current crew interaction review</a>.</p>'
    for name in ('marsh-run-carry-review-v1','marsh-consistency-review-v1','marsh-quality-pass-v2','marsh-gameplay-review-v1'):
        p=ROOT/'character'/name/'index.html';data=p.read_bytes()
        if b'<h2>Marsh crew interaction</h2>' not in data:
            anchor=b'<script>' if b'<script>' in data else b'<h1>'
            data=data.replace(anchor,section+anchor,1);p.write_bytes(data)
    print('Four current native/source conversation previews; links resolve')
if __name__=='__main__':main()
