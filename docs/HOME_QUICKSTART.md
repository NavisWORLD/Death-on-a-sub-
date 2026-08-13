# HEARTLIGHT Home — Family Quickstart

HEARTLIGHT Home is the no-terminal interface for The Lantern Archive.

## The simple version

1. Open the repository's **Releases** page.
2. Open **HEARTLIGHT Home — Latest**.
3. Download the file for your computer:
   - `HEARTLIGHT-Home-Windows.exe`
   - `HEARTLIGHT-Home-macOS.zip`
   - `HEARTLIGHT-Home-Linux-x86_64.tar.gz`
4. Open HEARTLIGHT Home.
5. Your browser opens a private local page at `127.0.0.1`. The app does not bind to the public network.
6. Choose **Create a Lantern**.
7. Drag in the photos, videos, audio, and text you have permission to preserve.
8. Optionally add a clean PCM WAV heartbeat recording.
9. Use **Teach** to add family memories and context.
10. Choose **Build Lantern**.
11. Use **Backup** whenever you want a ZIP copy of the complete Lantern vault.

No Python installation, terminal, Azure account, IBM account, or cloud service is required for this Home workflow.

## Where the files live

HEARTLIGHT Home stores local Lantern data in the operating system's normal application-data area:

- Windows: `%LOCALAPPDATA%\HEARTLIGHT`
- macOS: `~/Library/Application Support/HEARTLIGHT`
- Linux: `$XDG_DATA_HOME/heartlight` or `~/.local/share/heartlight`

You can override this location with `HEARTLIGHT_HOME_DATA_ROOT` in developer/managed deployments.

## What the buttons mean

### Memories

Drop in family records. HEARTLIGHT copies each record into the Lantern vault, computes a SHA-256 checksum, and records provenance such as the family source and optional note.

### Heartbeat

Upload a `.wav` heartbeat or pulse-style recording. The reference analyzer measures a reproducible timing signature. It is not a medical device and does not claim that the signal alone contains a person's entire identity.

### Teach

Add source-labeled family memories. Different relatives can preserve different recollections. HEARTLIGHT does not force them into one falsely certain story.

### Build

Create the machine-readable memorial profile that combines the evidence manifest, text corpus, family teaching, disclosure rules, and optional heartbeat signature.

### Backup

Download the complete Lantern as a ZIP. Keep backups somewhere you control.

## Security and privacy

The packaged Home server binds only to `127.0.0.1`, so it is intended for the person sitting at that computer. It does not upload family media by default. Azure and IBM cloud bridges remain optional developer/managed features.

Family records can be extremely sensitive. Keep device encryption enabled, protect backups, and do not add private records you do not have the right to use.

## Windows/macOS warnings

The community builds are currently unsigned. Windows SmartScreen or macOS Gatekeeper may therefore warn before opening them. Code signing and Apple notarization require external signing identities and are distribution credentials, not an engineering feature the repository can manufacture on its own.

## Mobile

The Home interface is responsive and PWA-capable. A properly HTTPS-hosted deployment can be installed from a phone browser. Native App Store and Play Store distribution still requires platform signing, store accounts, privacy declarations, and review/submission.

## The important disclosure

HEARTLIGHT Home creates an archive and computational memorial from supplied evidence and ongoing family teaching. It does not prove biological resurrection, soul recovery, consciousness survival, or exact identity transfer.
