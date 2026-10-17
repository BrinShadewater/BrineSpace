from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-east-inspect-body-grade-v26';out.mkdir(exist_ok=True)
shader=(p/'body-material.gdshader').read_bytes();(out/'body-material.gdshader').write_bytes(shader)
bake=(p/'material-bake.gd').read_text().replace('james-east-inspect-body-grade-v25','james-east-inspect-body-grade-v26')
bake=bake.replace('var r:=pixel.r*255.;var g:=pixel.g*255.;var b:=pixel.b*255.','var r:=roundi(pixel.r*255.);var g:=roundi(pixel.g*255.);var b:=roundi(pixel.b*255.)')
bake=bake.replace('(r+g+b)/3.0>16.0','r+g+b>48')
(out/'material-bake.gd').write_text(bake,encoding='utf-8')
(out/'verify_material.py').write_bytes((p/'verify_material.py').read_bytes())
prior=json.loads((p/'native-inputs.json').read_bytes())
files=[r/f for f in prior['preLaunchSha256'] if not f.startswith('character/james-east-inspect-body-grade-v25/')]
files += [Path(__file__),p/'native-inputs.json',p/'material-bake.gd',p/'body-material.gdshader',out/'material-bake.gd',out/'body-material.gdshader']
(out/'native-inputs.json').write_text(json.dumps(dict(preLaunchSha256={f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in set(files)},
    change='Versioned byte-rounded authoring selector. V25 fails outside-mask protection at bare4(72,153):RGB20,12,16 mean exactly16 selected due float epsilon, native roundtrip darkens by1. Keep source boundary exact.'),indent=2)+'\n')
(p/'rejection.json').write_text(json.dumps(dict(selected=False,sourceAcceptance=False,disposition='failed_exact_outside_color_selection_guard',
    firstFailure=dict(mode='bare',slot=4,pixel=[72,153],before=[20,12,16,244],after=[19,11,15,244]),
    nextVersion='character/james-east-inspect-body-grade-v26',normalChanged=False),indent=2)+'\n')
print('V26 byte-rounded native selector prepared; V25 retained as failed guard trial.')
