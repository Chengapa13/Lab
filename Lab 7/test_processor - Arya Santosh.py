from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry


# Test 1: Blood type validation
@given(st.text() | st.none())
def test_validate_blood_type_no_crash(s):
    try:
        validate_blood_type(s)
    except Exception as e:
        assert False, f"validate_blood_type crashed with input {s!r}: {e}"


# Test 2: Blood pressure calculation
@given(st.text() | st.none())
def test_calculate_pulse_pressure_safe(s):
    try:
        calculate_pulse_pressure(s)
    except Exception as e:
        assert False, f"calculate_pulse_pressure crashed with input {s!r}: {e}"


# Test 3: Donor registry parsing
@given(st.text() | st.none())
def test_parse_donor_registry_safe(s):
    try:
        parse_donor_registry(s)
    except Exception as e:
        assert False, f"parse_donor_registry crashed with input {s!r}: {e}"
