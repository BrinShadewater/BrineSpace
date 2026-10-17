from pathlib import Path
import json,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
assert json.loads((P/'package-checks.json').read_text())['failures']==0
def atomic(p,b):
    t=p.with_name(p.name+'.'+uuid.uuid4().hex+'.tmp');t.write_bytes(b);os.replace(t,p)
p=R/'scripts/grid_canvas.gd';b=p.read_bytes();newline=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'\t\t\t\tpush_error("James north construction torch helmet profile mismatch")'+newline
insert=newline.join([b'\t\t\tplayer.load_manifest("res://character/james-torch-material-residue-v2/bare-manifest.json", true)',b'\t\t\tif not player.load_equipment_manifest("diving-helmet", "res://character/james-torch-material-residue-v2/helmet-manifest.json"):',b'\t\t\t\tpush_error("James torch material residue helmet mismatch")'])+newline
assert b.count(anchor)==1 and b'james-torch-material-residue-v2/bare-manifest.json' not in b;atomic(p,b.replace(anchor,anchor+insert))
p=R/'character/ACTIVE_ASSETS.json';m=json.loads(p.read_text());m['actionOverrides']['branforth-torch-material-residue']='character/james-torch-material-residue-v2/bare-manifest.json';m['actionOverrides']['branforth-torch-material-residue-helmet']='character/james-torch-material-residue-v2/helmet-manifest.json'
for direction in ['east','north','south','west']:m['torchActionOverrides']['branforth-'+direction]='character/james-torch-material-residue-v2/bare-manifest.json'
atomic(p,(json.dumps(m,indent=2)+'\n').encode());(P/'selection.json').write_text(json.dumps({'status':'installed_native_validation_pending','runtimeInstalled':True,'fullSetComplete':False,'references':696,'newlyAuthoredDrawings':0,'packageChecks':3610,'sourceBindings':'source-bindings.json','visualReview':'All696 corrected refs reviewed on16paired boards; same original whole poses and matte brightness, bounded green residue correction. Owner pending.'},indent=2)+'\n')
print('Installed paired material-only override; original source packs retained.')
