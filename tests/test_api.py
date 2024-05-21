from app.main import app
from fastapi.testclient import TestClient


def test_upload_review():
    client = TestClient(app)
    response = client.post(
        "api/v1/upload_review",
        json={"reviews": "This is a test review."},
    )
    assert response.status_code == 200
    assert len(response.json()["document_id"]) > 0
    

# add more tests later


