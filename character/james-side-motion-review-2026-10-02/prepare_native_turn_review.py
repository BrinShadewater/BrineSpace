from pathlib import Path
P=Path(__file__).resolve().parent
text=(P/'validate-family-v2.gd').read_text()
text=text.replace('east-family-v2-','east-turn-v3-').replace('family-v2-native','turn-v3-native').replace('pickup-east','carry-turn-east-north').replace('James staged East cargo','James staged East-connected turns').replace('for i in range(6):','for i in range(state.frameFiles.size()):')
start=text.index('   for i in range(state.frameFiles.size()):check(rows[')
end=text.index('\n var board:=',start)
text=text[:start]+'''   var parts:Array=state.id.split("-")
   var reverse:String="carry-turn-"+parts[3]+"-"+parts[2]
   for i in range(state.frameFiles.size()):check(rows[state.id][i].get_image().get_data()==rows[reverse][state.frameFiles.size()-1-i].get_image().get_data(),"Exact paired reverse "+mode+state.id)
'''+text[end:]
text=text.replace('Staged paired manifests through actual CrewSpritePlayer, exact36source-clock slots/pivot/ruler/reverse aliases and18native paired scale captures. No normal grid selection or actual actor/task/turn/Continue admission.','Staged paired six-turn manifests through actual CrewSpritePlayer, exact92source-clock slots/pivot/ruler/reverse aliases and46native paired scale captures. No normal grid selection or actual actor/task/Continue admission.')
text=text.replace('JAMES FAMILY V2 NATIVE','JAMES TURN V3 NATIVE')
(P/'validate-turn-v3.gd').write_text(text)
