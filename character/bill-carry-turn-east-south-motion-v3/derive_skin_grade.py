from pathlib import Path
import json
import numpy as np
P=Path(__file__).resolve().parent
old=json.loads((P/'sources/material-grade-v7.json').read_text());audit=json.loads((P/'review-before-skin-v9/material-case-audit.json').read_text());correction=np.array(audit['suggestedSharedSkinCorrection']);old['fixedGains']['skin']=(np.array(old['fixedGains']['skin'])*correction).tolist()
old.update(scope='Shared bare skin correction derived from frozen prepass opaque warm skin populations; all4interiors same; non-skin gains unchanged; no pose exposure normalization',basis={'audit':'review-before-skin-v9/material-case-audit.json','baseline':'sources/material-grade-v7.json','pooledEndpointSkinMedian':audit['pooledEndpointSkinMedian'],'pooledInteriorSkinMedian':audit['pooledInteriorSkinMedian'],'sharedCorrection':correction.tolist()})
(P/'sources/material-grade-skin-v9.json').write_text(json.dumps(old,indent=2)+'\n');print('Shared skin correction: '+str(correction.tolist())+'; only bare skin gains changed')
