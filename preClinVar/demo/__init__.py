import pkg_resources

###### .csv files ######
casedata_old_csv = "CaseData_before_221121.csv"
variants_old_csv = "Variant_before_221121.csv"

variants_hgvs_csv = "Variant_snv_hgvs.csv"
casedata_csv = "CaseData.csv"

###### Path to .csv files ######
casedata_old_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", casedata_old_csv])
)
variants_old_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_old_csv])
)

casedata_csv_path = pkg_resources.resource_filename("preClinVar", "/".join(["demo", casedata_csv]))
variants_hgvs_csv_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["demo", variants_hgvs_csv])
)

###### Example of a json file submission ######
subm_json = "submission.json"
subm_json_path = pkg_resources.resource_filename("preClinVar", "/".join(["demo", subm_json]))
