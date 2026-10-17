from pathlib import Path
import subprocess,sys
p=Path(__file__).resolve().parent
s=(p/'prepare_room_journey_v45.py').read_text(encoding='utf-8').replace('room-journey-v45','room-journey-v46').replace('V45 actual','V46 open-floor actual').replace('james-carry-journey','james-carry-open-floor')
old='if npc.travel_segment_clear(from,at,"west") and npc.can_stand(from) and npc.can_stand(at):destination=at;start=from;break'
new='if npc.travel_segment_clear(from,at,"west") and npc.can_stand(from) and npc.can_stand(at) and (not destination.is_finite() or at.y>destination.y):destination=at;start=from'
assert old in s;s=s.replace(old,new)
injection="old=old.replace('func capture(label: String,npc) -> String:\\n','func capture(label: String,npc) -> String:\\n\\tgame.hand_panel.hide();game.card_drag.hide()\\n')\nprefix=old.split"
s=s.replace('prefix=old.split',injection)
target=p/'prepare_room_journey_v46_generated.py';target.write_text(s,encoding='utf-8');subprocess.run([sys.executable,str(target)],check=True)
