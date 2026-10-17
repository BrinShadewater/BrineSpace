from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;raw=Image.open(P/'generated-repair-pitch.png').convert('RGBA')
regions={
 'bare-east-bowed':{'polygon':[[330,85],[418,85],[477,117],[534,154],[577,201],[567,244],[511,277],[501,360],[474,421],[435,454],[389,458],[338,431],[283,406],[238,377],[233,330],[231,269],[208,234],[206,193],[218,157],[264,117]],'box':[206,85,578,459],'size':[31,31]},
 'bare-west-bowed':{'polygon':[[959,85],[1042,85],[1121,128],[1162,162],[1164,252],[1146,318],[1136,350],[1081,385],[1036,419],[990,451],[943,455],[908,436],[880,401],[877,355],[855,334],[857,286],[825,257],[791,234],[790,202],[809,153],[861,123]],'box':[790,85,1165,456],'size':[31,31]},
 'visor-east-bowed':{'polygon':[[377,789],[409,766],[488,750],[539,755],[545,799],[530,841],[509,870],[505,912],[478,940],[475,963],[449,970],[417,948],[390,916],[376,860]],'box':[376,750,546,971],'size':[18,23]},
 'visor-west-bowed':{'polygon':[[831,773],[866,753],[923,754],[970,777],[1004,814],[1004,881],[984,930],[957,966],[927,971],[900,952],[900,923],[876,902],[865,866],[843,833]],'box':[831,753,1005,972],'size':[18,23]}}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for key,q in regions.items():
 mask=Image.new('L',raw.size);ImageDraw.Draw(mask).polygon([tuple(p) for p in q['polygon']],fill=255);im=raw.copy();im.putalpha(Image.fromarray(np.minimum(np.array(raw)[:,:,3],np.array(mask))));im=im.crop(q['box']).resize(q['size'],Image.Resampling.NEAREST);target=P/'sources'/f'{key}-native.png';im.save(target);q.update(source='generated-repair-pitch.png',sourceHash=sha(P/'generated-repair-pitch.png'),output=target.relative_to(P).as_posix(),outputHash=sha(target))
(P/'repair-pitch-extraction.json').write_text(json.dumps({'regions':regions,'method':'Explicit isolated head/neck and visor polygons; native nearest extraction; generated collar/shell excluded. Builtin generation source preserved.'},indent=2)+'\n')
print('Extracted four bowed identity sources')
