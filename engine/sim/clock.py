"""Logical clock for the continuous simulation.

Wall-clock time never drives world logic. The logical clock advances only when the
runtime is playing, one tick per decision step. Pausing freezes logical time while
wall-clock keeps ticking; inhabitants never perceive a gap.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Clock:
    """Discrete logical time plus wall-clock bookkeeping for diagnostics only."""

    tick: int = 0
    # Wall-clock seconds accumulated while the runtime was playing (diagnostics).
    played_seconds: float = 0.0

    def advance(self) -> None:
        self.tick += 1

    @property
    def day(self) -> int:
        return self.tick // 48 + 1
