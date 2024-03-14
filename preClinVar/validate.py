import json
import logging
from typing import List, Tuple

from jsonschema import Draft7Validator, validate

from preClinVar.resources import subm_schema_path

LOG = logging.getLogger("uvicorn.access")


def validate_submission(submission_dict: dict) -> Tuple[bool, List[str]]:
    """Validate a submission dictionary against the ClinVar submission schema."""
    errors = []
    with open(subm_schema_path) as schema_file:
        schema = json.load(schema_file)

        v = Draft7Validator(schema)
        for error in sorted(v.iter_errors(submission_dict), key=str):
            errors.append(error.message)

    return errors == [], errors
