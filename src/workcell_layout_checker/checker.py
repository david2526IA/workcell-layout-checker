"""Axis-aligned rectangular clearance checks with readable findings."""

from __future__ import annotations

from itertools import combinations
from typing import Any


def _distance(a: dict[str, float], b: dict[str, float]) -> float:
    """Minimum edge-to-edge distance between two axis-aligned rectangles."""
    ax2, ay2 = a["x"] + a["width"], a["y"] + a["height"]
    bx2, by2 = b["x"] + b["width"], b["y"] + b["height"]
    horizontal = max(a["x"] - bx2, b["x"] - ax2, 0.0)
    vertical = max(a["y"] - by2, b["y"] - ay2, 0.0)
    return max(horizontal, vertical) if horizontal == 0 or vertical == 0 else (horizontal**2 + vertical**2) ** 0.5


def _validate(item: dict[str, Any]) -> None:
    required = {"id", "x", "y", "width", "height"}
    if not required <= item.keys() or item["width"] <= 0 or item["height"] <= 0:
        raise ValueError("each item needs id, x, y, positive width and positive height")


def check_layout(layout: dict[str, Any]) -> dict[str, Any]:
    """Check prototype equipment placements against declared restricted zones."""
    clearance = layout.get("minimum_clearance", 0.5)
    equipment = layout.get("equipment", [])
    restricted = layout.get("restricted_zones", [])
    if clearance < 0:
        raise ValueError("minimum_clearance must be non-negative")
    for item in equipment + restricted:
        _validate(item)
    findings = []
    for first, second in combinations(equipment, 2):
        distance = _distance(first, second)
        if distance < clearance:
            findings.append({"kind": "equipment_clearance", "items": [first["id"], second["id"]], "distance": round(distance, 4), "required": clearance})
    for item in equipment:
        for zone in restricted:
            distance = _distance(item, zone)
            if distance < clearance:
                findings.append({"kind": "restricted_zone_clearance", "items": [item["id"], zone["id"]], "distance": round(distance, 4), "required": clearance})
    return {"valid": not findings, "equipment": len(equipment), "restricted_zones": len(restricted), "minimum_clearance": clearance, "findings": findings, "scope": "2D geometric prototype check only; it is not a functional-safety or regulatory assessment"}
