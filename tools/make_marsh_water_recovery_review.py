"""Publish selected water shutdown and retained diagnostic recovery motion."""
from pathlib import Path
import re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit'
def main():
    paths=sorted((BASE/'water-recovery-native').glob('frame-*.png'));assert len(paths)==168,len(paths);frames=[Image.open(p).convert('RGB') for p in paths]
    contact=Image.new('RGB',(960,180*12),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate([0,4,8,16,24,47,48,56,72,96,108,136]):
        contact.paste(frames[i].crop((0,280,960,460)),(0,row*180));draw.text((4,row*180+4),str(i),fill='white')
    contact.save(OUT/'native-water-recovery-contact.png')
    section='<h2>Water shutdown and android recovery</h2><p>Installed: underwater battery shutdown now ends in an inert float. Retained distress and recovery clips show mechanical instability and chest-panel diagnostics. Marsh does not need air; these compatibility poses add no oxygen or injury mechanic. Battery depletion remains dry, while physical-injury fluid remains the white staged variant above.</p>'
    for action,title,lo,hi in [('death-water','Underwater shutdown',0,48),('swim-distress','Retained mechanical instability',48,96),('recover-air','Retained diagnostic reset',96,168)]:
        images=frames[lo:hi];images[0].save(OUT/f'native-{action}-player.gif',save_all=True,append_images=images[1:],duration=50,loop=0)
        section+=f'<h3>{title}</h3><div class="chain">'
        for d in ('south','north','east','west'):section+=f'<figure><img src="../marsh-water-recovery-match-v1/review/{action}-{d}/motion.gif"><figcaption>{d}</figcaption></figure>'
        section+=f'</div><img style="width:960px;max-width:100%" src="native-{action}-player.gif" alt="{title} at source and station scale">'
    page=OUT/'index.html';data=page.read_bytes()
    if b'<h2>Water shutdown and android recovery</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links);print('Published 168 native captures;',len(links),'image links resolve')
if __name__=='__main__':main()
