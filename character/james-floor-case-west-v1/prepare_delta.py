from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent;r=p.parents[1]
source=(p/'release.gd').read_text()
prefix=source[:source.index('\tfor mode in ["bare","helmet"]:')]
setup=source[source.index('\t\tgame.occupied[ORIGIN].erase(FLOOR.FIELD)'):source.index('\t\tvar gear:String=')]
setup=setup.replace('\t\t','\t\t\t')
tail='''			if failures:quit(1);return
			while game.visual_time_seconds<release-.35:
				npc.update(game,.02);game.visual_time_seconds+=.02;game.grid_view._get_branforth_frame(game)
			check(FLOOR.payload(game.occupied[ORIGIN]).is_empty(),"No ownership before skipped cue")
			await record_case(view,npc,mode+"-delta-"+jump+"-before")
			var before:float=game.visual_time_seconds
			var after:float=release+.001 if jump=="cue" else until+.001
			# Model a resumed frame whose clock crossed cue/completion without drawing
			# any intermediate source. Only the actual actor update can release here.
			game.visual_time_seconds=after
			npc.update(game,after-before)
			var owned:Dictionary=FLOOR.payload(game.occupied[ORIGIN]).duplicate(true)
			check(not owned.is_empty() and owned.anchor==fixed_foot-center,"Actor hook releases across skipped source holds")
			check(npc.foot==fixed_foot,"Cue/completion crossing preserves contact")
			check(player.return_plan.is_empty()==(jump=="complete"),"Finite cleanup follows release observation")
			game.grid_view._get_branforth_frame(game)
			check(view.embedded_case==(jump=="cue") and view.case_enabled==(jump=="complete"),"No duplicate or missing separate case after skipped cue")
			await record_case(view,npc,mode+"-delta-"+jump+"-after")
			check(FLOOR.payload(game.occupied[ORIGIN])==owned,"Render observation does not replace ownership")
			results.append({"crossing":true,"mode":mode,"jump":jump,"before":before,"after":after,"release":release,"until":until,"delta":after-before,"ownedBeforeDrawing":not owned.is_empty(),"returnClearedBeforeDrawing":player.return_plan.is_empty()})
			print("JAMES FLOOR DELTA ",mode," ",jump," delta=",after-before," failures=",failures)
			if failures:quit(1);return
	if not FileAccess.file_exists(OUT+"delta.gd.uid"):
		var uid:=FileAccess.open(OUT+"delta.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	var f:=FileAccess.open(OUT+"delta-evidence.json",FileAccess.WRITE)
	f.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Four actual prescribed power-loss carry returns: bare/helmet crossed release cue or entire remaining finite segment in one actor update without intermediate drawing. Ownership asserted before rendering; duplicate suppression/finite cleanup/native source-room capture. Staged West only; no priorities/Continue/normal selection/full-world admission."},"  "))
	print("JAMES FLOOR DELTA: ",checks,"checks; ",failures,"failures;8presentations;4crossings")
	quit(1 if failures else 0)
'''
(p/'delta.gd').write_text(prefix+'\tfor mode in ["bare","helmet"]:\n\t\tfor jump in ["cue","complete"]:\n'+setup+tail)
inputs=json.loads((p/'release-inputs.json').read_bytes())
inputs={k:v for k,v in inputs.items() if Path(k).name!='release.gd'}
paths=[r/k for k in inputs]+[p/'delta.gd']
(p/'delta-inputs.json').write_text(json.dumps({str(path.relative_to(r)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},indent=2)+'\n')
print('Four skipped-cue/completion native cases prepared;12 targeted inputs frozen.')
