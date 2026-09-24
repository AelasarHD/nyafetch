# nyafetch 

*A `neofetch`-style system info tool that doesn't just describe your machine — it reacts to it.*

Every other fetch tool bolts a static distro logo onto your specs. nyafetch
replaces that logo with an ASCII cat whose mood, pose, and color are computed
**live** from your actual CPU/RAM/disk load. The "logo" *is* the health check.

```
⠀⠀⠀⠀⠀⠀⣠⣶⣶⢶⣶⣶⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣀⡀⠀⠀⠀⠀⠀⠀   test-Mac-mini.local
⠀⠀⠀⠀⠀⢰⡿⠃⠀⠀⠀⠀⠀⠉⠙⢻⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⠀⢀⣠⣶⠿⠛⠉⠉⠙⣿⡄⠀⠀⠀⠀⠀   ---------------------------
⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠩⠉⠈⠇⠀⠀⢈⠀⠈⠉⠉⠛⠻⠟⠋⠁⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀   OS: macOS 15.2 (Sequoia)
⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀   CPU: Apple M4 (10C/10T) 4.4 GHz
⠀⠀⠀⠀⠀⠈⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠈⠀⠁⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀   GPU: Apple M4
⠀⣀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣶⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀   RAM: 16.0 GB | 6400 MHz
⠀⠛⠿⢶⣤⣄⠀⢀⣴⡟⠋⠉⠉⠙⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⢀⣠⣴⡆⠀   Disk: 10.4 GiB / 228.3 GiB (19%)
⠀⠀⠀⠀⠈⠉⠀⣾⣿⣧⠀⠀⠀⣠⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⣰⣿⣿⠋⠁⠀⠀⠈⣿⣿⣿⡆⠰⡿⠟⠋⠁⠀⠀
⢠⣴⣦⣤⣤⡀⠀⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢀⣿⣿⣿⣄⡀⠀⣀⣰⣿⣿⣿⡇⠀⠁⠀⠀⠀⠀⠀   meltdown incoming. seriously, close some tabs.
⠀⠀⠀⠉⠉⠁⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠶⠶⠶⠶⠶⠆
```
*(that's `overloaded` mode — 92%+ load on any of CPU/RAM/disk. Not pictured: `zen`, `chill`, and `stressed`, each with their own art and color.)*

## The moods

nyafetch samples CPU/RAM/disk usage and picks a mood from the worst of the three:

- 🩵 **zen** — under 40% load. curled up, dozing, cyan.
- 💚 **chill** — under 70%. mildly alert, green.
- 🧡 **stressed** — under 92%. something's eating resources, orange.
- ❤️ **overloaded** — 92%+. it's over, red.

Not into cats today? `nyafetch --classic` swaps the mascot for a plain
per-OS box logo, and `--ascii path/to/your.txt` swaps it for literally
anything you want.

## Install

```bash
git clone https://github.com/AelasarHD/nyafetch.git
cd nyafetch
python -m venv .venv
source .venv/bin/activate  # .venv\Scripts\activate on Windows
pip install -e .
```

Or grab a built wheel from the [Releases](https://github.com/AelasarHD/nyafetch/releases) page:

```bash
pip install nyafetch-*.whl
```

Requires Python 3.11+ (uses the standard library `tomllib`). The only
runtime dependency is [`psutil`](https://github.com/giampaolo/psutil).

## Usage

```bash
nyafetch
# or, without installing the console script:
python -m nyafetch
```

Flags:

- `--no-color` — disable ANSI colors
- `--color NAME` — override the accent color (red/green/yellow/blue/magenta/cyan/white/orange)
- `--classic` — plain per-OS box logo instead of the mood mascot
- `--ascii PATH` — use a custom ASCII art `.txt` file instead (overrides both)

## Configuration

On first run there's no config file; create one at:

- macOS: `~/Library/Application Support/nyafetch/config.toml`
- Linux: `~/.config/nyafetch/config.toml`
- Windows: `%APPDATA%\nyafetch\config.toml`

```toml
fields = ["os", "host", "cpu", "gpu", "ram", "disk"]
accent_color = "magenta"
no_color = false
classic = false
ascii_art = "/path/to/your/logo.txt"
```

Available `fields`: `os`, `host`, `kernel`, `uptime`, `shell`, `terminal`,
`cpu`, `gpu`, `ram`, `disk`, `python`.

## What it shows

- **OS** — on macOS, includes the release codename (Sequoia, Sonoma, Ventura,
  ... all the way back to Tiger); Windows/Linux version strings are
  descriptive enough on their own.
- **CPU** — brand string plus physical/logical core count and max frequency.
- **GPU** — `system_profiler` on macOS, `lspci` on Linux, `wmic` on Windows.
- **RAM** — total capacity and speed (speed detection is best-effort — some
  platforms/permissions won't expose it, in which case it prints `unknown`).

## Supported platforms

macOS, Linux, and Windows.

## Development

```bash
pip install -r requirements-dev.txt
pytest
```

Tests cover `render` (ASCII + info layout, color handling), `mood` (load
thresholds), and `config` (load/save/roundtrip) — the pure-logic parts that
don't touch the OS.

## Project layout

```
nyafetch/
  ascii_art.py           # classic per-OS box-art logos + accent colors (--classic)
  mood.py                 # the reactive cat mascot: load -> mood -> face/caption/color
  render.py              # combines logo + info into the printable block
  config.py              # TOML config load/save
  cli.py                 # argparse entry point
  collectors/
    base.py               # InfoSnapshot dataclass
    common.py             # cross-platform helpers (psutil-based)
    macos.py / linux.py / windows.py
tests/
```

## License

MIT — see [LICENSE](LICENSE).
