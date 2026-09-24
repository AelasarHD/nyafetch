"""Small, original box-art logos per OS family (no reproduction of any real
logo's pixel pattern). Users can swap these out entirely via config/--ascii."""
from __future__ import annotations

from typing import List

_WIDTH = 22


def _box(label: str) -> List[str]:
    inner_width = _WIDTH - 2
    top = "\u256d" + "\u2500" * inner_width + "\u256e"
    blank = "\u2502" + " " * inner_width + "\u2502"
    label_line = "\u2502" + label.center(inner_width) + "\u2502"
    bottom = "\u2570" + "\u2500" * inner_width + "\u256f"
    return [top, blank, label_line, blank, bottom]


# A braille-art cat, used as the macOS logo instead of a boxed label.
_CAT = """\
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡶⢤⡀⠀⠀⠀⢀⡇⡄⠈⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⡇⡄⢙⢦⣀⣀⣼⠁⠂⠀⠀⠙⢦⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⡇⡇⠀⠁⡍⠁⠀⠀⠈⠁⠂⠀⢈⠳⡄⠀⠀⠀⠀⠀⠀
⠀⠰⡇⢀⠀⡐⠁⠀⠀⠀⠀⠀⢀⡴⣋⡄⠹⣆⠀⠀⠀⠀⠀
⠀⠀⣗⠈⢅⣀⣀⣀⡀⠀⠀⠀⠛⠛⠤⠤⠤⡸⣆⣠⠟⢲⡄
⠀⠀⣿⠀⠰⠒⣺⠟⠁⢀⣠⠤⠶⡄⡁⠀⢀⠆⢹⠁⣠⠞⠁
⠀⠀⢻⡀⢀⠞⠑⠒⢄⢣⡀⠀⠀⡇⠈⠉⠀⣠⣾⡜⠃⠀⠀
⢀⣤⣼⣇⠈⠠⠤⠄⠊⠀⠑⠤⢠⣃⣠⠴⢛⡿⠋⠀⠀⠀⠀
⠸⢤⣄⣈⡓⡦⠤⠤⠤⠴⠖⠚⠋⠉⠀⢸⡍⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠉⠉⠛⠛⠒⢷⠀⠀⠀⠀⠀⠀⢷⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡃⠀⠀⠀⠀⠀⠘⡃⠀⠀⠀⠀⠀"""


LOGOS = {
    "macos": _CAT.splitlines(),
    "linux": _box("Linux"),
    "windows": _box("Windows"),
    "generic": _box("System"),
}

ACCENT_COLORS = {
    "macos": "cyan",
    "linux": "green",
    "windows": "blue",
    "generic": "magenta",
}


def get_logo(os_key: str) -> List[str]:
    return LOGOS.get(os_key, LOGOS["generic"])


def get_accent_color(os_key: str) -> str:
    return ACCENT_COLORS.get(os_key, ACCENT_COLORS["generic"])

