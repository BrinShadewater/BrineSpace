"""Reproduce cutouts/crew-scale sprite and authored console layout from saved sources."""
from pathlib import Path
import importlib.util
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location('cleanup', ROOT / 'tools/room_art_pipeline.py')
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)
body = cleanup.clear_exterior(Image.open(HERE / 'brine-source-v4-face.png'))
body.save(HERE / 'brine-cleaned-v4.png')
crop = body.crop(body.getbbox())
scale = 74 / crop.height
small = crop.resize((round(crop.width * scale), 74), Image.Resampling.NEAREST)
sprite = Image.new('RGBA', (92,92))
sprite.alpha_composite(small, ((92-small.width)//2,9))
sprite.save(HERE / 'brine-float-v4.png')
computers = cleanup.clear_exterior(Image.open(HERE / 'computers-source.png'))
computers.save(HERE / 'computers-cleaned.png')
profile = json.loads((HERE.parent / 'brine-composition-v1.json').read_text())
profile['textures']['computers'] = 'res://rooms/underwater/brine-core/renewal-v2/computers-cleaned.png'
profile['furniture'][0]['footprint'] = [97,69,24,12]
for identity, region, footprint, pivot, width in [
    ('brine_dual_workstation',[120,284,546,438],[72,-123,94,30],[393,718],546),
    ('brine_diagnostics',[789,304,316,417],[-158,112,64,30],[947,718],316),
    ('brine_server',[1183,254,212,467],[132,125,32,26],[1289,718],212),
]:
    profile['furniture'].append(dict(id=identity,texture='computers',region=region,
                                    footprint=footprint,pivot=pivot,ground_width=width))
(HERE/'composition.json').write_text(json.dumps(profile,indent=2)+'\n')
print('BRINE sprite:',sprite.size,'body bounds:',body.getbbox(),'; console alpha:',computers.getchannel('A').getextrema())
