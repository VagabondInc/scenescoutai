import re
from typing import Any, Dict, List


def _extract_sections(script_markdown: str) -> List[Dict[str, str]]:
    sections = []
    current_heading = None
    current_lines = []

    for line in script_markdown.splitlines():
        if line.startswith("## "):
            if current_heading and current_lines:
                sections.append({
                    "heading": current_heading,
                    "text": " ".join(current_lines).strip()
                })
            current_heading = line.replace("## ", "").strip()
            current_lines = []
        elif current_heading:
            clean = line.strip().lstrip(">").strip()
            if clean:
                current_lines.append(clean)

    if current_heading and current_lines:
        sections.append({
            "heading": current_heading,
            "text": " ".join(current_lines).strip()
        })

    return sections


def _keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    stop = {"with", "that", "this", "from", "will", "through", "today", "says", "have", "been"}
    return [w for w in words if w not in stop]


def _score_asset(section_text: str, asset: Dict[str, Any]) -> int:
    section_terms = set(_keywords(section_text))
    asset_blob = " ".join([
        asset.get("title", ""),
        " ".join(asset.get("detected_objects", [])),
        " ".join(asset.get("editorial_tags", [])),
        asset.get("transcript", ""),
        " ".join(scene.get("description", "") for scene in asset.get("detected_scenes", [])),
    ]).lower()

    return sum(1 for term in section_terms if term in asset_blob)


def _visual_intent(heading: str, text: str) -> str:
    lower = f"{heading} {text}".lower()

    if "anchor" in heading.lower():
        return "Anchor on-camera or studio presenter segment."
    if "families" in lower or "arrived" in lower:
        return "People arriving at cooling center, exterior activity, public service visuals."
    if "health" in lower or "seniors" in lower:
        return "Public health official, heat safety visuals, vulnerable residents context."
    if "transportation" in lower or "bus" in lower:
        return "Transit access, city services, exterior public infrastructure."
    return "Relevant local news B-roll matched to the script context."


def _generation_prompt(section: Dict[str, str], archive_tags: List[str]) -> str:
    return (
        "Generate realistic local newsroom-style B-roll for editorial review. "
        f"Script section: {section['heading']}. "
        f"Context: {section['text']} "
        f"Archive guidance tags: {', '.join(archive_tags[:8])}. "
        "Avoid identifiable private individuals, private addresses, logos, license plates, "
        "and any visuals that could mislead viewers."
    )


def create_package_plan(title: str, script_markdown: str, archive_assets: List[Dict[str, Any]]) -> Dict[str, Any]:
    sections = _extract_sections(script_markdown)
    all_tags = []
    for asset in archive_assets:
        all_tags.extend(asset.get("editorial_tags", []))

    visual_beats = []

    for index, section in enumerate(sections, start=1):
        scored_assets = []
        for asset in archive_assets:
            score = _score_asset(section["text"], asset)
            if score > 0:
                scored_assets.append({
                    "asset_id": asset["asset_id"],
                    "title": asset["title"],
                    "match_score": score
                })

        scored_assets = sorted(scored_assets, key=lambda item: item["match_score"], reverse=True)[:3]

        visual_beats.append({
            "beat_id": f"beat-{index:03d}",
            "section_heading": section["heading"],
            "script_text": section["text"],
            "visual_intent": _visual_intent(section["heading"], section["text"]),
            "archive_matches": scored_assets,
            "generation_prompts": [] if scored_assets else [_generation_prompt(section, all_tags)],
            "editorial_notes": [
                "Human editorial review required.",
                "Verify archive rights and context before use.",
                "Label or restrict generated visuals according to newsroom policy."
            ]
        })

    return {
        "package_id": "demo-package-001",
        "title": title,
        "script_source": "examples/scripts/sample_local_news_script.md",
        "visual_beats": visual_beats
    }
