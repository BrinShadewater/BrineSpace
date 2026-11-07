"""Register the canonical fitted helmet to each video-derived Veld walk pose."""
import json
import numpy as np
from PIL import Image
from prepare_veld_video_walk import BASE
from prepare_veld_east_identity_chain import head_layer
from rebuild_bill_art import binary, chroma


def main(direction='east'):
    if direction not in ['east','west','south','north']:raise ValueError('Unsupported video direction')
    folder = BASE / ('review/walk-video-cycle-01' if direction=='east' else f'review/walk-{direction}-video-cycle-01')
    source='east-sample-heads-01.png' if direction=='east' else 'scanner-south-west-heads-01.png'
    if direction=='north':source='scanner-north-helmet-heads-01.png'
    raw = binary(chroma(BASE / 'sources'/source))
    records = []
    sheet = Image.new('RGB', (1536, 512), '#293b40')
    for slot in range(6):
        body = Image.open(folder / f'walk-{direction}-{slot:03}.png').convert('RGBA')
        top = body.getbbox()[1]
        _, xs = np.where(np.asarray(body)[top:top + 12, :, 3] > 0)
        center = float(xs.min() + xs.max()) / 2
        anchor = (round(center + (3 if direction=='east' else (-3 if direction=='west' else 0))), top + 27)
        source_slot=3 if direction=='west' else 0
        layer = head_layer(raw, 1, source_slot, anchor) if direction!='north' else None
        if direction=='north':
            tile=raw.crop((0,0,raw.width//2,raw.height))
            bottom=tile.getbbox()[3]-1
            _,neck_x=np.where(np.asarray(tile)[bottom-8:bottom+1,:,3]>0)
            neck=float(neck_x.min()+neck_x.max())/2
            head=binary(tile.resize((round(tile.width*.09),round(tile.height*.09)),Image.Resampling.BOX),True)
            layer=Image.new('RGBA',(256,256))
            layer.alpha_composite(head,(round(anchor[0]-neck*.09),anchor[1]-(head.getbbox()[3]-1)))
        pose = body.copy()
        regions = [(round(center - 18), top - 5, round(center + 19), top + 22),
                   (round(center - 10), top + 22, round(center + 14), top + 28)]
        for region in regions:
            pose.paste((0, 0, 0, 0), region)
        pose.alpha_composite(layer)
        assert np.array_equal(np.asarray(body)[top + 29:], np.asarray(pose)[top + 29:]), 'Body below collar changed'
        pose.save(folder / f'helmet-walk-{direction}-{slot:03}.png')
        sheet.paste(body, (slot * 256, 0), body)
        sheet.paste(pose, (slot * 256, 256), pose)
        records.append(dict(slot=slot, anchor=anchor, regions=regions, headSourceSlot=source_slot))
    sheet.save(folder / 'paired-contact.png')
    (folder / 'helmet-registration.json').write_text(json.dumps(dict(status='prepared_selection_tracked_in_ledger', source='sources/'+source, records=records, limits=['Inspect collar and head proportions in motion at station scale before selection.']), indent=2) + '\n')
    print('Prepared six fitted helmet walk poses; lower-body preservation passed.')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('direction',choices=['east','west','south','north'],default='east',nargs='?')
    main(parser.parse_args().direction)
