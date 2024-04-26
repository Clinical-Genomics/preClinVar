import copy
import csv
import json
from tempfile import NamedTemporaryFile

import responses
from fastapi.testclient import TestClient

from preClinVar.__version__ import VERSION
from preClinVar.constants import DRY_RUN_SUBMISSION_URL, VALIDATE_SUBMISSION_URL
from preClinVar.demo import (
    casedata_old_csv,
    casedata_old_csv_path,
    casedata_snv_csv,
    casedata_snv_csv_path,
    casedata_sv_csv,
    casedata_sv_csv_path,
    subm_json_path,
    variants_hgvs_csv,
    variants_hgvs_csv_path,
    variants_old_csv,
    variants_old_csv_path,
    variants_sv_breakpoints_csv,
    variants_sv_breakpoints_csv_path,
    variants_sv_range_coords_csv,
    variants_sv_range_coords_csv_path,
)
from preClinVar.main import app

client = TestClient(app)

DEMO_API_KEY = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ab"
DEMO_SUBMISSION_ID = "SUB99999999"
OPTIONAL_PARAMETERS = {
    "submissionName": "SUB1234",
    "releaseStatus": "public",
    "assertionCriteriaDB": "PubMed",
    "assertionCriteriaID": "25741868",
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
        ("files", (variants_hgvs_csv, open(variants_old_csv_path, "rb"))),
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
        ("files", (variants_hgvs_csv, open(casedata_snv_csv_path, "rb"))),  # files are switched
        (
            "files",
            (casedata_snv_csv, open(variants_hgvs_csv_path, "rb")),
        ),
    ]
    response = client.post("/csv_2_json", files=files)
    # THEN the endpoint should return error
    assert response.status_code == 400
    assert response.json()["message"]


def test_csv_2_json_old_format():
    """Test the function that sends a request to the app to convert 2 cvs files (CaseData.csv, Variant.csv)
    into one json API submission object. Variant files contain 4 SNV with HGVS descriptors.
    Variant.csv file in old format contains assertion criteria fields"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        ("files", (variants_old_csv, open(variants_old_csv_path, "rb"))),
        ("files", (casedata_old_csv, open(casedata_old_csv_path, "rb"))),
    ]

    # THEN the response should be successful (code 200)
    response = client.post("/csv_2_json", params=OPTIONAL_PARAMETERS, files=files)
    assert response.status_code == 200

    # AND it should be a json object with the expected fields
    json_resp = response.json()
    assert json_resp["submissionName"]
    assert json_resp["clinvarSubmissionReleaseStatus"]
    assert json_resp["assertionCriteria"]
    assert json_resp["clinvarSubmission"]


def test_tsv_2_json_old_format():
    """Test the function that sends a request to the app to convert 2 tab separated cvs files (CaseData.tsv, Variant.tsv)
    into one json API submission object. Variant.tsv file in old format contains assertion criteria fields
    """

    # GIVEN Variant.csv and CaseData.csv temporary files based on the demo CSV files, but are tab-separated
    with NamedTemporaryFile(
        mode="a+", prefix="Variant", suffix=".csv"
    ) as tab_sep_var_file, NamedTemporaryFile(
        mode="a+", prefix="Casedata", suffix=".csv"
    ) as tab_sep_cdata_file, open(
        variants_old_csv_path, "r"
    ) as comma_sep_var_file, open(
        casedata_old_csv_path, "r"
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
            ("files", (variants_old_csv, open(tab_sep_var_file.name, "rb"))),
            ("files", (casedata_old_csv, open(tab_sep_cdata_file.name, "rb"))),
        ]

        # THEN the response should be successful (code 200)
        response = client.post("/tsv_2_json", params=OPTIONAL_PARAMETERS, files=files)
        # assert response.status_code == 200

        # AND it should be a json object with the expected fields
        json_resp = response.json()
        assert json_resp["submissionName"]
        assert json_resp["clinvarSubmissionReleaseStatus"]
        assert json_resp["assertionCriteria"]
        assert json_resp["clinvarSubmission"]


def test_csv_2_json_hgvs():
    """Test csv_2_json endpoint with a Variant file containing a SNV described by reference sequence and HGVS"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        ("files", (variants_hgvs_csv, open(variants_hgvs_csv_path, "rb"))),
        ("files", (casedata_snv_csv, open(casedata_snv_csv_path, "rb"))),
    ]

    # THEN the response should be successful (code 200)
    response = client.post("/csv_2_json", params=OPTIONAL_PARAMETERS, files=files)
    assert response.status_code == 200

    # AND it should be a json object with the expected fields
    json_resp = response.json()
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["gene"]
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["hgvs"]


def test_csv_2_json_SV_breakpoints():
    """Test csv_2_json endpoint with a Variant file containing a SV described by exact coordinates (breakpoints)"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        (
            "files",
            (variants_sv_breakpoints_csv, open(variants_sv_breakpoints_csv_path, "rb")),
        ),
        ("files", (casedata_sv_csv, open(casedata_sv_csv_path, "rb"))),
    ]

    # GIVEN a request that contains genome assembly as param
    req_params = copy.deepcopy(OPTIONAL_PARAMETERS)
    req_params["assembly"] = "GRCh37"

    # THEN the response should be successful (code 200)
    response = client.post("/csv_2_json", params=req_params, files=files)
    assert response.status_code == 200

    # AND it should be a json object with the expected fields
    json_resp = response.json()
    subm_coords = json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0][
        "chromosomeCoordinates"
    ]
    for item in ["assembly", "chromosome", "start", "stop"]:
        assert item in subm_coords
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["variantType"]
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["referenceCopyNumber"]
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["copyNumber"]


def test_csv_2_json_SV_range_coords():
    """Test csv_2_json endpoint with a Variant file containing a SV described by range coordinates (outer start, inner start, inner stop, outer stop)"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        (
            "files",
            (
                variants_sv_range_coords_csv,
                open(variants_sv_range_coords_csv_path, "rb"),
            ),
        ),
        ("files", (casedata_sv_csv, open(casedata_sv_csv_path, "rb"))),
    ]

    # GIVEN a request that contains genome assembly as param
    req_params = copy.deepcopy(OPTIONAL_PARAMETERS)
    req_params["assembly"] = "GRCh37"

    # THEN the response should be successful (code 200)
    response = client.post("/csv_2_json", params=req_params, files=files)
    assert response.status_code == 200

    # AND it should be a json object with the expected fields
    json_resp = response.json()
    subm_coords = json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0][
        "chromosomeCoordinates"
    ]
    for item in [
        "assembly",
        "chromosome",
        "innerStart",
        "innerStop",
        "outerStart",
        "outerStop",
    ]:
        assert item in subm_coords
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["variantType"]
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["referenceCopyNumber"]
    assert json_resp["clinvarSubmission"][0]["variantSet"]["variant"][0]["copyNumber"]


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
        status=204,  # The ClinVar API returns 204 (no content) when a dry-run submission was successful and no submission was created
    )

    response = client.post("/dry-run", data={"api_key": DEMO_API_KEY}, files=json_file)
    # THEN the ClinVar API proxy should return "success"
    assert response.status_code == 200  # Success
    assert response.json()["message"] == "success"


@responses.activate
def test_validate_wrong_api_key():
    """Test the validate API proxy endpoint without a valid ClinVar API key"""

    # GIVEN a json submission file
    json_file = {"json_file": open(subm_json_path, "rb")}

    # AND a mocked ClinVar API
    responses.add(
        responses.POST,
        VALIDATE_SUBMISSION_URL,
        json={"message": "No valid API key provided"},
        status=401,  # The ClinVar API returs code 201 when request is successful (created)
    )

    response = client.post("/validate", data={"api_key": DEMO_API_KEY}, files=json_file)

    # THEN the ClinVar API should return "unauthorized"
    assert response.status_code == 401  # Not authorized
    assert response.json()["message"] == "No valid API key provided"


@responses.activate
def test_validate():
    """Test the endpoint validate, a proxy to ClinVar apitest, with a mocked ClinVar API response."""

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

    @responses.activate
    def test_apitest_status():
        """Test the endpoint that sends GET requests to the apitest actions ClinVar endpoint."""

        # GIVEN a mocked error response from apitest actions endpoint
        actions: list[dict] = [
            {
                "id": "SUB14404390-1",
                "targetDb": "clinvar-test",
                "status": "error",
                "updated": "2024-04-26T06:41:04.533900Z",
                "responses": [
                    {
                        "status": "error",
                        "message": {
                            "severity": "error",
                            "errorCode": "2",
                            "text": 'Your ClinVar submission processing status is "Error". Please find the details in the file referenced by actions[0].responses[0].files[0].url.',
                        },
                        "files": [
                            {
                                "url": "https://submit.ncbi.nlm.nih.gov/api/2.0/files/vxgc6vtt/sub14404390-summary-report.json/?format=attachment"
                            }
                        ],
                        "objects": [],
                    }
                ],
            }
        ]

        responses.add(
            responses.GET,
            f"{VALIDATE_SUBMISSION_URL}/{DEMO_SUBMISSION_ID}/actions/",
            json={"actions": actions},
            status=200,  # The ClinVar API returns code 201 when request is successful (created)
        )

        # GIVEN a call to the apitest_status endpoint
        response = client.post(
            "/validate", data={"api_key": DEMO_API_KEY, "submission_id": DEMO_SUBMISSION_ID}
        )

        # THEN the response should contain the provided actions
        assert response.status_code == 200
        assert response.json()["actions"][0]["id"]
        assert response.json()["actions"][0]["responses"][0]["files"]
