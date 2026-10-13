# Project handoff

Updated: September 27, 2026 · Project: BrineSpace · Task: Veld 3D-source pilot

## Objective and acceptance
Try a reusable 3D Veld source rendered to sprites: helmet on/off, four directions, idle/walk/sample inspection. Acceptance requires actual model and motion review at source and station scale.

## Accepted decisions and constraints
Owner authorized trying the proposed pilot. Preserve selected v4 Veld identity and existing runtime art. One body with equipment variants; shared camera/material/light settings. No game conversion authorized or needed.

## Current state
`character/veld-3d-pilot-v1/` contains reproducible extraction script, eight unchanged reference crops, hashes and production/blocker notes. No model or animation generated. No purchase or generation submitted.

## Verification
Index and HEAD tree both contain 36,631 files. Selected source hash matches design-lock.json; eight crops exported. Front crop visually inspected: entire figure contained, source appearance preserved. No Godot execution or owner save access. Other crop quality and actual 3D/motion remain unverified.

## Next action
Obtain callable 3D generation route. Higgsfield catalogs Meshy multi_image_to_3d but lacks generate_3d in this connection; image estimate rejects 3D. API balance 2 credits, browser says all credits used; exact 3D cost unavailable. Restore generation capability/adequate balance, generate from four prepared bare views, inspect mesh, then rig/render and author detachable helmet/inspection action.
