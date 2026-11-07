"""Publish restored native furniture poses and the selected source chains."""
from pathlib import Path
import json,re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'character/marsh-furniture-match-v1'
def main():
    contract=json.loads((BASE/'contract.json').read_text());board=Image.new('RGB',(460,340*13),'#17212a');draw=ImageDraw.Draw(board);row=0
    for kind,v in contract.items():
        stamps=[0,200,550,800,1100,1400,1700] if kind=='bunk' else [0,200,550,850,1150,1400]
        crop=(375,275,505,410) if kind=='bunk' else (475,170,610,330)
        frames=[]
        for i,t in enumerate(stamps):
            name=f'restore-bare-{t:04}.png' if kind=='bunk' else f'restore-{t:04}.png'
            image=Image.open(ROOT/'output/crew-activity'/('marsh-'+kind)/name).convert('RGB').crop(crop).resize((crop[2]*2-crop[0]*2,crop[3]*2-crop[1]*2),Image.Resampling.NEAREST)
            frames.append(image);board.paste(image,(0,row*340));draw.text((280,row*340+10),kind+' / pose '+str(i),fill='white');row+=1
        states=v['manifest']['states'];entry=states[0];rest=next(s for s in states if s['loop']);exit=next(s for s in states if not s['loop'] and s!=entry)
        sequence=frames+[frames[-1]]+list(reversed(frames));times=entry['frameDurationsMs']+rest['frameDurationsMs']+exit['frameDurationsMs']
        sequence[0].save(OUT/f'native-furniture-{kind}.gif',save_all=True,append_images=sequence[1:],duration=times,loop=0)
    board.save(OUT/'native-furniture-contact.png')
    page=OUT/'index.html';data=page.read_bytes();section='<h2>Bed boarding and rest</h2><p>Matching face and fitted suit through the live station bunk and separate legacy berth. Native images are restored checkpoint poses at station size, enlarged 2x; exit in these review GIFs reverses the captured entry poses. Bunk validation covers normal chooser and arrival. The retired berth uses an isolated compatibility fixture.</p><div class="chain">'
    for kind in ('bunk','berth'):
        section+=f'<figure><img src="../marsh-furniture-match-v1/review/{kind}/chain.gif"><figcaption>{kind} selected sources</figcaption></figure><figure><img src="native-furniture-{kind}.gif"><figcaption>{kind} native restored poses</figcaption></figure>'
    section+='</div>'
    if b'<h2>Bed boarding and rest</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links)
    print('Published 13 native restored poses;',len(links),'review image links resolve')
if __name__=='__main__':main()
