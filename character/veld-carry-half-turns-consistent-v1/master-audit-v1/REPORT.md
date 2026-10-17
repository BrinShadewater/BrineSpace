# Project handoff

Updated:2026-09-30. Project:BrineSpace. Task:Veld helmet master audit.

## Objective and acceptance
Owner reports helmet changing mid-turn after smooth-shell-v2. Audit only;
animations remain staged and no installed asset/loader selection changed.

## Accepted decisions and constraints
Shared neutral matte graphite helmet, silver trim, sealed clear visor and white
lamp. Bun entirely inside shell. Directional shared idle masters and accepted
equipped east idle are authority; independently generated turn shells are not
new masters. Compare at common sprite scale without resizing individual heads.

## Current state and findings
helmet-heads.png compares four accepted masters and48 current half-turn head
crops at identical2x zoom. sources.json records all source paths. In north-south,
frames0-6 use repaired north/east heads; frame7 switches to east/south generated
pose1. Transition starts385ms into original680ms cycle. Port changes from bright
circular disk to recessed ring; visor outline/face tone and collar change rather
than simply rotate. At frame11 the south/west front helmet is a third design.
North/east heads lack the clear glass/rim read of accepted east master and have
warmer orange face shading. Other clips also combine these independently authored
families: changes at canonical endpoints and first interior frames as well as
quarter seams. North/west and south/west west views have larger glass/port/rim
features than north/east's east shell. Current master mismatch is design/material
consistency, not merely the bun bulge or a fixed join registration problem.

## Verification
Visually inspected master sources, same-scale crop sheet and source provenance.
Previous408 packaging/435 native checks established pixel provenance, metadata,
alpha and functional selection only. They did not establish helmet identity.
No new Godot test/probe needed for this read-only visual audit.

## Next action
Repair the helmet family from shared directional masters, preserving one shell,
port, glass/rim, lamp, collar and face treatment through each angle. Fit only head
regions onto accepted body motion. Recheck first interior frames and quarter
boundaries at gameplay scale. Existing installed quarter-turns reuse inconsistent
source heads too; track repairs separately rather than silently treating their
acceptance as approval of a new helmet design. Preserve masters and body pixels.
No generation, installation, commit, push or export in this audit.
