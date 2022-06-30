import logging
import os
from csv import DictReader
from tempfile import NamedTemporaryFile

LOG = logging.getLogger("uvicorn.access")

def set_item_assertion_criteria(item, line_dict):
    """Set the assertionCriteria key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        line_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    # Add CITATION key/value (a dict)
    citation = {}
    asc = line_dict.get("Assertion method citation")
    if asc and ":" in asc:
        citation["db"] = asc.split(":")[0]
        citation["id"] = asc.split(":")[1]

    # Add method key/value (a string)
    method = ""
    am = line_dict.get("Assertion method")
    if am:
        method = am

    item["assertionCriteria"] = {"citation":citation, "method": method}

def set_item_clin_sign(item, line_dict):
    """Set the clinicalSignificance key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        line_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    clinsig = line_dict.get("Clinical significance")
    last_eval = line_dict.get("Date last evaluated")

    item["clinicalSignificance"] = {"clinicalSignificanceDescription" : clinsig}
    if last_eval:
        item["clinicalSignificance"]["dateLastEvaluated"] = last_eval

def csv_fields_to_submission(variants_lines, casedata_lines):
    """Create a dictionary corresponding to a json submission file
       from the fields present in Variant and CaseData csv files

    Args:
        variants_lines(list of dicts). [{'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', ..}, {..}]
        casedata_lines(list of dicts). Example:

    Returns:
        subm_dict(dict): a json submission dictionary formatted according to this schema:
        https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/
    """
    clinvar_submission = {"title": "ClinVar Submission Set"} # The main ClinVar submission dictionary
    items = []
    # Loop over the variants to submit and create a
    for line_dict in variants_lines:
        LOG.error(line_dict)

        item = {} # For each variant in the csv file (one line), create a submission item

        set_item_assertion_criteria(item, line_dict)

        set_item_clin_sign(item, line_dict)


        items.append(item)



    clinvar_submission["items"] = items

    for item in clinvar_submission["items"]:
        LOG.debug(str(item)+"\n")













async def csv_lines(csv_file):
    """Extracts lines from a csv file using a csv DictReader

    Args:
        csv_file(starlette.datastructures.UploadFile)
    Returns:
        lines(list of dictionaries). Example [{'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH'}, ..]
    """

    contents = await csv_file.read()
    file_copy = NamedTemporaryFile(delete=False)
    lines = []
    try:
        with file_copy as f:
            f.write(contents)

        with open(file_copy.name, "r", encoding="utf-8") as csvf:
            csvreader = DictReader(csvf)
            next(csvreader)  # skip header
            for row in csvreader:
                lines.append(row)

    finally:
        file_copy.close()  # Close temp file
        os.unlink(file_copy.name)  # Delete temp file

    return lines
