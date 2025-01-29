from importlib_resources import files

BASE_PATH = "preClinVar.demo"

###### .csv files ######
casedata_old_csv = "CaseData_before_221121.csv"
variants_old_csv = "Variant_before_221121.csv"

variants_hgvs_csv = "Variant_snv_hgvs.csv"
variants_sv_breakpoints_csv = "Variant_sv_breakpoints.csv"
variants_sv_range_coords_csv = "Variant_sv_range_coords.csv"
casedata_snv_csv = "CaseData_snv.csv"
casedata_sv_csv = "CaseData_sv.csv"

###### Path to .csv files ######
casedata_old_csv_path = str(files(BASE_PATH).joinpath(casedata_old_csv))
variants_old_csv_path = str(files(BASE_PATH).joinpath(variants_old_csv))
casedata_snv_csv_path = str(files(BASE_PATH).joinpath(casedata_snv_csv))
casedata_sv_csv_path = str(files(BASE_PATH).joinpath(casedata_sv_csv))
variants_hgvs_csv_path = str(files(BASE_PATH).joinpath(variants_hgvs_csv))
variants_sv_breakpoints_csv_path = str(files(BASE_PATH).joinpath(variants_sv_breakpoints_csv))
variants_sv_range_coords_csv_path = str(files(BASE_PATH).joinpath(variants_sv_range_coords_csv))

###### Example of a json file submission ######
clinsig_subm_json = "sample_clinical_significance_hgvs_submission.json"
germline_subm_json_path = str(files(BASE_PATH).joinpath(clinsig_subm_json))
