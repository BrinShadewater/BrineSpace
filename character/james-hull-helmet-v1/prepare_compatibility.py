from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parents[1]
s=(R/'character/james-ward-helmet-v1/hull_regression.gd').read_text(encoding='utf-8')
s=s.replace('res://character/james-ward-helmet-v1/','res://character/james-hull-helmet-v1/')
s=s.replace('for other_goal in ["construction","hull-repair"]:', 'var hull:Dictionary=data.duplicate(true);hull.goal="hull-repair";check(actor.valid_branforth_snapshot(hull),"Explicit James dry helmet hull admission")\n\t\tfor other_goal in ["construction"]:')
s=s.replace('otherFamiliesAndWetRejected','constructionAndWetRejected')
s=s.replace('rejecting other repair families','admitting dry helmet Hull while rejecting construction')
(P/'hull_regression.gd').write_text(s,encoding='utf-8')
# Generate the already-run wrapper UID through Godot's resource UID API, in this isolated fixture.
s=s.replace('print("JAMES HULL REASSIGN ADMISSION:', 'var wrapper_uid:=FileAccess.open("res://character/james-hull-helmet-v1/bill_compat.gd.uid",FileAccess.WRITE);wrapper_uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));wrapper_uid.close()\n\tprint("JAMES HULL HELMET COMPATIBILITY:')
(P/'hull_regression.gd').write_text(s,encoding='utf-8')
