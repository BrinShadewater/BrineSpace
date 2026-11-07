# Floor mats and major prop scale

Owner feedback: dislike floor mats and Life Support lamp workbench; slightly increase most large props.

Automatic profile workstation mats, generated standing mats, and legacy medical/research/command/BRINE work mats are disabled. Explicitly saved standing-mat decorations remain; domestic rugs remain. Invisible profile pads no longer reserve floor-detail space. Life Support life_service_cart (the orange lamp bench) and its dependent mat entries are removed from the default composition; source art is retained.

Large full-wall installations now target 344 units instead of 328 (4.9% larger); split sections target 136 instead of 128 (6.25%). Existing depth caps, placement fallback and player drafts remain authoritative. Small accessories and standalone machinery are unchanged in this scale pass.

Final verification: 47 rooms / 376 rotation-state renders, 56 rollout draft orientations and 20 side variants passed with no ERROR output. All q0 rooms inspected in contact sheets, Life Support and Tidal additionally inspected at native 512 size. This is not a new crew-route proof for every room. All 47 room cards refreshed and current preview consumers updated. No executable rebuild.

Evidence: output/layout-scale-pass/final and *-final.log. Initial output/layout-scale-pass/rooms and assets/layout-scale-pass/cards are rejected: a removed local variable caused compile errors despite the fixtures printing PASS. Only cards-final is selected. The variable was restored and all checks rerun cleanly.
