from pathlib import Path
from PIL import Image
import json,sys
H=Path(__file__).resolve().parent
site=Path(sys.argv[1]);O=site/'dist/animations'
js=(O/'library.js').read_text();library=json.loads(js.removeprefix('const LIBRARY=').rstrip(';\n'));cache={}
for gear,rows in library.items():
 for key,s in rows.items():
  boxes=[]
  for path in s['files']:
   if path not in cache:cache[path]=Image.open(O/path).getbbox()
   boxes.append(cache[path])
  px,py=s['pivot'];s['bounds']=[min(b[0] for b in boxes)-px,min(b[1] for b in boxes)-py,max(b[2] for b in boxes)-px,max(b[3] for b in boxes)-py]
(O/'library.js').write_text('const LIBRARY='+json.dumps(library)+';\n')
p=O/'index.html';html=p.read_text(encoding='utf8')
html=html.replace("function draw(now){ctx.clearRect(0,0,c.width,c.height);if(record){", "function draw(now){const z=Number($('#scale').value),bounds=record?record.bounds:[0,-148,0,0],baseline=40-bounds[1]*z,height=Math.max(280,(bounds[3]-bounds[1])*z+80);if(c.height!==height)c.height=height;ctx.clearRect(0,0,c.width,c.height);if(record){")
html=html.replace("if(c.height!==height)c.height=height;ctx.clearRect", "const width=Math.max(640,2*Math.max(-bounds[0],bounds[2])*z+80);if(c.width!==width)c.width=width;if(c.height!==height)c.height=height;ctx.clearRect")
html=html.replace("const z=Number($('#scale').value),im=imgs[i],x=320-record.pivot[0]*z,y=600-record.pivot[1]*z", "const im=imgs[i],x=320-record.pivot[0]*z,y=baseline-record.pivot[1]*z")
html=html.replace('ctx.moveTo(310,600);ctx.lineTo(330,600);ctx.moveTo(320,596);ctx.lineTo(320,604);','ctx.moveTo(310,baseline);ctx.lineTo(330,baseline);ctx.moveTo(320,baseline-4);ctx.lineTo(320,baseline+4);')
html=html.replace('x=320-record.pivot[0]*z','x=c.width/2-record.pivot[0]*z').replace('ctx.moveTo(310,baseline);ctx.lineTo(330,baseline);ctx.moveTo(320,baseline-4);ctx.lineTo(320,baseline+4);','ctx.moveTo(c.width/2-10,baseline);ctx.lineTo(c.width/2+10,baseline);ctx.moveTo(c.width/2,baseline-4);ctx.lineTo(c.width/2,baseline+4);')
p.write_text(html,encoding='utf8')
print(json.dumps({'boundsCheckedStates':sum(map(len,library.values())),'boundsCheckedImages':len(cache),'allStatesWithin3xCanvasWidth':all(s['bounds'][0]*3>=-320 and s['bounds'][2]*3<=320 for rows in library.values() for s in rows.values())}))
