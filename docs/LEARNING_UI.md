# Station learning UI

This pass adds player-facing explanations and navigation without changing room
costs, operation budgets, discovery requirements or rewards.

- **Room status:** the inspector explains suspension, shared-input shortages and
  full habitats. Functioning status reflects the last evaluated cycle. The separate
  next-cycle forecast calls the existing economy simulator with known bonuses only;
  changing supplies or events can alter the result. Ordinary room production does
  not acquire an invented connectivity requirement.
- **Inspector hierarchy:** status and remedy, forecast, base production and inputs,
  then learned synergy records. Built-room patterns distinguish local functioning,
  a connected but non-functioning pair, and a missing local connection. The existing
  station-wide record is labeled separately. Hidden recipes remain unnamed.
- **Locate:** the inspector can center the selected built room. Its matching-door
  neighbors and physical connections are highlighted without exposing recipe names.
- **Discovery review:** pattern/blueprint notifications open their exact Codex entry.
  A sidebar review button and title badges expose unread records after notifications
  expire. Unread rooms, patterns and mastery ranks persist in the existing meta save.
  Codex and progression provide explicit Mark Reviewed actions. Toasts have a bounded
  queue; overflow does not discard the persistent records. Reduced Motion removes
  their entrance/exit animation.
- **Run summary:** outcome and retained knowledge appear first, with score research,
  pattern research, mastery and rank changes. Detailed run statistics remain below.
  Review Discoveries opens the archive and returns to the summary when closed.
- **Contextual guide:** first build, matching doors, functioning inputs, then three
  consecutive stabilization cycles. Stages derive from actual run state; the guide
  never grants resources or reveals a recipe. Skip and completion persist. Existing
  profiles with discoveries default to completed. Replay First-loop Guide in the
  pause menu restores the contextual guidance for the current station.

`tests/test_learning_ui.gd` uses isolated preferences, checkpoint and meta files.
It checks a paid placement, suspension remedy, spoiler protection, locate selection,
notification-to-Codex links for patterns and blueprints, unread persistence, guide
progress/skip and summary-to-progression return. Its direct discovery/reward calls
exercise UI transitions; they are not evidence of balance or discovery timing.
Native screenshots: `output/learning-ui-inspector.png` and
`output/learning-ui-summary.png`. Learning UI, menu, save and enlarged-overlay tests
pass. An exported-build rerun is not part of this pass.
