# Test-runner profile incident — October 15, 2026

During placement/navigation work, I invoked the maintained runner without an
external scratch APPDATA environment. That was an isolation mistake. Its old
default inherited the real profile for ordinary fixtures; guarded fixtures exited
2 and were misleadingly classified as native skips, while five unguarded tests
ran there. That invocation is excluded from acceptance.

The outer save fingerprint caught four changed paths: `brine_save.json`, a newly
created `nav_stagger_407132.meta`, and the two pre-existing
`room_transition_integration.meta` / `.meta.bak` test files. The primary progression
file differed from its untouched protected backup only in `large_room_run_index`
(12 versus 11). Its unlocks, selected crew, currency and other progression fields
were equal. The backup retained 235 total research points; the older F8 archive
had 229 and was deliberately not substituted.

The primary was restored byte-for-byte from the protected backup. Restored SHA-256:
`5ae4aa44c4eb2adbe064ad1957a648edf3e6ecbe69944069646c8ae31cc8aac8`.
The new nav metadata file was copied to recovery evidence and removed from the
player folder. The two legacy transition-test files have no available pre-test
byte snapshot; their changed versions remain preserved, with no guessed rewrite.
The whole folder therefore must not be described as unchanged or exactly restored.
The guard reported no changes to the loop checkpoint, comms sidecar, Studio
layouts or other non-log files.

The runner now creates a fresh scratch environment by default, sets the expected
`BRINESPACE_TEST_USER_DIR`, and refuses a Windows fixture override that resolves to
the real roaming folder. Inherited scratch APPDATA is intentionally replaced;
preseeded-profile workflows should use their dedicated isolated harness or named
fixture scratch path. Two fake-engine launch tests reproduced the unsafe Windows
default/override before the fix and pass afterwards. Two more exercise the Darwin
HOME and Linux XDG environment branches by simulation; this is not native Mac/Linux
runtime verification.

All eleven relevant source regressions were rerun in scratch profiles and passed,
with zero skips. The outer guard for that corrected suite preserves all 2,948
files relative to the post-recovery baseline. Full post-recovery fingerprints and
protected copies of progression/checkpoint/comms/layout files are now retained.

Evidence: `C:/bs-placement-nav-20261015/recovery/incident.json`, preserved changed
files, `normal-suite-owner.json` (the failed guard),
`normal-isolated-owner-before.json`, `normal-isolated-owner.json`,
`normal-isolated-summary.log`, and `protected-progress/`. Corrected runner output:
`output/test-runs/20261015-154239-headless/`.
