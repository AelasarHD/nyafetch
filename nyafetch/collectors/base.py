"""The data collected about the current machine, independent of OS or rendering."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class InfoSnapshot:
    os_name: str
    host: str
    kernel: str
    uptime: str
    shell: str
    terminal: str
    cpu: str
    gpu: str
    ram: str
    disk: str
    python_version: str
