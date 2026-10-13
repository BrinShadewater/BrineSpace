"""Publish installed dry shutdown and clearly staged white-fluid injury motion."""
from pathlib import Path
import re
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-run-carry-review-v1';BASE=ROOT/'output/marsh-animation-audit'
def main():
    paths=sorted((BASE/'shutdown-native').glob('frame-*.png'));assert len(paths)==96,len(paths);frames=[Image.open(p).convert('RGB') for p in paths]
    for name,images in [('shutdown',frames[:48]),('injury-candidate',frames[48:])]:images[0].save(OUT/f'native-{name}-player.gif',save_all=True,append_images=images[1:],duration=50,loop=0)
    slots=[0,4,8,12,18,24,48,52,56,60,66,72];contact=Image.new('RGB',(960,180*len(slots)),'#17212a');draw=ImageDraw.Draw(contact)
    for row,i in enumerate(slots):contact.paste(frames[i].crop((0,280,960,460)),(0,row*180));draw.text((4,row*180+4),('Installed dry shutdown' if i<48 else 'Staged white-fluid injury')+' / '+str(i),fill='white')
    contact.save(OUT/'native-shutdown-injury-contact.png')
    page=OUT/'index.html';data=page.read_bytes();section='<h2>Android shutdown and white-fluid injury</h2><p>Marsh is an android: physical injury leaks opaque milky white synthetic fluid. Battery depletion remains a clean shutdown. The dry collapse is installed; the white-fluid injury variant is staged visual coverage because a separate injury trigger is not implemented.</p>'
    for action,title,native in [('death-ground','Installed clean shutdown','shutdown'),('injury-ground','Staged injury with white fluid','injury-candidate')]:
        section+=f'<h3>{title}</h3><div class="chain">'
        for direction in ('south','north','east','west'):section+=f'<figure><img src="../marsh-shutdown-injury-match-v1/review/{action}-{direction}/motion.gif"><figcaption>{direction}</figcaption></figure>'
        section+=f'</div><img style="width:960px;max-width:100%" src="native-{native}-player.gif" alt="{title} native source and station-size preview">'
    if b'<h2>Android shutdown and white-fluid injury</h2>' not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>');page.write_bytes(data)
    links=re.findall(rb'<img[^>]+src="([^"]+)"',data);assert all((OUT/p.decode('utf8')).exists() for p in links);print('Published 96 native dry/staged captures;',len(links),'image links resolve')
if __name__=='__main__':main()
