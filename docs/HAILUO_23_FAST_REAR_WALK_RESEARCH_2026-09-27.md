# Hailuo 2.3 Fast: rear walk research

Research date: 2026-09-27. Scope: MiniMax-Hailuo-2.3-Fast through Higgsfield, not Hailuo 02, Director or H3. No generations submitted or credits spent during research.

## Findings that change our workflow

MiniMax explicitly supports bracketed camera commands for 2.3 Fast, including `[Static shot]`. Its documentation says explicit commands are more accurate than natural-language camera descriptions. The image is the starting frame, rather than a permanent pose constraint. The I2V API also defaults `prompt_optimizer` to true and recommends false for precise control. It documents a 2,000-character prompt limit and 6/10 seconds at 768P, with 6 seconds at 1080P. There is no dedicated negative-prompt or video-motion-reference field in that documented request. These facts do not guarantee a correct walk. [MiniMax I2V reference](https://platform.minimax.io/docs/api-reference/video-generation-i2v)

Hailuo's general image-to-video prompting guidance says to emphasize action, camera and constants because the supplied image already establishes subject/setting. It recommends positive descriptions instead of lists of prohibited events. Its short-versus-long discussion emphasizes covering the necessary decisions rather than maximizing or minimizing word count. This is general Hailuo guidance, not a published 2.3 Fast rear-walk benchmark. [Prompt anatomy](https://hailuoai.video/pages/blog/ai-video-prompt-anatomy)

Its source-image guidance recommends one clear subject, room to move and an image suggesting the requested motion. Our image is a symmetrical standing rear pose. A correctly drawn rear contact pose could therefore be a useful controlled input experiment, but this is a hypothesis, not proof that the standing master caused hopping. [Image-to-video guidance](https://hailuoai.video/pages/blog/what-is-image-to-video)

Character-animation guidance recommends explicitly retaining the outfit/colours/design and short clips. This supports one concise preservation clause, not repeating the whole costume specification in every motion prompt. [Character animation guidance](https://hailuoai.video/pages/blog/turn-oc-into-anime-video-clip)

MiniMax's 2.3 launch describes improved movement and illustration/game-CG support, and Fast as the lower-cost variant. It does not establish reliability for stationary rear-view sprite cycles or prove that the standard variant fixes our specific failure. [Model announcement](https://www.minimax.io/news/minimax-hailuo-23)

## Important connector uncertainty

Live Higgsfield models_get(minimax_hailuo) exposes variant, duration and resolution; it does not list prompt_optimizer. The generate tool accepts additional parameters, but that alone does not prove an extra parameter reaches the backend. Our generation.json files and returned submission metadata omit optimizer state. Therefore our prior claim that the owner's wording was used verbatim describes the submitted text only, not a verified downstream conditioning prompt.

Higgsfield's public Standard 2.3 API documents prompt_optimizer=true; that page is not proof of the exact Fast connector route. The exact Fast fal endpoint independently documents the same default. Neither establishes what Higgsfield's MCP adapter did on our runs. Do not silently claim optimizer was disabled, nor claim it caused the failures.

- [Higgsfield Standard API](https://open.higgsfield.ai/models/minimax/hailuo-2.3/standard/image-to-video/api-reference)
- [fal 2.3 Fast Standard I2V API](https://fal.ai/models/fal-ai/minimax/hailuo-2.3-fast/standard/image-to-video/api)

Start/end locking is also not an established 2.3 Fast fix: Higgsfield's catalog combines several Hailuo variants and lists end_image generically, whereas MiniMax's legacy first/last endpoint documents Hailuo 02. Do not add an end frame without variant-specific verification. [MiniMax first/last API](https://platform.minimax.io/docs/api-reference/video-generation-fl2v)

## Audit of our five rear trials

All used the same master, 6 seconds, 768px, Fast variant and no recorded optimizer setting. One output per prompt; no controlled replication, so differences cannot be attributed to wording alone.

| Trial | Prompt characters | Result / decision |
|---|---:|---|
| v1 | 1132 | Very slow irregular rear motion; five-second extracted cycle sped up roughly 3x for comparison. Owner rejected. |
| v2 | 1487 | Detailed heel/foot sequence; owner calls it hopscotch. |
| v3 | 1823 | Extensive planted-support instructions and exclusions; inward/crossing foot placement remains, not accepted. |
| v4 | 281 | Simplified treadmill text; sampled paired-foot motion/bobbing, held. |
| v5 | 48 | Exact owner sentence; rotates into side profile, owner rejected. |

None exceeded the documented character limit. None used `[Static shot]`. Length alone cannot explain the failures. The long prompts introduced multiple interacting movement constraints and undesirable-motion vocabulary. The shortest prompt omitted persistent orientation and camera locking. These are plausible contributing factors, not demonstrated causes. My earlier claim that heel-lift wording caused hopping was too certain.

The loop finder minimizes pixel differences; it does not understand planted support or distinguish a full gait cycle from a similar-looking partial cycle. Static contact sheets also cannot certify grounded locomotion. We must judge playback and foot support before packaging a candidate as a good walk.

## Recommended next prompt (untested)

> [Static shot] The character walks in place at a steady, natural pace, viewed directly from behind throughout the entire shot. Her back remains square to the camera as her legs alternate steps and her arms swing gently. She stays centered at the same size. Her design, colours, lighting and plain green background remain unchanged.

This keeps the user's core instruction. It adds only persistent rear orientation, positive camera control and visual constants. Omit treadmill, north, exact stride counts, anatomical choreography, hopping/negative lists, and extra style adjectives in the first test. These omissions are experimental choices rather than forbidden model syntax. Static shot controls the camera; the rear-view sentence separately controls the character.

## Controlled next test and stopping rule

1. Retain exact existing rear input, Fast model, 6 seconds and 768 resolution. Save all settings and prompt.
2. First verify whether the available Higgsfield route can explicitly forward prompt_optimizer=false. A cost estimate or accepted arbitrary key is not proof. If unavailable, state optimizer unknown and do not claim an exact-prompt experiment. Do not switch billing providers or assume API credits are interchangeable.
3. Test the proposed prompt once when generation is requested. Compare original-speed video before chroma keying or retiming. Check persistent rear orientation, alternating supporting feet, no shared airborne phase, both strides completing, no rotation/size drift, and gear identity. A clean seam is a later check.
4. If promising, repeat the same configuration before crediting the prompt change. If still hopping/turning, stop adding prose. Next controlled variable is a visually correct rear mid-stride starting pose; preserve the master design. That requires new reviewed artwork, not procedural anatomical warping.
5. If the pose experiment still fails, a driving rear-walk video on a motion-control model is the appropriate escalation. It is a different workflow, not an undocumented feature of 2.3 Fast.

No official source found supplies a tested magic prompt for this exact rear-view sprite task. Recommendation is evidence-informed and untested. Accepted east/west assets remain unchanged; rear remains unresolved.
