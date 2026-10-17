"""Source-viewed crown/axis registration retains the accepted body atlas ruler."""
from pathlib import Path
import json,hashlib
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1];C=R/'character/veld-swim-carry-north-coherent-v1'
scale=json.loads((C/'fit-checks.json').read_text())['fixedAtlasScale'];roles={}
axes={'work':[(258,104),(630,104),(1031,103),(253,720),(630,720),(1031,721)],'pickup':[(258,104),(661,104),(1032,103),(253,720),(630,720),(1031,721)]}
for role,points in axes.items():
 p=H/('work-source-v1.png' if role=='work' else 'pickup-source-v4.png');assert Image.open(p).size==(1254,1254)
 records=[dict(sourceCell=i,hairSpan=[x-50,x+50],crown=y,sourceViewedAxis=[x,y],registrationOnly=True) for i,(x,y) in enumerate(points)]
 roles[role]=dict(source=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),fixedAtlasScale=scale,records=records)
(H/'head-landmarks-v1.json').write_text(json.dumps(dict(method='Source-viewed rear crown/axis only; native128/104. Fixed accepted cargo body ruler retained because both selected sources edit its1254square anatomy. No hue-derived rescale; hair run/colored-alpha-noise ruler trial rejected.',cargoRulerSha256=hashlib.sha256((C/'fit-checks.json').read_bytes()).hexdigest(),roles=roles),indent=2)+'\n')
print('Rear source-viewed crown/axis retained, both atlases at accepted',scale)
