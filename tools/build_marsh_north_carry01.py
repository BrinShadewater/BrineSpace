"""Pack own rear cargo sheet at North's actual146 neutral calibration."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=(ROOT/'tools/build_marsh_south_carry01.py').read_text().replace('south','north').replace('South','North').replace('exec-93058684-6a69-4380-ad91-8a7f50de23b5','exec-f36e8bbe-a893-4895-99e9-4145a5f7c4ef').replace('scale=147/','scale=146/').replace("'neutralOccupiedTargetHeight':147","'neutralOccupiedTargetHeight':146")
source=source.replace("req['orderedReferences']+req['sourceFrames']", "req['orderedReferences']+req['sourceFrames']+req.get('guideToolDependencies',[])")
exec(compile(source,str(ROOT/'tools/build_marsh_north_carry01.py'),'exec'),{'__file__':str(ROOT/'tools/build_marsh_north_carry01.py'),'__name__':'__main__'})
