from pathlib import Path
import shutil,uuid,time
P=Path(__file__).resolve().parent;R=P.parents[1]
title='## Veld North quiet idle video trials rejected for head rotation — October 3, 2026'
note='## Veld North quiet idle video trials rejected for head rotation — October 3, 2026\n\nTwo exactsame preparedNorth scanner master first/last6s768P Hailuo02 trials:\n448622361043423 and448623780483544 terminalSuccess/downloaded. EstimatedUSD0.56total,\nbillingunverified. Exactinputs/prompts/INPUTS/generation/raw sources retained in\ncharacter/veld-idle-north-original-master-v1/quiet-video-v1 andquiet-video-v2.\nV1 quietbreath body planted butheadturns right~20..115; V2 explicitfixedheadangle\nprompt alone changes, yetheadturns left~29..62 andagain~75..127. ALL142rawposes of\neach andboth original/prepared/control/source boards inspected. BOTH REJECTED idle.\nHeadwidthV123..28/V222..28 vscontrol22; boot224allposes, fixed1/3offset0. V2height147..149,\naxis127..131. Uniformalpha tolerance8/components>=20/noerosion; no RGB or anatomy edits.\nEach710source/protectedwholehelmet/replaychecks0, actualrawmotion stillfails. All\nsourcebindings reverified. Native fixtures prepared but UNRUN: rejected raw motion\nis sufficient; no normal selection/controller/save change or owner profile access.\n\nLesson: exactfirstlastpose, plantedboots and quietcloth wording do not constrain\nhead rotation. Explicitpositive fixedrearhead wording failed the same condition;\ndo not spend additional prompt-only trials or remove failed middle poses to report\nan accepted loop. Stable suit grade and technical replay passes cannot compensate\nfor wrong directional motion. Preserve bothcomplete sources andtheir verdicts.\nNext changewhole-source authoring route for quietNorthidle, with original/prepared\nside-by-side and one fixed source ruler; then fullcontinuous scannerjoins, cardinal\nmatrix, ordinary contacts/controller/Continue and full-library fidelity/polish.\nExisting four-pose masteridle remains separately staged withhistorical per-cell\nregistration/clear-box limitations; not installed merely becausevideo failed.\nFullgoalactive/incomplete. Handoff: character/veld-idle-north-original-master-v1/HANDOFF.md.\n\n'
paths=[R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-life.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-life.md')]
for path in paths:
 for attempt in range(20):
  with path.open('r',encoding='utf-8') as f:head=''.join(next(f,'') for _ in range(120))
  if title in head:break
  before=path.stat();tmp=path.with_name(path.name+'.veld-'+uuid.uuid4().hex+'.tmp')
  with tmp.open('wb') as dest,path.open('rb') as source:dest.write(note.encode('utf-8'));shutil.copyfileobj(source,dest,1024*1024)
  after=path.stat()
  if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):tmp.unlink();time.sleep(.5);continue
  try:tmp.replace(path)
  except PermissionError:
   tmp.unlink();time.sleep(.5);continue
  print(path.name,'updated');break
 else:raise RuntimeError('Concurrent updates prevented guarded prepend: '+str(path))
