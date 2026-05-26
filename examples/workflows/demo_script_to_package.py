from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from scenescout_research.package_planner import create_package_plan

script_path = ROOT / "examples" / "scripts" / "sample_local_news_script.md"
archive_path = ROOT / "examples" / "metadata" / "sample_video_archive.json"
output_path = ROOT / "examples" / "output" / "sample_package_plan.json"

script = script_path.read_text(encoding="utf-8")
archive = json.loads(archive_path.read_text(encoding="utf-8"))

plan = create_package_plan(
    title="Community Cooling Centers Open During Heat Wave",
    script_markdown=script,
    archive_assets=archive,
)

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

print(f"Wrote {output_path}")
