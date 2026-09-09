# Cryo standard room material match

Three new sources in assets/material-polish-cryo-v1 replace the standard cryo support wall, paired side variants and equipment donor. The capsule glass is now subdued blue-grey with restrained frost, the casing is muted cream and the pipes matte charcoal with subdued brass. The padding remains visible. Both standard pods, compressor and console follow the same finish. Original sources, exact prompts and hashes are retained.

Three full-wall registrations now use read-only neutral-background vector geometry. The equipment source preserves its 1254-square UV layout and existing silhouettes. No recovery or animation logic changed. Current card consumers reference the refreshed standard room card.

Verification: eight rotation/state renders, one sealed offline card bake and twenty side variants passed without ERROR output. All four powered standard room rotations were visually inspected at native 512 size. No obvious exterior-white leaks were visible. Evidence: output/art-material-cryo-v1. No executable rebuild.

Recovery-state material acceptance remains incomplete. cryo_chamber_view.gd loads six separate rooms/derelict-cryo-v1/wake-0.png through wake-5.png images for occupied recovery pods, while architect-specific pods use scripts/architect_cryo_art.gd. The first occupied-pod source was visually inspected and retains brighter glass/cream. A coordinated six-frame review/repaint plus architect-specific material review is needed; standard room captures do not prove those states. Keep identities, pose progression, alpha, placement and recovery behavior intact. Other biological room families, risers, shared props and remaining art continue under the full goal.
