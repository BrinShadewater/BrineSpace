"""Repair clipped diagnostic scanner/gloves while retaining approved standing identity."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-diagnostics-v4'
DIRS=('south','north','east','west');ACTIONS=('interact','repair','inspect','salvage','kneel','stand')
# Arm regions include the full raised gloves and scanner, above the old cut line.
POLYGONS={
 'south':[[(59,69),(125,69),(125,128),(105,128),(105,109),(81,109),(81,128),(59,128)]],
 'north':[[(61,72),(81,72),(81,126),(61,126)],[(105,72),(124,72),(124,126),(105,126)]],
 'east':[[(74,73),(91,73),(91,69),(109,69),(109,62),(128,62),(128,107),(92,107),(92,121),(74,121)]],
 'west':[[(94,73),(111,73),(111,121),(93,121),(93,107),(57,107),(57,62),(79,62),(79,69),(94,69)]]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scanner_mask(image):
 a=np.asarray(image);rgb=a[:,:,:3].astype(int)
 y=np.arange(image.height)[:,None]
 return (a[:,:,3]>0)&(rgb[:,:,1]-rgb[:,:,0]>=18)&(rgb[:,:,2]-rgb[:,:,0]>=18)&(rgb[:,:,1]>=140)&(y>=60)&(y<=105)
def main():
 BASE.mkdir(parents=True,exist_ok=True)
 source_contract=ROOT/'character/marsh-quality-pass-v3/baseline-contract.json'
 baseline=json.loads(source_contract.read_text())['states'];records={};states=[]
 (BASE/'source-contract.json').write_bytes(source_contract.read_bytes())
 for action in ACTIONS:
  board=Image.new('RGB',(1152,816),'#293b40');draw=ImageDraw.Draw(board)
  for row,d in enumerate(DIRS):
   key=action+'-'+d;s=baseline[key];idle_path=ROOT/baseline['idle-'+d]['files'][0];idle=Image.open(idle_path).convert('RGBA');mask=Image.new('L',idle.size)
   for polygon in POLYGONS[d]:ImageDraw.Draw(mask).polygon(polygon,fill=255)
   mask.save(BASE/f'mask-{d}.png');files=[];gifs=[]
   for slot,(f,digest) in enumerate(zip(s['files'],s['hashes'])):
    source=ROOT/f;assert sha(source)==digest;im=Image.open(source).convert('RGBA');assert im.size==idle.size
    out=Image.composite(im,idle,mask)
    if np.array_equal(np.asarray(im),np.asarray(idle)):out=idle.copy()
    screen=scanner_mask(im);assert np.array_equal(np.asarray(out)[screen],np.asarray(im)[screen]),(key,slot,'clipped scanner')
    p=BASE/f'frames/{key}/{slot:03}.png';p.parent.mkdir(parents=True,exist_ok=True);out.save(p);rel=p.relative_to(ROOT).as_posix();files.append(p.relative_to(BASE).as_posix())
    records[rel]={'sha256':sha(p),'source':f,'sourceSha256':digest,'idleSource':idle_path.relative_to(ROOT).as_posix(),'idleSha256':sha(idle_path),'actor':'marsh','scannerPixels':int(screen.sum())}
    board.paste(out,(slot*192+4,row*204+15),out);draw.text((slot*192+4,row*204+190),key+' '+str(slot),fill='white');bg=Image.new('RGB',out.size,'#293b40');bg.paste(out,(0,0),out);gifs.append(bg.resize((368,368),Image.Resampling.NEAREST))
   gifs[0].save(BASE/f'{key}.gif',save_all=True,append_images=gifs[1:],duration=s['durations'],loop=0)
   states.append({'id':key,'frameFiles':files,'frameDurationsMs':s['durations'],'loop':s['loop']})
  board.save(BASE/f'{action}-contact.png')
 (BASE/'manifest.json').write_text(json.dumps({'revision':'marsh-diagnostics-v4','canvas':[184,184],'pivot':[92,172],'standingHeight':148,'textureFilter':'nearest','states':states},indent=2)+'\n')
 (BASE/'installation.json').write_text(json.dumps({'frames':records,'armPolygons':POLYGONS,'reason':'Owner rejected v3: masks removed lit scanner and upper raised gloves. Restore full authored arms/scanner; retain selected head/neck/legs and exact diagnostic joins.'},indent=2)+'\n')
 print('24 diagnostic states / 120 slots; all authored scanner pixels retained')
if __name__=='__main__':main()
