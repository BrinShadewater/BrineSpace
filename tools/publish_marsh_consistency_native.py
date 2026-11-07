"""Publish native phase samples and link the current consolidated review."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'character/marsh-consistency-review-v1';NATIVE=ROOT/'output/marsh-animation-audit/consistency-native'
def main():
    groups=json.loads((OUT/'groups.json').read_text());assert len(list(NATIVE.glob('group-*.png')))==len(groups)*16
    for start in range(0,len(groups),4):
        chunk=groups[start:start+4];board=Image.new('RGB',(960,len(chunk)*360),'#293b40');draw=ImageDraw.Draw(board)
        for row,g in enumerate(chunk):
            for col,sample in enumerate((8,15) if "shutdown" in g["title"].lower() else (4,10)):
                im=Image.open(NATIVE/f'group-{start+row:02}-{sample:02}.png');board.paste(im.crop((0,280,960,460)),(0,row*360+col*180));draw.text((4,row*360+col*180+4),g['title']+' / phase '+str(sample),fill='white')
        board.save(OUT/f'native-summary-{start//4:02}.png')
        for i,g in enumerate(chunk,start):
            frames=[Image.open(NATIVE/f'group-{i:02}-{j:02}.png').convert('RGB') for j in range(16)];frames[0].save(OUT/f'native-group-{i:02}.gif',save_all=True,append_images=frames[1:],duration=120,loop=0)
    page=OUT/'index.html';html=page.read_text(encoding='utf8');section='<h2>Native phase samples</h2><p>These samples cover source and station sizes. Use the selector above for authored timing.</p>'
    for i,g in enumerate(groups):section+=f'<details><summary>{g["title"]}</summary><img style="max-width:100%" src="native-group-{i:02}.gif" alt="{g["title"]} native phase samples"></details>'
    if '<h2>Native phase samples</h2>' not in html:html=html.replace('<script>',section+'<script>',1);page.write_text(html,encoding='utf8')
    old=ROOT/'character/marsh-run-carry-review-v1/index.html';data=old.read_bytes();marker=b'<h2>Consolidated current animation review</h2>';section='<h2>Consolidated current animation review</h2><p>The current review combines travel, work, rest, cargo, water motion and shutdown. Diagnostic ivory-panel brightness has been corrected in all four directions; earlier diagnostic media below retains the pre-polish colours.</p><p><a href="../marsh-consistency-review-v1/index.html">Open the complete current animation review</a></p><img style="max-width:100%" src="../marsh-controller-tone-v1/comparison.png" alt="Diagnostic suit before and after beside idle">'
    if marker not in data:data=data.replace(b'</body>',section.encode('utf8')+b'</body>');old.write_bytes(data)
    print(len(groups),'native phase previews published')
if __name__=='__main__':main()
