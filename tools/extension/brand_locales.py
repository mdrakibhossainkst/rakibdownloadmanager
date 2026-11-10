"""Apply Rakib's product identity to every browser-locale package copy."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if root is None or not root.is_dir():
    raise SystemExit("usage: brand_locales.py <copied _locales directory>")

updated = 0
for path in sorted(root.glob("*/messages.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("name", {})["message"] = "Rakib Download Manager"
    description = data.get("description", {})
    if "message" in description:
        description["message"] = description["message"].replace(
            "Mister Download Manager", "Rakib Download Manager"
        )
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )
    updated += 1

if updated == 0:
    raise SystemExit(f"no locale message files found in {root}")
print(f"Branded {updated} browser locales as Rakib Download Manager")
