from preClinVar.constants import CLNSIG_TERMS, SNV_COORDS, SV_COORDS
from preClinVar.file_parser import (
    parse_coords,
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
    assert (
        item["clinicalSignificance"]["clinicalSignificanceDescription"] in CLNSIG_TERMS
    )


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
    assert (
        item["conditionSet"]["multipleConditionExplanation"]
        == MULTIPLE_COND_EXPLANATION
    )
    for condition in item["conditionSet"]["condition"]:
        assert condition["db"] == CONDITION_DB
        assert condition["id"] in OMIM_NUMBERS


def test_parse_coords_sv():
    """Test the function that parse coordinates for a SV."""
    # GIVEN a SV variant dictionary with coordinates
    var_dict = {
        "##Local ID": "1d9ce6ebf2f82d913cfbe20c5085947b",
        "Chromosome": "7",
        "Breakpoint 1": 100000,
        "Breakpoint 2": 200000,
        "Outer start": 90000,
        "Inner start": 110000,
        "Inner stop": 190000,
        "Outer stop": 210000,
    }

    parsed_variant = {}
    # WHEN the variant is parsed by the parse_coords function
    parse_coords(parsed_variant, var_dict, SV_COORDS)

    # THEN all the expected fields should be present
    for _, items in SV_COORDS.items():
        assert parsed_variant[items["key"]]


def test_parse_coords_snv_m_chrom():
    """Test the function that parse coordinates for a SNV."""

    # GIVEN a SNV variant dictionary with coordinates
    var_dict = {
        "##Local ID": "1d9ce6ebf2f82d913cfbe20c5085947b",
        "Chromosome": "M",
        "Start": 1000,
        "Stop": 1000,
        "Reference allele": "G",
        "Alternate allele": "A",
    }

    parsed_variant = {}
    # WHEN the variant is parsed by the parse_coords function
    parse_coords(parsed_variant, var_dict, SNV_COORDS)

    # THEN all the expected fields should be present
    for _, items in SNV_COORDS.items():
        assert parsed_variant[items["key"]]

    # And chromosome 'M' should be remapped to 'MT'
    assert parsed_variant["chromosome"] == "MT"
