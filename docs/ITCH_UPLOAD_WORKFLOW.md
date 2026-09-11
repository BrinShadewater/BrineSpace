# BrineSpace itch.io uploads

Saved September 9, 2026 at the owner's request. Use Butler for future Windows
uploads, keeping the same channel so new builds update the existing download.

## Installed setup

- Page: https://brinshadewater.itch.io/brinespace
- Target: `brinshadewater/brinespace:windows`
- Executable: `C:/Users/Alex/AppData/Local/Programs/butler/butler.exe`
- Version verified: 15.31.0. User PATH includes the installation directory.
- Login is already stored locally. Only run `butler login` again if authentication
  fails; complete authorization in the browser. Never print or commit credentials.

## Upload a new release

1. Select the intended package and validate it using [Release workflow](RELEASE_WORKFLOW.md).
   Do not choose a ZIP solely by modification time. Keep EXE, PCK, README, NOTICE,
   build_info and SHA256SUMS together. No rebuild is needed merely to upload an
   already accepted release.
2. Run the command below, replacing both placeholders with the real path/version.
   Butler accepts either a ZIP or a complete release folder.
3. Wait for push to exit successfully. Then check status until the successful
   remote build and correct version appear. Save focused logs and build IDs.

```powershell
& 'C:/Users/Alex/AppData/Local/Programs/butler/butler.exe' push '<absolute release ZIP path>' 'brinshadewater/brinespace:windows' --userversion '<release version>'
& 'C:/Users/Alex/AppData/Local/Programs/butler/butler.exe' status 'brinshadewater/brinespace:windows'
```

Reusing `windows` updates the existing download and enables incremental patches.
Do not create a dated channel for each release. Browser upload limits do not
determine Butler's ZIP input limit.

The first upload temporarily returned `No channel windows found` after a successful
transfer, and the editor showed no file while the server processed it. Wait and
recheck with backoff instead of uploading duplicates. A successful transfer alone
does not establish that server processing is complete.

## First verified upload

- Package: `builds/BrineSpace-2026-09-09-face-icon.zip`, 5,233,196,379 bytes.
- Version: `2026-09-09-face-icon`.
- Remote upload: `19174644`; successful build: `1963891`.
- Local build identity: `brinespace-501dcca927427024`.
- Evidence: `output/itch-upload/push.log` and `output/itch-upload/HANDOFF.md`.

The page was Restricted at upload time. Upload authorization does not imply
changing visibility, pricing or posting a devlog. Check the current setting when
relevant; do not treat this historical value as permanent.

Official manuals: [installation](https://itch.io/docs/butler/installing.html)
and [pushing builds](https://itch.io/docs/butler/pushing.html).
