from pathlib import Path
import json,copy
p=Path(__file__).resolve().parent;r=p.parents[1]
audit=json.loads((r/'character/james-selected-turn-master-audit-v1/review.json').read_bytes())
keys=['carry-turn-south-west','carry-turn-west-south','carry-turn-east-west','carry-turn-west-east']
for gear in ['bare','helmet']:
    pack={'name':'James cap-source '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'selected_normal_loader_checked_helmet_cap_polish_cadence_pending' if gear=='helmet' else 'unselected_bare_native_fixture','states':[]}
    for key in keys:
        entry=audit['states'][gear+'/'+key];m=json.loads((r/entry['manifest']).read_bytes());state=copy.deepcopy(next(s for s in m['states'] if s['id']==key))
        state['frameFiles']=['res://'+file for file in entry['frames']]
        index={'carry-turn-south-west':2,'carry-turn-west-south':3,'carry-turn-east-west':7,'carry-turn-west-east':3}[key]
        if gear=='helmet':state['frameFiles'][index]='res://character/james-helmet-turn-dip-v1/candidate-cap.png'
        state['provenance']={'sourceSelectedManifest':entry['manifest'],'capTrialIndex':index if gear=='helmet' else None,'normalSelectionChanged':False}
        pack['states'].append(state)
    (p/(gear+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
text=(r/'character/james-cargo-turn-south-west-v1/validate.gd').read_text()
text=text.replace('character/james-cargo-turn-south-west-v1/bare-manifest.json','character/james-helmet-turn-dip-v1/bare-manifest.json').replace('character/james-cargo-turn-south-west-v1/helmet-manifest.json','character/james-helmet-turn-dip-v1/helmet-manifest.json').replace('character/james-cargo-turn-south-west-v1/native','character/james-helmet-turn-dip-v1/native')
text=text.replace('var player=grid.branforth_player','var player=grid.branforth_player\n    check(player.equipment_frames.has("diving-helmet"),"Normal helmet bank loaded")')
text=text.replace('var expected := Image.load_from_file(manifests[mode].get_base_dir().path_join(state.frameFiles[i]))','var path:String=state.frameFiles[i]\n                var expected := Image.load_from_file(path if path.begins_with("res://") else manifests[mode].get_base_dir().path_join(path))')
text=text.replace('for index in [0,1,int(state.frameCount/2),int(state.frameCount)-1]:','for index in range(int(state.frameCount)):')
text=text.replace('check(absf(elapsed-(.8))<0.00001,"Authored cargo duration")','check(absf(elapsed-(.8 if int(state.frameCount)==6 else 1.6))<0.00001,"Authored quarter/half cargo duration")')
# Existing normal turn-to-walking checks retained; capture all prescribed slots.
at=text.index('    if not FileAccess.file_exists(')
text=text[:at]+'''    print("JAMES CAP TRIAL: %d checks, %d failures, %d native captures"%[checks,failures,captures])
    grid.free()
    quit(1 if failures else 0)
'''
(p/'native_probe.gd').write_text(text)
# Pair UID before invocation; maintained Godot resource UID syntax.
(p/'native_probe.gd.uid').write_text('uid://djamescaptrial1\n')
print('Four-state normal equipment manifest/paired bare fixture; cap reused at exact reverse/half-turn indexes; native probe ready.')
