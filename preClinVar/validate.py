import json
import logging
from typing import List, Tuple

from jsonschema import Draft7Validator, validate

from preClinVar.resources import germline_subm_schema_path, somatic_subm_schema_path

LOG = logging.getLogger("uvicorn.access")
SCHEMAS = {"germline": germline_subm_schema_path, "somatic": somatic_subm_schema_path}


def validate_submission(schema: str, submission_dict: dict) -> Tuple[bool, List[str]]:
    """Validate a submission dictionary against the ClinVar submission schema."""
    errors = []
    with open(SCHEMAS[schema]) as schema_file:
        schema = json.load(schema_file)

        v = Draft7Validator(schema)
        for error in sorted(v.iter_errors(submission_dict), key=str):
            errors.append(error.message)

    return errors == [], errors
