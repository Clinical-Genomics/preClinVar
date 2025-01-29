import json

from preClinVar.demo import subm_json_path
from preClinVar.validate import validate_submission


def test_validate_submission():
    """Test the function that validates a json submission against the ClinVar API submission schema,"""

    # GIVEN a valid json file
    assert json.load(open(subm_json_path))

    # THEN the submission should be validated and return no errors when validated against the ClinVar Schema
    with open(subm_json_path) as json_file:
        submission_dict = json.load(json_file)
        assert validate_submission(schema="germline", submission_dict=submission_dict) == (True, [])
