from importlib_resources import files

BASE_PATH = "preClinVar.resources"

###### submission schema json file ######

germline_subm_schema = "germline_submission_schema.json"
somatic_subm_schema = "somatic_submission_schema.json"

###### Path to submission schema file ######
germline_subm_schema_path = str(files(BASE_PATH).joinpath(germline_subm_schema))
somatic_subm_schema_path = str(files(BASE_PATH).joinpath(somatic_subm_schema))
