"""Tests for report_chart_utils pure helpers."""

from typing import cast

from dbs_annotator.utils.report_chart_utils import (
    compute_aggregate_index,
    find_best_and_second,
    parse_scale_targets,
)

ScalePref = tuple[str, str, str, str, str]
ScalePrefs = list[ScalePref]


def test_parse_scale_targets_empty():
    assert parse_scale_targets(None) == {}
    assert parse_scale_targets([]) == {}
    assert parse_scale_targets(cast(ScalePrefs, [("a",)])) == {}


def test_parse_scale_targets_modes():
    prefs = [
        ("S1", "0", "10", "min", ""),
        ("S2", "0", "10", "max", ""),
        ("S3", "0", "10", "custom", "3.5"),
        ("S4", "0", "10", "custom", "bad"),
        ("short",),
    ]
    t = parse_scale_targets(cast(ScalePrefs, prefs))
    assert t["S1"]["type"] == "min"
    assert t["S2"]["type"] == "max"
    assert t["S3"]["value"] == 3.5
    assert t["S4"]["value"] == 0.0


def test_compute_aggregate_index_basic():
    scale_data = {"Mood": {1: 5.0, 2: 7.0}}
    targets = parse_scale_targets([("Mood", "0", "10", "max", "")])
    out = compute_aggregate_index(scale_data, [1, 2], targets)
    assert len(out) == 2
    assert all(0.0 <= v <= 1.0 for v in out.values())


def test_find_best_and_second():
    assert find_best_and_second({}) == (None, None)
    b, s = find_best_and_second({1: 0.2, 2: 0.9, 3: 0.5})
    assert b == 2
    assert s in (1, 3)
