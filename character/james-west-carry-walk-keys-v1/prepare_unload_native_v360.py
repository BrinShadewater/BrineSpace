from pathlib import Path

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
output = bank / 'north-unload-chain-v360'
source = (bank / 'release-cargo-playtest-v352/cargo_playtest.gd').read_text()
source = source.replace('cargo352', 'unload360').replace('JAMES PACKAGED CARGO', 'JAMES CANDIDATE UNLOAD')
source = source.replace('for gear in ["bare","helmet"]:', 'for gear in ["bare"]:')
source = source.replace('                if tick%6==0:', '                if tick%6==0 or npc.stage=="workshop_unload":')
injection = '''
    var spec_path:String=get_script().resource_path.get_base_dir()+"/playback.json"
    var spec=JSON.parse_string(FileAccess.get_file_as_string(spec_path))
    check(spec is Dictionary,"Candidate catalogue reads")
    if not spec is Dictionary:get_tree().quit(2);return
    var proposal:Dictionary=spec.unload[1]
    var candidate:Array=[];var cache:Dictionary={};var archive_root:String=get_script().resource_path.get_base_dir().get_base_dir().get_base_dir().get_base_dir()
    for path in proposal.paths:
        var filename:String=archive_root+str(path)
        if not cache.has(filename):
            var image:=Image.new();var result:int=image.load(filename)
            check(result==OK,"Candidate frame loads")
            if result!=OK:get_tree().quit(2);return
            var texture:Texture2D=ImageTexture.create_from_image(image)
            for attribute in player.frames["unload-north"][1].get_meta_list():
                texture.set_meta(attribute,player.frames["unload-north"][1].get_meta(attribute))
            texture.set_meta("crew_pivot",Vector2(128,224));texture.set_meta("crew_standing_height",148.0)
            var used:Rect2=Rect2(image.get_used_rect());var density:float=65.28/148.0
            texture.set_meta("crew_alpha_extent",Rect2((used.position-Vector2(128,224))*density,used.size*density))
            var filtered:=CanvasTexture.new();filtered.diffuse_texture=texture;filtered.texture_filter=CanvasItem.TEXTURE_FILTER_LINEAR
            for attribute in texture.get_meta_list():filtered.set_meta(attribute,texture.get_meta(attribute))
            cache[filename]=filtered
        candidate.append(cache[filename])
    check(candidate.size()==284,"Explicit forward/reverse source slots")
    # Fixture-only substitution; the tested PCK, original files and helmet bank
    # are unchanged. Ordinary actor update, room contact and floor-case logic run.
    candidate[0]=player.frames["unload-north"][0]
    candidate[-1]=player.frames["unload-north"][-1]
    player.frames["unload-north"]=candidate
    player.timing["unload-north"]={"durations":proposal.clocks,"loop":false,"seconds":.52}
'''
source = source.replace('    var cases:Array=[]', injection + '\n    var cases:Array=[]')
source = source.replace('No autonomous goal choice, real-time pacing, hazards, save interruption or full selected-library temporal acceptance.', 'Fixture-only bare North unload candidate substitution: generated lowering followed by explicit reversal and exact selected endpoints; four actual workshop layouts, normal actor/case renderer. 60Hz native captures during unload,10Hz other stages. No normal selection, helmet candidate, autonomous goal choice, real-time pacing, hazards, save interruption or original-master acceptance.')
(output / 'native_playtest.gd').write_text(source, encoding='utf8')
runner = (bank / 'run_cargo_playtest_v352.py').read_text()
runner = runner.replace('release-cargo-playtest-v352', 'north-unload-chain-v360').replace('james-cargo-playtest-v352', 'james-unload-playtest-v360').replace('JamesCargoPlaytest', 'JamesUnloadPlaytest').replace('cargo_playtest.gd', 'native_playtest.gd').replace('cargo352', 'unload360')
(bank / 'run_unload_native_v360.py').write_text(runner, encoding='utf8')
print('Prepared fixture-only North unload candidate in actual packaged workshop lifecycle')
