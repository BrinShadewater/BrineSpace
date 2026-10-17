# Project handoff

Updated: 2026-10-03 | Project: BrineSpace | Task: Krusher comms portrait

## Objective and acceptance
Continue Krusher after the completed station fixture. Prepared his own portrait candidate; roster-versus-polish clarification remains unanswered. No installation or owner visual acceptance inferred.

## Accepted decisions and constraints
Krusher Dom / System Administrator / AI & Robotics / matte muted cyan #527C80 / selected James utility suit. Real photo is likeness authority; canonical-v4 sheet is costume authority; BRINE comms v14 is portrait rendering authority. Portraits use painted realism separately from gameplay pixel sprites.

## Current state
v1 preserved the photo likeness but looked photographic. v2 refines the painted finish, retaining swept brown hair, blue-grey eyes, close beard and dark utility collar with matte cyan shoulder panels. Raw imagegen outputs preserved separately, exact prompts and reference/output hashes recorded. index.html displays full portrait and 150px comms-scale view with responsive layout.

## Verification and review
Generated v2 visually reviewed: likeness and costume retained, visibly painted finish, dry subdued systems rack background, no text or helmet. PNG decode and square dimensions checked. No Godot run needed for candidate art; no real save files or runtime source changed.

## Changed files
character/krusher-portrait-v1: portrait.png, generation.json, provenance.json, index.html.
character/krusher-portrait-v2: portrait.png, generation.json, provenance.json, index.html, HANDOFF.md.

## Remaining work
Owner review of portrait candidate and answer to pending roster-versus-polish question. Current canonical-v4 supports idle/walk/tablet in four directions, bare and helmet. Other normal crew life states, own actor identity, save integration and role behavior remain before a complete playable crew member. Do not inherit normal James behavior unchanged or invent gameplay perks.
