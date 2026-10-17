"""Publish authored turn motion and native direction-change playback."""
from pathlib import Path
import json,re,shutil
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit'
def main():
    contract=json.loads((ROOT/'character/marsh-loaded-water-match-v1/contract.json').read_text())
    for direction in ('south','north','east','west'):
        chain=[];durations=[]
        for action,repeats in [('swim-pickup',1),('swim-carry',2),('cargo-drain',1)]:
            info=contract['states'][action+'-'+direction]
            for _ in range(repeats):
                for path,ms in zip(info['files'],info['metadata']['frameDurationsMs']):
                    sprite=Image.open(ROOT/path).convert('RGBA');bg=Image.new('RGB',(280,244),'#17212a');bg.paste(sprite,(28,24),sprite);chain.append(bg);durations.append(ms)
        chain[0].save(OUT/f'loaded-water-chain-{direction}.gif',save_all=True,append_images=chain[1:],duration=durations,loop=0)
    paths=sorted((BASE/'loaded-water-native').glob('frame-*.png'));assert len(paths)==108,len(paths)
    frames=[Image.open(p).convert('RGB') for p in paths];frames[0].save(OUT/'native-loaded-water-player.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
    samples=[i for start in (0,24,48,72) for i in (start,start+3,start+8,start+13,start+18,start+23)]
    contact=Image.new('RGB',(960,180*len(samples)),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate(samples):contact.paste(frames[i].crop((0,280,960,460)),(0,180*row));draw.text((4,row*180+4),'Loaded direction/loop group %d / sample %d'%(i//24+1,i%24),fill='white')
    contact.save(OUT/'native-loaded-water-station-contact.png')
    page=OUT/'index.html';data=page.read_bytes()
    section='<h2>Matched cargo swimming and turns</h2><p>All four cargo swimming loops and 12 directed turns now match the selected fitted suit and face. Pickup exits, turn endpoints and drainage starts share the exact loaded loop frame. Return turns reverse their poses; half-turns join at a cardinal frame. Timing and water metadata are preserved.</p><div class="chain">'
    for pair in ('swim-carry-south','swim-carry-north','swim-carry-east','swim-carry-west','east-north','west-north','east-south','west-south','east-west','north-south'):section+=f'<figure><img src="../marsh-loaded-water-match-v1/review/{pair}/motion.gif"><figcaption>{pair} selected cargo motion</figcaption></figure>'
    section+='</div><h2>Native cargo swimming playback</h2><p>Each column starts from a different cardinal swim direction. Three groups exercise all 12 changes, followed by two loop cycles in all four directions at source and station size.</p><img style="width:960px;max-width:100%" src="native-loaded-water-player.gif" alt="Native swimming turn selection in all directions">'
    if b'<h2>Matched cargo swimming and turns</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>')
    if b'<h2>Pickup to cargo swim to drainage</h2>' not in data:
        section='<h2>Pickup to cargo swim to drainage</h2><p>Installed four-direction chains with shared loaded endpoints. Existing pickup and drainage interiors are retained.</p><div class="chain">'
        for direction in ('south','north','east','west'):section+=f'<figure><img src="loaded-water-chain-{direction}.gif"><figcaption>{direction} connected cargo chain</figcaption></figure>'
        section+='</div>';data=data.replace(b'</body>',section.encode('utf8')+b'</body>')
    expedition=BASE/'loaded-water-expedition/q0-delivery-120-return.png'
    if expedition.exists():
        shutil.copy2(expedition,OUT/'native-loaded-water-expedition.png')
        if b'<h2>Loaded expedition return</h2>' not in data:
            section='<h2>Loaded expedition return</h2><p>Actual native cargo-return turn during a completed rotation-zero expedition, including loaded checkpoint restore, pickup, drainage and delivery checks.</p><img style="max-width:100%" src="native-loaded-water-expedition.png" alt="Marsh carrying cargo on the expedition return">'
            data=data.replace(b'</body>',section.encode('utf8')+b'</body>')
    page.write_bytes(data);links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links)
    print('Published 108 native cargo captures;',len(links),'review links resolve')
if __name__=='__main__':main()
