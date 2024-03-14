import json
from preClinVar.validate import validate_submission
from preClinVar.demo import clinvar_germline_hgvs_path


def validate_submission_clinvar_examples():
    """Tests validation of submission_examples from ClinVar against their schema."""


def test_validate_submission():
    """Test the function that validates a json submission against the ClinVar API submission schema,"""

    # GIVEN a valid json file
    assert json.load(open(clinvar_germline_hgvs_path))
    with open(clinvar_germline_hgvs_path) as json_file:
        submission_dict = json.load(json_file)
        assert validate_submission(submission_dict=submission_dict) == (True, [])
