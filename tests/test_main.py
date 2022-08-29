from fastapi.testclient import TestClient
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


def test_heartbeat():
    """Test the function that returns a message if server is running"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "preClinVar is up and running!"}


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
    assert response.json()["message"] == "Both 'Variant' and 'CaseData' csv files are required"


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


def test_csv_2_json():
    """Test the function that sends a request to the app to convert 2 cvs files (CaseData.csv, Variant.csv)
    into one json API submission object"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        ("files", (variants_csv, open(variants_csv_path, "rb"))),
        ("files", (casedata_csv, open(casedata_csv_path, "rb"))),
    ]

    response = client.post("/csv_2_json", files=files)
    assert response.status_code == 200


def test_dry_run_wrong_api_key():
    """Test the dry run API proxy without a valid ClinVar API key"""
    json_file = {"json_file": open(subm_json_path, "rb")}

    url = "?api_key=".join(["/dry-run", DEMO_API_KEY])

    response = client.post(url, files=json_file)
    assert response.status_code == 401  # Not authorized
    assert response.json()["message"] == "No valid API key provided"


def test_validate_wrong_api_key():
    """Test the validate API proxy endpoint without a valid ClinVar API key"""
    json_file = {"json_file": open(subm_json_path, "rb")}

    url = "?api_key=".join(["/validate", DEMO_API_KEY])

    response = client.post(url, files=json_file)
    assert response.status_code == 401  # Not authorized
    assert response.json()["message"] == "No valid API key provided"
