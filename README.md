# FL Studio Project Organizer

A command-line tool that cleans up a messy FL Studio projects folder. It gives every loose `.flp` its own folder, moves matching exports in with it, and sorts untitled recordings by when they were made. If it can't tell where a recording belongs, it quarantines it instead of guessing.

Python 3, standard library only.

## Before / After

```
Before                              After
Projects/                           Projects/
├── Midnight_Drive.flp              ├── Midnight_Drive/
├── Midnight_Drive.mp3              │   ├── Midnight_Drive.flp
├── Neon_Rain.flp                   │   └── Midnight_Drive.mp3
└── untitled_2026-03-02.wav         ├── Neon_Rain/
                                    │   ├── Neon_Rain.flp
                                    │   └── Audio/
                                    │       └── untitled_2026-03-02.wav
                                    ├── Quarantine/
                                    └── untitled_2026-03-02.wav  (original stays; see Limitations)
```

## How it works

1. **Scan** the root folder for loose `.flp` files.
2. **Organize**: create a folder named after each project and move the `.flp` into it.
3. **Match exports by name**: `.mp3` / `.wav` files whose name matches a project (`Midnight_Drive.mp3`) are moved into that project's folder.
4. **Match untitled recordings by time**: FL Studio names recordings `untitled_YYYY-MM-DD.wav`, which says nothing about the project. For each one, the tool compares the file's modified time (`st_mtime`) against every project's last-saved time.

| Projects saved within 24h of the recording | Result |
|---|---|
| Exactly one | Copied into that project's `Audio/` folder |
| Zero or several | Copied into `Quarantine/` for manual sorting |

### Design decision: quarantine over guessing

Time-based matching breaks down when two projects are worked on in the same day. A wrong guess would quietly put audio in the wrong project, which is worse than leaving a file unsorted. So anything ambiguous goes to `Quarantine/` and the tool never picks a project it can't justify.

## Usage

```bash
git clone https://github.com/YOUR-USERNAME/fl-studio-organizer.git
cd fl-studio-organizer
python fl_organizer.py
```

Enter the path to your FL Studio projects folder when prompted.

> **Back up your projects folder before the first run.** The tool moves real files. There are still some limitations I intend to fix.




## Project structure

`FLOrganizer` class with one method per stage (`scan_projects`, `organize_projects`, `move_audio`, `copy_audio`) and a `run()` that chains them. Uses `pathlib` for paths and globbing and `shutil` for moves and metadata-preserving copies.
