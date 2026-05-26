from scenescout_research.package_planner import create_package_plan


def test_create_package_plan_basic():
    script = '''
## Anchor Intro
A heat wave is affecting the city.

## Reporter Track
Families arrived at the community center.
'''
    archive = [{
        "asset_id": "a1",
        "title": "Community center exterior",
        "detected_objects": ["building"],
        "editorial_tags": ["heat", "community center"],
        "detected_scenes": [{"description": "People entering community center"}],
        "transcript": ""
    }]

    plan = create_package_plan("Test", script, archive)

    assert plan["title"] == "Test"
    assert len(plan["visual_beats"]) == 2
    assert plan["visual_beats"][0]["beat_id"] == "beat-001"
