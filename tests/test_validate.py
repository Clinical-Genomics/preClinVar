import json

from preClinVar.demo import germline_subm_json_path, somatic_subm_json_path
from preClinVar.validate import validate_submission


def test_validate_germline_submission():
    """Test the function that validates a germline json submission against its respective ClinVar API submission schema."""

    # GIVEN a valid json file
    assert json.load(open(germline_subm_json_path))

    # THEN the submission should be validated and return no errors when validated against the ClinVar Schema
    with open(germline_subm_json_path) as json_file:
        submission_dict = json.load(json_file)
        assert validate_submission(submission_dict=submission_dict) == (True, [])


def test_validate_somatic_submission():
    """Test the function that validates a somatic json submission against its respective ClinVar API submission schema."""

    # GIVEN a valid json file
    assert json.load(open(somatic_subm_json_path))

    # THEN the submission should be validated and return no errors when validated against the ClinVar Schema
    with open(somatic_subm_json_path) as json_file:
        submission_dict = json.load(json_file)
        assert validate_submission(submission_dict=submission_dict) == (True, [])
