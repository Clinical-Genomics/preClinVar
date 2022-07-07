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
