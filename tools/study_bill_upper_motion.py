"""Stage preserved arm motion over the selected side-view leg cycle."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
from rebuild_bill_art import HelmetRebaker, WATER
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/bill-pixel-layer-2026-09-21/upper-motion-r2'
SOURCE=ROOT/'output/bill-body-motion-2026-09-20'

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 report={}
 helmets=HelmetRebaker(None)
 for direction in ('east','west'):
  source=Image.open(SOURCE/f'{direction}-preserved-0.png').convert('RGBA')
  sheet=Image.new('RGBA',(184*6,184*2),'#26383c')
  for phase,body_index in enumerate([0,1,2,5,2,1]):
   path=ROOT/f'character/major-bill-v3/frames/bare/walk-{direction}/{phase:03}.png'
   original=Image.open(path).convert('RGBA');frame=original.copy()
   body=Image.open(SOURCE/f'{direction}-preserved-{body_index}.png').convert('RGBA')
   bob=-1 if phase in (1,4) else 0
   shift=source.getbbox()[1]-body.getbbox()[1]+bob
   frame.paste((0,0,0,0),(0,0,184,119+bob))
   frame.alpha_composite(body.crop((0,0,184,119-shift+bob)),(0,shift))
   frame.paste(source.crop((0,0,184,60)),(0,bob))
   a=np.array(original);b=np.array(frame)
   assert np.array_equal(a[119+bob:],b[119+bob:]),(direction,phase,'legs changed')
   frame.save(OUT/f'{direction}-{phase:02}.png')
   registration=json.loads((WATER/'equipment/dry'/f'bill-walk-{direction}'/'registration.json').read_text())
   view=Path(registration['overlay']).parent.name
   position=np.array(registration['frames'][0]['overlayTopLeft'])*2
   position[1]+=bob
   overlay=helmets.overlay(view)
   check=original.copy();check.alpha_composite(overlay,tuple(position))
   production_helmet=Image.open(ROOT/f'character/major-bill-v3/frames/helmet/walk-{direction}/{phase:03}.png').convert('RGBA')
   assert np.array_equal(np.array(check),np.array(production_helmet)),(direction,phase,'helmet recipe differs')
   equipped=frame.copy();equipped.alpha_composite(overlay,tuple(position))
   equipped.save(OUT/f'helmet-{direction}-{phase:02}.png')
   report[f'{direction}-{phase}']={'preserved_body_pose':body_index,'changed_pixels':int(np.any(a!=b,axis=2).sum()),'production_source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'unchanged_from_row':119+bob}
   sheet.alpha_composite(original,(phase*184,0));sheet.alpha_composite(frame,(phase*184,184))
  sheet.resize((2208,736),Image.Resampling.NEAREST).save(OUT/f'{direction}-comparison.png')
 manifest=json.loads((OUT.parent/'whole-limbs/manifest.json').read_text())
 manifest['name']='bill-upper-motion-study'
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
 helmet_manifest=json.loads(json.dumps(manifest))
 helmet_manifest['name']='bill-upper-motion-helmet-study'
 for state in helmet_manifest['states']:
  state['frameFiles']=['helmet-'+name for name in state['frameFiles']]
 (OUT/'helmet-manifest.json').write_text(json.dumps(helmet_manifest,indent=2))
 (OUT/'report.json').write_text(json.dumps(report,indent=2))
 review=(OUT.parent/'whole-limbs/native_review.gd').read_text().replace('whole-limbs/',OUT.name+'/').replace('Whole-limb candidate','Upper-body candidate')
 (OUT/'native_review.gd').write_text(review)
 helmet_review=review.replace('candidate.load_manifest(OUT+"manifest.json")','candidate.load_manifest(OUT+"manifest.json")\n\t\tif not candidate.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"):\n\t\t\tpush_error("Helmet registration mismatch");quit(1);return')
 helmet_review=helmet_review.replace('var equipment: String=""','var equipment: String="diving-helmet"').replace(' / bare /',' / helmet /').replace('native-selected','native-helmet')
 (OUT/'native_helmet_review.gd').write_text(helmet_review)
 print('24 bare/equipped candidates; 12 production helmet recipe matches; selected legs unchanged.')
if __name__=='__main__':main()
