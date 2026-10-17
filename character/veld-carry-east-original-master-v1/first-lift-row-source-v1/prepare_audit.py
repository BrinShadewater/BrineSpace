from pathlib import Path
P=Path(__file__).resolve().parent
s=(P.parent/'stop-source-v2/register_source.py').read_text(encoding='utf-8').replace('raw-stop-v2.png','raw-first-lift-v1.png')
s=s.replace('figures[-1][3]-figures[-1][1]','figures[0][3]-figures[0][1]').replace("last=atlas.crop((round(gutters[-2]*scale),0,atlas.width,atlas.height))","last=atlas.crop((0,0,round(gutters[1]*scale),atlas.height))")
s=s.replace('final standing','first standing').replace("'standingRulerPose':5","'standingRulerPose':0").replace('New whole-source stop keys','New whole-source first-lift preparation keys')
(P/'register_source.py').write_text(s,encoding='utf-8')
print('One entire-atlas initial-standing ruler and whole-component gutter extraction prepared.')
