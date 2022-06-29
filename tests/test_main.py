from fastapi.testclient import TestClient
from preClinVar.demo import casedata_csv, casedata_csv_path, variants_csv, variants_csv_path
from preClinVar.main import app

client = TestClient(app)


def test_heartbeat():
    """Test the function that returns a message if server is running"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "preClinVar is up and running!"}


def test_submission_from_csv():
    """Test the function that sends a request to the app to convert 2 cvs files (CaseData.csv, Variant.csv)
    into one json API submission object"""

    # GIVEN a POST request to the endpoint with multipart-encoded files:
    # (https://requests.readthedocs.io/en/latest/user/advanced/#post-multiple-multipart-encoded-files)
    files = [
        ("files", (variants_csv, open(variants_csv_path, "rb"))),
        ("files", (casedata_csv, open(casedata_csv_path, "rb"))),
    ]

    response = client.post("/submission_from_csv", files=files)
    assert response.status_code == 200
