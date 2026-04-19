"""Tests for config_electrode_models rules and ElectrodeModel."""

import pytest

from dbs_annotator.config_electrode_models import (
    ELECTRODE_MODELS,
    ContactState,
    ElectrodeModel,
    StimulationRule,
)


@pytest.fixture(autouse=True)
def clear_custom_validators():
    StimulationRule._custom_validators.clear()
    yield
    StimulationRule._custom_validators.clear()


def test_validate_case_cathodic_conflict():
    states = {(0, 0): ContactState.CATHODIC}
    ok, msg = StimulationRule.validate_configuration(states, ContactState.CATHODIC)
    assert not ok
    assert "CASE is cathodic" in msg


def test_validate_case_anodic_conflict():
    states = {(0, 0): ContactState.ANODIC}
    ok, msg = StimulationRule.validate_configuration(states, ContactState.ANODIC)
    assert not ok
    assert "CASE is anodic" in msg


def test_validate_cathodic_requires_anodic():
    states = {(0, 0): ContactState.CATHODIC}
    ok, msg = StimulationRule.validate_configuration(states, ContactState.OFF)
    assert not ok
    assert "anodic" in msg.lower()


def test_validate_valid_simple():
    states = {(0, 0): ContactState.CATHODIC, (1, 0): ContactState.ANODIC}
    ok, msg = StimulationRule.validate_configuration(states, ContactState.OFF)
    assert ok
    assert msg == ""


def test_get_suggested_fix_paths():
    s1 = StimulationRule.get_suggested_fix(
        {(0, 0): ContactState.CATHODIC}, ContactState.CATHODIC
    )
    assert "Suggestion" in s1
    s2 = StimulationRule.get_suggested_fix(
        {(0, 0): ContactState.CATHODIC}, ContactState.OFF
    )
    assert "anodic" in s2.lower()


def test_add_validator_invoked():
    def bad_validator(contact_states, case_state):
        return False, "custom"

    StimulationRule.add_validator(bad_validator)
    StimulationRule.add_validator(bad_validator)  # duplicate ignored
    ok, msg = StimulationRule.validate_configuration({}, ContactState.OFF)
    assert not ok
    assert msg == "custom"


def test_add_validator_exception_swallowed():
    def boom(cs, c):
        raise RuntimeError("x")

    StimulationRule.add_validator(boom)
    ok, _ = StimulationRule.validate_configuration({}, ContactState.OFF)
    assert ok


def test_add_validator_returns_none_ignored():
    StimulationRule.add_validator(lambda a, b: None)
    assert StimulationRule.validate_configuration({}, ContactState.OFF)[0]


def test_electrode_model_directional_levels():
    m = ElectrodeModel(
        "TestDir",
        4,
        1.0,
        1.0,
        1.0,
        is_directional=True,
        directional_levels=[1, 2],
    )
    assert m.is_level_directional(1)
    assert not m.is_level_directional(0)


def test_electrode_models_dict_nonempty():
    assert len(ELECTRODE_MODELS) > 0
    first = next(iter(ELECTRODE_MODELS.values()))
    assert first.num_contacts >= 1
