# FL Studio Project Organizer

A command-line tool that automatically cleans up messy FL Studio root directories — sorting loose `.flp` files into their own project folders and reuniting them with exported audio, without guessing wrong and silently corrupting a project.

## Features & Architecture

This isn't just a file-mover. Each piece exists to solve a specific, real problem that came up while building it.

### 1. The Prefix Trap
**Problem:** Exported audio files don't always share an exact name with their `.flp` — a project called `Midnight_Drive.flp` might export as `Midnight_Drive_v2_master.mp3`. Naive exact-match string comparison misses these entirely, and nested loops scanning every file against every project are slow and fragile.

**Solution:** Instead of manual string slicing, the matcher uses dynamic f-string globbing — `fl_dir.glob(f"{folder.name}*.mp3")` — to let the filesystem itself do the prefix filtering. Each project folder generates its own glob pattern on the fly, so matching stays accurate as the naming gets messier, without extra branching logic.

### 2. The Generic Naming Trap
**Problem:** FL Studio's default recording name is `untitled_YYYY-MM-DD.wav`. There's no project name in the filename at all — string matching has nothing to grab onto.

**Solution:** When a name gives no signal, timing does. The tool reads each file's `st_mtime` (Epoch seconds, the raw modification timestamp the OS actually stores) and compares it against the `.flp` files modified within the same rough window. A `.wav` recorded the same day as a specific project's last save is very likely audio from that session — so the match happens on *when* the work happened, not *what it's called*.

### 3. The Quarantine Safety Net
**Problem:** Same-day matching breaks down the moment two different projects were touched on the same day. If the tool guesses and picks the wrong one, it doesn't just misfile a track — it silently pollutes another project's folder with audio that doesn't belong there. That's a correctness bug that's easy to miss and annoying to undo.

**Solution:** Rather than guessing, the tool counts how many `.flp` files fall inside the matching window for a given audio file. Exactly one match → confidently filed. Anything else — zero matches or more than one — gets routed to a `Manual_Review_Audio/` folder instead of being auto-assigned. The tool is deliberately conservative here: an unsorted file is a minor inconvenience; a wrongly-sorted one is a trust problem. When it isn't sure, it says so instead of guessing.

## Tech Stack

- **Python 3**
- **`pathlib`** — directory traversal, path construction, and pattern-based file discovery (`glob`)
- **`shutil`** — safe file moves and metadata-preserving copies (`copy2`)
- **`datetime`** — converting raw `st_mtime` Epoch timestamps into comparable dates for the matching logic

## Setup & Usage

**Requirements:** Python 3.10+ (no external dependencies — standard library only).

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/fl-studio-organizer.git
cd fl-studio-organizer

# 2. Run it
python fl_organizer.py
```

You'll be prompted for the FL Studio project directory to organize, and asked to confirm before anything is moved. From there, the script:

1. Scans the root folder for loose `.flp` files.
2. Creates a matching project folder for each one and moves the `.flp` inside.
3. Matches and relocates exported audio using the prefix + same-day logic above.
4. Routes anything ambiguous to `Manual_Review_Audio/` for you to sort by hand.

> **Note:** This tool moves and copies real files. Back up your FL Studio directory before the first run, especially if you're trying it on a project folder you care about.

## Status & Roadmap

This is a working, actively-developed tool, not a finished product — treated here honestly rather than oversold
