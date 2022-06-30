import logging
import os
from csv import DictReader
from tempfile import NamedTemporaryFile

LOG = logging.getLogger("uvicorn.access")


def set_item_assertion_criteria(item, variant_dict):
    """Set the assertionCriteria key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variants_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    # Add CITATION key/value (a dict)
    citation = {}
    asc = variant_dict.get("Assertion method citation")
    if asc and ":" in asc:
        citation["db"] = asc.split(":")[0]
        citation["id"] = asc.split(":")[1]

    # Add method key/value (a string)
    method = ""
    am = variant_dict.get("Assertion method")
    if am:
        method = am

    item["assertionCriteria"] = {"citation": citation, "method": method}


def set_item_clin_sig(item, variant_dict):
    """Set the clinicalSignificance key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    clinsig = variant_dict.get("Clinical significance")
    clinsig_comment = variant_dict.get("Comment on clinical significance")
    last_eval = variant_dict.get("Date last evaluated")
    inherit_mode = variant_dict.get("Mode of inheritance")

    item["clinicalSignificance"] = {"clinicalSignificanceDescription": clinsig}
    if clinsig_comment:
        item["clinicalSignificance"]["comment"] = clinsig_comment
    if last_eval:
        item["clinicalSignificance"]["dateLastEvaluated"] = last_eval
    if inherit_mode:
        item["clinicalSignificance"]["modeOfInheritance"] = inherit_mode


def set_item_condition_set(item, variant_dict):
    """Set the conditionSet key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    conditions = []

    # Check if phenotype was specified in Variant file or in CaseData file
    cond_dbs = variant_dict.get("Condition ID type")
    cond_values = variant_dict.get("Condition ID value")

    if cond_dbs and cond_values:
        cond_dbs = cond_dbs.split(";")
        cond_values = cond_values.split(";")
        for cond_n, cond_db in enumerate(cond_dbs):
            conditions.append({"db": cond_db, "id": cond_values[cond_n]})
    if conditions:
        item["conditionSet"] = {"condition": conditions}


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
    clinvar_submission = {
        "title": "ClinVar Submission Set"
    }  # The main ClinVar submission dictionary
    items = []
    # Loop over the variants to submit and create a
    for linen, line_dict in enumerate(variants_lines):

        LOG.error(line_dict)

        item = {}  # For each variant in the csv file (one line), create a submission item

        set_item_assertion_criteria(item, line_dict)
        set_item_clin_sig(item, line_dict)
        set_item_condition_set(item, line_dict)

        items.append(item)

    clinvar_submission["items"] = items

    for item in clinvar_submission["items"]:
        LOG.debug(str(item) + "\n")


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
