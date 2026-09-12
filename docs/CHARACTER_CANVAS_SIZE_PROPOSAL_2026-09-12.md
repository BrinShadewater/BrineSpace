# Proposal: move Bill's base pack to the 128px canvas — September 12, 2026

Owner complaint at the start of this work: the human characters look blurry.
A four-direction generation test (see [Higgsfield pilot](HIGGSFIELD_PILOT_2026-09-12.md))
showed that new art is **not** the fix. **Nothing is implemented.**

## What the test showed

1. New GPT Image 2.5 frames, put through the real 92x92 path, are visibly sharper at
   close zoom: better head, shoulders and boots, 42-55 colours, zero soft alpha.
2. At the owner's actual station fit zoom (`grid_zoom` 0.4446 in the live save), the
   character is about **29 pixels tall** and the improvement all but disappears.
3. The four independent generations drifted: shoulder patches moved from red caps to
   upper-arm squares between views, and east/west came out taller and slimmer than
   south. The shipped set is more internally consistent than what generation produced.

So re-arting the cast buys little where players spend most of their time, and costs
consistency that already exists. The lever for close-zoom quality is canvas size.

## Why this is cheaper than it sounds

The engine is already multi-canvas. Frame size and pivot are **data, not constants**:

| canvas | packs | pivot |
|---|---|---|
| 128x128 | 285 | (64, 112) |
| 92x92 | 139 | (46, 86) |
| 104x112, 92x104, 104x92 | 46 | per pack |

`crew_sprite_player.gd:66` reads `pivot` from the manifest with `[46, 86]` only as a
fallback, and `crew-actions-v1/bill/*` already ships Bill at 128x128 with pivot
(64, 112). The 92x92 profile is a compatibility baseline, exactly as the character
skill says — not an engine limit.

## The proposal

Move Bill's base locomotion pack (`character/major-bill-v2`, idle/walk/run/stand/
interact/kneel/repair) from 92x92 to 128x128 with pivot (64, 112), matching the
crew-actions packs he already has. Roughly **39% more linear resolution** for the
face and equipment at close zoom, with no change to world scale: he still occupies
65.28 world units, the frame simply carries more pixels.

Do the same for Veld and Branforth only if Bill lands well. Leave Josh, River and
Margot on 92x92 — they are chunky high-contrast shapes that already survive the
downsample.

## What has to be checked before it is safe

1. **Anything that assumes 92.** `crew_sprite_player.gd` sets a texture meta literally
   named `crew_frame_92`; whether that name is load-bearing or vestigial decides part
   of the work.
2. **Mixed-canvas playback.** Bill would have 128px locomotion and 128px actions, so he
   becomes uniform — but equipment overlays (`crew-underwater-v1/equipment/`) and
   companion packs must still align frame-for-frame.
3. **The audit.** `tools/audit_character_bindings.py` compares every frame against its
   manifest's declared size, so it validates the new pack automatically.
4. **Registration and bindings.** New pack means a new revision; `ACTIVE_ASSETS.json`
   and `installed-portraits.json` stay in step, and no existing art is overwritten.

## Cost and sequencing

The expensive part is not the engine: it is regenerating and hand-finishing every
state and direction Bill has, then re-checking motion. That is an art run, not a code
change. Sequence it as: confirm `crew_frame_92` is vestigial → produce one state at
128px → native motion check beside the existing pack → owner decision on the rest.

## Owner decisions

1. Is close-zoom sharpness worth a full re-art of Bill's locomotion states?
2. If yes, Bill only, or Veld and Branforth too?
3. Do the portraits matter more? They ship at 1254x1254 and are displayed large, which
   is where "blurry" would be most visible to a player.
