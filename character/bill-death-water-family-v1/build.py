"""Consolidate independently authored cardinal deaths with literal resource paths."""
from pathlib import Path
import json,hashlib,copy
P=Path(__file__).resolve().parent
bindings={}
for gear in ['bare','helmet']:
 states=[]
 for direction in ['east','west','north','south']:
  folder=P.parent/(f'bill-death-water-{direction}-coherent-v1' if gear=='bare' else f'bill-death-water-helmet-{direction}-coherent-v1')
  manifest=folder/'manifest.json';m=json.loads(manifest.read_text(encoding='utf-8'));s=copy.deepcopy(m['states'][0]);s['frameFiles']=['res://character/'+folder.name+'/'+file for file in s['frameFiles']];states.append(s)
  bindings[manifest.relative_to(P.parent.parent).as_posix()]=hashlib.sha256(manifest.read_bytes()).hexdigest()
  for file in m['states'][0]['frameFiles']:
   f=folder/file;bindings[f.relative_to(P.parent.parent).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
 pack={'name':f'Bill cardinal underwater death {gear} selected','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'installed_runtime_reviewed','states':states}
 if gear=='helmet':pack['equipment']='diving-helmet'
 (P/f'{gear}-manifest.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
(P/'source-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n',encoding='utf-8')
print('Consolidated 8 selected gear/direction states,48 authored refs')
