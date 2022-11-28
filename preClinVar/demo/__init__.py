import pkg_resources

###### .csv files ######
casedata_csv = "CaseData_before_221121.csv"
variants_csv = "Variant_before_221121.csv"

###### Path to .csv files ######
casedata_csv_path = pkg_resources.resource_filename("preClinVar", "/".join(["demo", casedata_csv]))
variants_csv_path = pkg_resources.resource_filename("preClinVar", "/".join(["demo", variants_csv]))

###### Example of a json file submission ######
subm_json = "submission.json"
subm_json_path = pkg_resources.resource_filename("preClinVar", "/".join(["demo", subm_json]))
