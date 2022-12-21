from preClinVar.constants import CLNSIG_TERMS
from preClinVar.file_parser import set_item_clin_sig


def test_set_item_clin_sig_fix_case():
    """Test the function that collects clinsig from Variant file when clisnsig term has wrong uppercase/lowercase"""
    # GIVEN a variant dictionary with a non-compliant slinsig value
    item = {}
    variant_dict = {"Clinical significance": "Likely Pathogenic"}

    # WHEN clisig is collected from variant_dict
    set_item_clin_sig(item, variant_dict)

    # THEN it's converted into a compiant term
    assert item["clinicalSignificance"]["clinicalSignificanceDescription"] in CLNSIG_TERMS
