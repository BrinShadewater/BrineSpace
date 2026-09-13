"""Explicit paired scanner override; preserve unrelated source-path aliases."""
from pathlib import Path
import contextlib,io,json
from PIL import Image
import rebuild_bill_art as shared

SELECTED={'veld','branforth','marsh'}
BASE=shared.ROOT/'character/crew-action-detail-v2'

def replacement(actor,state,equipped):
    if actor=='marsh' and state in ('idle-east','idle-west','idle-north','idle-south'):
        from extract_crew_motion_cycle import extract
        recipe_path=shared.ROOT/f'character/marsh-motion-polish-v1/{state}-cycle-recipe.json'
        recipe=shared.read(recipe_path)
        with contextlib.redirect_stdout(io.StringIO()):extract(recipe_path)
        folder=shared.ROOT/recipe['output']
        shared.OPS[actor+'/'+state]={'method':'Fixed-registration whole-body idle breathing; original two-slot timing','recipe':recipe_path.relative_to(shared.ROOT).as_posix(),'source':recipe['source']}
        return {'bare':[Image.open(folder/f'{state}-{i:03}.png').convert('RGBA').crop((36,52,220,236)) for i in range(2)]}
    if actor=='marsh' and state in ('walk-east','walk-west','walk-north','walk-south'):
        from extract_crew_motion_cycle import extract
        recipe_path=shared.ROOT/f"character/marsh-motion-polish-v1/{state.split('-')[-1]}-cycle-recipe.json"
        recipe=shared.read(recipe_path)
        with contextlib.redirect_stdout(io.StringIO()):extract(recipe_path)
        folder=shared.ROOT/recipe['output']
        shared.OPS[actor+'/'+state]={'method':'Whole-body Marsh video cycle with fixed registration; no helmet','recipe':recipe_path.relative_to(shared.ROOT).as_posix(),'source':recipe['source']}
        return {'bare':[Image.open(folder/f'{state}-{i:03}.png').convert('RGBA').crop((36,52,220,236)) for i in range(6)]}
    if actor=='branforth' and state in ('walk-east','walk-west','walk-north','walk-south'):
        from extract_crew_motion_cycle import extract
        import prepare_branforth_video_helmet as helmet
        direction=state.split('-')[-1]
        with contextlib.redirect_stdout(io.StringIO()):
            extract(helmet.BASE/f'{direction}-cycle-recipe.json')
            helmet.main(direction)
        recipe=json.loads((helmet.BASE/f'{direction}-cycle-recipe.json').read_text())
        folder=shared.ROOT/recipe['output']
        result={}
        for variant,prefix in [('bare',''),('helmet','helmet-')]:
            if variant=='helmet' and not equipped:continue
            result[variant]=[Image.open(folder/f'{prefix}{state}-{i:03}.png').convert('RGBA').crop((36,52,220,236)) for i in range(6)]
        shared.image(helmet.BASE/f'sources/{direction}-helmet-head-01.png')
        shared.OPS[actor+'/'+state]={'method':'Whole-body Branforth video cycle with authored fitted helmet and fixed registration','recipe':f'character/branforth-motion-polish-v1/{direction}-cycle-recipe.json','source':recipe['source']}
        return result
    if actor=='veld' and state in ['walk-east','walk-west','walk-south','walk-north']:
        import prepare_veld_video_walk as body
        import prepare_veld_video_walk_helmet as helmet
        direction=state.split('-')[-1]
        with contextlib.redirect_stdout(io.StringIO()):
            body.main(direction)
            helmet.main(direction)
        folder=body.BASE/('review/walk-video-cycle-01' if direction=='east' else f'review/walk-{direction}-video-cycle-01')
        result={}
        for variant,prefix in [('bare',''),('helmet','helmet-')]:
            if variant=='helmet' and not equipped:continue
            result[variant]=[Image.open(folder/f'{prefix}{state}-{i:03}.png').convert('RGBA').crop((36,52,220,236)) for i in range(6)]
        shared.image(body.BASE/'sources'/('east-sample-heads-01.png' if direction=='east' else ('scanner-north-helmet-heads-01.png' if direction=='north' else 'scanner-south-west-heads-01.png')))
        shared.OPS[actor+'/'+state]={'method':'Whole-body video cycle, fixed registration, fitted canonical Veld helmet; contact-calibrated stride','source':'character/veld-identity-correction-v1/sources/'+('walk-video-01.mp4' if direction=='east' else ('walk-north-video-02.mp4' if direction=='north' else f'walk-{direction}-video-01.mp4')),'registration':str((folder/'registration.json').relative_to(shared.ROOT))}
        return result
    if actor=='veld' and state in ['sit-down-east','sit-idle-east','sit-rise-east']:
        import prepare_veld_seated_helmet as seated
        with contextlib.redirect_stdout(io.StringIO()):seated.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['seated-east-body-02.png','east-sample-heads-01.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/seated-east-body-01'
        result={'bare':[Image.open(folder/f'{state}-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-{state}-{i:03}.png').convert('RGBA') for i in range(6)]
        # Frozen standing endpoints have an embedded source offset; interiors do not.
        endpoint=0 if state=='sit-down-east' else 5 if state=='sit-rise-east' else None
        if endpoint is not None:
            for poses in result.values():
                box=poses[endpoint].getbbox()
                assert box[0]>=36 and box[1]>=52 and box[2]<=220 and box[3]<=236
                poses[endpoint]=poses[endpoint].crop((36,52,220,236))
        shared.OPS[actor+'/'+state]={'method':'Canonical female Veld connected sitting with one anatomical ruler, pose-fitted helmet and corrected standing endpoints','sources':names}
        return result
    if actor=='veld' and state in ['equip-helmet-east','remove-helmet-east']:
        import prepare_veld_helmet_transition_body as transition
        with contextlib.redirect_stdout(io.StringIO()):transition.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        shared.image(identity_base/'sources/helmet-don-east-body-02.png')
        folder=identity_base/'review/helmet-transition-body-01'
        poses=[]
        for i in range(12):
            pose=Image.open(folder/f'{state}-{i:03}.png').convert('RGBA')
            box=pose.getbbox()
            assert box[0]>=36 and box[1]>=28 and box[2]<=220 and box[3]<=236
            # Preserve the taller frozen transition canvas and overhead helmet.
            poses.append(pose.crop((36,28,220,236)))
        shared.OPS[actor+'/'+state]={'method':'Canonical female Veld fitted helmet pickup/don and release/removal; six authored keys with original timing and exact corrected idle endpoints','source':'character/veld-identity-correction-v1/sources/helmet-don-east-body-02.png'}
        return {'bare':poses}
    if actor=='veld' and state in ['kneel-north','repair-north','stand-north']:
        import prepare_veld_north_kneel_body as kneel
        import prepare_veld_north_sample_body as sample
        import prepare_veld_north_chain_equipment as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            kneel.main()
            sample.main()
            helmet.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['kneel-north-body-01.png','sample-north-body-01.png','scanner-north-helmet-heads-01.png','turnaround-01.png','idle-north-body-original-000.png','idle-north-equipment-original-000.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/north-kneel-body-01'
        result={'bare':[Image.open(folder/f'{state}-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-{state}-{i:03}.png').convert('RGBA') for i in range(6)]
        shared.OPS[actor+'/'+state]={'method':'Canonical female Veld north kneel/sample/stand, fixed anatomical ruler and pose-fitted helmet with exact connected joins','sources':names}
        return result
    if actor=='veld' and state in ['kneel-west','repair-west','stand-west']:
        import prepare_veld_west_kneel_body as kneel
        import prepare_veld_west_sample_body as sample
        import prepare_veld_west_chain_equipment as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            kneel.main()
            sample.main()
            helmet.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['kneel-west-body-01.png','sample-west-body-01.png','scanner-south-west-heads-01.png','turnaround-01.png','idle-west-body-original-000.png','idle-west-equipment-original-000.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/west-kneel-body-01'
        result={'bare':[Image.open(folder/f'{state}-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-{state}-{i:03}.png').convert('RGBA') for i in range(6)]
        shared.OPS[actor+'/'+state]={'method':'Canonical female Veld west kneel/sample/stand, fixed anatomical ruler and pose-fitted helmet with exact connected joins','sources':names}
        return result
    if actor=='veld' and state in ['kneel-south','repair-south','stand-south']:
        import prepare_veld_south_kneel_body as kneel
        import prepare_veld_south_sample_body as sample
        import prepare_veld_south_chain_equipment as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            kneel.main()
            sample.main()
            helmet.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['kneel-south-body-01.png','sample-south-body-01.png','south-sample-chain-helmet-heads-01.png','turnaround-01.png','idle-south-body-original-000.png','idle-south-equipment-original-000.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/south-kneel-body-01'
        result={'bare':[Image.open(folder/f'{state}-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-{state}-{i:03}.png').convert('RGBA') for i in range(6)]
        shared.OPS[actor+'/'+state]={'method':'Canonical female Veld south kneel/sample/stand, fixed anatomical ruler and pose-fitted helmet with exact connected joins','sources':names}
        return result
    if actor=='veld' and state in [action+'-'+direction for action in ['idle','walk'] for direction in ['south','west','north']]:
        import prepare_veld_directional_identity as identity
        with contextlib.redirect_stdout(io.StringIO()):identity.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        shared.image(identity_base/'sources/turnaround-01.png')
        result={}
        for variant,group,prefix in [('bare','body',''),('helmet','equipment','helmet-')]:
            if variant=='helmet' and not equipped:continue
            poses=[]
            for i in range(6):
                shared.image(identity_base/'sources'/f'{state}-{group}-original-{i:03}.png')
                pose=Image.open(identity_base/'review/directional-movement-01'/f'{prefix}{state}-{i:03}.png').convert('RGBA')
                box=pose.getbbox();assert box[0]>=36 and box[1]>=52 and box[2]<=220 and box[3]<=236
                poses.append(pose.crop((36,52,220,236)))
            result[variant]=poses
        shared.OPS[actor+'/'+state]={'method':'Canonical directional female identity heads, no glasses; original movement body preserved','identitySource':'character/veld-identity-correction-v1/sources/turnaround-01.png'}
        return result
    if actor=='veld' and state in ['idle-east','kneel-east','repair-east','stand-east','interact-east','walk-east']:
        import prepare_veld_east_sample as body
        import prepare_veld_sample_helmet as helmet
        import prepare_veld_east_identity_chain as identity
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
            identity.main()
        names=['veld-east-sample-strip-01.png','veld-east-sample-helmet-heads-01.png']
        names += [f'veld-east-sample-{prefix}original-{i:03}.png' for prefix in ['', 'equipped-'] for i in [0,5]]
        for name in names:shared.image(BASE/'sources'/name)
        identity_sources=shared.ROOT/'character/veld-identity-correction-v1/sources'
        shared.image(identity_sources/'east-sample-heads-01.png')
        for key in ['idle-east','kneel-east','stand-east','interact-east','walk-east']:
            for variant in ['body','equipment']:
                for i in range(6):shared.image(identity_sources/f'{key}-{variant}-original-{i:03}.png')
        folder=identity_sources.parent/'review/east-chain-01'
        result={}
        for variant,prefix in [('bare',''),('helmet','helmet-')]:
            if variant=='helmet' and not equipped:continue
            poses=[]
            for i in range(6):
                pose=Image.open(folder/f'{prefix}{state}-{i:03}.png').convert('RGBA')
                # Study pivot128,224 maps to the frozen east source pivot92,172.
                box=pose.getbbox()
                assert box[0]>=36 and box[1]>=52 and box[2]<=220 and box[3]<=236
                poses.append(pose.crop((36,52,220,236)))
            result[variant]=poses
        shared.OPS[actor+'/'+state]={'method':'Canonical female Veld identity, no glasses; connected idle/kneel/sample/stand with shared head ruler and exact joins','sources':names,'identitySource':str(identity_sources.relative_to(shared.ROOT)/'east-sample-heads-01.png')}
        return result
    if actor=='veld' and state=='interact-north':
        import prepare_veld_north_scanner_body as body
        import prepare_veld_north_scanner_equipment as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['scanner-north-body-01.png','scanner-north-helmet-heads-01.png','turnaround-01.png','idle-north-body-original-000.png','idle-north-equipment-original-000.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/north-scanner-body-01'
        result={'bare':[Image.open(folder/f'interact-north-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-interact-north-{i:03}.png').convert('RGBA') for i in range(6)]
        # This study already uses the frozen north source profile:256px/pivot128,224.
        shared.OPS[actor+'/'+state]={'method':'Full-body canonical female Veld north scanner retrieval/tap/stow with fitted pose heads and corrected idle joins','sources':names}
        return result
    if actor=='branforth' and state=='interact-west':
        import prepare_branforth_west_meter as body
        import prepare_branforth_west_helmet as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
        names=['branforth-west-meter-strip-01.png','branforth-west-helmet-heads-01.png','branforth-west-meter-endpoints-01.png']
        names += [f'branforth-west-meter-{group}-{endpoint}-01.png' for group in ['body','equipment'] for endpoint in ['opening','closing']]
        for name in names:shared.image(BASE/'sources'/name)
        folder=BASE/'review/branforth-role-interact-west-strip-01'
        result={}
        for variant,prefix in [('bare',''),('helmet','helmet-')]:
            if variant=='helmet' and not equipped:continue
            poses=[]
            for i in range(6):
                pose=Image.open(folder/f'{prefix}interact-west-{i:03}.png').convert('RGBA')
                canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(pose,(36,52));poses.append(canvas)
            result[variant]=poses
        shared.OPS[actor+'/'+state]={'method':'Explicit west scanner with authored fitted heads and contract pivot translation','sources':names}
        return result
    if actor=='branforth' and state=='interact-north':
        import prepare_branforth_north_meter as body
        import prepare_branforth_north_helmet as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
        names=['branforth-north-meter-strip-01.png','branforth-north-helmet-heads-01.png']
        names += [f'branforth-north-meter-{group}-{endpoint}-01.png' for group in ['body','equipment'] for endpoint in ['opening','closing']]
        for name in names:shared.image(BASE/'sources'/name)
        folder=BASE/'review/branforth-role-interact-north-strip-01'
        result={}
        for variant,prefix in [('bare',''),('helmet','helmet-')]:
            if variant=='helmet' and not equipped:continue
            poses=[]
            for i in range(6):
                pose=Image.open(folder/f'{prefix}interact-north-{i:03}.png').convert('RGBA')
                canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(pose,(36,52));poses.append(canvas)
            result[variant]=poses
        shared.OPS[actor+'/'+state]={'method':'Explicit north scanner with authored fitted heads and contract pivot translation','sources':names}
        return result
    if actor=='branforth' and state=='interact-south':
        import prepare_branforth_south_meter as body
        import prepare_branforth_south_helmet as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
        names=['branforth-south-meter-strip-01.png','branforth-south-helmet-heads-01.png']
        names += [f'branforth-south-meter-{group}-{endpoint}-01.png' for group in ['body','equipment'] for endpoint in ['opening','closing']]
        for name in names:shared.image(BASE/'sources'/name)
        folder=BASE/'review/branforth-role-interact-south-strip-01'
        result={}
        for variant,prefix in [('bare',''),('helmet','helmet-')]:
            if variant=='helmet' and not equipped:continue
            poses=[]
            for i in range(6):
                pose=Image.open(folder/f'{prefix}interact-south-{i:03}.png').convert('RGBA')
                canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(pose,(36,52));poses.append(canvas)
            result[variant]=poses
        shared.OPS[actor+'/'+state]={'method':'Explicit south scanner with authored fitted heads and contract pivot translation','sources':names}
        return result
    if actor=='veld' and state=='interact-west':
        import prepare_veld_west_scanner_body as body
        import prepare_veld_west_scanner_equipment as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['scanner-west-body-01.png','scanner-south-west-heads-01.png','turnaround-01.png','idle-west-body-original-000.png','idle-west-equipment-original-000.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/west-scanner-body-01'
        result={'bare':[Image.open(folder/f'interact-west-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-interact-west-{i:03}.png').convert('RGBA') for i in range(6)]
        # This study already uses the frozen west source profile:256px/pivot128,224.
        shared.OPS[actor+'/'+state]={'method':'Full-body canonical female Veld west scanner retrieval/tap/stow with fitted pose heads and corrected idle joins','sources':names}
        return result
    if actor=='veld' and state=='interact-south':
        import prepare_veld_south_scanner_body as body
        import prepare_veld_south_scanner_equipment as helmet
        with contextlib.redirect_stdout(io.StringIO()):
            body.main()
            helmet.main()
        identity_base=shared.ROOT/'character/veld-identity-correction-v1'
        names=['scanner-south-body-02.png','scanner-south-west-heads-01.png','turnaround-01.png','idle-south-body-original-000.png','idle-south-equipment-original-000.png']
        for name in names:shared.image(identity_base/'sources'/name)
        folder=identity_base/'review/south-scanner-body-02'
        result={'bare':[Image.open(folder/f'interact-south-{i:03}.png').convert('RGBA') for i in range(6)]}
        if equipped:result['helmet']=[Image.open(folder/f'helmet-interact-south-{i:03}.png').convert('RGBA') for i in range(6)]
        # New study is already registered to this source profile:256px/pivot128,224.
        shared.OPS[actor+'/'+state]={'method':'Full-body canonical female Veld scanner retrieval/tap/stow with fitted pose heads and corrected idle joins','sources':names}
        return result
    if actor=='marsh' and state in ['interact-south','interact-west','interact-north']:
        direction=state.rsplit("-",1)[1]
        import prepare_marsh_south_controller as south
        with contextlib.redirect_stdout(io.StringIO()):south.main(direction)
        for name in [f'marsh-role-interact-{direction}-strip-01.png',f'marsh-role-interact-{direction}-reference-01.png',f'marsh-role-interact-{direction}-end-reference-01.png']:
            shared.image(BASE/'sources'/name)
        folder=BASE/f'review/marsh-role-interact-{direction}-strip-01'
        shared.OPS[actor+'/'+state]={'method':'Explicit controller state override; independent original endpoints and timing','source':f'marsh-role-interact-{direction}-strip-01.png'}
        return {'bare':[Image.open(folder/f'interact-{direction}-{i:03}.png').convert('RGBA') for i in range(6)]}
    if actor not in SELECTED or state!='interact-east':return None
    import prepare_veld_scanner_pose as build
    with contextlib.redirect_stdout(io.StringIO()):
        build.strip(actor)
        if actor!='marsh':build.equipment(actor)
    revision='02' if actor=='marsh' else '01'
    endpoint=f'{actor}-role-interact-east-end-reference-01.png' if actor=='marsh' else f'{actor}-role-interact-east-equipped-endpoint-01.png'
    for name in [f'{actor}-role-interact-east-strip-{revision}.png',f'{actor}-role-interact-east-reference-01.png',endpoint]:
        shared.image(BASE/'sources'/name)
    folder=BASE/f'review/{actor}-role-interact-east-strip-01'
    result={'bare':[Image.open(folder/f'interact-east-{i:03}.png').convert('RGBA') for i in range(6)]}
    if equipped and actor!='marsh':result['helmet']=[Image.open(folder/f'helmet-interact-east-{i:03}.png').convert('RGBA') for i in range(6)]
    shared.OPS[actor+'/interact-east']={'method':'Explicit instrument state override; fixed original timing and idle endpoints','source':f'{actor}-role-interact-east-strip-{revision}.png'}
    return result
