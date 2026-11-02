from __future__ import annotations

import argparse
import json
from pathlib import Path

from .checker import check_layout


def main() -> None:
    parser = argparse.ArgumentParser(description="Check 2D workcell prototype clearances.")
    parser.add_argument("layout", type=Path)
    parser.add_argument("--output", type=Path, default=Path("workcell_report.json"))
    args = parser.parse_args()
    report = check_layout(json.loads(args.layout.read_text(encoding="utf-8")))
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"valid": report["valid"], "findings": len(report["findings"])}))
