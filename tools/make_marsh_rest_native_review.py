"""Publish generic rest source and selected-player motion without furniture claims."""
from pathlib import Path
import re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit/rest-native'
def main():
    paths=sorted(BASE.glob('frame-*.png'));assert len(paths)==104,len(paths)
    frames=[Image.open(p).convert('RGB') for p in paths]
    frames[0].save(OUT/'native-rest-player.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
    samples=[0,4,8,12,16,34,88,92,96,100]
    contact=Image.new('RGB',(960,180*len(samples)),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate(samples):
        contact.paste(frames[i].crop((0,280,960,460)),(0,row*180))
        action='lie-down' if i<16 else 'sleep' if i<88 else 'get-up'
        draw.text((4,row*180+4),action+' / sample '+str(i),fill='white')
    contact.save(OUT/'native-rest-station-contact.png')
    page=OUT/'index.html';data=page.read_bytes()
    section='<h2>Generic lie-down, rest and get-up</h2><p>The rest chain now matches Marsh\'s fitted suit. Get-up reverses the selected descent, preserving head and foot orientation. Native review checks all four directions at station scale and generic crew-life stage selection; furniture-specific berth and bunk packs use separate animations.</p><div class="chain">'
    for d in ('south','north','east','west'):
        section+=f'<figure><img src="../marsh-rest-match-v1/review/{d}/chain.gif"><figcaption>{d}</figcaption></figure>'
    section+='</div><h2>Native generic rest playback</h2><img style="width:960px;height:460px;max-width:100%;object-fit:contain" src="native-rest-player.gif" alt="Four direction rest playback at source and station scale">'
    if b'<h2>Generic lie-down, rest and get-up</h2>' not in data:
        data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    links=re.findall(rb'<img[^>]+src="([^"]+)"',data)
    missing=[p for p in links if not (OUT/p.decode('utf8')).exists()];assert not missing,missing
    print('Published 104 native captures;',len(links),'review image links resolve')
if __name__=='__main__':main()
