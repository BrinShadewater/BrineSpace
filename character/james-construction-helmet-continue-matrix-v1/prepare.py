from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
original=(R/'character/james-construction-helmet-v1/continue.gd').read_text(encoding='utf-8')
for side,direction in enumerate(['north','east','south','west']):
    s=original.replace('const RESULT := "res://character/james-construction-helmet-v1/"',f'const RESULT := "res://character/james-construction-helmet-continue-matrix-v1/{direction}/"')
    s=s.replace('for side in range(3):',f'for case_index in range(9):\n\t\tvar side:int={side}')
    s=s.replace('var direction:String=["north","east","south"][side];var threshold:float=2.75','var direction:String=["north","east","south","west"][side];var threshold:float=[.4,2.75,9.68][case_index/3]\n\t\tvar work_phase:String=["torch-draw","weld","torch-stow"][case_index/3]')
    s=s.replace('var wanted:String=["exit","hold","return"][side]','check(actor.animation_state()==work_phase,"Checkpoint starts in intended authored work phase")\n\t\tvar wanted:String=["exit","hold","return"][case_index%3]')
    s=s.replace('var label:String=direction+"-"+phase','var label:String=direction+"-"+work_phase+"-"+phase')
    s=s.replace('"user://james-construction-case%d.loop"%side','"user://james-construction-case%d.loop"%case_index')
    s=s.replace('func settle(target: Vector2i):','func settle(target: Vector2i):\n\tif not game.hand_collapsed:game._toggle_hand_collapsed()')
    s=s.replace('"phase":phase,"sourceExact"','"phase":phase,"workPhase":work_phase,"sourceExact"')
    s=s.replace('"Three actual disk checkpoints into fresh main scenes during new power-loss tool motion: North partial exit, East held idle, South partial return. Exact actor/playback/source/clock/pause/paid order, normal60Hz update to paid completion. Bare only. Not all facing-phase combinations, repeated interruption checkpoints or safety preemption."','"Nine actual helmeted disk checkpoints into fresh main scenes: '+direction+' draw/held/stow crossed with partial exit/neutral hold/partial return. Exact actor/playback/source/clock/pause/paid order, normal60Hz update to paid completion. Five first resumed source changes captured per case; not all resumed slots. Supported prescribed worn gear, initial scene/foot reset, no locker integration or owner-layout acceptance; no repeated-loss or safety-preemption checkpoints."')
    s=s.replace('if not FileAccess.file_exists(RESULT+"continue.gd.uid"):', 'if not FileAccess.file_exists(get_script().resource_path+".uid"):')
    s=s.replace('FileAccess.open(RESULT+"continue.gd.uid",FileAccess.WRITE)','FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE)')
    # Fail fast for a reached-state or restore mismatch instead of recording a
    # visually plausible but inexact checkpoint after hundreds of updates.
    s=s.replace('\t\tgame.paused=true;var phase:', '\t\tif failures>0:quit(2);return\n\t\tgame.paused=true;var phase:')
    s=s.replace('\t\tawait settle(target);await capture(label+"-after",actor)', '\t\tif failures>0:quit(2);return\n\t\tawait settle(target);await capture(label+"-after",actor)')
    s=s.replace('\t\tcases.append(', '\t\tif failures>0:quit(2);return\n\t\tcases.append(')
    (P/(direction+'.gd')).write_text(s,encoding='utf-8')
runner=(R/'character/james-death-family-v1/run_validation.py').read_text()
(P/'run_validation.py').write_text(runner.replace('timeout=240','timeout=600'),encoding='utf-8')
files=list(json.loads((R/'character/james-construction-helmet-v1/runtime-input-before.json').read_text()))
(P/'runtime-input-before.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Four actual direction/work-phase/motion-phase Continue fixtures prepared; no production edits')
