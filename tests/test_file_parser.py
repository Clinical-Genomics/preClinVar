from preClinVar.constants import CLNSIG_TERMS
from preClinVar.demo import variants_hgvs_csv_path
from preClinVar.file_parser import (
    csv_lines,
    set_item_clin_sig,
    set_item_condition_set,
    set_item_variant_set,
)


def test_set_item_clin_sig_fix_case():
    """Test the function that collects clinsig from Variant file when clisnsig term has wrong uppercase/lowercase"""
    # GIVEN a variant dictionary with a non-compliant slinsig value
    item = {}
    variant_dict = {"Clinical significance": "Likely Pathogenic"}

    # WHEN clisig is collected from variant_dict
    set_item_clin_sig(item, variant_dict)

    # THEN it's converted into a compliant term
    assert item["clinicalSignificance"]["clinicalSignificanceDescription"] in CLNSIG_TERMS


def test_set_item_variant_set_hgvs():
    """Test the function that sets variantSet keys/values for a variant item in the submission object"""
    item = {}
    REFSEQ = "NM_015450.3"
    HGVS = "c.903G>T"
    variant_dict = {"Reference sequence": REFSEQ, "HGVS": HGVS}

    # WHEN variant set is created from variant_dict
    set_item_variant_set(item, variant_dict)
    # THEN hgvs field should contain both Reference sequence and HGVS
    assert item["variantSet"]["variant"][0]["hgvs"] == ":".join([REFSEQ, HGVS])


def test_set_item_condition_set():
    """Test the function that sets condition conditionSet values."""

    item = {}
    CONDITION_DB = "OMIM"
    OMIM_NUMBERS = "604187,604187"
    MULTIPLE_COND_EXPLANATION = "Novel disease"
    variant_dict = {
        "Condition ID type": CONDITION_DB,
        "Condition ID value": OMIM_NUMBERS,
        "Explanation for multiple conditions": MULTIPLE_COND_EXPLANATION,
    }

    # WHEN variant set is created from variant_dict containing condition info
    set_item_condition_set(item=item, variant_dict=variant_dict)

    # THEN it should contain the expected key/values
    assert item["conditionSet"]["MultipleConditionExplanation"] == MULTIPLE_COND_EXPLANATION
    for condition in item["conditionSet"]["condition"]:
        assert condition["db"] == CONDITION_DB
        assert condition["id"] in OMIM_NUMBERS
