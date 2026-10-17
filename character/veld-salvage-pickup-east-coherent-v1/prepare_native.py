from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
s=(R/'character/veld-swim-carry-east-coherent-v1/check_native.py').read_text().replace('review_veld_swim_carry_east_coherent_v1','review_veld_salvage_pickup_east_coherent_v1').replace('VELD EAST WATER CARGO CANDIDATE','VELD EAST WORK PICKUP CANDIDATE').replace('scratch-cargo-east','scratch-work-pickup-east')
s=s.replace('Paired candidate loading, exact pixels, metadata, every elapsed/distance phase, two loop seams, pause and player snapshot; not world routing or cargo pickup/turn handoffs','Paired action/cargo candidate loading, exact pixels, metadata, each finite/loop phase, seams/clamping, pause/snapshot and exact work/pickup/cargo endpoints; not controller phase offsets or world journeys')
(H/'check_native.py').write_text(s)
print('Isolated native runner prepared.')
