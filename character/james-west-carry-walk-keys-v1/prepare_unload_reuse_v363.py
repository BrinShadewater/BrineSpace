"""A registered seven-pose unload using only currently selected drawings."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1'
out=bank/'north-unload-reused-rise-v363';out.mkdir(exist_ok=True)
selected=json.loads((bank/'release-motion-review-v356/playback.json').read_text())
indices=[0,1,2,3,4,2,5];clocks=[80,100,100,90,40,40,70]
rows=[];hashes={}
for gear in ['bare','helmet']:
    source_gear='bare' if gear=='bare' else 'diving-helmet'
    old=next(r for r in selected['unload'] if r['gear']==source_gear and r['direction']=='north')
    assert len(old['paths'])==6 and sum(old['clocks'])==520
    original={**old,'gear':'current-'+gear}
    proposal={**old,'gear':'candidate-'+gear,'paths':[old['paths'][i] for i in indices],
              'meta':[old['meta'][i] for i in indices],'clocks':clocks}
    rows.extend([original,proposal])
    images=[]
    for path in proposal['paths']:
        file=root/path.lstrip('/');hashes[path]=hashlib.sha256(file.read_bytes()).hexdigest()
        images.append(Image.open(file).convert('RGBA'))
    target=out/(gear+'-motion.png')
    images[0].save(target,save_all=True,append_images=images[1:],duration=clocks,
                   loop=0,disposal=0,blend=0)
    decoded=Image.open(target);assert decoded.n_frames==7
    for i,image in enumerate(images):
        decoded.seek(i);assert decoded.convert('RGBA').tobytes()==image.tobytes()
        assert decoded.info['duration']==clocks[i]
    board=Image.new('RGB',(7*256,288),(48,59,64));draw=ImageDraw.Draw(board)
    for i,image in enumerate(images):
        board.paste(image,(i*256,28),image)
        draw.text((i*256+8,8),f'{gear} slot{i} / selected {indices[i]}',fill='white')
    board.save(out/(gear+'-chronology.png'))
(out/'playback.json').write_text(json.dumps({'unload':rows},indent=2)+'\n')
(out/'provenance.json').write_text(json.dumps({'version':363,'selected':False,
    'originalSlotIndices':indices,'clocksMs':clocks,'totalMs':520,
    'newArtwork':0,'rgbAltered':False,'normalChanged':False,'sourceSha256':hashes,
    'scope':'One reused selected mid-rise pose inserted before standing; previous80ms hold split40+40. Both original equipment banks retained. No new North case cue.'},indent=2)+'\n')
page=(bank/'north-unload-chain-v360/reversal.html').read_text()
page=page.replace('James unload reversal study','James reused rise study').replace('James - unload reversal comparison','James - smoother unload comparison')
page=page.replace("const x=row.gear==='current'?256:768,y=280", "const x=row.gear.startsWith('current')?256:768,y=row.gear.endsWith('bare')?180:390")
start=page.index('<p>Current unload');end=page.index('</p>',start)
page=page[:start]+'<p>Accepted unload on the left; unselected seven-pose timing study on the right. Bare above and helmet below. Uses only accepted drawings, adding the existing mid-rise pose before standing. Both actions remain 520ms. Persistent North case behavior is unchanged.'+page[end:]
(out/'index.html').write_text(page,encoding='utf8')
fixture=(bank/'north-unload-chain-v360/native_playtest.gd').read_text()
start=fixture.index('    var spec_path:');end=fixture.index('    var cases:Array=[]',start)
injection='''    # Fixture-only resequencing of exact packaged selected texture objects.
    for equipment in ["","diving-helmet"]:
        var original_bank:Dictionary=player.frames if equipment.is_empty() else player.equipment_frames[equipment]
        var original:Array=original_bank["unload-north"].duplicate()
        check(original.size()==6,"Packaged six-pose selected North unload")
        if original.size()!=6:get_tree().quit(2);return
        var proposal:Array=[]
        for index in [0,1,2,3,4,2,5]:proposal.append(original[index])
        check(proposal[0]==original[0] and proposal[-1]==original[-1],"Exact selected texture endpoints")
        original_bank["unload-north"]=proposal
        var clocks:Dictionary=player.timing if equipment.is_empty() else player.equipment_timing[equipment]
        clocks["unload-north"]={"durations":[80,100,100,90,40,40,70],"loop":false,"seconds":.52}

'''
fixture=fixture[:start]+injection+fixture[end:]
fixture=fixture.replace('unload360','unload363').replace('for gear in ["bare"]:', 'for gear in ["bare","helmet"]:')
fixture=fixture.replace('Fixture-only bare North unload candidate substitution: generated lowering followed by explicit reversal and exact selected endpoints; four actual workshop layouts, normal actor/case renderer.', 'Fixture-only both-gear North unload resequencing of exact selected packaged texture objects; original mid-rise reused before standing,520ms. Four actual workshop layouts, normal actor/case renderer.')
(out/'native_playtest.gd').write_text(fixture,encoding='utf8')
runner=(bank/'run_unload_native_v360.py').read_text().replace('north-unload-chain-v360','north-unload-reused-rise-v363').replace('james-unload-playtest-v360','james-unload-playtest-v363').replace('unload360','unload363')
(bank/'run_unload_native_v363.py').write_text(runner,encoding='utf8')
print(json.dumps({'newArtwork':0,'gears':2,'candidateSlotsPerGear':7,'decodedFramesVerified':14,'totalMs':520}))
