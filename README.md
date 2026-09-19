# Skyhorn Audio Stack

A small **Foundry VTT v14 meta-module** for the Skyhorn Lighthouse campaign.

It contains **no copyrighted audio and no game content**. Its purpose is to use Foundry's package-relationship system so one manifest can point Foundry at the audio tools used by the campaign.

## Install

In Foundry VTT:

1. Open **Configuration and Setup**.
2. Open **Add-on Modules**.
3. Click **Install Module**.
4. Paste this in **Manifest URL**:

   `https://raw.githubusercontent.com/Quarky/skyhorn-audio-stack/main/module.json`

5. Click **Install**.
6. Accept the missing **required** dependencies when Foundry offers them.
7. Choose any of the **recommended** integrations you also want.
8. Enter your world and enable **Skyhorn Audio Stack**. Required dependencies should be enabled with it.

## Required stack

- `moulinette` — Moulinette Media Search.
- `moulinette-soundboards` — Soundboard & Soundpad by Moulinette.
- `ambience-forge` — layered ambience control.
- `the-sound-of-silence` — cinematic playlist control and crossfades.
- `tabletop-rpg-music` — free Tabletop RPG Music Foundry content pack.

These are resolved by package ID through Foundry's package directory.

## Recommended / optional

- `soundbrett` — fast folder-based local soundboard.
- `yt-jukebox` — synchronized YouTube audio and an overlay channel.
- `syrinscape-control` — Syrinscape integration.
- `soundpainter-conductor` — SoundPainter.io integration.

These are optional because they overlap with other tools or require a separate service/account.

## Updating this bundle

The manifest is hosted at:

`https://raw.githubusercontent.com/Quarky/skyhorn-audio-stack/main/module.json`

The install archive is hosted at:

`https://raw.githubusercontent.com/Quarky/skyhorn-audio-stack/main/skyhorn-audio-stack.zip`

To publish a future update:

1. Change `version` in `module.json`.
2. Rebuild `skyhorn-audio-stack.zip` so it contains `module.json` and this README at the **root of the ZIP**.
3. Replace both files on `main`.

## Package layout inside the ZIP

```text
module.json
README.md
```

Foundry installs those into its own `Data/modules/skyhorn-audio-stack/` directory.

## Version

- Skyhorn Audio Stack: **1.0.0**
- Target Foundry VTT: **v14**
