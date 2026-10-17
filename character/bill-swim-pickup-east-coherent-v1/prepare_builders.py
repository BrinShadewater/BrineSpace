from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'bill-swim-distress-east-coherent-v1/build.py').read_text(encoding='utf-8')
replacements={
 'distress-v1.png':'pickup-atlas-legs-v5.png',
 '[(364,189),(870,189),(1366,189),(365,632),(880,633),(1380,632)]':'[(355,198),(866,198),(1410,200),(359,624),(868,624),(1390,622)]',
 "ENDPOINTS=[('bill-swim-east-coherent-v1/frames/swim-east/000.png',(6,40)),('bill-swim-east-coherent-v1/frames/swim-east/000.png',(6,40))]":"ENDPOINTS=[('bill-salvage-east-coherent-v1/frames/salvage-east/000.png',(0,0)),('bill-swim-carry-east-coherent-v1/frames/swim-carry-east/000.png',(6,40))]",
 '[(305,266),(802,276),(1320,275),(304,708),(832,710),(1320,716)]':'[(306,275),(803,264),(1357,283),(316,712),(830,712),(1353,712)]',
 '[(ENDPOINTS[0][0],(148,64)),(ENDPOINTS[1][0],(148,64))]':'[(ENDPOINTS[0][0],(154,104)),(ENDPOINTS[1][0],(148,64))]',
 'times=[160]*6':'times=[70,80,90,100,100,80]',
 'swim-distress-east':'swim-pickup-east',
 "'loop':True":"'loop':False",
 "'waterKinds':['swim']*6":"'waterKinds':['salvage']+['swim']*5",
 'four authored fatigue-stroke interiors;exact selected basic swimming join at both ends':'four authored pickup interiors;exact staged work and selected cargo endpoints',
 'Bill east distress stroke candidate':'Bill east underwater pickup candidate',
 'installed_runtime_reviewed':'staged_candidate',
 'exec-eb031fc7-927d-4bae-8929-95bdfa44c26a':'exec-d6f867ed-167c-426a-8f40-a1a6c9ff311a',
 'Built east distress stroke;exact closed join;four authored intermediates':'Built east pickup;exact work/cargo endpoints;four authored interiors',
 "'sourcePose':i":"'sourcePose':i,'alphaComponent':int(ids[i])",
}
for old,new in replacements.items():
 assert old in s,old
 s=s.replace(old,new)
(P/'build.py').write_text(s,encoding='utf-8')
h=P.parent/'bill-swim-pickup-helmet-east-coherent-v1';h.mkdir(exist_ok=True)
s=(P.parent/'bill-salvage-helmet-east-coherent-v1/build.py').read_text(encoding='utf-8').replace('bill-salvage-east-coherent-v1','bill-swim-pickup-east-coherent-v1')
s=s.replace("  b=np.array(Image.open(BARE/file).convert('RGBA'))","  b=np.array(Image.open(BARE/file).convert('RGBA'))")
s=s.replace("  outpath=HERE/file", "  if i in [0,5]:\n   authority,padding=('bill-salvage-helmet-east-coherent-v1/frames/salvage-east/000.png',(0,0)) if i==0 else ('bill-swim-carry-helmet-east-coherent-v1/frames/swim-carry-east/000.png',(6,40))\n   plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/authority).convert('RGBA'),padding)\n   records[-1]['exactEndpointAuthority']=authority;records[-1]['padding']=padding\n  outpath=HERE/file")
s=s.replace('Bill east helmet underwater salvage candidate','Bill east helmet underwater pickup candidate').replace('independently authored distress body; exact first equipped working pose repeated at wrap','independently authored pickup body; exact equipped work/cargo endpoints').replace('Built east helmet salvage;native selected head and authored cutter poses','Built east helmet pickup;native selected head;exact work/cargo endpoints')
(h/'build.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-salvage-east-coherent-v1/build_review.py').read_text(encoding='utf-8').replace('bill-salvage-helmet-east-coherent-v1','bill-swim-pickup-helmet-east-coherent-v1').replace('salvage-east','swim-pickup-east').replace('east salvage','east pickup').replace('east salvage work','east pickup').replace('underwater cutter work','underwater cargo pickup').replace('and840ms loop','and520ms finite transition')
s=s.replace('let cursor=elapsed%(s.frameDurationsMs.reduce((a,b)=>a+b,0));','let total=s.frameDurationsMs.reduce((a,b)=>a+b,0);let cursor=elapsed%(total+600);cursor=Math.min(cursor,total-1);')
(P/'build_review.py').write_text(s,encoding='utf-8')
