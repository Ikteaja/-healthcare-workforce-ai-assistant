import json

from fastapi.testclient import TestClient

from backend.main import app
from backend.services.document_ingestion import DocumentIngestionService


def test_split_text_creates_multiple_chunks():
    service = DocumentIngestionService(data_dir="/tmp/healthcare-workforce-test", chunk_size=80, chunk_overlap=10)
    text = " ".join(["Healthcare workforce staffing policy requires escalation and documentation."] * 8)

    chunks = service.split_text(text)

    assert len(chunks) > 1
    assert all(chunk for chunk in chunks)
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_upload_txt_document_processes_chunks(tmp_path, monkeypatch):
    monkeypatch.setenv("HEALTHCARE_DOCUMENT_DATA_DIR", str(tmp_path))
    client = TestClient(app)
    content = (
        "Healthcare workforce staffing procedures require charge nurses to document coverage gaps.\n\n"
        "Human resources reviews recurring vacancies and coordinates recruiting priorities."
    )

    response = client.post(
        "/documents/upload",
        files={"file": ("staffing_policy.txt", content, "text/plain")},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["filename"] == "staffing_policy.txt"
    assert payload["document_type"] == "txt"
    assert payload["chunk_count"] >= 1
    assert payload["chunks"][0]["chunk_index"] == 0
    assert payload["chunks"][0]["filename"] == "staffing_policy.txt"
    assert payload["chunks"][0]["document_type"] == "txt"

    processed_file = tmp_path / "processed" / payload["processed_file_path"].split("/")[-1]
    assert processed_file.exists()
    processed_payload = json.loads(processed_file.read_text(encoding="utf-8"))
    assert processed_payload[0]["content"]
    assert processed_payload[0]["upload_timestamp"] == payload["upload_timestamp"]


def test_upload_rejects_unsupported_document_type(tmp_path, monkeypatch):
    monkeypatch.setenv("HEALTHCARE_DOCUMENT_DATA_DIR", str(tmp_path))
    client = TestClient(app)

    response = client.post(
        "/documents/upload",
        files={"file": ("schedule.csv", "name,shift", "text/csv")},
    )

    assert response.status_code == 400
    assert "Unsupported document type" in response.json()["detail"]
