
from __future__ import annotations
import argparse
import json
from pathlib import Path

from .pipeline import review_launch
from .utils import load_json

def main() -> None:
    parser = argparse.ArgumentParser(description="Review launch readiness.")
    parser.add_argument("launch_path", help="Path to launch JSON file")
    args = parser.parse_args()

    launch = load_json(Path(args.launch_path))
    report = review_launch(launch)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
