import logging

OPTIONAL_SUBMISSION_PARAMS = {
    "submissionName": "submissionName",
    "releaseStatus": "clinvarSubmissionReleaseStatus",
}
OPTIONAL_ASSERTION_CRITERIA = {
    "assertionCriteriaDB": "db",
    "assertionCriteriaID": "id",
}

LOG = logging.getLogger("uvicorn.access")


def build_header(api_key):
    """Creates a header to be submitted a in a POST rquest to the CLinVar API

    Args:
        api_key(str): API key to be used to submit to ClinVar (64 alphanumeric characters)

    Returns:
        header(dict): contains "Content-type: application/json" and "SP-API-KEY: <API-KEY>" key/values
    """
    header = {
        "Content-Type": "application/json",
        "SP-API-KEY": api_key,
    }
    return header


def build_submission(subm_obj, request):
    """Parse request parameters and add items to a growing submission object dictionary

    Args:
        subm_obj(dict): a submission object like this { "clinvarSubmission" : [list of submission items]}
        request()

    """
    # Add items to submission if user provides any of the optional fields from OPTIONAL_SUBMISSION_PARAMS
    query_params = dict(request.query_params)
    for q_key, subm_key in OPTIONAL_SUBMISSION_PARAMS.items():
        if query_params.get(q_key):
            subm_obj[subm_key] = query_params[q_key]

    # Add assertion criteria item to submission if user provides "db", "id" or "url"
    if query_params.get("assertionCriteriaDB") and query_params.get("assertionCriteriaID"):
        assertion_criteria = {}
        for q_key, subm_key in OPTIONAL_ASSERTION_CRITERIA.items():
            if query_params.get(q_key):
                assertion_criteria[subm_key] = query_params.get(q_key)

        # This will override whatever is parsed from the CSV/TSV files
        subm_obj["assertionCriteria"] = assertion_criteria

    assembly = query_params.get("assembly")
    if assembly:  # Set genome assembly for all variants containing a chromosomeCoordinates field
        for subm_item in subm_obj.get("clinvarSubmission", []):
            if not "variantSet" in subm_item:
                continue
            for var in subm_item["variantSet"].get("variant", []):
                coords = var.get("chromosomeCoordinates")
                if coords:
                    coords["assembly"] = assembly
