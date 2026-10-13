"""Publish matched water source loops and active-player playback."""
from pathlib import Path
import re,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit'
def main():
    paths=sorted((BASE/'water-native').glob('frame-*.png'));assert len(paths)==92,len(paths);frames=[Image.open(p).convert('RGB') for p in paths]
    frames[0].save(OUT/'native-water-player.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
    slots=[0,5,10,15,40,42,44,46,48,50,54,58,62,82,84,86,88,90];contact=Image.new('RGB',(960,180*len(slots)),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate(slots):
        contact.paste(frames[i].crop((0,280,960,460)),(0,row*180));action='tread' if i<40 else 'swim-start' if i<50 else 'swim' if i<82 else 'swim-stop';draw.text((4,row*180+4),action+' / '+str(i),fill='white')
    contact.save(OUT/'native-water-station-contact.png')
    page=OUT/'index.html';data=page.read_bytes();section='<h2>Swimming, treading and start/stop</h2><p>Matching fitted suit and face across all four swim/tread loops and launch/stop transitions. Turns share the new exact swim endpoints; their middle poses still use historical sources and remain to match.</p><div class="chain">'
    for d in ('south','north','east','west'):section+=f'<figure><img src="../marsh-water-match-v1/review/{d}/chain.gif"><figcaption>{d} selected water chain</figcaption></figure>'
    section+='</div><h2>Native water-pose playback</h2><img style="width:960px;height:460px;max-width:100%;object-fit:contain" src="native-water-player.gif" alt="Four-direction water-pose playback at source and station scale">'
    if b'<h2>Swimming, treading and start/stop</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    expedition=BASE/'water-expedition/q0-delivery-003-leave.png'
    if expedition.exists():
        shutil.copy2(expedition,OUT/'native-water-expedition-leave.png')
        if b'<h2>Expedition water rendering</h2>' not in data:
            section='<h2>Expedition water rendering</h2><p>Native departure sample from one completed cargo-delivery journey at room rotation zero. The journey passed dispatch, water travel and delivery. The remaining historical turn interiors are not visually accepted by this check.</p><img style="max-width:100%" src="native-water-expedition-leave.png" alt="Marsh swimming through the flooded airlock during expedition departure">'
            data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links);print('Published 92 water-player captures;',len(links),'review links resolve')
if __name__=='__main__':main()
