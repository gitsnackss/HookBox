"""Tests for ingestion endpoint."""
def test_ingest_success(client, db):
    # Create a project first
    from app.models.project import Project
    from app.utils.id_generator import generate_id
    proj = Project(
        id=generate_id("proj"),
        name="Test",
        inbox_key="testkey123",
        api_key_hash="dummyhash",
    )
    db.add(proj)
    db.commit()

    response = client.post(
        "/i/testkey123",
        json={"event": "test"},
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert "received_at" in data

def test_ingest_not_found(client):
    response = client.post("/i/invalid_key", json={})
    assert response.status_code == 404
