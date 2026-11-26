import pytest

from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge
from CodeCoverageTest_blood_donation_screening import clinic, donor


@pytest.mark.parametrize(("cohorts", "volume"), [(None, 450), ([], 0), ([], -1)])
def test_invalid_inputs(cohorts, volume):
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort(cohorts, volume)


@pytest.mark.parametrize(("cohorts", "expected_ml", "status"), [
    ([], 0, "ZERO_YIELD"),
    ([{"donors": [donor()], "fast_track": True}], 0, "ZERO_YIELD"),
    ([{"clinic_registered": True}], 0, "ZERO_YIELD"),
    ([clinic(donor(17, 50, 12.5), donor(hb=18))], 900, "ACCEPTED"),
    ([clinic(donor(age=16), donor(weight=49), donor(hb=12.4), donor(hb=18.1),
             donor(), fast_track=True)], 500, "ACCEPTED"),
    ([clinic(donor(), {}, {}, {}, {}, {})], 450, "HIGH_DEFERRAL"),
    ([clinic(donor()), clinic(donor(hb=12), donor(), type="high_altitude"),
      clinic(donor(), fast_track=True)], 500, "ACCEPTED"),
], ids=["empty-list", "unregistered", "no-donors", "inclusive-cutoffs",
        "four-deferrals", "five-deferrals", "reset-break-and-resume"])
def test_screening_outcomes(cohorts, expected_ml, status):
    assert process_donor_cohort(cohorts, 450) == {
        "collected_ml": expected_ml, "status": status
    }


@pytest.mark.parametrize(("runs", "status"), [
    ([], "NO_DATA"),
    ([[]], "STABLE"),
    ([[2999, 3000, 2999]], "STABLE"),
    ([[2999], [2999]], "STABLE"),
    ([[3000], [2999, 2999, 3000]], "ABORT_SPIN"),
])
def test_spin_transitions(runs, status):
    assert verify_storage_centrifuge(runs) == status
