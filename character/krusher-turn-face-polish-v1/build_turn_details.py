from pathlib import Path
from PIL import Image,ImageDraw
import json,math
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;D=H/'native-turns'
q=json.loads((D/'report.json').read_text());lib=json.loads((R/'character/krusher-continuous-playback-v1/library.json').read_text())['states'];episodes=q['episodes'];out=H/'turn-details';out.mkdir(exist_ok=True)
for page in range(math.ceil(len(episodes)/6)):
 board=Image.new('RGB',(1210,6*190),'#1b272d');d=ImageDraw.Draw(board)
 for row,e in enumerate(episodes[page*6:page*6+6]):
  y=row*190;d.text((5,y+3),e['label']+' | all selected turn slots | native head/collar detail, 3x nearest',fill='white')
  selected={}
  for r in q['records']:
   if r['episode']==e['label'] and r['source'].get('key')==e['requested']:selected.setdefault(r['source']['index'],r)
  for col,(index,r) in enumerate(sorted(selected.items())):
   s=lib[e['gear']+':'+e['requested']];scale=r['screen'][2]/s['width'];head=s['heads'][index]
   cx=r['screen'][0]+head[0]*scale-r['crop'][0];cy=r['screen'][1]+head[1]*scale-r['crop'][1]
   im=Image.open(D/r['file']).convert('RGB');box=(round(cx-24*scale),round(cy-28*scale),round(cx+24*scale),round(cy+42*scale));im=im.crop(box);im=im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST)
   x=col*109;board.paste(im,(x+5,y+37));d.text((x+5,y+20),'slot '+str(index),fill='#b8dce2')
 board.save(out/('turns-%02d.png'%page))
print({'episodes':len(episodes),'turnSlots':sum(len(e['turnSlots']) for e in episodes),'pages':math.ceil(len(episodes)/6)})
