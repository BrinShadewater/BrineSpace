# Project handoff

## Objective and acceptance
Owner approved matte+linear in Studio ("Yeah, that looks much better") and authorized installation ("Okay keep going").

## Current state
`character/crew-runtime-matte-v1/` preserves673 approved preview frames byte-for-byte, three manifests, acceptance record, hashes and exact shader provenance. `textureFilter: linear` is opt-in per manifest. `scripts/crew_sprite_player.gd` wraps these frames in CanvasTexture and copies metadata, leaving default sampling for other packs. Gameplay and ordinary Studio override paths now point to this pack; ACTIVE_ASSETS updated. Previous source and review packs remain intact. Tests target the current pack and explicitly check linear filtering.

Scope:24 bare idle/walk states across Bill, Veld, Branforth. Veld's approved approximate face-region treatment is included. Helmet, action, Marsh and room textures retain previous artwork/filtering. No shadows added. Existing open engine processes must be reopened to load changes.

## Verification
2259 three-crew checks and415 Veld checks pass. Native production-loader captures120 frames. Station fixture20 views and96 independent Bill helmet samples pass; final station screenshot visually inspected. Installed673 frame files exactly match the selected Studio preview. Isolated APPDATA; real profile hashes unchanged. Saved results and station.png in runtime pack. No executable export, commit, push or generation credits spent; last confirmed56.

## Next action
Source-art issues remain explicitly open: Bill/Branforth side heads too small, Branforth side gait awkward, Bill south style mismatched. Tackle head proportions against accepted front/rear masters first and review at82/54/27px with the now-approved finish. Do not treat finish acceptance as acceptance of those defects.
