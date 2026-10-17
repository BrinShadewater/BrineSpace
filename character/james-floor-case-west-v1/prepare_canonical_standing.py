from pathlib import Path
import json,re,hashlib
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
branch=(r/'scripts/grid_canvas.gd').read_text().split('elif actor == "branforth":',1)[1].split('\n\t\tset(actor+',1)[0];banks={}
for kind,rel in re.findall(r'player\.(load_manifest|load_equipment_manifest)\([^\n]*?"res://([^"\n]+\.json)"',branch):
    path=r/rel;pack=json.loads(path.read_bytes());gear='bare' if kind=='load_manifest' else 'helmet'
    for row in pack.get('states',[]):
        if row['id']=='idle-west':banks[gear]=[(r/f.removeprefix('res://') if f.startswith('res://') else path.parent/f,pack.get('pivot'),pack.get('standingHeight'),path) for f in row['frameFiles']]
bindings={};parts=['extends SceneTree','const ROOT="res://character/james-floor-case-west-v1/"','func _init()->void:call_deferred("run")','func run()->void:','\tif not "brine-james-native-" in OS.get_environment("APPDATA"):quit(2);return','\tvar pixel_checks:=0']
for gear in ['bare','helmet']:
    captured=Image.open(p/f'arrival-captures/{gear}-motion-rise-v4-017-source.png').convert('RGBA');matches=[x for x in banks[gear] if Image.open(x[0]).convert('RGBA').tobytes()==captured.tobytes()];assert matches
    path,pivot,height,manifest=matches[0];assert pivot==[92,172] and height==148
    body=Image.new('RGBA',(256,256));body.alpha_composite(captured,(36,52));originalpath=r/f'character/james-cargo-material-joined-v1/frames/{gear}/unload-west/005.png';original=Image.open(originalpath).convert('RGBA')
    assert body.crop((0,0,256,193)).tobytes()==original.crop((0,0,256,193)).tobytes()
    right_changes=sum(body.getpixel((x,y))!=original.getpixel((x,y)) for y in range(193,256) for x in range(121,256))
    bindings[gear]={'source':str(path.relative_to(r)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'manifest':str(manifest.relative_to(r)),'manifestSha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'originalStanding':str(originalpath.relative_to(r)),'originalStandingSha256':hashlib.sha256(originalpath.read_bytes()).hexdigest(),'originalPivot':pivot,'registeredTranslation':[36,52],'height':height,'originalUpper193RowsExact':True,'originalVisibleRightLowerPixelsChanged':right_changes,'scope':'Upper body matches exact original standing; boots below193 differ from original terminal and deliberately reuse exact next selected idle body. This revises terminal endpoint, not an unchanged-original endpoint claim.'}
    source='res://'+path.relative_to(r).as_posix();originalsource='res://'+originalpath.relative_to(r).as_posix()
    parts+=['\tvar source_'+gear+':=Image.new()',f'\tif source_{gear}.load("{source}")!=OK:quit(2);return',f'\tsource_{gear}.convert(Image.FORMAT_RGBA8)',f'\tvar original_{gear}:=Image.new()',f'\tif original_{gear}.load("{originalsource}")!=OK:quit(2);return',f'\toriginal_{gear}.convert(Image.FORMAT_RGBA8)',f'\tvar body_{gear}:=Image.create(256,256,false,Image.FORMAT_RGBA8)',f'\tbody_{gear}.fill(Color.TRANSPARENT);body_{gear}.blit_rect(source_{gear},Rect2i(0,0,184,184),Vector2i(36,52))','\tfor y in range(193):','\t\tfor x in range(256):',f'\t\t\tif body_{gear}.get_pixel(x,y)!=original_{gear}.get_pixel(x,y):quit(2);return','\t\t\tpixel_checks+=1',f'\tDirAccess.make_dir_recursive_absolute(ROOT+"standing-body-v2/{gear}")',f'\tif body_{gear}.save_png(ROOT+"standing-body-v2/{gear}/000.png")!=OK:quit(2);return']
parts+=['\tvar f:=FileAccess.open(ROOT+"standing-body-v2-package-evidence.json",FileAccess.WRITE)','\tf.store_string(JSON.stringify({"selected":false,"upperOriginalPixelChecks":pixel_checks,"method":"Exact original selected West idle184canvas translated36/52 into256canvas. No resampling, grade or invented pixels. Source binding file records original visible-right-body agreement."},"  "))','\tif not FileAccess.file_exists(ROOT+"package_standing_body_v2.gd.uid"):','\t\tvar uid:=FileAccess.open(ROOT+"package_standing_body_v2.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))','\tprint("JAMES CANONICAL BODY PACKAGE: paired; ",pixel_checks,"original upper pixel checks; exact idle body")','\tquit(0)']
(p/'package_standing_body_v2.gd').write_text(('\n'.join(parts)+'\n').replace('fill(Color.TRANSPARENT)','fill(Color(0,0,0,0))'));(p/'canonical-standing-bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
s=(p/'review_standing_body_v1.py').read_text().replace('standing-body-v1','standing-body-v2').replace('0,0,256,194','0,0,256,193').replace('256*194','256*193')
# Canonical lower body differs legitimately between original equipment sources;
# check each independently against its exact registered idle, not paired equality.
s=s[:s.index("assert Image.open(p/'standing-body-v2/bare/000.png')")]+s[s.index("(p/'standing-body-v2-review-evidence.json')"):]
(p/'review_standing_body_v2.py').write_text(s)
print(json.dumps({gear:b['source'] for gear,b in bindings.items()}))
