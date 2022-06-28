from fastapi.testclient import TestClient
from preClinVar.main import app

client = TestClient(app)


def test_heartbeat():
    """Test the function that returns a message if server is running"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "preClinVar is up and running!"}


def test_csv_2_json():
    """Test the function that sends a request to the app to convert 2 cvs files (CaseData.csv, Variant.csv) into one json API submission object"""
    pass
