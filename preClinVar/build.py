import logging

LOG = logging.getLogger("uvicorn.access")
OPTIONAL_SUBMISSION_PARAMS = {
    "submissionName": "submissionName",
    "releaseStatus": "clinvarSubmissionReleaseStatus",
}
OPTIONAL_ASSERTION_CRITERIA = {
    "assertionCriteriaDB": "db",
    "assertionCriteriaID": "id",
}


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
    if [key for key in list(OPTIONAL_ASSERTION_CRITERIA.keys()) if key in query_params]:
        assertion_criteria = {}
        for q_key, subm_key in OPTIONAL_ASSERTION_CRITERIA.items():
            if query_params.get(q_key):
                assertion_criteria[subm_key] = query_params.get(q_key)

        # This will override whatever is parsed from the CSV/TSV files
        subm_obj["assertionCriteria"] = assertion_criteria
