import pkg_resources

###### .csv files ######
casedata_old_csv = "CaseData_before_221121.csv"
variants_old_csv = "Variant_before_221121.csv"

variants_hgvs_csv = "Variant_snv_hgvs.csv"
variants_accession_csv = "Variant_accession.csv"
variants_sv_breakpoints_csv = "Variant_sv_breakpoints.csv"
variants_sv_range_coords_csv = "Variant_sv_range_coords.csv"
casedata_snv_csv = "CaseData_snv.csv"
casedata_sv_csv = "CaseData_sv.csv"

###### Path to .csv files ######
casedata_old_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", casedata_old_csv])
)
variants_old_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_old_csv])
)

casedata_snv_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", casedata_snv_csv])
)
casedata_sv_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", casedata_sv_csv])
)
variants_hgvs_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_hgvs_csv])
)
variants_accession_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_accession_csv])
)
variants_sv_breakpoints_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_sv_breakpoints_csv])
)
variants_sv_range_coords_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_sv_range_coords_csv])
)
###### Example of a json file submission ######
subm_json = "submission.json"
subm_json_path = pkg_resources.resource_filename("preClinVar", "/".join(["demo", subm_json]))
