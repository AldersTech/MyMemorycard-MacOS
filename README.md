# MyMemorycard for macOS
Manage PlayStation 2 memory card images, the Mcd001.ps2 files.
Import and export save games, list them, delete them, make new cards.
```bash
Compatabile with all PCSX2 versions
```

This is a Python port of [mymc](https://www.csclub.uwaterloo.ca/~rridge/mymc/)
by Ross Ridge that runs on natively on the macOS. The original is a
2004 Windows program: Python 2.7, wxPython, and two Windows DLLs, one for
MAX Drive compression and one that drew the 3D save icons with Direct3D.
None of it worked on a recent silicon Macs.

![mymc running on macOS](screens/screenshot.png)


> [!IMPORTANT]
> [Download](https://github.com/AldersTech/MyMemorycard-MacOS/releases/download/v1.0.0/MyMemorycard-1.0.0-macOS-arm.dmg) our packaged application if you do not want to compile the source code yourself.

## Before you use it

Quit PCSX2 first. If you change a card while the emulator has it open, it
will write over your changes or wreck the card.

Back up your card images before writing to them. The original called
itself alpha quality. This port has tests behind it, but be careful with
saves you'd hate to lose.

### Mac app

Download the pre-compiled package file and drag it to your Applications folder.

> [!NOTE]
> After dragging to Applications, open it once, then go to System Settings → Privacy & Security and click Open Anyway.

## Using the app

The arrow next to the Open button lists the cards you opened recently,
and so does File > Open Recent.

Drop a memory card image on the window to open it. Drop a .psu, .max,
.cbs, .sps or .xps on it to import that save. It works out what a file is
by looking inside it, so a card called Mcd001.bin or Mcd001.mcd or with
no extension at all opens the same way.

Pick a save to see its 3D icon. Drag the icon with the mouse to turn it,
double-click to recentre, right-click for lighting and camera options.

Export writes .psu (the usual format) or .max (MAX Drive).

Japanese titles show as they are stored on the card. There's a View menu
option to convert them to ordinary letters.

## Save formats

| Format | Extension | Read | Write |
|---|---|:---:|:---:|
| EMS | .psu | yes | yes |
| MAX Drive | .max | yes | yes |
| Code Breaker | .cbs | yes | no |
| SharkPort / X-Port | .sps, .xps | yes | no |
| nPort | .npo | no | no |

## What it was tested on

Real PCSX2 cards with saves from Kingdom Hearts, Ratchet & Clank, Batman
Begins, Tekken 5, Burnout 3 and NFS Most Wanted. Listing them, reading
the titles, importing a downloaded .max, exporting, and the card check.
The 3D icons show up the same way they do in the PS2's own memory card
browser.

Saves come back byte for byte identical after going card to .psu to .max
and back onto a card.

A card PCSX2 made but no game has formatted yet is blank. mymc tells you
so and points at the format command instead of calling it broken.

One slow spot: MAX Drive compression is pure Python. A small save is
instant, but Gran Turismo 4's 1.5 MB of game data takes about twenty
seconds, and doesn't get any smaller because it's already compressed.
The .psu format is the default and has no such problem.

## Licence

Public domain, same as the original mymc. See LICENSE.txt.

mymc was written by Ross Ridge. The LZARI compression is Haruhiko
Okumura's.


## How to install from source

You need Python 3.9 or newer.

On a Mac with Homebrew:
```bash
brew install python
```

Then from this directory:

```bash
python3 -m venv .venv && .venv/bin/pip install -e ".[gui]"
```

That puts `mymc` and `mymc-gui` in `.venv/bin/`. Add it to your PATH, or
use [pipx](https://pipx.pypa.io/) instead:

```bash
pipx install ".[gui]"
```

If you only want the command line tool, drop the `[gui]` part. It has no
dependencies at all.
