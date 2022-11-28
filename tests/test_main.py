import csv
from tempfile import NamedTemporaryFile

import responses
from fastapi.testclient import TestClient
from preClinVar.__version__ import VERSION
from preClinVar.constants import DRY_RUN_SUBMISSION_URL, VALIDATE_SUBMISSION_URL
from preClinVar.demo import (
    casedata_csv,
    casedata_csv_path,
    subm_json_path,
    variants_csv,
    variants_csv_path,
)
from preClinVar.main import app

client = TestClient(app)

DEMO_API_KEY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ab"
DEMO_SUBMISSION_ID = "SUB99999999"
OPTIONAL_PARAMETERS = {
    "submissionName": "SUB1234",
    "releaseStatus": "public",
    "behalfOrgID": 1234,
    "assertionCriteriaDB": "PubMed",
    "assertionCriteriaID": "25741868",
    "assertionCriteriaURL": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4544753/",
}


def test_heartbeat():
    """Test the function that returns a message if server is running"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": f"preClinVar v{VERSION} is up and running!"}


def test_csv_2_json_missing_file():
    """Test the endpoint that converts 2 cvs files (CaseData.csv, Variant.csv)
    into one json API submission object, when one of the files is missing"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    # GIVEN that only one of the 2 required files is provided:
    files = [
        ("files", (variants_csv, open(variants_csv_path, "rb"))),
    ]

    response = client.post("/csv_2_json", files=files)
    # THEN the endpoint should return error
    assert response.status_code == 400
    assert (
        response.json()["message"]
        == "Both 'Variant' and 'CaseData' csv files are required and should not be empty"
    )


def test_csv_2_json_malformed_file():
    """Test the endpoint that converts 2 cvs files (CaseData.csv, Variant.csv)
    into one json API submission object, when one of the files is malformed"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        ("files", (variants_csv, open(variants_csv_path, "rb"))),
        (
            "files",
            (casedata_csv, open(variants_csv_path, "rb")),
        ),  # GIVEN that file is wrong (should be casedata_csv_path)
    ]
    response = client.post("/csv_2_json", files=files)
    # THEN the endpoint should return error
    assert response.status_code == 400
    assert "Created json file contains validation errors" in response.json()["message"]


def test_tsv_2_json():
    """Test the function that sends a request to the app to convert 2 tab separated cvs files (CaseData.tsv, Variant.tsv)
    into one json API submission object"""

    # GIVEN Variant.csv and CaseData.csv temporary files based on the demo CSV files, but are tab-separated
    with NamedTemporaryFile(
        mode="a+", prefix="Variant", suffix=".csv"
    ) as tab_sep_var_file, NamedTemporaryFile(
        mode="a+", prefix="Casedata", suffix=".csv"
    ) as tab_sep_cdata_file, open(
        variants_csv_path, "r"
    ) as comma_sep_var_file, open(
        casedata_csv_path, "r"
    ) as comma_sep_cdata_file:

        # Convert Variant file to tsv
        csvin = csv.reader(comma_sep_var_file)
        tsvout = csv.writer(tab_sep_var_file, delimiter="\t")
        for row in csvin:
            tsvout.writerow(row)
        tab_sep_var_file.flush()
        tab_sep_var_file.seek(0)

        # convert CaseData file to tsv
        csvin = csv.reader(comma_sep_cdata_file)
        tsvout = csv.writer(tab_sep_cdata_file, delimiter="\t")
        for row in csvin:
            tsvout.writerow(row)
        tab_sep_cdata_file.flush()
        tab_sep_cdata_file.seek(0)

        # GIVEN a POST request to the endpoint with multipart-encoded files:
        # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
        files = [
            ("files", (variants_csv, open(tab_sep_var_file.name, "r"))),
            ("files", (casedata_csv, open(tab_sep_cdata_file.name, "r"))),
        ]

        params = OPTIONAL_PARAMETERS
        params["files"] = files

        # THEN the response should be successful (code 200)
        response = client.post("/tsv_2_json", params.items())
        assert response.status_code == 200

        # AND it should be a json object with the expected fields
        json_resp = response.json()
        assert json_resp["submissionName"]
        assert json_resp["releaseStatus"]
        assert json_resp["behalfOrgID"]
        assert json_resp["assertionCriteria"]
        assert json_resp["clinvarSubmission"]


def test_csv_2_json():
    """Test the function that sends a request to the app to convert 2 cvs files (CaseData.csv, Variant.csv)
    into one json API submission object"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        ("files", (variants_csv, open(variants_csv_path, "rb"))),
        ("files", (casedata_csv, open(casedata_csv_path, "rb"))),
    ]

    params = OPTIONAL_PARAMETERS
    params["files"] = files

    # THEN the response should be successful (code 200)
    response = client.post("/csv_2_json", params.items())
    assert response.status_code == 200

    # AND it should be a json object with the expected fields
    # AND it should be a json object with the expected fields
    json_resp = response.json()
    assert json_resp["submissionName"]
    assert json_resp["releaseStatus"]
    assert json_resp["behalfOrgID"]
    assert json_resp["assertionCriteria"]
    assert json_resp["clinvarSubmission"]


def test_dry_run_wrong_api_key():
    """Test the dry run API proxy without a valid ClinVar API key"""

    # GIVEN a json submission file
    json_file = {"json_file": open(subm_json_path, "rb")}

    response = client.post("/dry-run", data={"api_key": DEMO_API_KEY}, files=json_file)

    # THEN the ClinVar API should return "unathorized"
    assert response.status_code == 401
    assert response.json()["message"] == "No valid API key provided"


@responses.activate
def test_dry_run():
    """Test the dry_run API proxy endpoint (with a mocked ClinVar API response)"""

    # GIVEN a json submission file
    json_file = {"json_file": open(subm_json_path, "rb")}

    # AND a mocked ClinVar API
    responses.add(
        responses.POST,
        DRY_RUN_SUBMISSION_URL,
        json={},
        status=204,  # The ClinVar API returns 204 (no content) when a dry-run submission was successful and no submission was created
    )

    response = client.post("/dry-run", data={"api_key": DEMO_API_KEY}, files=json_file)
    # THEN the ClinVar API proxy should return "success"
    assert response.status_code == 200  # Success
    assert response.json()["message"] == "success"


def test_validate_wrong_api_key():
    """Test the validate API proxy endpoint without a valid ClinVar API key"""

    # GIVEN a json submission file
    json_file = {"json_file": open(subm_json_path, "rb")}

    response = client.post("/validate", data={"api_key": DEMO_API_KEY}, files=json_file)

    # THEN the ClinVar API should return "unathorized"
    assert response.status_code == 401  # Not authorized
    assert response.json()["message"] == "No valid API key provided"


@responses.activate
def test_validate():
    """Test the validated API proxy endpoint (with a mocked ClinVar API response)"""

    # GIVEN a json submission file
    json_file = {"json_file": open(subm_json_path, "rb")}

    # AND a mocked ClinVar API
    responses.add(
        responses.POST,
        VALIDATE_SUBMISSION_URL,
        json={"id": DEMO_SUBMISSION_ID},
        status=201,  # The ClinVar API returs code 201 when request is successful (created)
    )

    response = client.post("/validate", data={"api_key": DEMO_API_KEY}, files=json_file)

    # THEN the ClinVar API proxy should return "success"
    assert response.status_code == 201  # Created
    assert response.json()["id"] == DEMO_SUBMISSION_ID
