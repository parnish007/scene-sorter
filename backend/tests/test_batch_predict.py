import os
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_batch_endpoint_exists():
    # Ensures route is registered
    res = client.post("/predict/batch", files=[])
    assert res.status_code in (400, 422)  # 422 if files missing, 400 if empty list handled


def test_download_not_found_for_unknown_job():
    res = client.get("/download/does_not_exist")
    assert res.status_code == 404
