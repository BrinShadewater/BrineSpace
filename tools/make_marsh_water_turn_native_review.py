"""Publish authored turn motion and native direction-change playback."""
from pathlib import Path
import json,re,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit'
def main():
    paths=sorted((BASE/'water-turn-native').glob('frame-*.png'));assert len(paths)==72,len(paths)
    frames=[Image.open(p).convert('RGB') for p in paths];frames[0].save(OUT/'native-water-turn-player.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
    samples=[i for start in (0,24,48) for i in (start,start+3,start+8,start+13,start+18,start+23)]
    contact=Image.new('RGB',(960,180*len(samples)),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate(samples):contact.paste(frames[i].crop((0,280,960,460)),(0,180*row));draw.text((4,row*180+4),'Direction group %d / sample %d'%(i//24+1,i%24),fill='white')
    contact.save(OUT/'native-water-turn-station-contact.png')
    page=OUT/'index.html';data=page.read_bytes()
    section='<h2>Matched swimming turns</h2><p>All 12 directed swimming turns now match the selected water loops. Four authored quarter-turn chains share exact swim endpoints. Return turns reverse their poses; half-turns join two quarter-turns at an exact cardinal pose. Timing and water metadata are preserved.</p><div class="chain">'
    for pair in ('east-north','west-north','east-south','west-south','east-west','north-south'):section+=f'<figure><img src="../marsh-water-turn-match-v1/review/{pair}/motion.gif"><figcaption>{pair} selected turn</figcaption></figure>'
    section+='</div><h2>Native direction-change playback</h2><p>Each column starts from a different cardinal swim direction. Three groups exercise all 12 changes at source and station size.</p><img style="width:960px;max-width:100%" src="native-water-turn-player.gif" alt="Native swimming turn selection in all directions">'
    if b'<h2>Matched swimming turns</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>')
    expedition=BASE/'water-turn-expedition/q0-delivery-008-outbound.png'
    if expedition.exists():
        shutil.copy2(expedition,OUT/'native-water-turn-expedition.png')
        if b'<h2>Exterior turn in an expedition</h2>' not in data:
            section='<h2>Exterior turn in an expedition</h2><p>Native exterior turn sample from one completed cargo-delivery journey at room rotation zero.</p><img style="max-width:100%" src="native-water-turn-expedition.png" alt="Matched Marsh swimming turn in the exterior ocean">'
            data=data.replace(b'</body>',section.encode('utf8')+b'</body>')
    data=data.replace(b'Turns share the new exact swim endpoints; their middle poses still use historical sources and remain to match.',b'Turns share these exact swim endpoints; their matched middle poses are shown in the swimming-turn review below.')
    data=data.replace(b'The remaining historical turn interiors are not visually accepted by this check.',b'This earlier expedition sample predates the matched swimming-turn interiors below.')
    page.write_bytes(data);links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links)
    print('Published 72 native turn captures;',len(links),'review links resolve')
if __name__=='__main__':main()
