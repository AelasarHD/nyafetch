"""CLI entry point: `nyafetch` / `python -m nyafetch`."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ascii_art import get_accent_color, get_logo
from .collectors import collect
from .config import NyafetchConfig
from .mood import sample_mood
from .render import render


def _os_key() -> str:
    if sys.platform == "darwin":
        return "macos"
    if sys.platform.startswith("win"):
        return "windows"
    if sys.platform.startswith("linux"):
        return "linux"
    return "generic"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nyafetch", description="A tiny, hackable neofetch-style system info tool.")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors.")
    parser.add_argument("--ascii", type=Path, help="Path to a custom ASCII art text file.")
    parser.add_argument("--color", type=str, help="Override the accent color (red/green/yellow/blue/magenta/cyan/white).")
    parser.add_argument(
        "--classic", action="store_true", help="Show the plain OS logo instead of the reactive mood mascot."
    )
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    config = NyafetchConfig.load()
    no_color = args.no_color or config.no_color

    os_key = _os_key()
    ascii_path = args.ascii or (Path(config.ascii_art) if config.ascii_art else None)
    extra_lines = None

    if ascii_path and ascii_path.exists():
        logo_lines = ascii_path.read_text().splitlines()
        accent = args.color or config.accent_color or get_accent_color(os_key)
    elif args.classic or config.classic:
        logo_lines = get_logo(os_key)
        accent = args.color or config.accent_color or get_accent_color(os_key)
    else:
        mood = sample_mood()
        logo_lines = mood.face
        accent = args.color or config.accent_color or mood.color
        extra_lines = [mood.caption]

    snapshot = collect()
    print(render(snapshot, logo_lines, config.fields, accent=accent, no_color=no_color, extra_lines=extra_lines))


if __name__ == "__main__":
    main()
