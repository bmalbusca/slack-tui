"""Helpers for CLI argument normalization."""

from __future__ import annotations

def normalize_types(types: str | None) -> str:
    """Normalize --types argument (comma-separated)."""
    parts = [p.strip() for p in (types or "").split(",") if p.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for p in parts:
        if p not in seen:
            out.append(p)
            seen.add(p)
    return ",".join(out) if out else "public_channel"
