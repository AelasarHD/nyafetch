"""User config: which fields to show, accent color, no-color, custom ASCII art path.
Stored as TOML in the OS-appropriate config directory."""
from __future__ import annotations

import os
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


def _default_config_dir() -> Path:
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA", str(Path.home()))
    elif sys.platform == "darwin":
        base = str(Path.home() / "Library" / "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
    return Path(base) / "nyafetch"


CONFIG_PATH = _default_config_dir() / "config.toml"

DEFAULT_FIELDS = ["os", "host", "kernel", "uptime", "shell", "terminal", "cpu", "gpu", "ram", "disk", "python"]


@dataclass
class NyafetchConfig:
    fields: List[str] = field(default_factory=lambda: list(DEFAULT_FIELDS))
    accent_color: Optional[str] = None
    ascii_art: Optional[str] = None
    no_color: bool = False
    classic: bool = False

    @classmethod
    def load(cls, path: Path = CONFIG_PATH) -> "NyafetchConfig":
        if not path.exists():
            return cls()
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (tomllib.TOMLDecodeError, OSError):
            return cls()
        return cls(
            fields=data.get("fields", list(DEFAULT_FIELDS)),
            accent_color=data.get("accent_color"),
            ascii_art=data.get("ascii_art"),
            no_color=data.get("no_color", False),
            classic=data.get("classic", False),
        )

    def save(self, path: Path = CONFIG_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "fields = [" + ", ".join(f'"{name}"' for name in self.fields) + "]",
            f"no_color = {str(self.no_color).lower()}",
            f"classic = {str(self.classic).lower()}",
        ]
        if self.accent_color:
            lines.append(f'accent_color = "{self.accent_color}"')
        if self.ascii_art:
            lines.append(f'ascii_art = "{self.ascii_art}"')
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
