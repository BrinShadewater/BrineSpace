from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
# Reuse the established source-clock/camera review construction with the worn
# paired library and actual helmet captures. No new visual source processing.
code=(R/'character/james-ward-cardinal-v1/build_review.py').read_text(encoding='utf-8')
code=code.replace("directions=['east','south','west']","directions=['north','east','south','west']")
code=code.replace("bare-manifest.json","helmet-manifest.json").replace("character/crew-runtime-matte-v1/branforth","character/james-shared-helmet-runtime-v1")
code=code.replace("master_board=Image.new('RGB',(1104,648)","master_board=Image.new('RGB',(1104,864)")
code=code.replace("'James ward repair / 18-second source clock / no room overlays'","'James helmet ward repair / 18-second source clock'")
code=code.replace("(600,240)","(800,240)")
code=code.replace("'Three actual paid18-second/8Metal cryo ward jobs", "'Four actual paid18-second/8Metal helmet cryo ward jobs")
code=code.replace("Not owner layouts/other gears/ward types/pause-work/power/door/flood/incoming worker acceptance.","Prescribed worn gear via supported setter; not locker fitting, owner layouts, other ward types/power/door/flood/incoming worker acceptance. North pause/reentry evidence separate.")
code=code.replace("for facing,e in evidence.items():", "for facing,e in evidence.items():")
code=code.replace("assert e['failures']==0", "assert e['failures']==0\n    assert all(r['helmet'] for r in e['records'])")
exec(compile(code,str(P/'build_review.py'),'exec'))
