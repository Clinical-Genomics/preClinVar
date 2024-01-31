import logging
import os
from csv import DictReader
from tempfile import NamedTemporaryFile

from preClinVar.constants import CLNSIG_TERMS, CONDITIONS_MAP, SNV_COORDS, SV_COORDS

LOG = logging.getLogger("uvicorn.access")


def set_assertion_criteria_from_csv(subm_obj, variants_lines):
    """Set the assertionCriteria key/values for an API submission item

    Args:
        subm_obj(dict). An empty submission object
        variants_dict(list) list of dicts. May contain or not the Assertion method citation fields
    """
    assertion_criteria = {}
    a_line = variants_lines[0]
    # Look for Assertion method citation info on the first line of the CVS
    if a_line.get("Assertion method citation"):
        asc = a_line.get("Assertion method citation")
        asc_db = asc.split(":")[0]
        if asc_db in ["PMID", "DOI", "pmc"]:
            if asc_db == "PMID":
                assertion_criteria["db"] = "PubMed"
            else:
                assertion_criteria["db"] = asc_db
            assertion_criteria["id"] = asc.split(":")[1]

    if assertion_criteria:
        subm_obj["assertionCriteria"] = assertion_criteria


def set_record_status(item):
    """Set status for an API submission item"""
    item["recordStatus"] = "novel"


def set_item_clin_sig(item, variant_dict):
    """Set the clinicalSignificance key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    # set first required params
    clinsig = variant_dict.get("Clinical significance")
    # Make sure clinsig term is compliant with API standards:
    for term in CLNSIG_TERMS:
        if clinsig.lower() == term.lower():
            clinsig = term
            break

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

    # NOT parsing the following key/values for now:
    # citation
    # customAssertionScore


def set_item_condition_set(item: dict, variant_dict: dict):
    """Set the conditionSet key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    conditions: list = []

    # Check if condition ID is specified in Variant file
    cond_db: str = CONDITIONS_MAP.get(variant_dict.get("Condition ID type"))
    cond_values: str = variant_dict.get("Condition ID value")
    multi_condition_explanation: str = variant_dict.get("Explanation for multiple conditions")

    if cond_db and cond_values:
        cond_values = cond_values.split(";")
        for cond_id in cond_values:
            condition = {"db": cond_db, "id": cond_id}
            conditions.append(condition)
    if conditions:
        item["conditionSet"] = {"condition": conditions}
        if multi_condition_explanation:
            item["conditionSet"][
                "MultipleConditionExplanation"
            ] = multi_condition_explanation.capitalize()


def set_item_local_id(item, variant_dict):
    """Set the local id (#Local ID) for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    local_id = variant_dict.get("##Local ID")
    if local_id:
        item["localID"] = local_id


def set_item_local_key(item, variant_dict):
    """Set the local key (Linking ID) for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    local_key = variant_dict.get("Linking ID")
    if local_key:
        item["localKey"] = local_key


def set_item_observed_in(item, casedata_lines):
    """Set the observedIn key/values for an API submission item
    Args:
        item(dict). An item in the clinvarSubmission.items list
        casedata_lines(list of dicts). Example:
            [{'Linking ID': '69b138a4c5caf211d796a59a7b46e40d', 'Individual ID': '20210316-03', 'Collection method': 'clinical testing', 'Allele origin': 'germline', 'Affected status': 'yes', 'Sex': 'male', 'Family history': 'no', 'Proband': 'yes', ..}, ..]
    """
    var_link_id = item.get("localKey")  # ID of the variant
    obs_in = []

    # Loop over case data and collect individuals associated with the variant linking ID
    for line_dict in casedata_lines:
        if var_link_id != line_dict.get("Linking ID"):
            continue

        # set first required params
        obs = {
            "affectedStatus": line_dict.get("Affected status"),
            "alleleOrigin": line_dict.get("Allele origin"),
            "collectionMethod": line_dict.get("Collection method"),
        }
        if line_dict.get("Clinical features"):
            obs["clinicalFeatures"] = line_dict.get("Clinical features").split(";")

        obs_in.append(obs)

    item["observedIn"] = obs_in

    # NOT parsing the following key/values for now:
    # clinicalFeaturesComment
    # numberOfIndividuals
    # structVarMethodType


def set_item_record_status(item):
    """Set status for clinvar record (variant submmitted). Set it to novel for the time being"""
    item["recordStatus"] = "novel"


def _parse_cooords(coords, variant_dict, coords_items):
    """Parse coordinates for SNVs or SVs

    Args:
        coords(dict): an empty dictionary
        variant_dict(dict): Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
        coords_items(dict): either SNV_COORDS, or SV_COORDS

    """
    for csv_key, item in coords_items.items():
        if csv_key not in variant_dict or variant_dict[csv_key] == "":
            continue
        try:
            coords[item["key"]] = item["format"](variant_dict[csv_key])
        except Exception as ex:
            LOG.error(
                f"Exception when converting {csv_key} value->{variant_dict[csv_key]} to {item['format']}"
            )


def _set_snv_coordinates(coords, variant_dict):
    """Set coordinates for a SNV variant

    Args:
        coords(dict): an empty dictionary
        variant_dict(dict): Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    _parse_cooords(coords, variant_dict, SNV_COORDS)


def _set_sv_coordinates(coords, variant_dict):
    """Set coordinates for a SV variant

    Args:
        coords(dict): an empty dictionary
        variant_dict(dict): Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}
    """
    _parse_cooords(coords, variant_dict, SV_COORDS)


def _set_chrom_coordinates(variant_dict):
    """Set the chromosomeCoordinates dictionary for a variant.
    chromosomeCoordinates can be described by an accession or chromosome coordinates

    Args:
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}

    Returns:
        coords(dict)
    """
    coords = {}

    # Parse coordinates from file instead
    if variant_dict.get("Variant type"):  # SV variant
        _set_sv_coordinates(coords, variant_dict)
    else:
        _set_snv_coordinates(coords, variant_dict)

    return coords


def set_item_variant_set(item, variant_dict):
    """Set the variantSet keys/values for a variant item in the submission object

    Args:
        item(dict). An item in the clinvarSubmission.items list
        variant_dict(dict). Example: {'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', 'HGVS': 'c.2751del', ..}

    """
    # According the schema: The interpreted variant must be described either by HGVS or by chromosome coordinates, but not both.
    # Our cvs files contain HGVS so we parse only these at the moment
    item["variantSet"] = {}
    variant = {}
    genes = variant_dict.get("Gene symbol")
    if genes:
        variant["gene"] = [{"symbol": symbol} for symbol in genes.split(";")]
    refseq = variant_dict.get("Reference sequence")
    hgvs = variant_dict.get("HGVS")
    if hgvs and refseq:  # A Variant should have either HGVS (hgvs in schema)
        variant["hgvs"] = ":".join([refseq, hgvs])
    else:  # OR chromosome coordinates (chromosomeCoordinates in schema)
        variant["chromosomeCoordinates"] = _set_chrom_coordinates(variant_dict)

    # Check if file contains copy number info
    if variant_dict.get("Copy number"):
        variant["copyNumber"] = variant_dict["Copy number"]
    if variant_dict.get("Reference copy number"):
        try:
            variant["referenceCopyNumber"] = int(variant_dict["Copy number"])
        except Exception as ex:
            LOG.error(
                "Error while converting referenceCopyNumber {variant_dict['Copy number']} to int"
            )

    # Check if file contains type of variant (SV variants)
    if variant_dict.get("Variant type"):
        variant["variantType"] = variant_dict["Variant type"]

    item["variantSet"]["variant"] = [variant]


def file_fields_to_submission(variants_lines, casedata_lines):
    """Create a dictionary corresponding to a json submission file
       from the fields present in Variant and CaseData csv files

    Args:
        variants_lines(list of dicts). [{'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH', 'Reference sequence': 'NM_000379.4', ..}, {..}]
        casedata_lines(list of dicts). Example:

    Returns:
        clinvar_submission(dict): a json submission dictionary formatted according to this schema:
        https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/
    """
    subm_object = {}

    # try to parse assertion criteria from old format of CSV file
    set_assertion_criteria_from_csv(subm_object, variants_lines)

    items = []
    # Loop over the variants to submit and create a
    for line_dict in variants_lines:
        item = {}  # For each variant in the csv file (one line), create a submission item
        set_item_clin_sig(item, line_dict)
        set_item_condition_set(item, line_dict)
        set_item_local_id(item, line_dict)
        set_item_local_key(item, line_dict)
        set_item_observed_in(item, casedata_lines)
        set_item_variant_set(item, line_dict)
        set_item_record_status(item)

        filtered = {k: v for k, v in item.items() if v is not None}

        items.append(filtered)

    subm_object["clinvarSubmission"] = items

    return subm_object


def _tsv_file_lines(contents):
    """Retrieve contents of a tab-separated file

    Args:
        contents(bytes): contents of one of the files uploaded, as bytes

    Returns:
        line_dicts(list): a list of dictionaries, one for each line of the original file
    """
    lines = []
    try:
        line_contents = contents.decode("UTF-8").replace("\r", "").split("\n")
        header = line_contents[0].split("\t")
        for row in line_contents[1:]:
            if row.rstrip():
                row_values = row.split("\t")
                line = {}
                for n, key in enumerate(header):
                    line[key.strip('"')] = row_values[n].strip('"')
                lines.append(line)
    except Exception as ex:
        LOG.error("An error occurred while parsing TSV file")

    return lines


def _csv_file_lines(contents):
    """Retrieve contents of a tab-separated file

    Args:
        contents(bytes): contents of one of the files uploaded, as bytes

    Returns:
        lines(list): a list of rows from a DictReader object
    """
    lines = []
    file_copy = NamedTemporaryFile(delete=False)
    try:
        with file_copy as f:
            f.write(contents)

        with open(file_copy.name) as csvf:
            csvreader = DictReader(csvf)
            for row in csvreader:
                lines.append(row)

    finally:
        file_copy.close()  # Close temp file
        os.unlink(file_copy.name)  # Delete temp file

    return lines


async def tsv_lines(tsv_file):
    """Extracts lines from a csv file using a csv DictReader

    Args:
        tsv_file(starlette.datastructures.UploadFile)

    Returns:
        lines(list of dictionaries). Example [{'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH'}, ..]

    """
    contents = await tsv_file.read()
    return _tsv_file_lines(contents)


async def csv_lines(csv_file):
    """Extracts lines from a csv file using a csv DictReader

    Args:
        csv_file(starlette.datastructures.UploadFile)

    Returns:
        lines(list of dictionaries). Example [{'##Local ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Linking ID': '1d9ce6ebf2f82d913cfbe20c5085947b', 'Gene symbol': 'XDH'}, ..]
    """
    contents = await csv_file.read()
    return _csv_file_lines(contents)
