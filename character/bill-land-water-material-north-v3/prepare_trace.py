from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent
t=(R/'tests/test_bill_land_water_material_north_v3.gd').read_text(encoding='utf-8')
t=t.replace('   if tick in range(60,105) or tick in range(410,460):','   if false:')
t=t.replace('   shown=step(game)','''   shown=step(game)
   if tick in [0,60,66,100,300,350,375,400] or tick in range(410,451):
    print("NORTH TRACE "+JSON.stringify({"tick":tick,"pair":[[pair[0].x,pair[0].y],[pair[1].x,pair[1].y]],"length":best,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"state":actor.animation_state(),"medium":actor.movement_medium,"water":water,"pathPoints":actor.path.size(),"goal":actor.goal,"stage":actor.stage,"bridge":not game.grid_view.bridge.is_empty(),"events":game.grid_view.bridge_events}))''')
t=t.replace('if not guards_done and','if false and not guards_done and').replace('if not exit_guards_done and','if false and not exit_guards_done and')
t=t.replace('check(guards_done,"Actual North admission supplies active guard interval")','check(true,"Trace-only guard capture omitted")').replace('check(exit_guards_done,"Actual North exit supplies active guard interval")','check(true,"Trace-only guard capture omitted")')
trace=R/'tests/trace_bill_land_water_material_north_v3.gd';trace.write_text(t,encoding='utf-8');trace.with_suffix('.gd.uid').write_text('uid://cbillnorthwettrace03\n',encoding='utf-8')
runner=(R/'tools/run_bill_land_water_material_north_v3_validation.py').read_text(encoding='utf-8').replace("OUT=ROOT/'output/bill-land-water-material-north-v3'","OUT=ROOT/'output/bill-land-water-material-north-v3-trace'").replace('res://tests/test_bill_land_water_material_north_v3.gd','res://tests/trace_bill_land_water_material_north_v3.gd')
runner=runner.replace('targeted-inputs.json','trace-targeted-inputs.json')
(R/'tools/run_bill_land_water_material_north_v3_trace.py').write_text(runner,encoding='utf-8')
files=json.loads((P/'targeted-inputs.json').read_text(encoding='utf-8'));files['tests/trace_bill_land_water_material_north_v3.gd']=hashlib.sha256(trace.read_bytes()).hexdigest()
files['tools/run_bill_land_water_material_north_v3_trace.py']=hashlib.sha256((R/'tools/run_bill_land_water_material_north_v3_trace.py').read_bytes()).hexdigest()
(P/'trace-targeted-inputs.json').write_text(json.dumps(files,indent=2)+'\n',encoding='utf-8')
print('Prepared isolated no-capture real-controller trace; expected failure is retained as diagnostic, not acceptance.')
