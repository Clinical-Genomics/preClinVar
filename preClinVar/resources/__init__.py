import pkg_resources

###### submission schema json file ######

subm_schema = "submission_schema.json"

###### Path to submission schema file ######
subm_schema_path = pkg_resources.resource_filename(
    "preClinVar", "/".join(["resources", subm_schema])
)
