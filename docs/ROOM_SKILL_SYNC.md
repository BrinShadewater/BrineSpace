# Room-pipeline installed skill synchronization

The installed `C:/Users/Alex/.codex/skills/brinespace-room-pipeline` main skill
and lessons reference were compared with the checkout versions. The installed
main skill lacked source-batch audit guidance; its lessons reference pointed to
the checkout but did not include the accumulated room-production observations.

SKILL.md and references/lessons.md are now synchronized and byte-verified with
the checkout. Attribution is retained. Both copies explicitly state that installed
references are snapshots and newer checkout observations take precedence. Previous
installed bytes are backed up under `output/production-ten/installed-skill-backup-*`.
Exact paths and before/after SHA-256 values are in `installed-skill-sync.json`.

Other references were compared but not overwritten: art-direction has a separate
condition-language revision and layered-assets a wording revision. Those remain
outside this narrow synchronization of batch-workflow additions. This operation
does not certify room art, change gameplay or publish/install an external app.
