import json
import logging

from jsonschema import Draft3Validator, validate
from preClinVar.resources import subm_schema_path

LOG = logging.getLogger("uvicorn.access")


def validate_submission(submission_dict):
    """Validate a submission dictionary against the ClinVar submission schema

    Args:
        submission_dict(dict): a dictionary corresponding to an API submission file

    Returns:
        a tuple => False, [] or True, [error str, error str]
    """
    errors = []
    with open(subm_schema_path) as schema_file:
        schema = json.load(schema_file)
        v = Draft3Validator(schema)
        for error in sorted(v.iter_errors(submission_dict), key=str):
            errors.append(error.message)

    return errors == [], errors
