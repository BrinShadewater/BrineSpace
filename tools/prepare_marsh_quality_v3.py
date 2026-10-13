"""Preserve approved standing anatomy through existing authored diagnostic gestures."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-quality-pass-v3'
DIRS=('south','north','east','west');ACTIONS=('interact','repair','inspect','salvage','kneel','stand')
POLYGONS={
 'south':[[(59,69),(81,69),(81,84),(108,84),(108,109),(81,109),(81,128),(59,128)],[(105,69),(125,69),(125,128),(105,128),(105,109),(82,109),(82,84),(105,84)]],
 'north':[[(61,72),(81,72),(81,126),(61,126)],[(105,72),(124,72),(124,126),(105,126)]],
 'east':[[(74,73),(92,73),(124,73),(124,107),(92,107),(92,121),(74,121)]],
 'west':[[(94,73),(111,73),(111,121),(93,121),(93,107),(57,107),(57,73)]]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 baseline=json.loads((BASE/'baseline-contract.json').read_text())['states'];records={};states=[]
 for action in ACTIONS:
  board=Image.new('RGB',(1152,816),'#293b40');draw=ImageDraw.Draw(board)
  for row,d in enumerate(DIRS):
   key=action+'-'+d;s=baseline[key];idle_path=ROOT/baseline['idle-'+d]['files'][0];idle=Image.open(idle_path).convert('RGBA')
   mask=Image.new('L',idle.size);md=ImageDraw.Draw(mask)
   for polygon in POLYGONS[d]:md.polygon(polygon,fill=255)
   mask.save(BASE/f'mask-{d}.png');files=[];gifs=[]
   for slot,(f,digest) in enumerate(zip(s['files'],s['hashes'])):
    source=ROOT/f;assert sha(source)==digest;im=Image.open(source).convert('RGBA');assert im.size==idle.size
    out=Image.composite(im,idle,mask)
    if np.array_equal(np.asarray(im),np.asarray(idle)):out=idle.copy()
    p=BASE/f'frames/{key}/{slot:03}.png';p.parent.mkdir(parents=True,exist_ok=True);out.save(p);rel=p.relative_to(ROOT).as_posix();files.append(p.relative_to(BASE).as_posix())
    records[rel]={'sha256':sha(p),'source':f,'sourceSha256':digest,'idleSource':idle_path.relative_to(ROOT).as_posix(),'idleSha256':sha(idle_path),'actor':'marsh'}
    board.paste(out,(slot*192+4,row*204+15),out);draw.text((slot*192+4,row*204+190),key+' '+str(slot),fill='white');bg=Image.new('RGB',out.size,'#293b40');bg.paste(out,(0,0),out);gifs.append(bg.resize((368,368),Image.Resampling.NEAREST))
   gifs[0].save(BASE/f'corrected-{key}.gif',save_all=True,append_images=gifs[1:],duration=s['durations'],loop=0)
   states.append({'id':key,'frameFiles':files,'frameDurationsMs':s['durations'],'loop':s['loop']})
  board.save(BASE/f'corrected-{action}-contact.png')
 (BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-quality-pass-v3','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
 (BASE/'installation.json').write_text(json.dumps({'frames':records,'armPolygons':POLYGONS,'reason':'Standing diagnostics changed head/torso/leg identity on entering active poses. Preserve exact canonical pixels outside coherent authored arm/tool regions. No resampling, new artwork or palette changes.'},indent=2)+'\n')
 print('24 standing diagnostic states / 120 source-preserving corrected slots')
if __name__=='__main__':main()
