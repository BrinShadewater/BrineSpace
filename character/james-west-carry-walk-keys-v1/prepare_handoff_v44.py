from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
text=(p/'prepare_finite_v41.py').read_text(encoding='utf-8')
text=text.replace("out=p/'finite-bridge-v41'","out=p/'finite-handoff-v44'")
text=text.replace(",p/'master-head-review-v16'/(m+'-000.png')]", "]")
text=text.replace('clock=[70,70,70,40]','clock=[70,70,70]').replace('frameCount=4','frameCount=3').replace('range(4)','range(3)').replace('assert im.n_frames==4','assert im.n_frames==3')
text=text.replace("replace('finite-bridge-v36','finite-bridge-v41')","replace('finite-bridge-v36','finite-handoff-v44')")
text=text.replace(";(out/'native_probe.gd').write_text(program,encoding='utf-8')", "\n+DRAW_AND_RUN_SEPARATOR\n+(out/'native_probe.gd').write_text(program,encoding='utf-8')".replace('\n+','\n'))
adjust='''prefix,body=program.split('func _init()',1)
body=body.replace('range(4)','range(3)').replace('size()==4','size()==3').replace('Four authored slots','Three authored slots').replace('-.25)','-.21)').replace('250ms','210ms').replace('.251','.211').replace('[3-i]','[2-i]').replace('eight paired','six paired').replace('four-pose','three-pose').replace('    ','\\t')
program=prefix+'func _init()'+body
extra="""\t# At210ms hand off to distance-driven walk0, rather than replaying its40ms.
\tplayer.load_manifest(\"res://character/james-west-carry-walk-keys-v1/master-head-review-v16/bare-manifest.json\",true)
\tcheck(player.load_equipment_manifest(\"diving-helmet\",\"res://character/james-west-carry-walk-keys-v1/master-head-review-v16/helmet-manifest.json\"),\"Walking pair appended\")
\tcheck(absf(player.cycle_seconds(\"carry-prepare-west\")+player.cycle_seconds(\"carry-west\")-1.89)<.000001,\"Runtime study equals1890ms source preview\")
\tvar handoff_samples:=0
\tfor equipment in [\"\",\"diving-helmet\"]:
\t\tvar row: Array=player.frames[\"carry-west\"] if equipment.is_empty() else player.equipment_frames[equipment][\"carry-west\"]
\t\tcheck(player.frame(\"carry\",\"west\",.21,Vector2.ZERO,equipment)==row[0],\"Walk0 begins at210ms\")
\t\tvar elapsed:=0.0
\t\tfor slot in range(49):
\t\t\tvar distance: float=.1796875*(elapsed+.000001)/1.68
\t\t\tvar tex: Texture2D=player.frame(\"carry\",\"west\",.21+elapsed+.000001,Vector2(-distance,0),equipment)
\t\t\tcheck(tex==row[slot],\"Exact chronological distance source after handoff\")
\t\t\tif slot==1:check(absf(.21+elapsed-.25)<.000001,\"Walk1 begins at250ms without duplicate walk0\")
\t\t\thandoff_samples+=1
\t\t\telapsed+=float(player.timing[\"carry-west\"].durations[slot])/1000.0
"""
program=program.replace('\\tvar uid_path:=',extra+'\\tvar uid_path:=')
program=program.replace('"captures":captures,','"captures":captures,"handoffSourceSamples":handoff_samples,"handoffMs":210,"journeyMs":1890,')
program=program.replace('\\t','    ')
'''
text=text.replace('DRAW_AND_RUN_SEPARATOR',adjust.rstrip()).replace('sourcePoses=4,preparationMs=250','sourcePoses=3,preparationMs=210')
text=text.replace('V41 four-source250ms','V44 three-source210ms').replace('V40 coherent turn anatomy replaces leg-only V20 slot. No normal adoption.','V40 coherent turn anatomy; three finite preparation sources then distance walk0. No normal adoption.')
target=p/'prepare_finite_v44_generated.py';target.write_text(text,encoding='utf-8');subprocess.run([sys.executable,str(target)],check=True)
