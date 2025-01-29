from importlib_resources import files

BASE_PATH = "preClinVar.resources"

###### submission schema json file ######

subm_schema = "submission_schema.json"

###### Path to submission schema file ######
subm_schema_path = str(files(BASE_PATH).joinpath(subm_schema))
