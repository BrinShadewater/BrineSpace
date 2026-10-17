"""Publish selected galley gesture motion."""
from pathlib import Path
import re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit'
def main():
    paths=sorted((BASE/'galley-native').glob('frame-*.png'));assert len(paths)==80,len(paths);frames=[Image.open(p).convert('RGB') for p in paths]
    contact=Image.new('RGB',(960,180*10),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate([0,3,6,9,15,40,43,46,49,55]):
        contact.paste(frames[i].crop((0,280,960,460)),(0,row*180));draw.text((4,row*180+4),str(i),fill='white')
    contact.save(OUT/'native-galley-contact.png')
    section="<h2>Matched galley gestures</h2><p>Installed meal and drink gestures match Marsh's selected blond, clean-shaven face and fitted suit. All four views retain planted boots and exact selected idle endpoints. Existing galley stages and timing remain unchanged; Marsh still uses battery power and has no air requirement.</p>"
    for action,title,lo,hi in [('eat','Meal-break gesture',0,40),('drink','Cup gesture',40,80)]:
        images=frames[lo:hi];images[0].save(OUT/f'native-{action}-player.gif',save_all=True,append_images=images[1:],duration=50,loop=0)
        section+=f'<h3>{title}</h3><div class="chain">'
        for d in ('south','north','east','west'):section+=f'<figure><img src="../marsh-galley-match-v1/review/{action}-{d}/motion.gif"><figcaption>{d}</figcaption></figure>'
        section+=f'</div><img style="width:960px;max-width:100%" src="native-{action}-player.gif" alt="{title} at source and station scale">'
    page=OUT/'index.html';data=page.read_bytes()
    if b'<h2>Matched galley gestures</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links);print('Published 80 native captures;',len(links),'image links resolve')
if __name__=='__main__':main()
